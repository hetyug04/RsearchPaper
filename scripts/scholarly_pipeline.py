#!/usr/bin/env python3
"""Reproducible scholarly discovery and first-public-date cross-check.

The script uses only Python's standard library and runs on a local machine or
Google Colab. Network responses are cached as immutable JSON envelopes with
request provenance and a SHA-256 digest. It intentionally keeps bibliographic
dates separate from submission, deposit, indexing, and update dates.

Commands:

    python scripts/scholarly_pipeline.py discover
    python scripts/scholarly_pipeline.py verify
    python scripts/scholarly_pipeline.py all

Optional environment variables:

    SCHOLARLY_API_EMAIL  Contact email for Unpaywall and polite API pools.
    NCBI_API_KEY         Free NCBI key (raises limit from 3 to 10 requests/s).
    OPENALEX_API_KEY     Free OpenAlex key required by current 2026 docs.
    SSL_CERT_FILE        CA bundle override. macOS /etc/ssl/cert.pem is used
                         when the framework Python trust store is missing.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/scholarly_metadata"
INTERIM = ROOT / "data/interim"
CUTOFF = dt.date(2024, 12, 1)
TODAY = dt.date(2026, 7, 29)

DISCOVERY_QUERY = (
    '("2026/07/01"[Publication Date] : "2026/07/29"[Publication Date]) '
    'AND open_access[filter] AND "cohort study"[Title] AND '
    '(cardiovascular[Title] OR metabolic[Title] OR diabetes[Title] OR '
    'coronary[Title] OR stroke[Title] OR "heart failure"[Title])'
)

SOURCE_RATES = {
    "pmc_aws": 5.0,
    "ncbi": 2.5,
    "europe_pmc": 2.5,
    "crossref": 0.9,
    "openalex": 2.0,
    "biorxiv": 1.0,
    "unpaywall": 2.0,
}

CONTACT_EMAIL = os.environ.get("SCHOLARLY_API_EMAIL", "").strip()
NCBI_KEY = os.environ.get("NCBI_API_KEY", "").strip()
OPENALEX_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def parse_date(value: Any) -> dt.date | None:
    """Parse a conservative public date from a string or Crossref date-parts."""
    if not value:
        return None
    if isinstance(value, dict) and "date-parts" in value:
        value = value["date-parts"]
    if isinstance(value, list):
        if value and isinstance(value[0], list):
            value = value[0]
        if not value:
            return None
        parts = [int(x) for x in value[:3]]
        while len(parts) < 3:
            parts.append(1)
        try:
            return dt.date(*parts)
        except ValueError:
            return None
    text = str(value).strip()
    month_names = {
        name.lower(): index
        for index, name in enumerate(
            ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
            start=1,
        )
    }
    textual = re.search(
        r"(\d{4})\s+([A-Za-z]{3,9})(?:\s+(\d{1,2}))?", text
    )
    if textual:
        month = month_names.get(textual.group(2)[:3].lower())
        if month:
            return dt.date(
                int(textual.group(1)), month, int(textual.group(3) or 1)
            )
    match = re.search(r"(\d{4})(?:[-/](\d{1,2}))?(?:[-/](\d{1,2}))?", text)
    if not match:
        return None
    year = int(match.group(1))
    month = int(match.group(2) or 1)
    day = int(match.group(3) or 1)
    try:
        return dt.date(year, month, day)
    except ValueError:
        return None


def date_text(value: Any) -> str:
    if isinstance(value, dict) and "date-parts" in value:
        value = value["date-parts"]
    if isinstance(value, list):
        if value and isinstance(value[0], list):
            value = value[0]
        if not value:
            return ""
        try:
            parts = [int(x) for x in value[:3]]
        except (TypeError, ValueError):
            return ""
        if len(parts) == 1:
            return f"{parts[0]:04d}"
        if len(parts) == 2:
            return f"{parts[0]:04d}-{parts[1]:02d}"
        return f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"
    parsed = parse_date(value)
    return parsed.isoformat() if parsed else ""


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value.rstrip(" .")


def article_ids(summary: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in summary.get("articleids", []):
        kind = (item.get("idtype") or "").lower()
        value = item.get("value") or ""
        if kind and value:
            result[kind] = value
    return result


def ssl_context() -> ssl.SSLContext:
    configured = os.environ.get("SSL_CERT_FILE")
    if configured:
        return ssl.create_default_context(cafile=configured)
    defaults = ssl.get_default_verify_paths()
    if defaults.cafile and os.path.exists(defaults.cafile):
        return ssl.create_default_context()
    if os.path.exists("/etc/ssl/cert.pem"):
        return ssl.create_default_context(cafile="/etc/ssl/cert.pem")
    return ssl.create_default_context()


class CachedClient:
    def __init__(self) -> None:
        self.context = ssl_context()
        self.last_request: dict[str, float] = {}
        self.records: list[dict[str, Any]] = []

    def _wait(self, source: str) -> None:
        interval = 1.0 / SOURCE_RATES[source]
        elapsed = time.monotonic() - self.last_request.get(source, 0.0)
        if elapsed < interval:
            time.sleep(interval - elapsed)

    def get_json(
        self,
        source: str,
        url: str,
        params: dict[str, Any] | None = None,
        *,
        allow_error: bool = False,
    ) -> dict[str, Any]:
        params = {k: v for k, v in (params or {}).items() if v not in (None, "")}
        encoded = urllib.parse.urlencode(params, doseq=True)
        full_url = f"{url}?{encoded}" if encoded else url
        cache_key = hashlib.sha256(f"{source}\n{full_url}".encode()).hexdigest()
        path = RAW / source / f"{cache_key}.json"
        if path.exists():
            envelope = json.loads(path.read_text(encoding="utf-8"))
            cleaned = sanitize_response(source, envelope["response"])
            if cleaned != envelope["response"]:
                envelope["response"] = cleaned
                path.write_text(
                    json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
            envelope["provenance"]["cache_hit"] = True
            self.records.append(envelope["provenance"])
            return envelope["response"]

        headers = {
            "Accept": "application/json",
            "User-Agent": (
                "RsearchPaper-corpus-audit/1.0"
                + (f" (mailto:{CONTACT_EMAIL})" if CONTACT_EMAIL else "")
            ),
        }
        error: Exception | None = None
        for attempt in range(1, 6):
            self._wait(source)
            request = urllib.request.Request(full_url, headers=headers)
            retrieved = utc_now()
            try:
                with urllib.request.urlopen(
                    request, timeout=45, context=self.context
                ) as response:
                    body = response.read()
                    self.last_request[source] = time.monotonic()
                    payload = sanitize_response(
                        source, json.loads(body.decode("utf-8"))
                    )
                    provenance = {
                        "source": source,
                        "request_url": full_url,
                        "retrieved_at_utc": retrieved,
                        "http_status": response.status,
                        "response_sha256": hashlib.sha256(body).hexdigest(),
                        "cache_path": str(path.relative_to(ROOT)),
                        "cache_hit": False,
                        "attempts": attempt,
                        "rate_limit": response.headers.get("X-RateLimit-Limit", ""),
                        "rate_remaining": response.headers.get("X-RateLimit-Remaining", ""),
                        "retry_after": response.headers.get("Retry-After", ""),
                    }
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(
                        json.dumps(
                            {"provenance": provenance, "response": payload},
                            ensure_ascii=False,
                            indent=2,
                            sort_keys=True,
                        )
                        + "\n",
                        encoding="utf-8",
                    )
                    self.records.append(provenance)
                    return payload
            except urllib.error.HTTPError as exc:
                error = exc
                self.last_request[source] = time.monotonic()
                if exc.code not in {429, 500, 502, 503, 504}:
                    break
                retry_after = exc.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 2 ** (attempt - 1)
                time.sleep(min(delay, 30) + 0.1 * attempt)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                error = exc
                self.last_request[source] = time.monotonic()
                time.sleep(min(2 ** (attempt - 1), 30) + 0.1 * attempt)
        if allow_error:
            return {"_incomplete": True, "_error": str(error), "_url": full_url}
        raise RuntimeError(f"{source} request failed after retries: {full_url}: {error}")

    def write_manifest(self) -> None:
        path = RAW / "request-manifest.csv"
        fields = [
            "source", "request_url", "retrieved_at_utc", "http_status",
            "response_sha256", "cache_path", "cache_hit", "attempts",
            "rate_limit", "rate_remaining", "retry_after",
        ]
        unique = {r["cache_path"]: r for r in self.records}
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(sorted(unique.values(), key=lambda r: (r["source"], r["cache_path"])))


def sanitize_response(source: str, value: Any) -> Any:
    """Remove copyrighted abstract text while preserving its audit digest."""
    if source not in {"biorxiv", "crossref"}:
        return value
    if isinstance(value, list):
        return [sanitize_response(source, item) for item in value]
    if not isinstance(value, dict):
        return value
    out = {}
    for key, item in value.items():
        if key in {"abstract", "preprint_abstract"} and isinstance(item, str):
            out[f"{key}_sha256"] = hashlib.sha256(item.encode("utf-8")).hexdigest()
            out[f"{key}_omitted"] = "copyright-sensitive text omitted"
        else:
            out[key] = sanitize_response(source, item)
    return out


def ncbi_params(extra: dict[str, Any]) -> dict[str, Any]:
    values = dict(extra)
    values["retmode"] = "json"
    if CONTACT_EMAIL:
        values["email"] = CONTACT_EMAIL
    values["tool"] = "RsearchPaper"
    if NCBI_KEY:
        values["api_key"] = NCBI_KEY
    return values


def discover(client: CachedClient) -> list[dict[str, Any]]:
    """Write the complete, fixed July 2026 discovery frame before screening."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search = client.get_json(
        "ncbi",
        f"{base}/esearch.fcgi",
        ncbi_params(
            {
                "db": "pmc",
                "term": DISCOVERY_QUERY,
                "retmax": 1000,
                "sort": "pub date",
            }
        ),
    )["esearchresult"]
    ids = search["idlist"]
    summaries: dict[str, Any] = {}
    for start in range(0, len(ids), 100):
        batch = ids[start : start + 100]
        response = client.get_json(
            "ncbi",
            f"{base}/esummary.fcgi",
            ncbi_params({"db": "pmc", "id": ",".join(batch)}),
        )["result"]
        for uid in batch:
            summaries[uid] = response[uid]

    prior = prior_candidates()
    rows: list[dict[str, Any]] = []
    for uid in ids:
        summary = summaries[uid]
        ids_map = article_ids(summary)
        pmcid = ids_map.get("pmc") or f"PMC{uid}"
        title = re.sub(r"<[^>]+>", "", summary.get("title", "")).strip()
        rows.append(
            {
                "discovery_run": "DISC-2026-07-29-PMC-01",
                "source": "NCBI ESearch db=pmc",
                "query": DISCOVERY_QUERY,
                "query_translation": search.get("querytranslation", ""),
                "retrieved_at_utc": utc_now(),
                "pmc_uid": uid,
                "pmcid": pmcid,
                "pmid": ids_map.get("pubmed", ""),
                "doi": normalize_doi(ids_map.get("doi", "")),
                "title": title,
                "pubdate": summary.get("pubdate", ""),
                "existing_48_candidate": "yes" if pmcid in prior else "no",
                "automated_scope_flag": title_scope_flag(title),
            }
        )
    path = INTERIM / "discovered-candidates.csv"
    write_csv(path, rows)
    return rows


def title_scope_flag(title: str) -> str:
    lower = title.lower()
    exclusions = {
        "prediction_or_ml": ("prediction model", "machine learning", "risk score", "predictive model"),
        "genetic_or_omics": ("genetic", "polygenic", "mendelian", "proteomic", "transcriptomic"),
        "meta_or_review": ("meta-analysis", "systematic review"),
        "cross_sectional": ("cross-sectional",),
        "nonhuman": ("rat ", "mice", "mouse", "porcine"),
    }
    for code, terms in exclusions.items():
        if any(term in lower for term in terms):
            return f"exclude_title:{code}"
    return "requires_full_text_screen"


def prior_candidates() -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    with (INTERIM / "screening-judgements.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row["_prior_disposition"] = row["inclusion_recommendation"]
            records[row["pmcid"]] = row
    with (INTERIM / "screening-exclusions.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row["_prior_disposition"] = row["reason_code"]
            records[row["pmcid"]] = row
    return records


def fetch_ncbi_summaries(client: CachedClient, pmcids: list[str]) -> dict[str, dict[str, Any]]:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    out: dict[str, dict[str, Any]] = {}
    for start in range(0, len(pmcids), 100):
        batch = pmcids[start : start + 100]
        numeric = [x.removeprefix("PMC") for x in batch]
        result = client.get_json(
            "ncbi", base, ncbi_params({"db": "pmc", "id": ",".join(numeric)})
        )["result"]
        for pmcid, uid in zip(batch, numeric):
            if uid in result:
                out[pmcid] = result[uid]
    return out


def provider_record(
    client: CachedClient, pmcid: str, doi: str, ncbi: dict[str, Any]
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "pmcid": pmcid,
        "doi": doi,
        "ncbi_status": "complete",
        "ncbi_pubdate": ncbi.get("pubdate", ""),
        "ncbi_epubdate": ncbi.get("epubdate", ""),
    }

    pmc_metadata: dict[str, Any] = {}
    for version in range(1, 4):
        candidate = client.get_json(
            "pmc_aws",
            f"https://pmc-oa-opendata.s3.amazonaws.com/metadata/{pmcid}.{version}.json",
            allow_error=True,
        )
        if not candidate.get("_incomplete"):
            pmc_metadata = candidate
            # Version 1 is present for the overwhelming majority of records.
            # A higher version is tried only when the lower object is absent.
            break
    if pmc_metadata:
        record.update(
            {
                "pmc_aws_status": "complete",
                "pmc_aws_article_version": pmc_metadata.get("version", ""),
                "pmc_aws_license": pmc_metadata.get("license_code", ""),
                "pmc_aws_open_access": str(
                    pmc_metadata.get("is_pmc_openaccess", "")
                ).lower(),
                "pmc_aws_retracted": str(
                    pmc_metadata.get("is_retracted", "")
                ).lower(),
                "pmc_aws_xml_url": pmc_metadata.get("xml_url", ""),
            }
        )
    else:
        record["pmc_aws_status"] = "not_found_or_source_incomplete"

    epmc = client.get_json(
        "europe_pmc",
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        {
            "query": pmcid,
            "resultType": "lite",
            "pageSize": 2,
            "format": "json",
            "email": CONTACT_EMAIL,
        },
        allow_error=True,
    )
    epmc_items = epmc.get("resultList", {}).get("result", [])
    if epmc.get("_incomplete"):
        record["europe_pmc_status"] = "source_incomplete"
    elif not epmc_items:
        record["europe_pmc_status"] = "not_found"
    else:
        item = epmc_items[0]
        record.update(
            {
                "europe_pmc_status": "complete",
                "europe_pmc_first_publication_date": item.get("firstPublicationDate", ""),
                "europe_pmc_electronic_publication_date": item.get("electronicPublicationDate", ""),
                "europe_pmc_first_index_date": item.get("firstIndexDate", ""),
                "europe_pmc_open_access": str(item.get("isOpenAccess", "")).lower(),
            }
        )

    if doi:
        crossref = client.get_json(
            "crossref",
            "https://api.crossref.org/works",
            {
                "filter": f"doi:{doi}",
                "rows": 1,
                "mailto": CONTACT_EMAIL,
            },
            allow_error=True,
        )
        items = crossref.get("message", {}).get("items", [])
        if crossref.get("_incomplete"):
            record["crossref_status"] = "source_incomplete"
        elif not items:
            record["crossref_status"] = "not_found"
        else:
            item = items[0]
            record.update(
                {
                    "crossref_status": "complete",
                    "crossref_published_online": date_text(item.get("published-online")),
                    "crossref_published_print": date_text(item.get("published-print")),
                    "crossref_issued": date_text(item.get("issued")),
                    "crossref_created": date_text(item.get("created", {}).get("date-parts")),
                    "crossref_deposited": date_text(item.get("deposited", {}).get("date-parts")),
                    "crossref_relation": canonical_json(item.get("relation", {})),
                }
            )

        openalex_params: dict[str, Any] = {
            "filter": f"doi:{doi}",
            "per-page": 1,
            "select": (
                "id,doi,title,publication_date,ids,primary_location,locations,"
                "open_access,type,authorships,updated_date"
            ),
        }
        if OPENALEX_KEY:
            openalex_params["api_key"] = OPENALEX_KEY
        openalex = client.get_json(
            "openalex",
            "https://api.openalex.org/works",
            openalex_params,
            allow_error=True,
        )
        oa_items = openalex.get("results", [])
        if openalex.get("_incomplete"):
            record["openalex_status"] = "source_incomplete"
        elif not oa_items:
            record["openalex_status"] = "not_found"
        else:
            item = oa_items[0]
            record.update(
                {
                    "openalex_status": (
                        "complete_keyed" if OPENALEX_KEY
                        else "complete_unauthenticated_compatibility"
                    ),
                    "openalex_id": item.get("id", ""),
                    "openalex_publication_date": item.get("publication_date", ""),
                    "openalex_updated_date": item.get("updated_date", ""),
                }
            )

        matches: list[dict[str, Any]] = []
        for server in ("medrxiv", "biorxiv"):
            pubs = client.get_json(
                "biorxiv",
                f"https://api.biorxiv.org/pubs/{server}/{urllib.parse.quote(doi, safe='/')}",
                allow_error=True,
            )
            if pubs.get("_incomplete"):
                record[f"{server}_status"] = "source_incomplete"
            else:
                collection = pubs.get("collection", [])
                record[f"{server}_status"] = "match" if collection else "not_found"
                matches.extend(collection)
        if matches:
            earliest = min(
                (parse_date(x.get("preprint_date")) for x in matches),
                default=None,
            )
            record["preprint_first_date"] = earliest.isoformat() if earliest else ""
            record["preprint_matches"] = canonical_json(matches)
        else:
            record["preprint_first_date"] = ""
            record["preprint_matches"] = "[]"
    else:
        for key in (
            "crossref_status", "openalex_status", "medrxiv_status", "biorxiv_status"
        ):
            record[key] = "not_applicable_no_doi"

    if not CONTACT_EMAIL:
        record["unpaywall_status"] = "source_incomplete_missing_contact_email"
    elif doi:
        unpaywall = client.get_json(
            "unpaywall",
            f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi, safe='/')}",
            {"email": CONTACT_EMAIL},
            allow_error=True,
        )
        if unpaywall.get("_incomplete"):
            record["unpaywall_status"] = "source_incomplete"
        else:
            record["unpaywall_status"] = "complete"
            record["unpaywall_published_date"] = unpaywall.get("published_date", "")
            record["unpaywall_oa_status"] = unpaywall.get("oa_status", "")
            record["unpaywall_best_location"] = canonical_json(
                unpaywall.get("best_oa_location", {})
            )
    else:
        record["unpaywall_status"] = "not_applicable_no_doi"

    public_dates = []
    for field, lineage in (
        ("preprint_first_date", "preprint_server"),
        ("crossref_published_online", "publisher_crossref"),
        ("crossref_issued", "publisher_crossref"),
        ("europe_pmc_first_publication_date", "bibliographic_index"),
        ("europe_pmc_electronic_publication_date", "bibliographic_index"),
        ("ncbi_epubdate", "bibliographic_index"),
        ("ncbi_pubdate", "bibliographic_index"),
        ("openalex_publication_date", "crossref_derived_index"),
    ):
        raw_date = str(record.get(field, ""))
        # A year-only value does not identify public availability within the
        # cutoff window and must not be normalized to January 1.
        parsed = parse_date(raw_date) if len(raw_date) >= 7 else None
        if parsed:
            public_dates.append((parsed, field, lineage))
    if public_dates:
        earliest = min(public_dates)
        record["computed_earliest_public_date"] = earliest[0].isoformat()
        record["computed_earliest_public_source"] = earliest[1]
        record["date_lineages"] = ";".join(sorted({x[2] for x in public_dates}))
        spread = (max(x[0] for x in public_dates) - min(x[0] for x in public_dates)).days
        straddles_cutoff = min(x[0] for x in public_dates) < CUTOFF <= max(
            x[0] for x in public_dates
        )
        record["date_conflict"] = "yes" if (straddles_cutoff or spread > 180) else "no"
        if earliest[0] < CUTOFF:
            record["crosscheck_disposition"] = "ineligible_pre_cutoff"
            record["human_date_review_required"] = "no"
        elif record["date_conflict"] == "yes":
            record["crosscheck_disposition"] = "unresolved_date_conflict"
            record["human_date_review_required"] = "yes"
        elif len({x[2] for x in public_dates if x[2] != "crossref_derived_index"}) >= 2:
            record["crosscheck_disposition"] = "verified_post_cutoff_metadata"
            record["human_date_review_required"] = "no"
        else:
            record["crosscheck_disposition"] = "unresolved_single_lineage"
            record["human_date_review_required"] = "yes"
    else:
        record["computed_earliest_public_date"] = ""
        record["computed_earliest_public_source"] = ""
        record["date_lineages"] = ""
        record["date_conflict"] = "unknown"
        record["crosscheck_disposition"] = "source_incomplete_no_public_date"
        record["human_date_review_required"] = "yes"
    return record


def verify(client: CachedClient) -> list[dict[str, Any]]:
    prior = prior_candidates()
    discovery_path = INTERIM / "discovered-candidates.csv"
    discovery = (
        list(csv.DictReader(discovery_path.open(encoding="utf-8")))
        if discovery_path.exists()
        else discover(client)
    )
    combined: dict[str, dict[str, str]] = {}
    for pmcid, row in prior.items():
        combined[pmcid] = {
            "pmcid": pmcid,
            "candidate_origin": "prior_48",
            "prior_disposition": row["_prior_disposition"],
            "discovery_scope_flag": "",
        }
    for row in discovery:
        pmcid = row["pmcid"]
        combined.setdefault(
            pmcid,
            {
                "pmcid": pmcid,
                "candidate_origin": "extended_discovery",
                "prior_disposition": "",
                "discovery_scope_flag": row["automated_scope_flag"],
            },
        )
        if combined[pmcid]["candidate_origin"] == "prior_48":
            combined[pmcid]["candidate_origin"] = "prior_48+extended_discovery"
            combined[pmcid]["discovery_scope_flag"] = row["automated_scope_flag"]

    pmcids = sorted(combined)
    summaries = fetch_ncbi_summaries(client, pmcids)
    rows = []
    for index, pmcid in enumerate(pmcids, start=1):
        summary = summaries.get(pmcid, {})
        ids = article_ids(summary)
        doi = normalize_doi(ids.get("doi", ""))
        row = dict(combined[pmcid])
        row["title"] = re.sub(r"<[^>]+>", "", summary.get("title", "")).strip()
        row["pmid"] = ids.get("pubmed", "")
        row["doi"] = doi
        row.update(provider_record(client, pmcid, doi, summary))
        rows.append(row)
        print(f"[{index}/{len(pmcids)}] {pmcid} {row['crosscheck_disposition']}")

    write_csv(INTERIM / "metadata-crosscheck.csv", rows)
    write_source_status(rows)
    return rows


def write_source_status(rows: list[dict[str, Any]]) -> None:
    sources = [
        "pmc_aws", "ncbi", "europe_pmc", "crossref", "openalex",
        "medrxiv", "biorxiv", "unpaywall",
    ]
    output = []
    for source in sources:
        field = f"{source}_status"
        counts: dict[str, int] = {}
        for row in rows:
            value = row.get(field, "not_recorded")
            counts[value] = counts.get(value, 0) + 1
        output.append(
            {
                "source": source,
                "records": len(rows),
                "status_counts": canonical_json(counts),
                "run_at_utc": utc_now(),
            }
        )
    write_csv(INTERIM / "source-access-status.csv", output)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("discover", "verify", "all"))
    args = parser.parse_args()
    client = CachedClient()
    if args.command in {"discover", "all"}:
        rows = discover(client)
        print(f"discovered {len(rows)} candidates")
    if args.command in {"verify", "all"}:
        rows = verify(client)
        print(f"cross-checked {len(rows)} unique candidates")
    client.write_manifest()


if __name__ == "__main__":
    main()

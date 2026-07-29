#!/usr/bin/env python3
"""Blind corpus screening helper for the eight-paragraph feasibility pilot.

Fetches a PubMed Central Open Access Subset article's JATS XML from the
AWS Open Data mirror of the PMC OA Subset (s3://pmc-oa-opendata) and reports
the fields the screening protocol requires:

  * bibliographic metadata (title, authors, journal, DOI, PMCID, PMID)
  * the verbatim <permissions> block (OA subset membership + license)
  * every date the record carries (history, epub, ppub, collection)
  * section structure of the body
  * paragraph inventory with word counts, section labels and opening words
  * table/figure reference density per paragraph

It performs no model generation and no judgement about eligibility; a human
or a screening agent reads the output and records the decision.

Usage:
    python3 scripts/screen_pmc_article.py PMC12345678 [--paras] [--section Results]
    python3 scripts/screen_pmc_article.py PMC12345678 --dump-para 41
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

S3_BASE = "https://pmc-oa-opendata.s3.amazonaws.com"
CACHE = os.environ.get(
    "PMC_CACHE",
    "/tmp/claude-0/-home-user-RsearchPaper/"
    "4994eabd-f287-5f59-a550-da2245dfc4ce/scratchpad/pmc-cache",
)


def _get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as fh:
        return fh.read()


def resolve_key(pmcid: str) -> str:
    """Find the highest available version prefix for a PMCID in the bucket."""
    listing = _get(
        f"{S3_BASE}/?list-type=2&delimiter=/&prefix={pmcid}."
    ).decode("utf-8", "replace")
    versions = sorted(
        set(re.findall(rf"<Prefix>({re.escape(pmcid)}\.(\d+))/</Prefix>", listing)),
        key=lambda m: int(m[1]),
    )
    if not versions:
        raise SystemExit(f"{pmcid}: not present in the PMC OA Subset bucket")
    stem = versions[-1][0]
    return f"{stem}/{stem}.xml"


def fetch_xml(pmcid: str) -> bytes:
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{pmcid}.xml")
    if os.path.exists(path):
        with open(path, "rb") as fh:
            return fh.read()
    key = resolve_key(pmcid)
    blob = _get(f"{S3_BASE}/{key}")
    with open(path, "wb") as fh:
        fh.write(blob)
    with open(os.path.join(CACHE, f"{pmcid}.key"), "w") as fh:
        fh.write(key)
    return blob


# Elements whose text is display material, not running prose. JATS routinely
# nests these *inside* <p>, so flattening naively mixes table and figure
# captions into the paragraph body and inflates word counts.
NON_PROSE = {
    "table-wrap", "fig", "fig-group", "table-wrap-group", "graphic",
    "media", "supplementary-material", "disp-formula", "alternatives",
    "table", "array", "label", "caption",
}


def _flatten(node, skip_non_prose: bool = True) -> str:
    """Flatten an element to whitespace-normalised running-prose text."""
    if node is None:
        return ""
    parts = [node.text or ""]
    for child in node:
        if skip_non_prose and child.tag in NON_PROSE:
            pass  # drop the display object, keep the prose that follows it
        else:
            parts.append(_flatten(child, skip_non_prose))
        parts.append(child.tail or "")
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def embedded_objects(node) -> list[str]:
    """Names of display objects physically nested inside a paragraph."""
    return [c.tag for c in node.iter() if c.tag in {"table-wrap", "fig", "supplementary-material"}]


def xref_kinds(node) -> list[str]:
    return [x.get("ref-type", "?") for x in node.iter("xref")]


def article_meta(root) -> dict:
    meta = root.find(".//front/article-meta")
    jmeta = root.find(".//front/journal-meta")
    ids = {i.get("pub-id-type"): (i.text or "").strip()
           for i in meta.findall("article-id")}

    authors = []
    for c in meta.findall(".//contrib[@contrib-type='author']"):
        sn = c.findtext("name/surname") or ""
        gn = c.findtext("name/given-names") or ""
        if sn or gn:
            authors.append(f"{sn} {gn}".strip())

    dates = {}
    for d in meta.findall("pub-date"):
        label = d.get("pub-type") or d.get("date-type") or "pub-date"
        label = f"pub-date[{label}]"
        dates.setdefault(label, []).append(_ymd(d))
    for d in meta.findall("history/date"):
        dates.setdefault(f"history[{d.get('date-type')}]", []).append(_ymd(d))

    perms = meta.find("permissions")
    lic = perms.find("license") if perms is not None else None
    lic_href = None
    lic_type = None
    if lic is not None:
        lic_type = lic.get("license-type")
        lic_href = lic.get("{http://www.w3.org/1999/xlink}href")
        ref = lic.find("{http://www.niso.org/schemas/ali/1.0/}license_ref")
        if ref is not None:
            lic_href = lic_href or (ref.text or "").strip()
            lic_type = lic_type or ref.get("content-type")

    return {
        "pmcid": ids.get("pmcid") or ("PMC" + ids.get("pmc", "")),
        "pmid": ids.get("pmid", ""),
        "doi": ids.get("doi", ""),
        "title": _flatten(meta.find("title-group/article-title"))
        if meta.find("title-group/article-title") is not None else "",
        "journal": (jmeta.findtext("journal-title-group/journal-title")
                    or jmeta.findtext("journal-title") or "") if jmeta is not None else "",
        "publisher": jmeta.findtext("publisher/publisher-name") if jmeta is not None else "",
        "authors": authors,
        "n_authors": len(authors),
        "dates": dates,
        "license_type": lic_type,
        "license_href": lic_href,
        "permissions_text": _flatten(perms) if perms is not None else "",
        "article_type": root.getroot().get("article-type") if hasattr(root, "getroot")
        else root.get("article-type"),
    }


def _ymd(d) -> str:
    y = d.findtext("year") or "????"
    m = d.findtext("month") or ""
    day = d.findtext("day") or ""
    return "-".join(x for x in [y, m.zfill(2) if m else "", day.zfill(2) if day else ""] if x)


def paragraphs(root) -> list[dict]:
    """Walk body sections, returning every <p> with its section path."""
    body = root.find(".//body")
    rows: list[dict] = []
    if body is None:
        return rows

    def walk(node, path):
        for child in node:
            if child.tag == "sec":
                title = _flatten(child.find("title")) if child.find("title") is not None else ""
                walk(child, path + [title or "(untitled)"])
            elif child.tag == "p":
                txt = _flatten(child)
                rows.append({
                    "idx": len(rows),
                    "section": " > ".join(path) if path else "(body root)",
                    "words": len(txt.split()),
                    "xrefs": xref_kinds(child),
                    "embedded": embedded_objects(child),
                    "opening": " ".join(txt.split()[:12]),
                    "text": txt,
                })
            elif child.tag in {"boxed-text", "app", "statement"}:
                walk(child, path + [child.tag])

    walk(body, [])
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pmcid")
    ap.add_argument("--paras", action="store_true", help="list paragraph inventory")
    ap.add_argument("--section", help="only paragraphs whose section path matches (case-insensitive)")
    ap.add_argument("--min-words", type=int, default=0)
    ap.add_argument("--max-words", type=int, default=10**6)
    ap.add_argument("--dump-para", type=int, help="print one paragraph in full")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    blob = fetch_xml(args.pmcid)
    root = ET.fromstring(blob)
    meta = article_meta(root)
    meta["article_type"] = root.get("article-type")
    paras = paragraphs(root)

    if args.dump_para is not None:
        p = paras[args.dump_para]
        print(f"[{p['idx']}] {p['section']}  ({p['words']} words, xrefs={p['xrefs']})\n")
        print(p["text"])
        return

    if args.json:
        print(json.dumps({"meta": meta, "n_paragraphs": len(paras)}, indent=2))
        return

    print(f"PMCID       : {meta['pmcid']}   PMID: {meta['pmid']}")
    print(f"DOI         : {meta['doi']}")
    print(f"Article type: {meta['article_type']}")
    print(f"Title       : {meta['title']}")
    print(f"Journal     : {meta['journal']}  ({meta['publisher']})")
    print(f"Authors     : {meta['n_authors']} — {', '.join(meta['authors'][:4])}"
          f"{' ...' if meta['n_authors'] > 4 else ''}")
    print(f"License     : {meta['license_type']}  {meta['license_href']}")
    print(f"Permissions : {meta['permissions_text'][:400]}")
    print("Dates       :")
    for k, v in sorted(meta["dates"].items()):
        print(f"    {k:28s} {', '.join(v)}")

    secs = []
    for p in paras:
        top = p["section"].split(" > ")[0]
        if top not in secs:
            secs.append(top)
    print(f"Top sections: {secs}")
    print(f"Body <p> count: {len(paras)}")

    if args.paras:
        print("\nidx  words  xrefs(tbl/fig)  section :: opening")
        for p in paras:
            if args.section and args.section.lower() not in p["section"].lower():
                continue
            if not (args.min_words <= p["words"] <= args.max_words):
                continue
            nt = sum(1 for x in p["xrefs"] if x == "table")
            nf = sum(1 for x in p["xrefs"] if x == "fig")
            emb = f" [emb:{','.join(sorted(set(p['embedded'])))}]" if p["embedded"] else ""
            print(f"{p['idx']:3d}  {p['words']:5d}  t{nt}/f{nf:<3d}  "
                  f"{p['section'][:58]} :: {p['opening']}{emb}")


if __name__ == "__main__":
    main()

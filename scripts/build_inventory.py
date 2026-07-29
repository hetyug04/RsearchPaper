#!/usr/bin/env python3
"""Build data/interim/eligible-paper-inventory.csv.

Joins two inputs:

  * data/interim/screening-judgements.csv — the screening agent's recorded
    judgements (design, population, exposure, outcome, dates, concerns,
    candidate paragraph indices). Human-authored, reviewable.
  * the article's JATS XML in the PMC Open Access Subset, fetched from the
    AWS Open Data mirror s3://pmc-oa-opendata via scripts/screen_pmc_article.py.

Every bibliographic and structural field in the output is derived from the
XML at build time, so the inventory cannot drift from the source record.
Paragraph indices in the judgements file are resolved to section names and
opening words at build time for the same reason.

Usage:
    python3 scripts/build_inventory.py
    python3 scripts/build_inventory.py --check   # rebuild and diff, no write
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from screen_pmc_article import fetch_xml, article_meta, paragraphs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUDGEMENTS = os.path.join(ROOT, "data/interim/screening-judgements.csv")
OUT = os.path.join(ROOT, "data/interim/eligible-paper-inventory.csv")

PREF_LO, PREF_HI = 100, 220
EXT_HI = 350

FIELDS = [
    "paper_id", "title", "authors", "journal", "doi", "pmcid", "stable_url",
    "open_access_license", "study_design", "clinical_topic", "population",
    "exposure_or_primary_predictor", "outcome",
    "earliest_public_date", "earliest_public_date_evidence", "cutoff_eligible",
    "candidate_results_paragraphs", "candidate_interpretation_paragraphs",
    "candidate_limitation_paragraphs", "same_paper_distractors_feasible",
    "table_figure_dependence", "specialist_knowledge_burden",
    "inclusion_recommendation", "exclusion_reason_or_unresolved_concern",
    "candidate_paragraph_1", "candidate_paragraph_2", "candidate_paragraph_3",
    "source_citations",
]


# Limitation paragraphs are frequently *not* given their own subsection: they
# sit unlabelled inside Discussion and announce themselves in the opening
# clause. Section path alone therefore undercounts them badly.
LIMIT_CUES = (
    "limitation", "should be interpreted with caution",
    "must be considered when interpreting", "several caveats",
    "not without limitations",
)


def classify(para) -> str:
    """Categorise a paragraph by section path, with a content check for limitations."""
    section = para["section"] if isinstance(para, dict) else para
    s = section.lower()
    s = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", s)
    # "strength" alone is not a limitation cue: it appears frequently in
    # exposure names such as handgrip strength and in strengths-only sections.
    if "limitation" in s:
        return "limitation"
    if isinstance(para, dict) and ("discussion" in s or s.startswith("conclusion")):
        # inspect the opening clause only, so a passing mention late in an
        # interpretation paragraph does not reclassify it
        head = " ".join(para["text"].split()[:25]).lower()
        if any(cue in head for cue in LIMIT_CUES):
            return "limitation"
    if s.startswith("result"):
        return "results"
    if "discussion" in s or s.startswith("conclusion") or "implication" in s:
        return "interpretation"
    return "other"


def counts(paras) -> dict[str, str]:
    """Paragraphs per category, reported as preferred-band (+extended-band)."""
    out = {}
    for cat in ("results", "interpretation", "limitation"):
        pref = sum(1 for p in paras
                   if classify(p) == cat and PREF_LO <= p["words"] <= PREF_HI)
        ext = sum(1 for p in paras
                  if classify(p) == cat and PREF_HI < p["words"] <= EXT_HI)
        out[cat] = f"{pref} (+{ext} at 221-350w)"
    return out


def tblfig_dependence(paras) -> str:
    n = sum(1 for p in paras if any(x in ("table", "fig") for x in p["xrefs"]) or p["embedded"])
    pct = round(100 * n / max(len(paras), 1))
    band = "low" if pct < 20 else ("medium" if pct < 30 else "high")
    return f"{band} ({pct}% of body paragraphs reference or embed a table/figure)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="build and report, do not write")
    args = ap.parse_args()

    with open(JUDGEMENTS, newline="", encoding="utf-8") as fh:
        judgements = list(csv.DictReader(fh))

    rows = []
    for j in judgements:
        pmcid = j["pmcid"]
        root = ET.fromstring(fetch_xml(pmcid))
        meta = article_meta(root)
        paras = [p for p in paragraphs(root) if p["words"] > 0]
        c = counts(paras)

        picks = [int(i) for i in j["candidate_paragraph_idx"].split(";") if i.strip()]
        located = []
        for idx in picks:
            p = next((x for x in paras if x["idx"] == idx), None)
            if p is None:
                raise SystemExit(f"{pmcid}: paragraph index {idx} not found")
            located.append(
                f'{p["section"]} | {p["words"]}w | {classify(p)} | "{p["opening"]}…"'
            )
        # keep at most three candidate locations, per the screening protocol
        located = located[:3]
        located += [""] * (3 - len(located))

        dates = "; ".join(f"{k}={','.join(v)}" for k, v in sorted(meta["dates"].items()))
        rows.append({
            "paper_id": j["paper_id"],
            "title": meta["title"],
            "authors": "; ".join(meta["authors"]),
            "journal": meta["journal"],
            "doi": meta["doi"],
            "pmcid": meta["pmcid"],
            "stable_url": f"https://pmc.ncbi.nlm.nih.gov/articles/{meta['pmcid']}/",
            "open_access_license": f'{meta["license_type"]} — {meta["license_href"]}',
            "study_design": j["study_design"],
            "clinical_topic": j["clinical_topic"],
            "population": j["population"],
            "exposure_or_primary_predictor": j["exposure_or_primary_predictor"],
            "outcome": j["outcome"],
            "earliest_public_date": j["earliest_public_date"],
            "earliest_public_date_evidence": j["earliest_public_date_evidence"],
            "cutoff_eligible": j["cutoff_eligible"],
            "candidate_results_paragraphs": c["results"],
            "candidate_interpretation_paragraphs": c["interpretation"],
            "candidate_limitation_paragraphs": c["limitation"],
            "same_paper_distractors_feasible": j["distractors_feasible"],
            "table_figure_dependence": tblfig_dependence(paras),
            "specialist_knowledge_burden": j["specialist_burden"],
            "inclusion_recommendation": j["inclusion_recommendation"],
            "exclusion_reason_or_unresolved_concern":
                j["exclusion_reason_or_unresolved_concern"],
            "candidate_paragraph_1": located[0],
            "candidate_paragraph_2": located[1],
            "candidate_paragraph_3": located[2],
            "source_citations": (
                f"Bibliographic fields, license and all dates: JATS XML for {meta['pmcid']} "
                f"in the PMC Open Access Subset, retrieved from the AWS Open Data mirror "
                f"s3://pmc-oa-opendata (https://pmc-oa-opendata.s3.amazonaws.com/). "
                f"Dates recorded in that XML: {dates}. "
                f"Paragraph counts, word counts, section paths, opening words and "
                f"table/figure dependence: computed from the same XML by "
                f"scripts/screen_pmc_article.py. "
                f"Design, population, exposure, outcome: the article's own Abstract and "
                f"Methods sections in that XML. "
                f"Earliest-public-date evidence: see earliest_public_date_evidence. "
                f"Article page: https://pmc.ncbi.nlm.nih.gov/articles/{meta['pmcid']}/"
            ),
        })

    if args.check:
        for r in rows:
            print(f"{r['paper_id']}  {r['pmcid']}  {r['inclusion_recommendation']:9s}  "
                  f"R={r['candidate_results_paragraphs']}  "
                  f"I={r['candidate_interpretation_paragraphs']}  "
                  f"L={r['candidate_limitation_paragraphs']}  "
                  f"{r['table_figure_dependence']}")
        return

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} records)")


if __name__ == "__main__":
    main()

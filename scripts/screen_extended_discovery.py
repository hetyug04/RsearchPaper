#!/usr/bin/env python3
"""Structural screen for every record in the fixed extended discovery frame."""

from __future__ import annotations

import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_inventory import classify  # noqa: E402
from screen_pmc_article import article_meta, fetch_xml, paragraphs  # noqa: E402

PREF_LO, PREF_HI = 100, 220


def count_category(paras, category):
    return sum(
        1
        for para in paras
        if classify(para) == category and PREF_LO <= para["words"] <= PREF_HI
    )


def main():
    source = ROOT / "data/interim/discovered-candidates.csv"
    rows = []
    for index, candidate in enumerate(csv.DictReader(source.open(encoding="utf-8")), 1):
        result = dict(candidate)
        if candidate["automated_scope_flag"].startswith("exclude_title:"):
            result.update(
                {
                    "pmc_xml_status": "not_fetched_title_exclusion",
                    "results_in_band": "0",
                    "interpretation_in_band": "0",
                    "limitation_in_band": "0",
                    "structural_disposition": candidate["automated_scope_flag"],
                    "human_full_text_review_required": "no",
                }
            )
            rows.append(result)
            continue
        try:
            root = ET.fromstring(fetch_xml(candidate["pmcid"]))
            meta = article_meta(root)
            paras = paragraphs(root)
            results = count_category(paras, "results")
            interpretation = count_category(paras, "interpretation")
            limitation = count_category(paras, "limitation")
            two_types = sum(x > 0 for x in (results, interpretation, limitation)) >= 2
            two_paras = results + interpretation + limitation >= 2
            if not meta["license_href"] and not meta["license_type"]:
                disposition = "exclude_no_machine_readable_license"
                review = "no"
            elif not two_paras or not two_types:
                disposition = "exclude_insufficient_paragraph_structure"
                review = "no"
            else:
                disposition = "structurally_eligible_pending_human_scope_review"
                review = "yes"
            result.update(
                {
                    "pmc_xml_status": "complete",
                    "open_access_license": meta["license_type"] or meta["license_href"],
                    "body_paragraphs": str(len(paras)),
                    "results_in_band": str(results),
                    "interpretation_in_band": str(interpretation),
                    "limitation_in_band": str(limitation),
                    "structural_disposition": disposition,
                    "human_full_text_review_required": review,
                }
            )
        except Exception as exc:
            result.update(
                {
                    "pmc_xml_status": f"source_incomplete:{type(exc).__name__}",
                    "results_in_band": "",
                    "interpretation_in_band": "",
                    "limitation_in_band": "",
                    "structural_disposition": "unresolved_source_incomplete",
                    "human_full_text_review_required": "yes",
                }
            )
        rows.append(result)
        print(f"[{index}] {candidate['pmcid']} {result['structural_disposition']}")

    output = ROOT / "data/interim/extended-discovery-screen.csv"
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {output} ({len(rows)} records)")


if __name__ == "__main__":
    main()

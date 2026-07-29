# Eligible-Paper Inventory — Extended Database Cross-Check

**Run:** `DISC-2026-07-29-PMC-01`
**Status:** complete for the pilot inventory; unresolved records remain flagged
**No model generation or judge evaluation was performed.**

## Executive result

The local-machine rerun replaced the original convenience search with a fixed,
rerunnable PMC query and a seven-source metadata audit.

- 119 papers were captured by the complete fixed discovery query.
- The 48 previously screened papers were all rechecked.
- The combined metadata audit covers 167 unique PMC records.
- 19 papers are now in the manually inspected eligible/reserve inventory.
- 34 manually inspected papers remain excluded, with reasons preserved.
- All 119 discovery records received title triage and structural XML screening;
  101 pass the automated paragraph-structure gate but require human scope review
  before they can enter the manually curated inventory.
- The frozen 3 Results / 3 interpretation / 2 limitation mixture remains
  feasible.

The original files are preserved under `data/interim/legacy/`. No prior
exclusion or raw metadata was silently overwritten.

## Reproducible discovery

The fixed query was run through NCBI ESearch against `db=pmc`:

```text
("2026/07/01"[Publication Date] : "2026/07/29"[Publication Date])
AND open_access[filter]
AND "cohort study"[Title]
AND (
  cardiovascular[Title] OR metabolic[Title] OR diabetes[Title]
  OR coronary[Title] OR stroke[Title] OR "heart failure"[Title]
)
```

This is an auditable pilot search frame, not a systematic-review claim. Its
deliberately narrow title/date window makes the complete result set small
enough to retain and screen without stopping after convenient papers appear.
The query, translation, pagination results, and retrieval timestamp are stored
in `data/interim/discovered-candidates.csv`.

## Database access

| Source | Access result | Role |
|---|---|---|
| PMC OA AWS | Complete through current PMCID-version metadata and XML paths | OA status, licence, retraction flag, JATS structure |
| NCBI E-utilities | Complete without API key at the public rate | Discovery, PMID/PMCID/DOI, bibliographic dates |
| Europe PMC | Queried for all records; 49 indexed, 118 not found at retrieval | Independent life-science index metadata |
| Crossref | Complete for all 167 DOI records using the public pool | Publisher dates, relations, conference abstracts |
| OpenAlex | Complete for all 167 via currently functioning unauthenticated compatibility access | Discovery corroboration and OA locations |
| medRxiv/bioRxiv | Complete published-DOI lookups; one medRxiv match, no bioRxiv matches | Explicit preprint mapping |
| Unpaywall | Incomplete for all records | A real contact email is required and was not invented |

Current OpenAlex documentation requests a free API key even though unkeyed
requests still succeeded. The pipeline supports `OPENALEX_API_KEY` and labels
this run `complete_unauthenticated_compatibility`. Unpaywall support is complete
in code but remains `source_incomplete_missing_contact_email`.

Raw metadata envelopes, response digests, canonical request URLs, retrieval
times, rate-limit headers, and cache paths are stored in provider JSONL bundles
under `data/raw/scholarly_metadata/bundles/`. Run
`python scripts/bundle_metadata_cache.py unpack` to restore the individual
request cache before an offline rebuild. Copyright-sensitive preprint abstracts are
replaced by SHA-256 digests in committed caches.

## Date decisions changed by the rerun

| PMCID | Prior status | Revised status | Evidence |
|---|---|---|---|
| PMC11467773 | date uncertain | confirmed pre-cutoff; excluded | NCBI/Crossref/OpenAlex place public release in Oct 2024 |
| PMC11695108 | date uncertain | date-eligible reserve | JATS, NCBI and Crossref give 2024-12-03 |
| PMC11969775 | date uncertain | date-eligible; added to inventory | 2025-04-04 across indexes; no mapped medRxiv/bioRxiv preprint |
| PMC12421259 | date uncertain | confirmed pre-cutoff; excluded | Crossref/OpenAlex record 2024-11-11 |
| PMC12093672 | conference abstract suspected | confirmed same analysis; excluded | full 2023 Crossref abstract matches cohort, sample, analysis and results |
| PMC12418469 | conference identity uncertain | conservative exclusion pending owner confirmation | full 2024 abstract matches cohort, sample, exposure, outcome and estimates, but lacks a unique cohort accession |

`conference-abstract-review.csv` records every component score and the evidence.

## Conference-abstract rule (D-005)

An earlier abstract counts only when a full abstract is available and both
study identity and central-analysis similarity are supported.

Study identity is scored 0–8 from a unique cohort/registry identifier, data
source and recruitment window, sample, author linkage, and population.
Central-analysis similarity is scored 0–8 from exposure, outcome, estimand,
effect, and adjustment/subgroup agreement.

- Automatic same study/analysis: identity ≥6, analysis ≥6, exposure and outcome
  both match, and no decisive conflict.
- Automatic different: either score ≤3 with positive contradictory evidence.
- Human review: scores 4–5, missing full abstract, unexplained sample changes,
  or conflicting evidence.

A preliminary-to-final sample or model change is not itself a contradiction.
Borderline cases stay unresolved and cannot be optimistically admitted.

## Ranked top 12

Ranking uses cutoff certainty, study-design clarity, prose-carried claims,
paragraph diversity, distractor feasibility, and annotation burden. It does
not use expected model performance.

| Rank | ID | PMCID | Short description | R / I / L in 100–220 words |
|---:|---|---|---|---|
| 1 | CP-014 | PMC13336533 | Digital engagement and incident stroke | 4 / 6 / 3 |
| 2 | CP-016 | PMC13411413 | MASLD and aortic disease | 2 / 3 / 2 |
| 3 | CP-015 | PMC13341244 | T2DM complications with/without HIV | 2 / 5 / 1 |
| 4 | CP-017 | PMC13310656 | Handgrip weakness/asymmetry and stroke | 4 / 7 / 0 |
| 5 | CP-001 | PMC12925122 | Frailty, sex and AMI outcomes | 6 / 5 / 0 |
| 6 | CP-002 | PMC12141897 | PCI outcomes across racial groups | 4 / 5 / 1 |
| 7 | CP-005 | PMC12085925 | Deprivation and PCI outcomes | 3 / 5 / 2 |
| 8 | CP-006 | PMC11802414 | Balance ability and incident CVD | 4 / 3 / 1 |
| 9 | CP-019 | PMC11969775 | Sleep transitions and incident CVD | 2 / 3 / 1 |
| 10 | CP-013 | PMC13387849 | Sex differences after CABG | 2 / 6 / 1 |
| 11 | CP-004 | PMC12911675 | Youth-onset diabetes complications | 3 / 3 / 0 |
| 12 | CP-003 | PMC13243855 | Anticoagulants after GI surgery in AF | 3 / 3 / 0 |

Counts come from JATS running prose after removing nested tables, figures,
captions, formulas, and supplements. The classifier was corrected during this
rerun so “handgrip strength” and numbered headings such as “3. Results” are not
misclassified.

## Revised strongest four-paper configuration

This is a recommended configuration, not a final selection.

| Paper | Paragraph | Type | Words | Opening |
|---|---:|---|---:|---|
| CP-014 | 35 | Results | 160 | “Three additional prespecified sensitivity analyses…” |
| CP-014 | 45 | Limitation | 126 | “Several limitations warrant consideration…” |
| CP-015 | 30 | Interpretation | 130 | “Contrary to earlier findings…” |
| CP-015 | 32 | Limitation | 209 | “Some limitations should be considered…” |
| CP-016 | 16 | Results | 177 | “We evaluated the robustness of the findings…” |
| CP-016 | 19 | Interpretation | 126 | “In this Korean nationwide health-screening cohort…” |
| CP-017 | 14 | Results | 122 | “In the joint analysis of handgrip weakness…” |
| CP-017 | 22 | Interpretation | 205 | “Moreover, our findings suggest…” |

Totals: 3 Results, 3 interpretation, 2 limitation; four papers × two
paragraphs; 122–209 words. Every paper was received and first published after
the frozen boundary, has machine-readable OA licensing, and has adequate
nonadjacent Methods prose for distractors.

## Remaining blockers

- PMC12418469 remains conservatively excluded until the owner confirms the
  borderline conference-identity adjudication.
- Unpaywall remains incomplete until a real contact email is provided.
- OpenAlex should be rerun with a free key before a publication-quality release,
  although all 167 current requests succeeded.
- The 101 structurally eligible new discovery records have not all received
  human clinical-scope review; they are retained, not silently discarded.
- The search frame supports this pilot inventory but is not a systematic review
  or an exhaustive inventory of all eligible literature since December 2024.

## Reproduction

```bash
python scripts/scholarly_pipeline.py all
python scripts/screen_extended_discovery.py
python scripts/build_inventory.py
python -m pytest -q
```

Optional access variables are documented in `.env.example`. Rebuilding from
the committed cache does not require network access.

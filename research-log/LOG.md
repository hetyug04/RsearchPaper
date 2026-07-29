# Research Log

Append entries in reverse chronological order. Do not rewrite prior entries except to correct a factual error, and record the correction separately.

## 2026-07-29 — Local multi-database corpus rerun (EXP-001-CORPUS)

- Used GPT-5.6 Sol at medium reasoning for synthesis and conference-abstract
  adjudication; no reconstruction generator or model judge was run.
- Replaced the convenience discovery frame with fixed NCBI PMC run
  `DISC-2026-07-29-PMC-01`: 119 complete query results, retained before
  screening.
- Cross-checked 167 unique records (48 prior plus 119 new) through PMC OA AWS,
  NCBI E-utilities, Europe PMC, Crossref, OpenAlex, and medRxiv/bioRxiv.
  Unpaywall support was implemented but recorded incomplete because no real
  contact email was available.
- Source results: PMC OA AWS 167/167 complete; NCBI 167/167; Crossref 167/167;
  OpenAlex 167/167 through unauthenticated compatibility access; Europe PMC 49
  found and 118 not indexed; medRxiv one published-DOI mapping; bioRxiv zero.
- Metadata dispositions: 155 verified post-cutoff, 4 confirmed pre-cutoff, 5
  date conflicts, and 3 single-lineage records requiring review.
- Structurally screened all 119 discovery records against JATS XML: 101 passed
  the automated paragraph-structure gate and remain explicitly pending human
  scope review.
- Manually advanced five new papers and two newly date-resolved prior papers,
  producing a 19-paper eligible/reserve inventory and a revised top 12.
- Confirmed the 2023 Portfolio Diet abstract is the same analysis. The 2024
  statin-target abstract remains conservatively excluded pending owner review.
- Corrected two extraction/classification defects: numbered Results headings are
  now recognized, and “strength” in exposure names no longer creates false
  limitation paragraphs.
- Preserved the original PR #5 inventory, judgments, and exclusions under
  `data/interim/legacy/`; no primary scientific generation was performed.

## 2026-07-29 — Eligible-paper inventory built (EXP-001)

- Screened 48 distinct PMC Open Access Subset papers against the frozen corpus rules; advanced 12 to the ranked inventory and excluded 36 with recorded reasons.
- Artifacts: `data/interim/eligible-paper-inventory.csv`, `data/interim/screening-judgements.csv`, `data/interim/screening-exclusions.csv`, `docs/corpus/eligible-paper-inventory.md`.
- Tooling: `scripts/screen_pmc_article.py` (fetches and parses JATS full text) and `scripts/build_inventory.py` (rebuilds the inventory from judgements joined to source XML).
- Search method: web-search discovery restricted to `pmc.ncbi.nlm.nih.gov` across 12 topic-and-design-targeted queries, then verification of every candidate against its JATS XML in the PMC OA Subset AWS Open Data mirror `s3://pmc-oa-opendata`. No bibliographic, licence, date, or paragraph fact was taken from a search snippet.
- Constraint recorded, not worked around: NCBI E-utilities, the PMC website, Europe PMC, Crossref, OpenAlex and the preprint-server APIs are blocked by this environment's egress policy, and `WebFetch` is blocked for all hosts. The OA Subset metadata filelists return 404 under the bucket's current layout. The search frame is therefore **not a reproducible exhaustive query** and must be re-run from an unrestricted network before the 48-paragraph study.
- Corrected a real extraction defect before screening: JATS nests `<table-wrap>` and `<fig>` inside `<p>`, so naive flattening counted table bodies and figure captions as paragraph prose (inflating some paragraphs from ~110 to ~500 words). All recorded counts come from the corrected extractor.
- Exclusion counts by reason: insufficient qualifying prose 9; prediction/risk-score 7; uncertain first-public date 5; outside subdomain 5; ineligible design 5; pre-cutoff date 3; genetic 1; meta-analysis component 1.
- Two structurally strong papers were excluded on earliest-public-date grounds because congress abstracts of apparently the same analyses appeared before the cutoff: PMC12093672 (AHA *Circulation* abstract, Nov 2023) and PMC12418469 (ESC *European Heart Journal* abstract, Oct 2024). Whether congress abstracts count as "public appearance" is an open protocol question; both are reinstatable if the researcher rules them out of scope.
- Frozen 3/3/2 paragraph mixture appears feasible: a four-paper, eight-paragraph configuration exists entirely inside the 100–220 word preferred band with no length justification required.
- Binding constraint identified: usable limitation paragraphs are scarce. Only 5 genuine limitation paragraphs fall in the preferred band across the 12 eligible papers, because this literature writes limitations as single omnibus paragraphs of 280–395 words. Sufficient for the 8-item pilot; likely insufficient at 48 items without a preregistered amendment.
- No paragraphs were finalised, no model generation was run, and no judge evaluation was performed.
- Next action: researcher ruling on the congress-abstract question, then final selection of the eight paragraphs.

## 2026-07-29 — Pilot protocol frozen

- Selected clinical and observational epidemiology, focused on cardiovascular and metabolic cohort research.
- Fixed PMC Open Access as the corpus and December 1, 2024 as the earliest eligible public date.
- Fixed `google/gemma-3-1b-it` and `google/gemma-3-4b-it` as generators using sequential 4-bit inference with an 8,000-token input limit.
- Fixed the eight-item paragraph mix, claim taxonomy, four context conditions, annotation workflow, judge-validation gates, human scoring rubric, and 15-minute maximum verification time.
- Recorded protocol freeze commit `88833dae64cd263e85fbba4d3b6d0d659fe7f588` in the decision log.
- No primary scientific generation has been run.
- Next action: build the eligible-paper inventory and attempt eight candidate paragraph annotations.

## 2026-07-29 — Repository initialized

- Established `hetyug04/RsearchPaper` as the canonical source of truth for the research arc.
- Added the initial context-and-verifier research plan.
- Added an eight-paragraph feasibility pilot preregistration in draft status.
- Added cross-device and agent operating protocols.
- No scientific experiment has been run yet.
- Next action: select a single scientific domain and construct the eight-item development/pilot candidate pool without using primary test items.

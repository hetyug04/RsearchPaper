# Eligible-Paper Inventory — Eight-Paragraph Feasibility Pilot

**Experiment:** EXP-001 (`preregistration/pilot-preregistration.md`, frozen at `88833dae64cd263e85fbba4d3b6d0d659fe7f588`)
**Screening date:** 2026-07-29
**Machine-readable inventory:** `data/interim/eligible-paper-inventory.csv`
**Screening judgements (input):** `data/interim/screening-judgements.csv`
**Exclusion ledger:** `data/interim/screening-exclusions.csv`
**Tooling:** `scripts/screen_pmc_article.py`, `scripts/build_inventory.py`

This is a blind corpus-screening product. No model generation and no judge
evaluation were run. Papers were assessed only for corpus suitability, never
for whether a generator is likely to reconstruct them well or badly.

---

## 1. Search strategy

### 1.1 What was actually done

Screening used a two-stage **discover-then-verify** procedure:

1. **Discovery (web search).** Twelve topic-and-design-targeted queries were
   issued against `pmc.ncbi.nlm.nih.gov`, spanning the cardiovascular and
   metabolic subdomain space: heart failure, atrial fibrillation and
   anticoagulation, myocardial infarction, stroke, hypertension, type 1 and
   type 2 diabetes, obesity and metabolic syndrome, MASLD, lipids and statins,
   chronic kidney disease with cardiometabolic exposures, adverse pregnancy
   outcomes, air pollution, sleep and physical function, socioeconomic and
   ethnic disparities. Queries also varied by design vocabulary (prospective
   cohort, retrospective cohort, nationwide registry, EHR-based cohort,
   national health insurance database, TriNetX) and by cohort resource
   (UK Biobank, CHARLS, NHANES-linked mortality, MINAP, BCIS, Korean NHIS,
   Taiwan NHI, Nordic registries).
2. **Verification (primary source).** Every candidate surfaced by discovery was
   verified against the article's **JATS XML in the PMC Open Access Subset**,
   retrieved from the AWS Open Data mirror `s3://pmc-oa-opendata`
   (`https://pmc-oa-opendata.s3.amazonaws.com/`). Presence of the article in
   that bucket is the operational test of Open Access Subset membership. The
   XML supplied, first-hand: title, authors, journal, DOI, PMCID, the verbatim
   `<permissions>`/`<license>` block, every recorded date (`epub`, `ppub`,
   `collection`, `received`, `accepted`, `rev-recd`), the full section tree,
   and every body paragraph with word counts and table/figure cross-references.

No bibliographic, licence, date, or paragraph fact in the inventory comes from
a search snippet. Search was used to *find* papers and to *look for earlier
public versions*; everything recorded about a paper comes from its own full
text.

### 1.2 Paragraph extraction correctness

An early version of the extractor flattened `<p>` elements naively. JATS
routinely nests `<table-wrap>` and `<fig>` **inside** `<p>`, so table bodies and
figure captions were being counted as paragraph prose — inflating several
paragraphs from ~110 words to ~500. The extractor now drops display objects and
records their presence separately. All counts in this document and in the CSV
come from the corrected extractor. This mattered: it changed the eligibility
assessment of multiple papers.

### 1.3 Known limitations of this search strategy

**This is not a reproducible exhaustive query, and it should not be described
as one.** The NCBI E-utilities, the PMC website, Europe PMC, Crossref,
OpenAlex, and the bioRxiv/medRxiv APIs are all blocked by this environment's
egress policy (403 at the proxy), and `WebFetch` is blocked for all hosts. The
PMC OA Subset bucket's `oa_comm`/`oa_noncomm` metadata filelists — which would
have provided a systematic sampling frame — return 404 under the bucket's
current flat per-PMCID layout.

Consequences the researcher must weigh:

- Discovery is **search-engine-mediated and non-exhaustive**. The screened set
  is a convenience sample of the eligible population, not a census.
- **Selection is biased toward well-indexed, frequently-linked papers.** This
  does not bias the *pilot* toward favourable results — nothing in screening
  used model-performance expectations — but it does mean the corpus is not a
  random draw from PMC OA cardiometabolic cohort studies.
- **Preprint checking is best-effort.** Without preprint-server APIs, earlier
  public versions were sought by targeted title searches only. Five papers were
  excluded on date uncertainty precisely because this check could not be closed
  (§3, §6).

Before the 48-paragraph study, the search should be re-run with a real PMC
boolean query from an unrestricted network.

---

## 2. Total screened

| Stage | Count |
|---|---|
| Candidate records surfaced by discovery queries | ~90 (with duplicates across queries) |
| **Distinct papers screened against full text** | **48** |
| Papers advanced to the ranked inventory | 12 |
| Papers excluded | 36 |

Every one of the 48 had its complete JATS full text fetched and parsed. None
was screened on title or abstract alone.

---

## 3. Exclusion counts by reason

| Code | Count | Reason |
|---|---|---|
| `E-PARA` | 9 | Insufficient qualifying prose paragraphs; findings carried by tables/figures |
| `E-PRED` | 7 | Diagnostic-prediction, risk-score development, or risk-score evaluation |
| `E-DATE-UNCERTAIN` | 5 | Earliest public date not verifiable against the 2024-12-01 cutoff |
| `E-SUBDOMAIN` | 5 | Outside cardiovascular/metabolic clinical epidemiology (renal, cognitive, transplant outcomes) |
| `E-DESIGN` | 5 | Not an eligible cohort design (cross-sectional, letter, review) |
| `E-DATE-PRE` | 3 | Earliest verifiable public appearance before 2024-12-01 |
| `E-GENETIC` | 1 | Genetic/polygenic association study |
| `E-SR-META` | 1 | Contains a systematic review / meta-analysis component |
| **Total** | **36** | |

Per-paper reasons are in `data/interim/screening-exclusions.csv`. Three
exclusions are worth naming here because they are the kind that quietly become
contamination if missed:

- **PMC12093672** (BMC Medicine, Portfolio dietary pattern and CVD mortality)
  looked like one of the strongest candidates on structure — five Results and
  two labelled Limitations paragraphs in the preferred band, CC BY, `epub`
  2025-05-21. It was excluded because an **AHA congress abstract of what appears
  to be the same analysis was published in November 2023** (*Circulation*
  2023;148(suppl_1):Abstract 14297, same title and same NHANES III 1988–2019
  analysis). Earliest public appearance therefore predates the cutoff.
- **PMC12418469** (JACC: Advances, cholesterol levels after statin initiation)
  was excluded for the same class of reason: an ESC Congress 2024 abstract
  reporting what appears to be the same Ontario statin-initiator cohort
  (*European Heart Journal* 2024;45(Suppl 1):ehae666.2860, October 2024).
- **PMC12755569** carries a PMCID in the 12.7M range but has `epub` 2022-10-28.
  High PMCIDs reflect deposit date, not publication date. Any future screening
  must read the dates, never infer recency from the accession number.

---

## 4. Ranked inventory (12 papers)

Ranked by corpus suitability only: certainty of cutoff eligibility, clarity of
study design, prose-carried claims, external recoverability, paragraph
diversity, distractor feasibility, low annotation ambiguity.

Paragraph counts are `preferred band (100–220 w)` with `(+n)` in the extended
`221–350 w` band.

| # | ID | PMCID | Short title | Design | Earliest public | Licence | R / I / L | Tbl-fig | Burden | Rec. |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CP-001 | PMC12925122 | Frailty, sex and AMI outcomes (MINAP, England/Wales) | Retrospective registry/EHR-linked cohort | 2026-02-12 | CC BY | 6 / 5(+1) / 0(+1) | low 11% | med | **strong** |
| 2 | CP-002 | PMC12141897 | PCI outcomes by 5 race/ethnic subgroups | Retrospective cohort on a prospective PCI registry | 2025-05-13 | CC BY-NC-ND | 4(+1) / 5(+2) / 1 | low 14% | low | **strong** |
| 3 | CP-005 | PMC12085925 | Deprivation and PCI outcomes (BCIS) | Retrospective national registry cohort | 2025-02-28 | CC BY | 3(+1) / 5 / 2 | low 6% | low | **strong** |
| 4 | CP-006 | PMC11802414 | Balance ability and incident CVD (CHARLS) | Observational cohort in a national survey | 2025-01-24 | CC BY | 4 / 3 / 2 | low 11% | low | **strong** |
| 5 | CP-004 | PMC12911675 | Youth-onset T1D/T2D cardiovascular complications (Taiwan NHI) | Nationwide population-based cohort | 2026-02-16 | CC BY-NC | 3(+1) / 3 / 1 | low 18% | med | **strong** |
| 6 | CP-003 | PMC13243855 | GI surgery, DOAC vs warfarin, stroke in AF (Korea) | Nationwide claims-based cohort | 2026-04-23 | CC BY-NC | 3 / 3 / 0(+1) | med 22% | med | **strong** |
| 7 | CP-007 | PMC12273069 | Outpatient CVRM across COVID-19 periods (Utrecht) | Prospective EHR-based cohort | 2025-07-16 | CC BY | 4 / 2(+2) / 0(+1) | med 22% | med | **strong** |
| 8 | CP-008 | PMC12748521 | Metabolic-health transitions and CAD (COMMODORE) | Retrospective EHR cohort, time-to-event | 2025-11-11 | CC BY-NC-ND | 4(+2) / 3(+3) / 1(+1) | med 25% | med | possible |
| 9 | CP-009 | PMC12341586 | Steatotic liver disease and CV burden (Taiwan) | Prospective cohort linked to NHI/death registry | 2025-06-06 | CC BY | 4 / 6(+1) / 0 | med 21% | med | possible |
| 10 | CP-012 | PMC12005981 | HDP/GDM and predicted ASCVD risk (HAPO FUS) | Secondary analysis of an international prospective cohort | 2025-01-17 | CC BY-NC | 3 / 1(+1) / 0(+1) | low 11% | med | possible |
| 11 | CP-011 | PMC12664052 | GLP-1 RA vs DPP-4i in T2DM with HFrEF (TriNetX) | Retrospective active-comparator new-user cohort | 2025-11-13 | CC BY | 1 / 6(+1) / 1 | high 38% | med | possible |
| 12 | CP-010 | PMC12611492 | TyG index across CKM stages (Korean NHIS) | Retrospective cohort, national screening + claims | 2025-10-31 | CC BY-NC | 1(+1) / 4(+1) / 0 | med 20% | med | possible |

Full records — including authors, DOIs, stable URLs, verbatim licence URIs,
population/exposure/outcome, date evidence, up to three candidate paragraph
locations per paper, and per-field source citations — are in
`data/interim/eligible-paper-inventory.csv`.

### Why the ranking falls this way

- **CP-001** ranks first on every axis at once: a `received` date of 2025-10-09
  makes a pre-cutoff version logically impossible, the design is stated
  unambiguously, its Discussion is almost entirely free of table pointers, and
  its summary paragraph restates the Results paragraphs — giving genuine
  external recoverability for masked Results targets.
- **CP-002, CP-005, CP-006** rank high largely because each carries a
  **well-formed limitation paragraph inside the preferred 100–220 word band**,
  which is the scarcest resource in this corpus (§7).
- **CP-011 and CP-010** rank last among the possibles because each can realistically
  contribute only one paragraph type: CP-011 has one Results paragraph in band
  and the highest table dependence in the inventory (38%); CP-010 has no usable
  limitation paragraph at all, its strengths and limitations being fused into a
  single 395-word paragraph.

---

## 5. Strongest four-paper configuration

This configuration yields exactly the frozen 3 / 3 / 2 mixture from four
papers at two paragraphs each, with every paragraph inside the preferred
100–220 word band and no length justification required.

| Paper | Paragraph | Type | Words | Section | Opening words |
|---|---|---|---|---|---|
| CP-001 PMC12925122 | idx 19 | Results | 207 | Results > Adjusted outcomes | "After multivariable adjustment, greater frailty at 1-year was associated with higher risks…" |
| CP-001 PMC12925122 | idx 27 | Interpretation | 137 | Discussion | "Our results show that the prevalence of severe frailty was substantially higher…" |
| CP-002 PMC12141897 | idx 10 | Results | 119 | Results > Subgroup analysis | "To further elucidate the clinical outcomes among different racial groups, we performed…" |
| CP-002 PMC12141897 | idx 18 | Limitation | 114 | Discussion > Study Limitations | "Despite valuable insights provided by this study, we acknowledge certain limitations. First,…" |
| CP-005 PMC12085925 | idx 17 | Results | 160 | Results | "From a procedural perspective, patients from the most deprived quintile (Q5) underwent…" |
| CP-005 PMC12085925 | idx 22 | Interpretation | 152 | Discussion | "Furthermore, the concept that lower socioeconomic status groups can experience adverse health…" |
| CP-006 PMC11802414 | idx 21 | Interpretation | 173 | Discussion | "Balance ability, an essential physical measurement, is associated with death from all…" |
| CP-006 PMC11802414 | idx 26 | Limitation | 124 | Discussion (unlabelled limitation paragraph) | "In addition, there are some limitations in this study. First, due to…" |

**Totals: 3 Results, 3 interpretation/reconciliation, 2 limitation, 4 papers × 2
paragraphs.** All eight are 114–207 words.

This is offered as the *strongest available configuration*, not as a selection.
The eight paragraphs are **not finalised**; per the task, final selection is the
researcher's. Candidate alternates for each slot are recorded in the CSV.

Properties of this configuration relevant to the four context conditions:

- **True context** is available for all eight: each sits among adjacent
  same-section paragraphs.
- **Shuffled context** is available: the four papers are section- and
  length-comparable, and six further eligible papers exist as donors.
- **Same-paper distractors** are feasible for all eight. Each paper carries a
  long Methods section (CP-001: 12 paragraphs; CP-005: 10; CP-006: 8) that is
  nonadjacent to every target, states no outcome conclusion, and can be
  length-matched within ±25%.
- **Leakage hazards to exclude explicitly:** CP-001's "Research in context" box
  (paragraph 0) restates the headline findings verbatim, as do CP-008's "What Is
  New?" box, CP-010's "KEY MESSAGE" boxed text, and CP-012's "What is already
  known?" box. These must not be used as distractors or true context.

---

## 6. Unresolved eligibility questions

Recorded rather than resolved. Each needs a researcher decision or an
unrestricted-network check before generation.

1. **Do conference abstracts count as "earliest public appearance"?**
   This single ruling moves two otherwise-strong papers. PMC12093672 and
   PMC12418469 were excluded on the reading that a published congress abstract
   in *Circulation* or the *European Heart Journal* is a public version of the
   same findings, and therefore a contamination surface. If the researcher rules
   congress abstracts out of scope, **both papers are reinstatable** —
   PMC12093672 in particular would likely rank in the top four, since it carries
   five Results and two labelled Limitations paragraphs in the preferred band.
   The preregistration says "earliest public version" without defining whether
   abstracts qualify. It should be defined explicitly before generation.
2. **Is the PMC12418469 congress abstract actually the same analysis?**
   The ESC 2024 abstract title differs ("Association of lipid target
   achievement…" vs "Cholesterol Levels and Cardiovascular Outcomes…") but the
   cohort description matches. This could not be confirmed without full-text
   access to the abstract.
3. **Does PMC11969775 have a Research Square preprint?** A search result
   asserted a preprint exists but returned no citation. Its `received` date of
   2024-11-05 means any submission-linked "In Review" posting would fall just
   before the cutoff. Excluded on uncertainty; resolvable in one lookup.
4. **PMC12085925 has no online-first date.** Its earliest public date rests on a
   single source — the journal's stated issue date of 2025-02-28, corroborated by
   the journal's own article page. It is currently ranked 3rd. If the researcher
   requires two independent date sources, it should be demoted.
5. **PMC12748521 has a pre-cutoff `received` date (2024-08-01) and an
   AHA-affiliated author group.** No pre-cutoff congress abstract was found, but
   absence of evidence here is weak given the blocked search surfaces.
6. **Is a predicted risk score an acceptable outcome?** CP-012's outcome is
   10- and 30-year *predicted* ASCVD risk, not observed events. It is not a
   risk-score development or validation paper, so it is not strictly excluded,
   but every claim scored from it would be a claim about a surrogate. The claim
   taxonomy has no natural label for this.
7. **Two papers describe themselves inconsistently.** PMC12093672's Methods call
   NHANES "cross-sectional" while the title and analysis are a prospective
   mortality-linkage cohort; PMC12823638 is "prospective" in Methods and
   "retrospective" in Limitations. Both were excluded for other reasons, but the
   pattern means design classification cannot be automated from keyword matching
   for the 48-paragraph study.
8. **The search frame is not reproducible from this environment** (§1.3). This is
   the largest outstanding methodological gap.

---

## 7. Is the frozen paragraph mixture feasible?

**Yes — with one material caveat about limitation paragraphs.**

| Requirement (frozen protocol) | Status | Evidence |
|---|---|---|
| 3 Results paragraphs | **Comfortable** | 40 Results paragraphs in the 100–220 w band across the 12 papers; 6 in CP-001 alone |
| 3 interpretation/reconciliation paragraphs | **Comfortable** | 46 in band across the 12 papers; every paper contributes at least one |
| 2 limitation paragraphs | **Adequate but tight** | Only **8** limitation-classified paragraphs in the 100–220 w band across 6 papers — and of those, 3 are *strengths* or *conclusions* paragraphs, leaving **5 genuine limitation paragraphs** in band (CP-002 ×1, CP-005 ×2, CP-006 ×1, CP-011 ×1). 5 more sit in the 221–350 w band |
| ~4 papers × 2 paragraphs | **Achievable** | §5 gives an eight-item configuration from exactly 4 papers |
| 100–220 w preferred length | **Achievable for all 8** | §5 configuration spans 114–207 w |
| 2–4 scoreable claims per paragraph | **Appears satisfied** | Inspected in prose for the §5 eight; each contains 2–4 distinct assertions of result, comparison, or qualification |
| ≥2 claims recoverable outside the masked paragraph | **Appears satisfied for Results and interpretation; weakest for limitations** | Results claims recur in the Discussion summary paragraph and abstract (abstracts are permitted as annotation evidence). Limitation claims are, by nature, often stated once |
| Same-paper distractors constructible | **Yes for all 12** | Every paper has ≥8 Methods paragraphs nonadjacent to the targets and free of outcome conclusions |
| Tables/figures excluded from the pilot | **Compatible** | 7 of 12 papers have low table/figure dependence (≤18% of paragraphs); the §5 four are 6–14% |

### The limitation-paragraph constraint, stated plainly

This is the binding constraint on the corpus and the finding most likely to
affect the 48-paragraph scale-up. Limitation paragraphs in this literature tend
to be **single long omnibus paragraphs** — "First… Second… Third…" — that run
well past 220 words:

| Paper | Limitation paragraph | Words | Usable? |
|---|---|---|---|
| CP-002 PMC12141897 | idx 18 | 114 | yes |
| CP-006 PMC11802414 | idx 26 | 124 | yes |
| CP-005 PMC12085925 | idx 36 / idx 37 | 147 / 112 | yes (also idx 34 at 96 w and idx 35 at 88 w, both below the 100 w floor) |
| CP-011 PMC12664052 | idx 23 | 212 | yes |
| CP-008 PMC12748521 | idx 24 | 225 | marginal — needs justification |
| CP-001 PMC12925122 | idx 30 | 280 | needs justification; also merges strengths |
| CP-012 PMC12005981 | idx 31 | 282 | needs justification |
| CP-007 PMC12273069 | idx 30 | 314 | needs justification |
| CP-003 PMC13243855 | idx 34 | 337 | needs justification; at the ceiling |
| CP-004 PMC12911675 | idx 19 | 372 | **exceeds the 350 w ceiling — unusable** |
| CP-009 PMC12341586 | — | — | **no limitation paragraph exists** |
| CP-010 PMC12611492 | idx 21 | 395 | **exceeds the ceiling — unusable** |

The pilot's requirement of 2 needs only the clean cases, so the eight-item
pilot is feasible as frozen. But at 48 items the protocol would need **12
limitation paragraphs**, and this corpus yields 5 genuine in-band limitation
paragraphs across 12 eligible papers — roughly one usable limitation paragraph
per 2.4 eligible papers. Scaling would require either screening on the order of
30 eligible papers, or a preregistered amendment — for example,
permitting a sub-paragraph span of a long omnibus limitation paragraph, or
raising the limitation-paragraph ceiling. That is a methodological decision for
the researcher and a decision-log entry, not something screening should settle.

### Feasibility verdict

The frozen eight-paragraph mixture — 3 Results, 3 interpretation, 2 limitation,
approximately 4 papers at 2 paragraphs each, 100–220 words, four context
conditions — **appears feasible from this inventory**, and §5 gives a concrete
configuration that satisfies every stated constraint without invoking the
length-justification clause.

---

## 8. Provenance

- Inventory generated by `scripts/build_inventory.py` from
  `data/interim/screening-judgements.csv` joined against each article's JATS XML.
  Bibliographic, licence, date, and structural fields are re-derived from the
  XML at build time and cannot drift from source.
- Full text retrieved from the PMC Open Access Subset AWS Open Data mirror
  `s3://pmc-oa-opendata`. No copyrighted full text is committed to this
  repository; the inventory stores identifiers, metadata, and short opening-word
  excerpts only, consistent with `AGENTS.md`.
- Rebuild and verify with `python3 scripts/build_inventory.py --check`.
- No primary generation, model inference, or judge evaluation was performed.

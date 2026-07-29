# Decision Log

Record methodological and operational decisions here. Each entry must include date, status, decision, rationale, alternatives considered, and consequences.

## D-001 — 2026-07-29

**Status:** accepted

**Decision:** Treat GitHub as the canonical cross-device source of truth.

**Rationale:** Multiple devices and agents will operate on the project. A shared versioned record is necessary to prevent divergent prompts, annotations, analyses, and claims.

**Alternatives considered:** local folders, cloud drive, chat history.

**Consequences:** meaningful work must be committed or represented by an issue, log entry, experiment record, or versioned artifact.

## D-002 — 2026-07-29

**Status:** accepted

**Decision:** Frame the first paper as a context-and-verifier audit, not as an RLVR result or recovery of human reasoning traces.

**Rationale:** An LLM evaluator is not objective verification, and scientific papers usually do not expose the authors' full reasoning process.

**Alternatives considered:** direct RL training paper; synthetic reasoning-trace paper; broad scientific reasoning benchmark.

**Consequences:** the initial study measures evidence dependence, factual reconstruction, and verifier reliability. Stronger training claims require later evidence.

## D-003 — 2026-07-29

**Status:** accepted and frozen

**Decision:** Use an eight-paragraph feasibility pilot before scaling to the proposed 48-item study.

**Rationale:** Annotation quality and throughput are the main unknowns. Scaling before measuring them would create avoidable design drift.

**Alternatives considered:** immediately annotate 48 items; table-only study; human-first verifier study.

**Consequences:** the pilot must pass its preregistered feasibility gate before scaling.

## D-004 — 2026-07-29 15:12 EDT

**Status:** accepted and frozen

**Decision:** Freeze the complete pilot protocol in `preregistration/pilot-preregistration.md`.

**Frozen protocol commit:** `88833dae64cd263e85fbba4d3b6d0d659fe7f588`

**Rationale:** The domain, corpus, temporal boundary, exact generator checkpoints, quantization, context limit, paragraph mix, claim taxonomy, context conditions, annotation pipeline, judge design, scoring rules, workload ceiling, and feasibility gates are now specified before primary generation.

**Alternatives considered:** Qwen-family generators; broader clinical specialties; two-condition design; stochastic repeated generation; local small-model judge as primary.

**Consequences:** Primary pilot generation may begin only from this frozen protocol. Any methodological change requires a new version and decision-log entry; failed or inconvenient items cannot be silently replaced.

## D-005 — 2026-07-29

**Status:** proposed — requires researcher ruling before paragraph selection

**Decision sought:** Whether a published conference abstract counts as an "earliest public version" under the corpus temporal rule.

**Context:** Screening for the eligible-paper inventory found two structurally strong candidates whose PMC publication dates are comfortably post-cutoff but for which a congress abstract of apparently the same analysis appeared before 2024-12-01:

- `PMC12093672` — BMC Medicine, Portfolio dietary pattern and CVD mortality. Congress abstract: *Circulation* 2023;148(suppl_1):Abstract 14297, November 2023.
- `PMC12418469` — JACC: Advances, cholesterol levels after statin initiation. Congress abstract: *European Heart Journal* 2024;45(Suppl 1):ehae666.2860, October 2024 (title differs; cohort description matches, but identity of analysis is unconfirmed).

**Screening treated both as ineligible**, on the reading that a published abstract is a public version of the same findings and therefore a contamination surface. This is the conservative reading and it was applied without regard to how convenient the papers were — `PMC12093672` would likely have ranked in the top four.

**Alternatives considered:** (a) count congress abstracts as public appearance (current screening behaviour); (b) count only preprints, accepted manuscripts, and full publications, excluding abstracts; (c) count abstracts only when the abstract states the study's central numerical results.

**Consequences:** Under (b) or (c), both papers are reinstatable and the ranked inventory changes. The preregistration says "earliest public version" without defining the term; it should be defined explicitly before any primary generation, and the ruling recorded here.

## D-006 — 2026-07-29

**Status:** accepted

**Decision:** Record the corpus-discovery search frame as non-reproducible from the current execution environment, rather than presenting it as a systematic PMC query.

**Rationale:** NCBI E-utilities, the PMC website, Europe PMC, Crossref, OpenAlex, and the preprint-server APIs are all blocked by this environment's egress policy, and `WebFetch` is blocked for all hosts. The PMC OA Subset metadata filelists, which would have supplied a systematic sampling frame, return 404 under the bucket's current per-PMCID layout. Discovery therefore had to run through web search, which is non-exhaustive and biased toward well-indexed papers.

**Alternatives considered:** presenting the web-search yield as if it were a boolean PMC query; loosening criteria to fill the inventory faster; routing around the egress policy.

**Consequences:** Every fact in the inventory is verified against primary JATS full text, so the *records* are sound, but the *sampling* is a convenience sample and must be described that way. The search must be re-run from an unrestricted network before the 48-paragraph study. Preprint checking was best-effort, which is why five papers were excluded on unresolved date uncertainty rather than admitted optimistically.
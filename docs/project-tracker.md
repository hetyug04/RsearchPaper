# Canonical Project Tracker

This file is the canonical operational tracker for the research arc. It summarizes scope, status, decisions, blockers, gates, and next actions. Methodological choices become frozen only when they are recorded in the [preregistration](../preregistration/pilot-preregistration.md) and [decision log](../decisions/DECISIONS.md) at an identified commit.

## Project status

| Field | Value |
|---|---|
| Owner | Het Patel |
| Project status | Phase 0 — feasibility and design freeze |
| Tracker status | Active; proposal consolidated, empirical work not started |
| Experiment ID | `EXP-001` |
| Created | 2026-07-29 |
| Last updated | 2026-07-29 |
| Planned study start | `TBD — after pilot configuration is frozen` |
| Planned study finish | `TBD — four working days after start` |
| Tracker creation commit | `TBD — fill with branch commit SHA` |
| Pilot freeze commit | `TBD — required before primary pilot generation` |
| Primary analysis commit | `TBD` |
| Release/manuscript commit | `TBD` |
| Active branch | `agent/canonical-project-tracker` |
| Related issues | [#1 — Select domain and freeze pilot](https://github.com/hetyug04/RsearchPaper/issues/1); [#2 — Run the feasibility pilot](https://github.com/hetyug04/RsearchPaper/issues/2) |
| Formal decision record | [`decisions/DECISIONS.md`](../decisions/DECISIONS.md) |

No scientific experiment has been run. The pilot preregistration remains draft until the domain, sampling rules, prompts, model configuration, parameters, schemas, and analysis gates are frozen.

## Working title

*Where Does Masked-Paragraph Reconstruction Signal Come From? A Context and Verifier Audit in Scientific Papers*

## Research question

When an LLM reconstructs a masked scientific paragraph, how much factual improvement comes from relevant document evidence rather than generic prior knowledge—and how reliably can an LLM judge detect planted and naturally occurring scientific errors?

## Terminology guardrails

- Do not describe this study as an RLVR experiment. [DeepSeek-R1](https://arxiv.org/abs/2501.12948) demonstrates reinforcement learning with verifiable rewards, while the proposed model evaluator is not itself an objective verifier.
- Do not equate an LLM judge with the symbolic or Lean-grounded verification used in [AlphaGeometry](https://www.nature.com/articles/s41586-023-06747-5) or [AlphaProof](https://www.nature.com/articles/s41586-025-09833-y).
- Describe model-evaluated feedback as closer to RLAIF or model-based feedback, and explicitly audit known judge weaknesses such as position bias. See [RLAIF](https://arxiv.org/abs/2309.00267) and the cited [position-bias study](https://arxiv.org/abs/2406.07791).
- Call the exploratory prompt condition **claim-first reconstruction** or **claim decomposition**, not hidden chain-of-thought collection.
- Treat reconstructed text and model-generated rationales as model outputs, not recovered author reasoning.
- Keep confirmatory and exploratory analyses separate. Do not tune prompts, exclusions, metrics, or gates on primary outputs and then describe them as preregistered.

## Experiment options and selection criteria

The options below are deliberately unordered. Choose by applying the stated criterion, not by treating table order as a ranking.

| Option | Scope | Choose when |
|---|---|---|
| Context-and-verifier audit | Compare prior-only, true adjacent context, shuffled context, and irrelevant same-paper context; validate the judge with controlled errors. | Use as the working default unless the Day 1 pilot exposes a clear feasibility or validity obstacle. |
| Table-grounded subset | Restrict or add a subset of results paragraphs with checkable numbers, directions, units, or comparisons. | Add only if at least 12 usable examples can be obtained without building a custom table parser. |
| Larger context-only study | Drop the prompt comparison and expand to approximately 72 paragraphs. | Choose if annotation is unusually fast and estimating context effects matters more than testing claim-first prompting. |
| Human-first verification | Make blinded human ratings primary and LLM-judge scores secondary. | Choose only if an independent second rater is already available. |

Selection decision: `TBD — record the chosen design and rationale in decisions/DECISIONS.md before primary generation`.

## Minimum viable experiment

### Corpus and sample

- 16 recent open-access empirical papers from one scientific domain.
- 48 masked paragraphs, approximately three per paper.
- 12 paragraphs each from background, methods, results, and discussion.
- Before generation, freeze 2–4 atomic factual claims and their supporting evidence spans for every item.
- Record objective anchors when present: numbers, magnitudes, units, signs, directions, entities, comparators, and experimental conditions.
- Store stable paper and paragraph IDs, paragraph type, masking boundaries, ambiguity flags, and annotation time.

Structured corpora such as [S2ORC](https://arxiv.org/abs/1911.02782) make acquisition plausible, but annotation throughput is the primary feasibility risk.

### Primary conditions

| Condition | Information supplied |
|---|---|
| Prior-only | Paragraph type, with no paper-specific information. |
| True context | The immediately preceding and following paragraphs. |
| Shuffled context | Matched context from another paper with the same paragraph type. |
| Same-paper distractor | Similarly sized text from an irrelevant section of the same paper. |

Run direct reconstruction for all 48 items in all four conditions: **192 primary outputs**.

For the prior-only and true-context conditions, also run claim-first reconstruction: list recoverable claims, then write the paragraph. This adds **96 exploratory outputs**.

Archive the exact provider, model identifier, prompt version, decoding parameters, seeds, input IDs, code commit, run manifest, and output paths.

## Judge validation

Build 40 clean claim records and three corrupted versions of each, producing 120 controlled corruptions across:

- direction or sign reversal;
- number, magnitude, or unit alteration;
- entity, comparator, or experimental-condition substitution.

The judge is a usable weak filter only if all gates pass:

| Gate | Required result |
|---|---|
| Balanced accuracy | `>= 0.75` |
| Critical-error false acceptance | `<= 0.15` |
| Position-order reversal | `<= 0.10` |

If any gate fails, report LLM-judge scores as descriptive and make the human audit primary. Report planted-error and natural-error detection separately.

## Metrics and analysis

Track:

- atomic-claim recovery;
- supported-claim precision;
- critical contradiction rate;
- unsupported causal claims;
- hedge and uncertainty preservation;
- judge false-acceptance rate;
- judge position-reversal rate;
- numeric, sign, unit, and condition accuracy on objective anchors.

Use paper-clustered bootstrap confidence intervals and paired permutation tests. Treat paragraph-type and prompting interactions as exploratory unless separately powered and preregistered.

## Four-day schedule

The clock starts only when work can proceed without changing the primary design on observed primary outputs.

### Day 1 — Prove feasibility

- [ ] Hours 1–2: freeze the research question, outcomes, exclusions, and falsifiers.
- [ ] Hours 3–4: complete a targeted literature and novelty check.
- [ ] Hours 5–7: build eight development examples and run the complete pipeline.
- [ ] Hour 8: measure researcher minutes per usable paragraph.
- [ ] Hour 9: preregister prompts, gates, sample size, and analysis.
- [ ] Apply the proceed gate: at least six of eight examples have unambiguous claims, and measured workload permits 48 items with 25% contingency.

### Day 2 — Dataset and validation

- [ ] Hours 1–3: select and mask 48 paragraphs.
- [ ] Hours 4–5: freeze atomic claims and evidence spans.
- [ ] Hours 6–7: construct controlled corruptions.
- [ ] Hours 8–9: validate the judge; make at most two logged prompt repairs using development data only.
- [ ] Hours 9–10: generate and archive the 192 primary reconstructions.

### Day 3 — Evaluation and analysis

- [ ] Hours 1–2: generate 96 claim-first exploratory outputs.
- [ ] Hours 3–4: run automated evaluation and objective checks.
- [ ] Hours 5–8: blindly audit 48 outputs manually.
- [ ] Hour 9: re-score 12 outputs after intervening work to estimate intra-rater stability.
- [ ] Hour 10: calculate effects, confidence intervals, and gate failures.

### Day 4 — Manuscript and release

- [ ] Hours 1–2: inspect errors, leakage, exclusions, and failed hypotheses.
- [ ] Hours 3–5: write Methods and Results first.
- [ ] Hours 6–7: write Introduction, Related Work, and Limitations.
- [ ] Hours 8–9: package prompts, annotations, IDs, raw outputs, and analysis code.
- [ ] Hour 10: reproduce headline tables and finish a 6–8 page pilot manuscript.

## Preregistered falsifiers

These remain proposed until the preregistration is frozen.

| Hypothesis | Falsifier |
|---|---|
| Relevant context improves claim recovery. | The paired confidence interval includes zero. |
| True context beats shuffled context. | No reliable difference appears. |
| Claim-first prompting improves fidelity. | Recall does not improve or critical errors increase. |
| The judge is a usable weak filter. | Any judge-validation gate fails. |
| Planted errors approximate natural errors. | Planted-error detection exceeds natural-error detection by more than 15 percentage points. |

A null result remains a genuine result when the design and analysis are frozen first.

## Claim boundaries

The initial study must not claim that it:

- performed RLVR;
- recovered authors' hidden reasoning;
- eliminated memorization;
- demonstrated general scientific reasoning;
- established that an LLM judge is an objective verifier;
- produced publication-ready evidence merely by completing a four-day pilot.

The defensible target is a preregistered pilot measuring evidence dependence, reconstruction fidelity, and verifier reliability. Publication quality depends on what the pilot discovers and whether the findings replicate.

## Decisions

Formal methodological decisions belong in [`decisions/DECISIONS.md`](../decisions/DECISIONS.md). This table is an operational index and does not itself freeze a pending choice.

| Record | Status | Decision or choice | Required follow-up |
|---|---|---|---|
| D-001 | Accepted | GitHub is the canonical cross-device source of truth. | Keep tracker, logs, artifacts, and issues current. |
| D-002 | Accepted | Frame the first paper as a context-and-verifier audit, not RLVR or recovered reasoning. | Enforce terminology and claim boundaries in prompts and manuscript. |
| D-003 | Proposed; not frozen | Run an eight-paragraph feasibility pilot before scaling. | Freeze the pilot configuration and commit SHA before primary generation. |
| Pending | Open | Choose one scientific domain and inclusion/exclusion rules. | Record rationale and alternatives in the decision log. |
| Pending | Conditional | Retain the default combined audit or select one of the alternative designs. | Apply the selection criteria above after Day 1 evidence is available. |
| Pending | Open | Select model/provider, prompts, parameters, seeds, and run-manifest schema. | Freeze exact values before primary generation. |

## Blockers

- Scientific domain and paper eligibility rules are not selected.
- The pilot preregistration is draft; no freeze commit exists.
- Exact generation and judge models, prompts, decoding parameters, and seeds are not frozen.
- The eight-item development pool and input manifest do not yet exist.
- Availability of an independent second human rater is unknown.
- Feasibility of a table-grounded subset is unknown.
- Annotation throughput has not been measured.

Blocker owner: `Het Patel unless reassigned in the experiment registry`.

## Completion criteria

### Design freeze complete

- [ ] Domain, eligibility rules, IDs, schemas, prompts, models, parameters, seeds, metrics, exclusions, and gates are recorded.
- [ ] Pilot preregistration is marked frozen with a commit SHA in the decision log.
- [ ] Development examples are separate from primary pilot items.

### Feasibility pilot complete

- [ ] All eight attempted items, including failures, are preserved.
- [ ] At least six of eight items yield unambiguous atomic claims and evidence spans.
- [ ] Annotation time supports the 48-item study with 25% contingency.
- [ ] The pipeline is reproducible and provenance is complete.
- [ ] Outcome is recorded as proceed, redesign, or stop.

### Verifier audit complete

- [ ] Controlled corruptions and clean records are versioned.
- [ ] Balanced accuracy, critical-error false acceptance, and position reversal are reported.
- [ ] Gate failures are retained and the human/model evaluation hierarchy follows the preregistered rule.

### Study and manuscript complete

- [ ] All planned primary and exploratory outputs are archived with immutable manifests.
- [ ] Prespecified analyses reproduce from versioned code and inputs.
- [ ] Null results, exclusions, leakage, limitations, and failed gates are reported.
- [ ] The 6–8 page pilot manuscript and release package reproduce their headline tables.

## Immediate next action

Run the **three-hour, eight-paragraph throughput pilot setup and dry run**:

1. Select one scientific domain using documented inclusion and exclusion criteria.
2. Build eight development examples with 2–4 atomic claims and evidence spans each.
3. Freeze the prompt, model, parameters, schemas, input IDs, gates, and preregistration commit before any primary pilot generation.
4. Run the complete pipeline and measure researcher minutes per usable paragraph.
5. Proceed only if at least six of eight examples are unambiguous and the projected workload supports 48 items with 25% contingency.

Owner: **Het Patel**  
Status: **Not started**  
Start date: `TBD`  
Completion date: `TBD`  
Evidence links: `TBD — input manifest, freeze commit, run manifest, outputs, and feasibility summary`

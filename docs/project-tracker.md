# Project Tracker

**Project:** Where Does Masked-Paragraph Reconstruction Signal Come From?  
**Owner:** Het Patel  
**Current phase:** Day 1 — frozen feasibility pilot  
**Protocol:** `preregistration/pilot-preregistration.md`  
**Freeze commit:** `88833dae64cd263e85fbba4d3b6d0d659fe7f588`

## Current configuration

- Domain: clinical and observational epidemiology
- Subdomain: cardiovascular and metabolic epidemiology
- Corpus: PMC Open Access Subset
- Earliest public date: December 1, 2024
- Models: Gemma 3 1B IT and Gemma 3 4B IT
- Inference: sequential 4-bit, 8,000-token input limit
- Pilot: 8 attempted paragraphs, 64 primary outputs
- Judge: GPT-5.6 Sol medium reasoning
- Adversarial checker: Claude Opus on disputes and frozen 25% audit subset
- Human reference: full adjudication plus blinded 25% rescore

## Day 1 checklist

- [x] Select domain and subdomain.
- [x] Select study-design scope and corpus source.
- [x] Fix temporal eligibility rule.
- [x] Fix generator checkpoints and inference configuration.
- [x] Fix paragraph mix and claim taxonomy.
- [x] Fix context conditions.
- [x] Fix annotation and judge roles.
- [x] Fix judge-validation gates.
- [x] Fix human-scoring rubric and workload ceiling.
- [x] Freeze pilot protocol.
- [x] Build candidate-paper inventory. (167 metadata-cross-checked; 119-record
  fixed discovery frame; 19 manually inspected eligible/reserve papers)
- [x] Resolve the blocked-database cross-check through the local/Colab pipeline.
- [x] Operationalize the conference-abstract identity rule (D-007).
- [ ] Attempt and log eight candidate paragraphs.
- [ ] Verify all eight against inclusion rules.
- [ ] Prepare prompts and schemas before generation.

## Feasibility gate

Proceed only if at least 6 of 8 attempted paragraphs are usable, all four conditions run reproducibly, provenance is complete, no usable item exceeds 15 minutes of human verification, and no major leakage failure is found.

## Next action

1. Confirm or reject the conservative human-review disposition for
   `PMC12418469`; it remains excluded meanwhile.
2. Select the eight pilot paragraphs from the revised four-paper configuration
   in `docs/corpus/eligible-paper-inventory.md`.
3. Attempt the eight paragraph annotations without generating primary outputs.

## Open corpus risks

- Unpaywall is source-incomplete until a real contact email is provided.
- OpenAlex succeeded without a key, but its current documentation requests a
  free key for stable publication use.
- 101 structurally eligible discovery records remain pending human scope review;
  this is retained as unresolved work rather than silently discarded.
- Limitation-paragraph supply remains the likely binding constraint at 48 items,
  although the enlarged inventory comfortably supports the eight-item pilot.
- Several papers carry summary boxes ("Research in context", "What Is New?", "KEY MESSAGE") that restate headline findings and must be excluded from true-context and distractor windows.

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
- [ ] Build candidate-paper inventory.
- [ ] Attempt and log eight candidate paragraphs.
- [ ] Verify all eight against inclusion rules.
- [ ] Prepare prompts and schemas before generation.

## Feasibility gate

Proceed only if at least 6 of 8 attempted paragraphs are usable, all four conditions run reproducibly, provenance is complete, no usable item exceeds 15 minutes of human verification, and no major leakage failure is found.

## Next action

Create the candidate-paper inventory and attempt the first eight paragraph annotations without generating primary model outputs.
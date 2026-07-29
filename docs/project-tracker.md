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
- [x] Build candidate-paper inventory. (`docs/corpus/eligible-paper-inventory.md`; 48 screened, 12 eligible)
- [ ] Attempt and log eight candidate paragraphs.
- [ ] Verify all eight against inclusion rules.
- [ ] Prepare prompts and schemas before generation.

## Feasibility gate

Proceed only if at least 6 of 8 attempted paragraphs are usable, all four conditions run reproducibly, provenance is complete, no usable item exceeds 15 minutes of human verification, and no major leakage failure is found.

## Next action

1. Rule on D-005: does a published conference abstract count as an "earliest public version"? This decides whether `PMC12093672` and `PMC12418469` re-enter the inventory.
2. Select the eight pilot paragraphs from `data/interim/eligible-paper-inventory.csv`. A four-paper configuration satisfying the frozen 3/3/2 mixture entirely within the 100–220 word band is proposed in `docs/corpus/eligible-paper-inventory.md` §5.
3. Attempt the eight paragraph annotations without generating primary model outputs.

## Open corpus risks

- The discovery search frame is not reproducible from the current environment (D-006); re-run from an unrestricted network before the 48-paragraph study.
- Usable limitation paragraphs are the binding corpus constraint: 5 genuine limitation paragraphs fall in the 100–220 word band across the 12 eligible papers. Sufficient for the 8-item pilot, likely insufficient for 48 items without a preregistered amendment.
- Several papers carry summary boxes ("Research in context", "What Is New?", "KEY MESSAGE") that restate headline findings and must be excluded from true-context and distractor windows.
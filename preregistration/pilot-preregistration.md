# Eight-Paragraph Feasibility Pilot Preregistration

**Working title:** *Where Does Masked-Paragraph Reconstruction Signal Come From? A Context and Verifier Audit in Scientific Papers*  
**Status:** frozen protocol candidate  
**Domain:** clinical and observational epidemiology  
**Subdomain:** cardiovascular and metabolic epidemiology

## Corpus

- Prospective, retrospective, registry, and EHR-based cohort studies.
- PubMed Central Open Access Subset only.
- Earliest public version must appear on or after **December 1, 2024**.
- Titles and abstracts are excluded from model prompts but allowed as annotation evidence.
- Tables and figures are excluded from the pilot.

## Generator models

- `google/gemma-3-1b-it`
- `google/gemma-3-4b-it`
- 4-bit quantized inference, loaded sequentially.
- Maximum input length: 8,000 tokens.

Generation settings:

```yaml
do_sample: false
temperature: 0
max_new_tokens: 384
repetition_penalty: 1.0
```

## Pilot sample

- Eight attempted paragraphs from approximately four papers.
- Three Results paragraphs.
- Three interpretation or reconciliation paragraphs.
- Two limitation paragraphs.
- Preferred length: 100–220 words; longer items require explicit justification.
- Each usable paragraph must contain 2–4 scoreable claims.

## Claim taxonomy

Each claim must be labeled as one of:

```text
empirical_result
statistical_result
author_interpretation
causal_hypothesis
limitation
uncertainty
```

At least two claims per paragraph must be recoverable from evidence outside the masked paragraph.

Interpretations and hypotheses are scored for faithful recovery and correct epistemic status, not treated as proven facts.

## Context conditions

Each paragraph is generated under four conditions:

1. **Prior-only:** broad domain and paragraph category only.
2. **True context:** immediately adjacent relevant paragraphs.
3. **Shuffled context:** length- and section-matched adjacent context from another eligible paper.
4. **Same-paper distractor:** nonadjacent text from the same paper that contains no evidence for the target claims.

Distractors must not state the target conclusion, cite the same analysis, or differ in length by more than approximately 25%.

Total primary outputs: **8 paragraphs × 4 conditions × 2 models = 64**.

## Annotation pipeline

1. GPT-5.6 Sol at medium reasoning proposes claims, labels, evidence spans, and controlled corruptions.
2. Deterministic scripts validate schemas, identifiers, and quoted evidence.
3. The researcher accepts, edits, or rejects every annotation.
4. Human-approved records become frozen reference annotations.
5. All proposals, edits, and final records are retained.

Maximum human verification time: **15 minutes per attempted paragraph**.

## Judge system

- GPT-5.6 Sol at medium reasoning is the primary model judge.
- Claude Opus is used as an adversarial checker for disputed cases, judge–human disagreements, and a frozen 25% audit subset.
- Codex orchestrates repository workflows but is not itself identified as the judge.
- Human scoring remains the reference standard.

## Judge validation

Construct:

- 40 clean claim–evidence records;
- one direction/sign corruption per record;
- one number/unit/magnitude corruption per record;
- one entity/comparator/exposure/condition corruption per record.

Total: 160 judge items.

Required gates:

```text
balanced accuracy >= 0.75
critical-error false acceptance <= 0.15
order-reversal disagreement <= 0.10
```

Failure of any gate makes model-judge scores exploratory and human scores primary.

## Human scoring

Each claim receives:

```text
2 = correct and appropriately qualified
1 = partially correct, vague, or missing an important qualifier
0 = absent, contradicted, or unsupported
```

Additional binary flags:

```text
critical contradiction
unsupported causal claim
invented number, unit, or entity
lost hedge or uncertainty
```

The researcher blindly rescores 25% and reports exact agreement and weighted Cohen’s kappa.

## Feasibility gate

Proceed to the 48-paragraph study only if:

- at least 6 of 8 attempted paragraphs are usable;
- all four conditions are reproducibly generated;
- complete model, prompt, source, annotation, and output provenance is retained;
- maximum annotation time does not exceed 15 minutes for any usable item;
- no major context leakage or corpus-construction failure is found.

Rejected items and rejection reasons must remain in the dataset.

## Claim boundary

Results apply only to the exact tested model checkpoints and the selected biomedical domain.

The study does not claim to recover authors’ private reasoning, perform RLVR, eliminate training contamination, or establish general LLM scientific-reasoning ability.

## Freeze rule

This protocol becomes formally frozen when `decisions/DECISIONS.md` records the commit SHA containing this version before any primary pilot generation.
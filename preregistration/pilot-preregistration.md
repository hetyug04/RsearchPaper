# Eight-Paragraph Feasibility Pilot Preregistration

Status: draft until explicitly marked frozen in the decision log.

## Purpose

Determine whether the proposed study is executable and whether masked scientific paragraphs can be annotated into sufficiently unambiguous factual claims for a larger context-and-verifier audit.

## Sample

Eight masked paragraphs drawn from recent open-access empirical papers in one domain. Development items must not later enter the confirmatory test set.

## Required annotation per item

- stable paper ID and paragraph ID;
- paragraph type;
- 2–4 atomic factual claims;
- supporting evidence spans available outside the masked paragraph;
- objective anchors where present;
- annotation time in minutes;
- ambiguity flag and reason.

## Pilot generation conditions

For each item:

1. prior-only;
2. true adjacent context;
3. shuffled matched context;
4. irrelevant same-paper context.

Use one fixed generation model, one fixed direct-reconstruction prompt, and frozen decoding parameters for the throughput pilot. Prompt debugging must use separate development examples and be logged.

## Feasibility gate

Proceed to the larger study only if:

- at least 6 of 8 paragraphs yield unambiguous atomic claims and evidence spans;
- no unresolved pipeline failure prevents reproducing inputs and outputs;
- measured annotation time supports the planned sample size with at least 25% contingency;
- the provenance record contains model identifier, prompt version, code commit, decoding parameters, item IDs, and output paths.

## Failure interpretation

Failure does not justify quietly replacing items until the threshold is met. Record all attempted items and reasons for failure. A failed gate means redesign, narrow the domain or paragraph type, reduce scope, or abandon the proposed study.

## Pilot outcomes to report

- usable items out of eight;
- annotation minutes per attempted and usable item;
- ambiguity categories;
- pipeline failures;
- preliminary claim-recovery and contradiction patterns, clearly labeled descriptive;
- recommendation: proceed, redesign, or stop.

## Freeze record

The preregistration becomes frozen only when `decisions/DECISIONS.md` records a timestamp, commit SHA, and explicit freeze decision before primary pilot generation.

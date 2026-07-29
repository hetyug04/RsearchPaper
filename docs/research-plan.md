# Research Plan

## Working title

*Where Does Masked-Paragraph Reconstruction Signal Come From? A Context and Verifier Audit in Scientific Papers*

## Primary research question

When an LLM reconstructs a masked scientific paragraph, how much factual improvement comes from relevant document evidence rather than generic prior knowledge, and how reliably can an LLM judge detect planted and naturally occurring scientific errors?

## Initial design

Corpus: open-access empirical papers from one scientific domain.

Initial full-study target: 48 masked paragraphs, balanced across background, methods, results, and discussion where feasible.

Primary context conditions:

1. Prior-only: paragraph type without paper-specific evidence.
2. True context: immediately preceding and following paragraphs.
3. Shuffled context: matched context from another paper and paragraph type.
4. Same-paper distractor: similarly sized but irrelevant text from the same paper.

Exploratory prompting comparison:

- direct reconstruction;
- claim-first reconstruction, where the model first lists recoverable claims and then writes the paragraph.

This is claim decomposition, not collection of hidden chain-of-thought.

## Annotation unit

Before generation, each item receives:

- stable paper and paragraph IDs;
- paragraph type;
- 2–4 atomic factual claims;
- supporting evidence spans;
- objective anchors when present, including numbers, units, signs, directions, entities, comparators, and experimental conditions.

## Verifier audit

Construct clean claim records and controlled corruptions covering:

- direction or sign reversal;
- number, magnitude, or unit alteration;
- entity, comparator, or experimental-condition substitution.

Provisional judge gates:

- balanced accuracy at least 0.75;
- critical-error false acceptance at most 0.15;
- position-order reversal at most 0.10.

A failed gate demotes model-judge results to descriptive status and makes human audit primary.

## Metrics

Primary candidate metrics:

- atomic-claim recovery;
- supported-claim precision;
- critical contradiction rate;
- numeric/sign/unit/condition accuracy on objective anchors.

Secondary or exploratory metrics:

- unsupported causal claims;
- hedge and uncertainty preservation;
- planted versus natural error detection;
- paragraph-type interactions;
- prompt interactions.

## Statistical plan

Use paired comparisons where the same masked item appears under multiple conditions. Estimate uncertainty using paper-clustered bootstrap confidence intervals. Use paired permutation tests for prespecified contrasts. Treat interactions as exploratory unless separately powered and preregistered.

## Claims the project must not make

The initial study does not establish that it:

- performed RLVR;
- recovered authors' hidden reasoning;
- eliminated memorization;
- demonstrated general scientific reasoning;
- produced publication-quality evidence merely by completing the pilot.

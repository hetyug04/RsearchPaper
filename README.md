# Scientific Reasoning Reconstruction

This repository is the canonical source of truth for an independent research arc on whether masked-paragraph reconstruction in scientific papers contains grounded scientific-reasoning signal, and whether model-based evaluators can reliably detect consequential scientific errors.

## Current paper

**Working title:** *Where Does Masked-Paragraph Reconstruction Signal Come From? A Context and Verifier Audit in Scientific Papers*

**Primary question:** When an LLM reconstructs a masked scientific paragraph, how much factual improvement comes from relevant document evidence rather than generic prior knowledge, and how reliably can an LLM judge detect planted and naturally occurring scientific errors?

This is not being framed as RLVR. A model judging another model is closer to model-based feedback unless the reward is grounded in objective verification. The initial study is therefore a context-and-verifier audit, not a claim that author reasoning traces have been recovered.

## Current phase

Phase 0: feasibility and design freeze.

The first empirical action is an eight-paragraph throughput pilot. The full study proceeds only if at least six of eight examples yield unambiguous atomic claims and the measured annotation workload supports the planned sample with contingency.

See:

- [Canonical project tracker](docs/project-tracker.md) for current status, decisions, blockers, gates, and next actions
- [Research plan](docs/research-plan.md) for the proposed design
- [Pilot preregistration](preregistration/pilot-preregistration.md) for frozen pilot decisions
- [Research log](research-log/LOG.md) for chronological work
- [Decision log](decisions/DECISIONS.md) for methodological decisions
- [`experiments/registry.csv`](experiments/registry.csv) for experiment status
- [`AGENTS.md`](AGENTS.md) for Codex and agent operating rules
- [`WORKFLOW.md`](WORKFLOW.md) for the cross-device synchronization protocol

The project tracker is the canonical operational view. The preregistration and decision log govern which methodological choices are frozen.

## Repository principles

1. GitHub is the ground truth. Local devices and agent workspaces are disposable replicas.
2. Every meaningful research action must leave a durable artifact: commit, issue, log entry, experiment record, or decision record.
3. Raw outputs are immutable. Corrections create new versions rather than silently replacing old results.
4. Hypotheses, exclusions, metrics, and gates must be frozen before primary generation.
5. Null results and failed gates are retained and reported.
6. Agents may propose changes, but must not rewrite provenance or quietly alter preregistered decisions.

## Planned structure

```text
.
├── AGENTS.md
├── WORKFLOW.md
├── docs/
├── preregistration/
├── research-log/
├── decisions/
├── experiments/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── prompts/
├── src/
├── scripts/
├── notebooks/
├── outputs/
│   ├── raw/
│   ├── metrics/
│   └── figures/
└── paper/
```

Empty directories are represented by `.gitkeep` files until populated.

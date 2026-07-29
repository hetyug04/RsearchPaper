# AGENTS.md

These instructions apply to Codex and any other coding or research agent operating in this repository.

## Source of truth

- The remote GitHub repository is canonical.
- Before work: fetch and inspect the current default branch, open issues, `research-log/LOG.md`, `decisions/DECISIONS.md`, and `experiments/registry.csv`.
- Never assume a local checkout is current.
- Never force-push shared branches or rewrite published history.

## Branch and commit protocol

1. Start from an updated `main`.
2. Use a focused branch named `agent/<short-task>`.
3. Keep one conceptual change per commit when practical.
4. Commit messages must state what changed, not vague phrases such as `updates` or `work`.
5. Push the branch and open a pull request for substantive changes.
6. Do not merge a pull request that changes preregistered hypotheses, metrics, exclusions, or primary analyses without an explicit decision-log entry.

## Research provenance

Every meaningful action must update at least one durable record:

- `research-log/LOG.md` for chronological activity;
- `decisions/DECISIONS.md` for choices and rationale;
- `experiments/registry.csv` for experiment state;
- an issue or pull request for work tracking;
- a versioned artifact under `outputs/` for generated results.

Record model/provider, exact model identifier, date, prompt version, code commit, seed, decoding parameters, input IDs, and output path whenever applicable.

## Data and output rules

- Treat `data/raw/` and `outputs/raw/` as append-only.
- Never silently edit generated outputs or human annotations after analysis begins.
- Corrections require a new version and a log entry explaining the change.
- Do not commit copyrighted full-text papers unless redistribution is permitted. Store stable identifiers, metadata, extraction code, and permitted excerpts instead.
- Do not commit secrets, API keys, tokens, credentials, private correspondence, or personally identifying reviewer data.
- Large artifacts should use an external store or Git LFS only after the repository owner approves the choice.

## Methodological boundaries

- Do not describe model-generated rationales as recovered human reasoning.
- Do not call model-judged rewards RLVR unless the reward is grounded in objective verification.
- Distinguish confirmatory analyses from exploratory analyses.
- Do not tune prompts, exclusions, or metrics on primary test outputs and then present them as preregistered.
- Preserve null results, failed verifier gates, and excluded examples with reasons.
- Do not invent citations, measurements, experimental runs, or model access.

## Before changing code or analysis

- State the exact task and files in scope.
- Inspect existing tests and data contracts.
- Prefer deterministic scripts over notebook-only logic.
- Add or update validation for schemas, IDs, duplicate records, and missing metadata.
- Run the smallest relevant check, then the complete available test suite.

## Completion checklist

Before declaring work complete:

- Pull/rebase against current `main` and resolve conflicts without discarding others' work.
- Run relevant tests or validation scripts.
- Update the research log.
- Update the experiment registry if an experiment changed state.
- Add a decision entry for methodological changes.
- Verify generated artifact paths exist and are referenced from the log.
- Summarize limitations and unresolved failures in the pull request.

# Cross-Device Research Workflow

## Start of every session

```bash
git clone https://github.com/hetyug04/RsearchPaper.git  # first use only
cd RsearchPaper
git fetch origin
git checkout main
git pull --ff-only origin main
```

Read `README.md`, `AGENTS.md`, the latest entries in `research-log/LOG.md`, `decisions/DECISIONS.md`, and the relevant rows in `experiments/registry.csv` before changing anything.

## Claim a unit of work

Use a GitHub issue for any task that could overlap across devices or agents. State:

- objective;
- files or experiment IDs in scope;
- expected artifact;
- completion condition;
- dependencies or blocked decisions.

Create a branch:

```bash
git checkout -b agent/<short-task>
```

One active writer per experiment ID is the default. Parallel work should use separate experiment IDs or clearly disjoint artifacts.

## During work

- Commit checkpoints that would be costly to reconstruct.
- Do not leave the only copy of annotations, prompts, or outputs in a notebook runtime.
- Use stable IDs for papers, paragraphs, claims, prompts, and runs.
- Write generated data to a new path; do not overwrite a prior run.
- Log deviations immediately rather than reconstructing them later from memory.

Recommended run naming:

```text
outputs/raw/<experiment_id>/<YYYYMMDD-HHMM>_<model>_<prompt_version>_<seed>.jsonl
```

## End of every session

1. Run validation/tests.
2. Update `research-log/LOG.md`.
3. Update `experiments/registry.csv`.
4. Update `decisions/DECISIONS.md` if a methodological choice changed.
5. Commit and push.
6. Open or update the pull request.
7. Leave the issue with an explicit state: complete, blocked, or next action.

## Conflict policy

- Never resolve conflicts by accepting all of one side without inspection.
- Preserve both provenance records, then reconcile duplicates explicitly.
- Do not edit immutable raw outputs to make branches agree.
- If two agents changed the same preregistration, stop and create a decision issue rather than choosing silently.

## Main branch policy

`main` should contain the latest accepted ground truth. Exploratory code, unfinished annotations, and uncertain methodological changes remain on branches until reviewed. A merged commit is not evidence that a scientific claim is correct; it only establishes the accepted project record.

## Codex connection

In Codex, select or clone `hetyug04/RsearchPaper`, instruct it to read `AGENTS.md` before acting, and give each task a specific issue or artifact target. Codex must work on an `agent/*` branch and leave a pull request rather than making unlogged local-only changes.

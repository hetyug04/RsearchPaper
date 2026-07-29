# Decision Log

Record methodological and operational decisions here. Each entry must include date, status, decision, rationale, alternatives considered, and consequences.

## D-001 — 2026-07-29

**Status:** accepted

**Decision:** Treat GitHub as the canonical cross-device source of truth.

**Rationale:** Multiple devices and agents will operate on the project. A shared versioned record is necessary to prevent divergent prompts, annotations, analyses, and claims.

**Alternatives considered:** local folders, cloud drive, chat history.

**Consequences:** meaningful work must be committed or represented by an issue, log entry, experiment record, or versioned artifact.

## D-002 — 2026-07-29

**Status:** accepted

**Decision:** Frame the first paper as a context-and-verifier audit, not as an RLVR result or recovery of human reasoning traces.

**Rationale:** An LLM evaluator is not objective verification, and scientific papers usually do not expose the authors' full reasoning process.

**Alternatives considered:** direct RL training paper; synthetic reasoning-trace paper; broad scientific reasoning benchmark.

**Consequences:** the initial study measures evidence dependence, factual reconstruction, and verifier reliability. Stronger training claims require later evidence.

## D-003 — 2026-07-29

**Status:** proposed, not frozen

**Decision:** Use an eight-paragraph feasibility pilot before scaling to the proposed 48-item study.

**Rationale:** Annotation quality and throughput are the main unknowns. Scaling before measuring them would create avoidable design drift.

**Alternatives considered:** immediately annotate 48 items; table-only study; human-first verifier study.

**Consequences:** pilot generation must not begin until its domain, prompts, model, parameters, item rules, and freeze commit are recorded.

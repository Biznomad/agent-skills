---
name: graph-engineering
description: Design, evaluate, and operate reliable multi-agent or multi-step workflow graphs for Codex, Claude Code, and mixed-agent systems. Use when a task may benefit from specialized agents, fan-out/fan-in parallelism, conditional routing, maker-checker review, PM/Engineer/QA handoffs, shared-state orchestration, worktree isolation, or an explicit DAG; also use to decide whether a proposed graph should remain a simpler single-agent loop.
---

# Graph Engineering

Design the smallest explicit workflow whose topology materially improves reliability, speed, isolation, or auditability. Treat each node as a well-engineered loop with its own inputs, tools, outputs, stop condition, and verification.

## Core rules

- Prefer a single loop unless a graph earns its coordination cost.
- Keep control flow diagram-legible: define routes before execution.
- Give every node one job and a narrow context.
- Pass structured state, not unbounded chat history.
- Separate makers from checkers; keep reviewer context fresh.
- Use executable gates whenever possible: tests, schemas, linters, oracles, or explicit acceptance checks.
- Preserve immutable anchors that optimizing nodes cannot rewrite.
- Cap concurrency, retries, tokens, and elapsed time.
- Obey the active environment's delegation and permission rules. Never spawn agents merely because this skill describes a graph.
- Verify version-sensitive limits and product features against installed or official documentation before relying on them.

## Workflow

### 1. Define the objective and success bar

Write a checkable objective before drawing nodes.

Capture:

- Deliverable
- Acceptance criteria
- Constraints and out-of-scope work
- Available tools, agents, models, and isolation mechanisms
- Token, cost, concurrency, and time budgets
- Human approval or external-write boundaries
- Final verification command or observable verdict

If the success bar is vague, stop and improve it before designing the graph.

### 2. Run the graph eligibility check

Answer these questions:

1. Does the work require genuinely separate specialized contexts?
2. Is there real fan-out/fan-in or another useful dependency structure?
3. Can the routing be defined explicitly instead of emerging from one agent's reasoning?
4. Does the topology add a distinct quality, risk, ownership, or verification objective?

Use the result:

- 0-1 yes: keep one agent loop.
- 2-3 yes: use a small graph, normally two or three nodes.
- 4 yes: use an explicit graph with shared state and gates.

Reject graphing when the task is tightly sequential, shared context is essential, coordination costs exceed the likely gain, or the proposed nodes are only renamed personas.

Read [decision-and-topologies.md](references/decision-and-topologies.md) when comparing shapes, costs, or failure modes.

### 3. Write the graph contract

Specify the graph before launching it:

```yaml
objective: "Checkable outcome"
success_bar:
  - "Observable acceptance criterion"
state:
  task_spec: "Immutable brief"
  evidence: []
  artifacts: []
  verdicts: []
nodes:
  - id: implementer
    job: "Produce the artifact"
    reads: [task_spec]
    writes: [artifacts]
    tools: []
    isolation: "worktree or shared workspace"
    stop: "Artifact exists and local checks pass"
  - id: reviewer
    job: "Test artifact against the immutable brief"
    reads: [task_spec, artifacts]
    writes: [verdicts]
    stop: "Return PASS or FAIL with evidence"
edges:
  - "implementer -> reviewer"
  - "reviewer FAIL -> implementer"
  - "reviewer PASS -> ship"
budgets:
  concurrency: 2
  max_retries: 3
  timeout_minutes: 30
```

For each node, define:

- Exact responsibility and exclusions
- Minimum required input
- Structured output contract
- Allowed tools and mutation scope
- Workspace ownership or isolation
- Stop condition
- Failure and timeout behavior

### 4. Choose the smallest suitable topology

Prefer these in order:

1. **Maker -> Checker** for most implementation or analysis work.
2. **Researcher fan-out -> Synthesizer -> Reviewer** for independent sources.
3. **Map -> Reduce** for mechanical batches with a deterministic join.
4. **Orchestrator -> Workers -> Aggregator** for decomposable work with centralized control.
5. **PM -> Engineer -> QA** for acceptance-driven backlog execution.
6. **Generator <-> Evaluator** for bounded iterative optimization.

Do not add a node unless it changes context, tools, ownership, isolation, or the success bar.

### 5. Design shared state and edges

Keep state explicit and compact:

- Store the task specification once as an immutable anchor.
- Store evidence with provenance.
- Store artifacts by path, identifier, or structured result instead of pasting full histories.
- Store verdicts as `PASS`, `FAIL`, or `BLOCKED` plus evidence and next action.
- Use conditional edges only on machine-checkable or tightly specified predicates.
- Use fan-in only after every required branch is terminal.
- Define partial-failure policy: retry, degrade, exclude, or fail the graph.

Prevent metric gaming:

- Pair an optimization metric with a counter-metric.
- Let slower review loops own the reference values used by faster worker loops.
- Keep held-out tests, safety constraints, and acceptance criteria frozen.

### 6. Map the graph to the runtime

For Codex, read [codex-orchestration.md](references/codex-orchestration.md) before creating agents, worktrees, custom roles, resumable tasks, automations, or issue-driven workflows.

For the PM/Engineer/QA operating model, read [pm-engineer-qa-template.md](references/pm-engineer-qa-template.md) and adapt the templates rather than inventing new role boundaries.

Use:

- The strongest reasoning model for orchestration, synthesis, and acceptance review.
- Lower-cost workers for bounded scans or mechanical implementation when appropriate.
- Worktrees or file ownership for parallel code mutations.
- Fresh reviewer context to reduce shared blind spots.
- Cross-model review only when the risk justifies its additional cost.

### 7. Execute in bounded waves

Only execute after authorization permits delegation and mutations.

1. Launch independent nodes in parallel up to the concurrency cap.
2. Continue useful orchestrator work while branches run.
3. Collect structured outputs at a fan-in point.
4. Deduplicate and reconcile conflicts centrally.
5. Run the reviewer or executable gate.
6. Route failures back with specific evidence.
7. Stop after the retry cap and report the unresolved blocker.

Never let parallel workers edit overlapping files without explicit ownership or isolation.

### 8. Verify and terminate

Require all of the following:

- Every required node reached a terminal state.
- Every acceptance criterion has evidence.
- Executable checks ran successfully or failures are disclosed.
- The final artifact matches the immutable task specification.
- No branch result was silently dropped.
- External mutations are confirmed.
- The graph stops; no open-ended reviewer loop remains.

## Output format

Lead with the loop-or-graph decision and its justification. Then provide only the useful artifacts:

1. Objective and success bar
2. Topology and optional Mermaid diagram
3. Graph contract
4. Node ownership and state schema
5. Execution/budget plan
6. Verification gates and termination rule

When asked to execute, report the final outcome rather than narrating every routing event.

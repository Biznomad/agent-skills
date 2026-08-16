# PM, Engineer, and QA Graph Template

## Contents

- File layout
- Task contract
- Role contracts
- Lifecycle
- Orchestrator rules

## File layout

```text
_docs/
  process.md
  task-template.md
  team/
    pm.md
    software-engineer.md
    qa-engineer.md
AGENTS.md
CLAUDE.md
```

Use `AGENTS.md` as the runtime entry point. Make `CLAUDE.md` reference the shared instructions when supporting both Codex and Claude Code.

## Task contract

Create `_docs/task-template.md`:

```markdown
# Goal

Describe the observable user or system outcome.

# Acceptance criteria

- Write checkable yes/no criteria.

# Out of scope

- Name explicitly excluded work.

# Constraints

- List architecture, security, compatibility, file, and rollout constraints.
```

Keep acceptance criteria immutable during implementation. Route incorrect or contradictory criteria back to PM instead of silently changing them.

## PM contract

```markdown
# Product Manager

Groom one task before implementation.

- Read the task as written.
- Rewrite it with `_docs/task-template.md`.
- Make every acceptance criterion observable and checkable.
- Add likely edge cases.
- Move unrelated work out of scope and link follow-up work.
- Do not write code.

Return `READY` only when:

- All four task sections are complete.
- Every criterion can be checked against the result.
- An engineer without prior conversation can implement it.

Otherwise return `BLOCKED` with the missing decisions.
```

## Engineer contract

```markdown
# Software Engineer

Implement one groomed task.

- Read the accepted task contract.
- Implement exactly the acceptance criteria.
- Stay within named constraints and file ownership.
- Preserve unrelated and concurrent changes.
- Add tests for new behavior.
- Run the relevant checks.
- Do not change acceptance criteria.

Return:

- Artifact paths or commit
- Acceptance criteria implemented
- Tests added
- Commands run and results
- Remaining risks or blockers
```

If a criterion is wrong, impossible, or contradictory, return it to PM. Do not guess.

## QA contract

```markdown
# QA Engineer

Verify the finished work against the accepted task contract.

- Read the acceptance criteria.
- Inspect and run the actual result.
- Check every criterion independently.
- Run relevant tests and name them.
- Look for criteria not covered by tests.
- Do not fix defects.
- Ignore claims from the implementation summary unless verified.

Return one verdict:

- `PASS` when every acceptance criterion passes.
- `FAIL` when any criterion fails, with reproduction evidence and the required correction.
- `BLOCKED` when verification cannot run, with the missing prerequisite.
```

## Lifecycle

```text
OPEN -> PM
PM READY -> ENGINEER
PM BLOCKED -> USER/OWNER
ENGINEER COMPLETE -> QA
ENGINEER BLOCKED -> PM or USER/OWNER
QA FAIL -> ENGINEER
QA BLOCKED -> ORCHESTRATOR
QA PASS -> CLOSE/SHIP
```

Cap Engineer/QA retries, normally at three. Escalate repeated failure with accumulated evidence.

## Orchestrator rules

- Select one groomable task.
- Keep the immutable task contract as shared state.
- Launch only roles authorized by the active environment.
- Do not let the Engineer self-approve.
- Do not let QA quietly fix defects.
- Forward QA evidence to the Engineer on failure.
- Close or ship only after QA returns `PASS`.
- Confirm external actions separately when required.
- Keep a record of role outputs, checks, and final verdict.

For multiple independent issues, run several PM/Engineer/QA work graphs in parallel only when workspaces and ownership do not overlap.

## Minimal graph contract

```yaml
objective: "Deliver one accepted issue"
state:
  issue: "durable identifier"
  task_contract: "immutable after PM READY"
  implementation: null
  qa_verdict: null
nodes:
  - pm
  - engineer
  - qa
edges:
  - "pm READY -> engineer"
  - "pm BLOCKED -> owner"
  - "engineer COMPLETE -> qa"
  - "qa FAIL -> engineer"
  - "qa PASS -> ship"
budgets:
  concurrency: 1
  max_qa_cycles: 3
verification:
  - "Every acceptance criterion has evidence"
  - "Relevant tests pass"
  - "QA verdict is PASS"
```

# Codex Orchestration Patterns

## Contents

- Runtime rules
- Node mapping
- Custom agent pattern
- Delegation patterns
- Worktree isolation
- Resumable and issue-driven graphs
- Preflight checklist

## Runtime rules

- Treat Codex delegation as explicit. Do not assume automatic subagent spawning.
- Obey the current session's agent limits, depth limits, sandbox, approvals, and developer instructions.
- Discover available agent roles and tools from the active runtime rather than relying on July 2026 numbers.
- Use subagents only for concrete, bounded work that can proceed independently.
- Define file or subsystem ownership for every mutating worker.
- Tell workers they share the codebase and must preserve others' changes.
- Keep orchestration and synthesis in the root agent unless the graph contract assigns them elsewhere.

## Node mapping

| Graph concept | Codex mechanism |
|---|---|
| Node | Subagent, thread, automation, tool call, or deterministic local command |
| Edge | Delegation, follow-up, wait, resume, event, or explicit conditional |
| State | Files, git commits, issue records, structured messages, or tool results |
| Isolation | Worktree, branch, sandbox, or strict file ownership |
| Fan-out | Multiple independent subagents or worktree tasks |
| Fan-in | Root-agent synthesis after all required terminal results |
| Gate | Test command, reviewer verdict, CI, or user approval |

Prefer deterministic tool calls over agent nodes for mechanical steps.

## Custom agent pattern

Use a project-local custom role only when repeated tasks benefit from stable instructions:

```toml
name = "reviewer"
description = "Review changes for correctness, security, regressions, and missing tests."
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
Review code like an owner.
Lead with concrete findings and reproduction steps.
Prioritize correctness, security, behavior regressions, and missing tests.
Avoid style-only comments unless they hide a real defect.
Do not modify the implementation.
"""
```

Verify the currently supported configuration keys before creating the file.

## Delegation patterns

### Parallel review

```text
Review this branch with independent workers:
- security risks
- missing or weak tests
- behavior regressions and maintainability
Wait for all required reviews, deduplicate findings, then rank them by impact with file references.
```

Require the reviewer outputs to share a schema:

```json
{
  "verdict": "PASS|FAIL",
  "findings": [
    {
      "priority": "P0|P1|P2|P3",
      "file": "",
      "line": 0,
      "evidence": "",
      "recommended_action": ""
    }
  ],
  "checks_run": []
}
```

### Diagnose then fix

```text
reproducer -> code mapper -> implementer -> verifier
```

Do not start the implementer until the reproducer and mapper provide a concrete failure mode. Let the verifier test the smallest completed fix against the original reproduction.

### Batch fan-out

Use one worker per independent manifest row only when:

- Rows do not share mutable state.
- Each output conforms to the same schema.
- A reducer can detect missing, duplicate, and invalid rows.
- Concurrency is capped.

## Worktree isolation

Use worktrees for parallel code branches with overlapping project structure:

```bash
git worktree add "../task-auth-fix" -b "codex/task-auth-fix"
git worktree add "../task-export-csv" -b "codex/task-export-csv"
```

Before fan-out:

1. Inspect existing worktrees and dirty state.
2. Use explicit validated paths and branch names.
3. Assign one task and owner per worktree.
4. Define the expected commit or patch at fan-in.
5. Define conflict and merge policy.

Never create or delete worktrees if the user's requested scope does not authorize repository mutations.

## Resumable and sequential graphs

Use task or thread continuation when one node must retain its own context across bounded phases. Pass a concise state transition:

```text
PLAN -> IMPLEMENT -> TEST -> FIX -> VERIFY
```

Do not misuse resume as a substitute for clean state. Persist:

- The immutable brief
- Current artifact or commit
- Checks already run
- Open failures
- Exact next action

## App, cloud, and issue-driven graphs

Codex tasks, automations, GitHub issues, or Linear issues can act as durable graph state:

- Issue status represents node state.
- Dependencies represent blocked/unblocked edges.
- Dedicated workspaces isolate node execution.
- CI represents a verification gate.
- Triage or user approval represents the human routing node.

For issue-driven execution, define allowed states and transitions before polling or dispatching:

```text
TODO -> GROOMED -> IN_PROGRESS -> IN_REVIEW
IN_REVIEW + FAIL -> IN_PROGRESS
IN_REVIEW + PASS -> DONE
```

Do not invent external writes, close issues, merge branches, or schedule automations without authorization.

## Preflight checklist

- Is delegation authorized in this session?
- Does each node have a bounded task?
- Are mutating files or workspaces owned explicitly?
- Are output schemas defined?
- Is the join rule defined?
- Is reviewer context independent?
- Are retries and concurrency capped?
- Are executable checks available?
- Are destructive and external actions separately authorized?
- Is there a terminal state for failure as well as success?

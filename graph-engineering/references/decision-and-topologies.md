# Decision Framework and Topologies

## Contents

- Eligibility decision
- Topology selection
- State and routing rules
- Cost and reliability warnings
- Failure-mode checklist

## Eligibility decision

Treat a loop as a one-node graph with a self-edge. Add topology only when it creates a real boundary or dependency.

### Four-question check

1. **Separate contexts:** Does a specialist need a context that should not be polluted by another node's raw work?
2. **Real dependency shape:** Is there independent fan-out/fan-in, a useful conditional edge, or a handoff with changed ownership?
3. **Explicit routing:** Can the control flow be read from a diagram before execution?
4. **Distinct success responsibility:** Does a node own a different quality bar, risk, or decision?

Interpretation:

- 0-1 yes: use one loop.
- 2-3 yes: compose a small graph.
- 4 yes: model a formal graph with shared state and explicit gates.

### Signals that justify a graph

- Distinct specialties with clean handoffs
- Parallel branches that can work without shared mutable context
- Different models, tools, permissions, or sandboxes per step
- Auditable routing or regulated approval
- Failure isolation
- Independent maker-checker review
- Stable organizational ownership plus task-specific work decomposition

### Signals that reject a graph

- The task is primarily sequential reasoning.
- Every role needs the same growing context.
- The only difference between nodes is a persona label.
- The reviewer has no independent criterion or executable check.
- Human review bandwidth is already the bottleneck.
- A simple loop has not yet acquired a reliable stop condition.

## Topology selection

| Topology | Shape | Use it for | Avoid it when |
|---|---|---|---|
| Maker-checker | maker -> checker -> pass/return | Code, documents, plans, risky edits | The checker lacks a separate bar |
| Research-write-review | N researchers -> writer -> reviewer | Multi-source synthesis | Sources are dependent or sequential |
| Map-reduce | task -> N homogeneous maps -> reducer | Per-file audits, batch classification | Branch outputs cannot be normalized |
| Orchestrator-workers | planner -> N specialists -> aggregator | Mixed specialties under central control | Workers require constant peer negotiation |
| PM-engineer-QA | groom -> implement -> acceptance gate | Backlog or issue execution | Requirements are still exploratory |
| Evaluator-optimizer | generator <-> evaluator -> ship | Bounded refinement | There is no objective evaluator |
| Peer mesh | agents exchange directly | Genuine coordination among equals | Hub-spoke delegation is sufficient |

Start with two or three nodes. Expand only after observing a concrete bottleneck.

## Canonical contracts

### Maker-checker

```text
brief -> maker -> artifact -> checker
                         FAIL -> maker (specific evidence)
                         PASS -> ship
```

Keep the brief immutable. Give the checker the brief, artifact, and verification tools, not the maker's full chain of thought.

### Research fan-out

```text
question -> source A researcher --\
         -> source B researcher ----> synthesizer -> reviewer -> answer
         -> source C researcher --/
```

Require every branch to return the same schema:

```json
{
  "claims": [],
  "evidence": [],
  "source_urls": [],
  "uncertainties": []
}
```

### Map-reduce

```text
manifest -> map(item_1..item_n) -> normalized results -> deterministic reducer
```

Use a deterministic reducer when possible. Define missing-item and duplicate-item policies before fan-out.

### Evaluator-optimizer

```text
generator -> evaluator
   ^          |
   |--REVISE--|
      APPROVE -> ship
```

Cap retries, normally at three. Treat repeated identical failure as a blocker, not permission to loop forever.

## State and routing rules

- Pass structured payloads across edges.
- Keep source evidence and provenance together.
- Store large artifacts on disk and pass their paths.
- Distinguish organizational roles from task-time nodes:
  - **Org graph:** durable ownership and stable responsibilities.
  - **Work graph:** ephemeral branches created for one task.
- Centralize aggregation when independent workers could amplify each other's errors.
- Use explicit join semantics: all required, quorum, first-success, or best-score.
- Treat timeouts and tool errors as states with defined routes.

## Cost and reliability warnings

The July 2026 source guide reports:

- Multi-agent systems can materially outperform on parallelizable tasks.
- They can underperform badly on tightly sequential reasoning.
- Independent agents may amplify errors more than centrally coordinated agents.
- Multi-agent research can consume roughly an order of magnitude more tokens than chat.
- Human review throughput is often the true system ceiling.

Treat these as directional findings, not timeless constants. Verify current studies and vendor limits before using exact numbers in a decision.

## Failure-mode checklist

- **Persona theater:** Nodes have titles but no distinct inputs, tools, outputs, or success bars.
- **The oversized org chart:** Many handoffs optimize explainability rather than throughput.
- **Context leakage:** Reviewers inherit the maker's assumptions and blind spots.
- **Unbounded revision:** No retry cap or terminal blocker state.
- **Implicit routing:** The orchestrator invents paths while executing.
- **No fan-in contract:** Branch results cannot be reconciled deterministically.
- **Shared-write collisions:** Parallel workers mutate overlapping files or records.
- **Metric gaming:** Optimizers can rewrite their own evaluation targets.
- **No anchors:** Tests, acceptance criteria, or external outcomes are mutable.
- **Stale platform assumptions:** Limits or features are copied from an old guide.
- **Dropped branches:** The final synthesis ignores failed or late workers without disclosure.
- **Cost blindness:** Parallelism is increased before measuring token and review costs.

Correct these topologically: reduce nodes, centralize coordination, freeze anchors, isolate writes, add executable gates, and bound retries.

# Layer 3 — the orchestration graph

How a cycle's work actually executes: which agents run, in what topology, and what has to
agree before an increment counts as done.

## Contents
- [When to fan out at all](#when-to-fan-out-at-all)
- [Picking a parallel batch from the frontier](#picking-a-parallel-batch-from-the-frontier)
- [The maker/checker contract](#the-makerchecker-contract)
- [Topologies](#topologies)
- [Model tiering](#model-tiering)
- [Failure handling](#failure-handling)

## When to fan out at all

Fan-out costs tokens and coordination. It pays only when the frontier holds several nodes
that are genuinely independent — no shared files, no shared schema migration, no ordering
between them.

Sequential is correct when: the frontier has one node; nodes touch the same files; or the
phase is `spike` (spikes are for learning, and parallel learning does not compound —
the second spike should be informed by the first).

Fan out when: three or more frontier nodes touch disjoint areas, or a single node needs
independent verification from multiple angles.

**Requires explicit user opt-in.** The Workflow tool must not be invoked unless the user
asked for multi-agent orchestration. Without that, run cycles sequentially in the main
loop — the graph still provides all its value; only execution is serial.

## Picking a parallel batch from the frontier

```
batch = []
for node in frontier(phase=current):
    if node.effort <= 3 and disjoint(node.files, [n.files for n in batch]):
        batch.append(node)
    if len(batch) == max_parallel: break
```

Disjointness is the hard constraint. Two agents editing the same file in one cycle will
clobber each other — either give each a git worktree (`isolation: "worktree"`) or keep
them out of the same batch. Worktrees cost real setup time, so prefer disjoint batching
and reserve isolation for genuine conflicts.

Cap `max_parallel` at 3–4 for build work. Verification fan-out can go wider; it is
read-only.

## The maker/checker contract

Every increment passes a checker before its node flips to `done`. The checker is a
**separate agent with a default stance of REJECT** — it must be convinced, and silence or
uncertainty means rejection. A maker validating its own work is not verification.

The checker gets: the node's `title` (the finished condition), the diff, and how to
exercise the change. It returns a verdict plus evidence. Reject → node returns to `todo`
with the rejection in `notes`; it re-enters the frontier and does not silently vanish.

For risky nodes (auth, billing, permissions, anything touching money or access), use
**perspective-diverse checkers** rather than N identical ones — one for correctness, one
for security, one for "does it actually reproduce end to end". Redundant identical
checkers agree with each other; diverse ones catch different failure classes.

## Topologies

**Pipeline (default).** Each node flows through build→verify independently, no barrier.
Node A can be verifying while node B is still building. Wall-clock is the slowest single
chain, not the sum of stage maxima.

```
pipeline(batch,
  n => agent(build_prompt(n),  {phase: 'build'}),
  r => agent(verify_prompt(r), {phase: 'verify', schema: VERDICT})
)
```

**Barrier.** Only when a stage genuinely needs every prior result at once — deduping
findings across an audit, or an early exit when the total is zero. "I need to flatten the
list first" is not a reason; do that inside a stage.

**Diverse-lens verify.** One node, several checkers, majority rules.

```
votes = parallel(['correctness','security','e2e'].map(lens => () =>
  agent(`Try to REFUTE this increment via the ${lens} lens. Default to refuted.`,
        {schema: VERDICT})))
accepted = votes.filter(v => v && !v.refuted).length >= 2
```

## Model tiering

Deliberately spend where judgment matters:

| Work | Tier |
|---|---|
| Graph edits, scoring, phase-gate calls, synthesis | strongest |
| Building an increment, verifying it | mid |
| Formatting, log writes, link/console scans, mechanical checks | cheapest |

The graph layer is where a bad decision costs the most and a good one compounds, so it
gets the strongest model even though it is the smallest token spend.

## Failure handling

- An agent that dies returns `null` — filter before use, and never treat a missing result
  as a pass.
- A node whose maker fails goes back to `todo` with the error in `notes`. Do not retry
  blindly in the same cycle; a second identical attempt usually fails identically.
- If the same node fails twice across cycles, it is mis-scoped. Split it into smaller
  nodes and re-link, rather than attempting it a third time.
- Log what was skipped. A cycle that silently dropped two of four batch nodes reads as a
  clean run in the log and is the easiest way to lose work.

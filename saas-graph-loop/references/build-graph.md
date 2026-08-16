# Layer 2 — the build graph

The dependency DAG that decides what gets built next. Managed by `scripts/graph.py`;
this file explains the semantics the script enforces.

## Contents
- [The core claim](#the-core-claim)
- [Node anatomy](#node-anatomy)
- [Edges mean "cannot start until"](#edges-mean-cannot-start-until)
- [Phases](#phases)
- [Scoring](#scoring)
- [Frontier vs critical path](#frontier-vs-critical-path)
- [Keeping the graph honest](#keeping-the-graph-honest)

## The core claim

A loop that picks work from a flat backlog drifts, because "what's most valuable" is
answered from whatever is in context that cycle. A loop that picks from a *dependency
frontier* cannot drift: the set of legal next moves is computed from structure, and the
ranking within it is arithmetic. The model's judgment goes into **scoring nodes and
writing edges** — done once, deliberately — not into re-litigating priorities every cycle.

This is the whole reason the graph exists. Preserve it: never build something that is not
on the frontier. If it feels urgent and it is not on the frontier, the graph is wrong —
fix the graph first, then build. That keeps the graph a true model instead of a stale doc.

## Node anatomy

```json
"billing": {
  "layer": "build",          // domain | build | gtm
  "title": "Stripe subscriptions, webhooks, dunning",
  "status": "todo",          // todo | doing | done | blocked | dropped
  "needs": ["auth"],         // hard prerequisites
  "impact": 5, "reach": 4, "confidence": 4, "effort": 3,
  "phase": "mvp",            // spike | mvp | launch | scale
  "notes": "per-seat; annual later",
  "evidence": "checkout e2e green, webhook replay tested"
}
```

`title` states a **finished condition**, not an activity. "Stripe subscriptions" is
checkable; "work on billing" is not. `evidence` is filled at completion with what was
actually verified — it is the audit trail that makes `done` trustworthy.

## Edges mean "cannot start until"

`needs` is a hard technical or logical prerequisite, not a preference. Three tests:

- Could this be built first, badly, and fixed later? → not an edge, just an ordering wish.
- Would building it first produce work that must be thrown away? → real edge.
- Does it need the other node's *output* (a schema, a token, a decision)? → real edge.

Soft preferences belong in `impact`/`effort`, not edges. Over-edged graphs serialize work
that could run in parallel and starve the frontier down to one node — if the frontier is
persistently tiny, suspect invented edges before believing the product is that linear.

## Phases

Phases are gates, not labels. Do not open the next phase while the current one has
unfinished high-value nodes.

| Phase | Question it answers | Exit gate |
|---|---|---|
| `spike` | Should this exist, and can we build it? | Problem evidenced, riskiest assumption resolved, domain modelled |
| `mvp` | Does it deliver the core value to one user? | A stranger completes the core workflow and can pay |
| `launch` | Can strangers find, trust, and buy it? | Public surfaces live, e2e pass, monitoring on |
| `scale` | Does it compound without you? | Real customers, feedback loop feeding the graph |

`graph.py frontier --phase mvp` restricts the queue to a phase. Use it to hold the gate.

## Scoring

```
value = (impact + reach + confidence) / effort      each factor 1-5
```

- **impact** — how much it moves the goal in the graph header, not "how big is it".
- **reach** — fraction of users or of the core workflow it touches.
- **confidence** — how sure the estimate is. Low confidence on a big bet is a signal to
  spike it first, not to build it.
- **effort** — the divisor. Honest units; a 5 is "days", not "hard".

**Known bias:** cheap trivia outranks foundational work, because a 1-effort node with
average factors scores 12.0 while a 3-effort critical node scores ~4.3. The seeded graph
shows exactly this — `error-monitoring` outranks `auth`. Two corrections: score `impact`
against the *goal* (monitoring rarely moves "10 paying customers"), and let the critical
path override raw value when the two disagree. Value ranks the frontier; it does not
decide what matters.

Re-score after each phase gate. Estimates made before the spike are guesses.

## Frontier vs critical path

- **`frontier`** — everything unblocked right now, ranked. The build queue. Answers
  "what *can* I do?"
- **`critical`** — the longest dependency chain to the goal. Answers "what *must* happen
  eventually, in order?" Nodes on this path gate the ship date; nodes off it do not.

Read both each cycle. When a high-value frontier node is off the critical path and a
lower-value one is on it, prefer the critical-path node — otherwise the finish date does
not move no matter how much gets shipped. Shipping fast on non-critical work is the most
common way an autonomous loop feels productive and delivers nothing.

## Keeping the graph honest

- Run `graph.py validate` every cycle. It catches cycles, dangling `needs`, out-of-range
  factors, and nodes marked `done` whose dependencies are not — the integrity check that
  catches optimistic completion.
- Mark `done` only with `--evidence` describing a *verification*, not an assertion.
  "tests pass" is weak; "signup→checkout→webhook replay green in staging" is evidence.
- When reality contradicts the graph, edit the graph in the same cycle. A graph that
  lags reality stops being a decision tool within about three cycles.
- Never delete a node to make progress look better — set `status: dropped` with a note.
  Dropped nodes are how you remember what was deliberately not built.

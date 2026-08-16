---
name: saas-graph-loop
description: >
  Build a SaaS from zero to shipped by modelling it as three layered graphs (domain
  entities, a dependency DAG of capabilities, an agent orchestration topology) and
  running autonomous build cycles over the graph's unblocked frontier. The graph decides
  what to build next structurally instead of the loop guessing, which is what stops long
  autonomous runs from drifting. Composes with the growth-loop skill, replacing its
  backlog-replenish stage and handing off to it once the product reaches scale.
  Use when the user says "build me a SaaS", "zero to shipped", "/saas-graph-loop",
  "graph engineering", "what should I build next", asks to plan or sequence a new
  product, or wants an autonomous loop that builds a product rather than marketing it.
---

# SaaS graph-loop — structure decides, the loop executes

Autonomous build loops fail the same way: they run out of obvious work, start generating
their own tasks, and drift into polish while something structural stays unbuilt. The fix
is not a better prompt — it is to stop asking the model what to build next.

**Three graphs, one loop.** The domain graph defines what the product *is*. The build
graph derives what is *legal to build now*. The orchestration graph decides *how* that
work executes. The loop then does one thing: take the top unblocked node, build it, prove
it, mark it, repeat.

## Start here

```bash
S=~/.agents/skills/saas-graph-loop/scripts

python3 $S/seed_graph.py --product acme --goal "10 paying customers"   # 31-node skeleton
python3 $S/graph.py frontier                                            # what to build now
python3 $S/graph.py critical                                            # what gates the date
```

A freshly seeded graph has exactly **one** frontier node: `problem-evidence`. That is
deliberate — the structure forbids building before the problem is evidenced.

Full command reference: `python3 $S/graph.py --help`.

## The cycle

Run this loop. Each pass ships exactly one verified increment (or one disjoint batch).

1. **Read state** — `graph.py stats` and `graph.py validate`. **Stop on validation
   errors**; a graph with a cycle or a dangling dependency gives wrong answers, and every
   later step inherits them.
2. **Pick** — `graph.py frontier --phase <current>`. Take the top node. Cross-check
   against `graph.py critical`: if the top frontier node is off the critical path and a
   lower-value one is on it, prefer the critical-path node. Shipping fast on non-critical
   work is how a loop feels productive and moves no date.
3. **Build** — the single node, to its `title` as a finished condition. Idempotent and
   reversible.
4. **Verify** — a **separate checker with a default stance of REJECT**. A maker validating
   its own work is not verification. Risky nodes (auth, billing, permissions, money,
   access) get perspective-diverse checkers, not N identical ones.
5. **Mark** — on pass, `graph.py status <id> --set done --evidence "<what was actually
   verified>"`. The command prints newly unlocked nodes. On fail, leave it `todo` with the
   rejection in `notes` — it re-enters the frontier rather than vanishing.
6. **Log** — one run-log line, memory update, changelog. Report unlocked nodes and the new
   completion percentage; that is the compounding story.

Then evaluate the stop condition (below) before starting another pass.

## The three layers

Read the layer's reference when working in it — they are one level deep from here.

| Layer | What it decides | Reference |
|---|---|---|
| 1. Domain | Entities, ownership, permissions, billable unit | [references/domain-graph.md](references/domain-graph.md) |
| 2. Build | The dependency DAG, phases, scoring, frontier | [references/build-graph.md](references/build-graph.md) |
| 3. Orchestration | Fan-out topology, maker/checker, model tiering | [references/orchestration.md](references/orchestration.md) |

Layer 1 generates layer 2's early nodes (schema, permissions, core-crud all derive from
the domain model). Layer 3 only matters once the frontier holds several independent nodes.

Composing with the existing loop fleet — mode semantics, stage mapping, handoff:
[references/loop-integration.md](references/loop-integration.md).

## Phase gates

Phases are gates, not labels. Do not open the next while the current has unfinished
high-value nodes, and **never auto-advance a phase** — the next one is more expensive and
harder to reverse, so it is the user's call.

| Phase | Exit gate |
|---|---|
| `spike` | Problem evidenced, riskiest assumption resolved, domain modelled |
| `mvp` | A stranger completes the core workflow and can pay |
| `launch` | Public surfaces live, full e2e pass, monitoring on |
| `scale` | Real customers, feedback loop feeding the graph |

## Stop conditions

Stop and report; do not schedule another cycle when:

- **phase-complete** — no frontier nodes left in the current phase. Report the gate, ask
  before opening the next.
- **frontier-empty with unfinished nodes** — this is a **graph bug, not completion**. Run
  `validate` and `critical`, say which edges are wrong. Never report success here.
- **budget cap, kill switch, or max cycles** — as in growth-loop.

## Rules that keep this working

- **Never build what is not on the frontier.** If something feels urgent and is not on it,
  the graph is wrong — fix the graph in that cycle, then build. Bypassing the frontier once
  turns the graph into a stale document within about three cycles.
- **Edit the graph the moment reality contradicts it.** Discovered dependency, changed
  requirement, node that turned out to be two nodes — same cycle, before building.
- **`done` requires evidence of verification, not assertion.** "tests pass" is weak;
  "signup→checkout→webhook replay green in staging" is evidence.
- **Add nodes only from product reality**, never to fill an empty cycle. An empty frontier
  is information; padding it destroys the information.
- **Never delete a node to make progress look better** — `status: dropped` with a note.
- **Score `impact` against the goal in the graph header.** The scoring formula
  systematically overvalues cheap trivia (a 1-effort node scores ~12 against a 3-effort
  critical node's ~4.3); the seeded graph shows exactly this. Value ranks the frontier, it
  does not decide what matters — that is what `critical` is for.
- **Hard-denylist applies in every mode**: money, secrets, infra/DNS, live sends, public
  posts, destructive ops. Frontier position is a build decision, never a permission grant.
- **Confirm account / server / live-vs-dev** before any production push. Approval in one
  context does not carry to the next.
- **Do not invoke the Workflow tool** for fan-out unless the user explicitly asked for
  multi-agent orchestration. Sequential cycles retain all the graph's value.

## Scripts

| Script | Use |
|---|---|
| `scripts/seed_graph.py` | Bootstrap a 31-node greenfield skeleton. Seeded scores are generic defaults — re-score against the real product before trusting frontier order. |
| `scripts/graph.py` | The engine: `init`, `add`, `link`, `status`, `frontier`, `critical`, `validate`, `render`, `stats`. |

`graph.py render --mermaid` emits a diagram for changelogs and buyer-facing docs;
`--ascii` groups by layer for a quick terminal read.

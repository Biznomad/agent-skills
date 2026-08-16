# Composing with growth-loop and the rest of the loop fleet

`growth-loop` is the execution engine already in use across the client businesses. This
skill does not replace it — it replaces the part of it that guesses.

## Contents
- [The one substitution](#the-one-substitution)
- [Stage-by-stage mapping](#stage-by-stage-mapping)
- [Modes](#modes)
- [Stop conditions](#stop-conditions)
- [Handing off to growth-loop](#handing-off-to-growth-loop)
- [What to reuse verbatim](#what-to-reuse-verbatim)

## The one substitution

growth-loop's stage 2 is **Replenish** — audit the product, generate candidate tasks,
append to the backlog. That stage is where an autonomous loop drifts: candidates come from
whatever the model noticed that cycle, so priorities wobble and the loop can churn on
polish while something structural stays unbuilt.

Substitute the graph:

| growth-loop stage 2 | becomes |
|---|---|
| Audit product → generate candidates → append to backlog | `graph.py frontier --phase <current>` |

Everything else in growth-loop stays. The graph is a better backlog, not a different loop.

## Stage-by-stage mapping

| growth-loop stage | With the graph |
|---|---|
| 1. Read state | Read `saas-graph.json` + run-log + memory. `graph.py validate` and `stats` — refuse to proceed on validation errors. |
| 2. Replenish | Replaced by `frontier`. Add nodes only when the *product* revealed new structure (a discovered dependency, a customer requirement), never to fill an empty cycle. |
| 3. Score | Already on the nodes. Re-score at phase gates, not every cycle — churning scores each cycle reintroduces the drift the graph removes. |
| 4. Build | Top frontier node, cross-checked against `critical`. One node in single-stream modes; a disjoint batch in turbo. |
| 5. Verify | Unchanged: separate checker, default REJECT. On pass `graph.py status <id> --set done --evidence "..."`; on fail leave `todo` with notes. |
| 6. Log + ship | Unchanged, plus: report the unlocked nodes (`status` prints them) and the new completion percentage. That is the compounding story a changelog should tell. |

## Modes

growth-loop's four modes carry over with graph-specific meanings:

- **advisor** — build the graph and report the frontier and critical path. Builds nothing.
  The right first run on any new product.
- **copilot** (default) — build frontier nodes; outward-facing actions (deploy, public
  post, send, spend) wait for a human tap.
- **autonomous** — build and ship all but hard-denied nodes, gated by an independent
  checker.
- **turbo** — parallel disjoint batches with tiered models. See `orchestration.md`.

The **hard-denylist applies in every mode**: money, secrets, infra/DNS, live sends, public
posts, destructive operations. A node being on the frontier is never authorization to
cross that line — frontier position is a build decision, not a permission grant.

## Stop conditions

The graph gives a cleaner stop than "value-dry", and it composes with growth-loop's:

- **phase-complete** — no frontier nodes left in the current phase. Report the gate, ask
  whether to open the next. Do not auto-advance a phase; the gate exists because the next
  phase is more expensive and harder to reverse.
- **frontier-empty** — nothing unblocked anywhere. Either the product is done, or edges
  are wrong. Run `validate` and `critical` and report which.
- **budget cap / kill switch / max cycles** — unchanged from growth-loop.

An empty frontier with unfinished nodes is a *graph bug*, not completion. Say so plainly
rather than reporting success.

## Handing off to growth-loop

Once a product reaches `scale` phase with real customers, this skill's job is done. The
graph's remaining `scale` nodes become growth-loop's three value tracks:

| Graph layer | growth-loop track |
|---|---|
| `gtm` nodes | (a) growth engine |
| `build` nodes | (b) product/UX |
| reporting + evidence | (c) showcase reporting |

Write the `loop-config-<product>.md` growth-loop expects, seed its backlog from remaining
graph nodes, and hand over. Keep the graph file — it stays the structural record and is
what makes the asset legible to a buyer.

## What to reuse verbatim

Do not re-derive these; growth-loop already got them right:

- **Telegram changelog contract** — branded card + caption + `InlineKeyboardMarkup` with
  handler-backed buttons. Every button needs a real callback handler.
- **Deploy discipline** — write the patch locally, `scp` it, run with the remote
  interpreter. Never pipe code through `ssh '... python -c "..."'` or heredocs.
- **Memory discipline** — dated H2 at the top of `SESSION_STATE`, detail in the project
  file, absolute dates. Automated loops write to `SESSION_STATE-<business>.md` and promote
  only milestones to the shared file. **Never log a no-op cycle.**
- **Safety** — confirm account/server/live-vs-dev before any production push; approval in
  one context does not carry to the next.

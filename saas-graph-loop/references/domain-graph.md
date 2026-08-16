# Layer 1 — the domain graph

Entities and their relations. This layer is the product's spine: get it wrong and every
later layer inherits the error, because schema, authorization, API surface, and screens
are all derivable from it.

## Contents
- [Why this layer goes first](#why-this-layer-goes-first)
- [Modelling procedure](#modelling-procedure)
- [Notation](#notation)
- [What the graph generates](#what-the-graph-generates)
- [The tenancy decision](#the-tenancy-decision)
- [Smells](#smells)

## Why this layer goes first

A SaaS is a set of nouns a customer pays to manipulate. Naming them precisely early is
cheap; renaming `Project` to `Workspace` after 40 files reference it is not. The domain
graph is also the only artifact that makes the *authorization* question answerable — you
cannot state a permission rule without knowing which entity owns which.

Build this before `stack-decision`. The stack serves the model, not the reverse.

## Modelling procedure

1. **List the nouns from the customer's sentence.** "I want my *team* to track *deals*
   across *pipelines*." → Team, Deal, Pipeline. Use the customer's word, not a
   generic one — `Deal` beats `Item` forever.
2. **Draw ownership edges first.** Every entity answers: who owns this row? That chain
   terminates at the billable entity (usually Account/Org/Workspace). An entity with no
   ownership path to the billable root is either global config or a modelling mistake.
3. **Mark cardinality** on each edge (1:1, 1:N, M:N). M:N edges almost always become
   their own entity later with attributes on the join — anticipate it.
4. **Mark the lifecycle** of each entity: created by whom, mutated by whom, deleted or
   soft-deleted, and retained how long. This is where GDPR/deletion work gets discovered
   cheaply instead of at launch.
5. **State the permission rule per entity in one sentence.** "A member reads Deals in
   their own Pipelines; an admin reads all Deals in the Account." If a rule needs a
   paragraph, the model is wrong.
6. **Identify the billable unit.** Seats, records, usage events, or flat. This directly
   determines whether `usage-metering` is an MVP node or a scale node — a per-seat
   product can ship without metering; a usage-priced one cannot.

## Notation

Keep it in one fenced block in the product's planning doc. Mermaid is fine, but plain
text is faster to edit and diffs cleanly:

```
Account (billable root)
  ├─1:N─ User ──M:N── Role
  ├─1:N─ Pipeline
  │        └─1:N─ Deal ──1:N── Activity
  └─1:1─ Subscription

Deal.owner   -> User        (nullable; unassigned deals are legal)
Deal.deleted -> soft        (30d retention, then purge job)
perm(Deal)   : member reads own-pipeline deals; admin reads account-wide
billable     : per seat (User where status=active)
```

## What the graph generates

Once stable, the domain graph is not documentation — it is input. Derive, in order:

| From the model | Produce | Build-graph node |
|---|---|---|
| Entities + fields | schema + migrations | `schema` |
| Ownership edges | authorization predicates | `permissions` |
| Entity list | CRUD routes + validators | `core-crud` |
| The customer's verb | the one workflow that matters | `core-workflow` |
| Billable unit | plans, limits, checkout | `billing` |
| Lifecycle rules | retention jobs, soft-delete, export | `legal`, `backups` |

Regenerate rather than hand-patch when the model changes. If the model changed and the
schema was hand-patched to match, the next regeneration silently reverts it.

## The tenancy decision

Decide once, at this layer, and record the reason: shared tables with an
`account_id` predicate (default — simplest, cheapest, fine to very large scale) versus
schema-per-tenant or database-per-tenant (only when a customer contract or regulator
demands physical isolation).

This is the single hardest thing to change later. Every query, index, and migration
inherits it. Write the choice and its justification into the graph node's `notes`.

## Smells

- **An entity with no owner.** Either it is global config, or the ownership edge is
  missing and authorization will be written ad hoc per route.
- **A generic name** (`Item`, `Record`, `Thing`). Means the domain is not understood yet;
  keep interviewing.
- **Permission rules that reference more than two hops.** "A user can see a Deal if their
  Team is in a Group that shares a Pipeline…" — flatten with a denormalized column or an
  explicit membership entity, or authorization becomes an N+1 query per page.
- **More than ~9 entities before first revenue.** The MVP is modelling a product nobody
  has paid for yet. Cut to the ones the core workflow touches.

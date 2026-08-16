---
name: seo-geo-aeo-action-plan
description: Use after completing an SEO/GEO/AEO audit wave to classify every finding into a phased action plan with AI-doable vs OWNER tags, estimate score impact, and write the ACTION-PLAN.md artifact that gates fix execution.
---

# SEO/GEO/AEO — Action Plan

Classify every finding from `findings/*.md` into the Phase 0–3 taxonomy. Write `ACTION-PLAN.md` in the audit dir. This document gates all fix execution — the fix executor reads it.

## Phase Taxonomy

| Phase | Timeline | Focus |
|---|---|---|
| Phase 0 | Same day | Trust & safety — fake/placeholder content, fabricated schema, conversion blockers |
| Phase 1 | Week 1 | Identity unification — NAP consistency, single-entity schema, llms.txt, security headers |
| Phase 2 | Weeks 2–3 | Money pages + speed — rebuild primary pages, cost cluster, dedupe doorways, perf |
| Phase 3 | Month 2 | Authority — reviews engine, GBP appeal, citation wiring, local links, measurement loop |

## Tags (required on every item)

- **AI-doable** — executable from this environment with backups + validation
- **OWNER** — requires client decision, credentials, physical access, or login-gated platform

**Never silently convert an OWNER item to AI-doable** by routing around an access gate. Bot-blocked platforms (Yelp/DataDome, Google login walls) stay OWNER with a handoff card.

## ACTION-PLAN.md Structure

```
# Action Plan — <Business> — <Date>
## Score: <weighted-score>/100 (<grade-band>)

## Phase 0 — Same Day
- [ ] [AI-doable] <finding>: <one-line why it matters>
- [ ] [OWNER] <finding>: <handoff card with exact steps>

## Phase 1 — Week 1
...

## Phase 2 — Weeks 2–3
...

## Phase 3 — Month 2
...

## OPEN backlog
<!-- Updated every session — done items get date + backup stamp -->
```

## Scoring discipline

- Include score impact estimate per item (e.g. "+3–5 pts technical if redirects fixed")
- Phase 0 items are highest priority regardless of estimated score delta
- OWNER items get a handoff card: exact steps, prefilled canonical NAP, reply keywords so the owner can confirm from their phone

## Cross-reference

- Preceded by: `seo-geo-aeo-audit-wave`
- Feeds into: `seo-geo-aeo-qa-gate` (Gate 1 reads this plan)
- Full taxonomy: `references/action_plan_taxonomy.md` in `seo-geo-aeo-engine` skill

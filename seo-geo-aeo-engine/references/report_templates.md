# Report Templates & Artifact Layout

## Audit directory layout

```
<client-project-dir>/<domain>-audit/
├── FULL-AUDIT-REPORT.md     # executive report — score table + summaries
├── ACTION-PLAN.md           # phased plan + OPEN backlog (living document)
├── audit-data.json          # machine-readable scores/findings, snapshot history
├── preflight.txt            # site_preflight.sh output
├── findings/
│   ├── technical.md
│   ├── schema.md
│   ├── geo-aeo.md
│   ├── content.md
│   ├── performance.md
│   ├── local.md             # or ecommerce.md per profile
│   ├── sxo.md
│   ├── visual.md
│   └── sitemap.md
├── screenshots/             # visual-audit captures (element/viewport, not full-page)
└── CITATIONS-PACK.md        # when citations work is in scope
```

## FULL-AUDIT-REPORT.md skeleton

```markdown
# SEO/GEO/AEO Audit — <domain>
Date: <ISO date> · Profile: <local-service|ecommerce> · Pages crawled: <n>

## Health Score: NN/100 (<band>)
| Dimension | Score | Weight | Top issue |
|-----------|------:|-------:|-----------|
| ...       |       |        |           |

## Critical findings (fix same day)
1. <finding> — <impact> — <phase/tag>

## Dimension summaries
### <Dimension> — NN/100
<One paragraph: state, top issues, link to findings/<dimension>.md>

## What's already strong
<Keep this honest — it calibrates the owner's trust in the criticism>
```

## ACTION-PLAN.md skeleton

```markdown
# Action Plan — <domain>
Prioritized. "AI-doable" = executable here with backups; "OWNER" = needs client
decision/access.

## Phase 0 — Same day (trust & safety)
1. **<item>** — <why>. <AI-doable|OWNER>.

## Phase 1 — Week 1 (identity unification)
## Phase 2 — Weeks 2–3 (money pages + speed)
## Phase 3 — Month 2 (authority)

## OPEN backlog
- [ ] <item> (<phase>, <tag>)
- [x] <item> — DONE <date>, backups <stamp>
```

## audit-data.json schema

```json
{
  "domain": "example.com",
  "profile": "local-service",
  "snapshots": [
    {
      "date": "2026-07-04",
      "health_score": 59,
      "dimensions": {
        "technical": {"score": 74, "critical": [], "high": ["..."], "medium": ["..."]},
        "schema":    {"score": 60, "critical": ["..."], "high": [], "medium": []}
      }
    }
  ],
  "owner_directives": ["never degrade hero animation"],
  "canonical_nap": {"name": "", "address": "", "phone": ""}
}
```

Re-audits APPEND a snapshot; never overwrite history.

## Telegram completion card (cron/loop runs)

Message: score + delta, top finding, artifact path. MUST attach inline keyboard buttons —
standard set `[💾 Save] [✅ Acknowledge] [⏭ Skip] [🔍 Investigate]`, or decision buttons
when a fix batch awaits approval (`[🟢 Apply] [🟡 Defer] [🔴 Block]`). Every button needs a
callback handler; if no handler exists on that bot, say so and fall back to reply keywords.

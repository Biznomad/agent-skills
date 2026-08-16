---
name: seo-geo-aeo-engine
description: End-to-end SEO/GEO/AEO engine for any portfolio business or client site. Runs a parallel multi-specialist audit (technical, schema, GEO/AEO, local, content, performance, SXO, visual, sitemap + conditional specialists), computes a weighted health score, writes a standard audit artifact set, generates a phased action plan (Phase 0 trust through Phase 3 authority), and executes approved fixes with per-file backups and validation. This skill should be used when the user asks to "run an SEO audit", "audit a site", "run the SEO/GEO/AEO engine for a business", "re-audit a domain", "check AI visibility or citability", or requests GEO/AEO work (llms.txt, entity schema, AI-citable pages, citations) on any business or client site.
argument-hint: [business-or-domain] [audit|fix|re-audit|status]
---

# SEO/GEO/AEO Engine

Audit → score → plan → fix → re-audit loop for search visibility across three surfaces:
**SEO** (classic organic), **GEO** (generative engine optimization — being cited by
ChatGPT/Perplexity/Claude/AI Overviews), **AEO** (answer engine optimization — direct-answer
content, FAQ/entity schema). Battle-tested on a full 62-page local-service audit + same-week
fix cycle (baseline health 59/100) with concrete, validated live fixes.

## Modes

| Mode | Trigger | What happens |
|------|---------|--------------|
| `audit` | "audit <business>", first run | Full parallel specialist audit → score → report → action plan. No changes to the site. |
| `fix` | "execute the plan", "fix phase 0/1" | Gated execution of AI-doable action-plan items with backups + validation. |
| `re-audit` | "re-audit", prior audit dir exists | Re-run audit, compute score deltas vs baseline, refresh backlog. |
| `status` | "pull up / where is <business> SEO" | Read existing artifacts + memory; report state and open backlog. No agents spawned. |

## Step 0 — Resolve the target business (ALWAYS FIRST)

1. Load `references/business_registry.md`. Match the user's business/domain to a registry row.
2. Read that business's own project `CLAUDE.md` and memory files — the registry is a pointer
   map, not the authority. Per-business guardrails there OVERRIDE anything in this skill.
3. If the business is not in the registry, collect: domain, platform (static/nginx, Shopify,
   Netlify, app), project directory, server/deploy access, Telegram channel, canonical NAP,
   owner directives. Add a row to the registry before proceeding.
4. Confirm the target with the user before any mode that changes the site: which business,
   which environment (live server vs dev theme vs staging). Never assume.

## Autonomous Loop (Sub-Skills)

This orchestrator delegates each stage to a dedicated sub-skill. Each sub-skill is
independently usable and cross-tool compatible (Claude Code, Codex, OpenCode, Gemini CLI).

```
seo-geo-aeo-preflight        → Step 1: HTTP, SSL, AI crawlers, llms.txt, sitemap
seo-geo-aeo-audit-wave       → Step 2: Parallel specialist agents + health score
seo-geo-aeo-action-plan      → Step 3–4: Phase 0–3 classification + ACTION-PLAN.md
seo-geo-aeo-qa-gate          → Gate 1 (pre-approval) + Gate 2 (post-fix) + auto-rollback
seo-geo-aeo-hitl-approval    → Human approval via Telegram inline keyboard / CLI
seo-geo-aeo-fix-executor     → Step 5: Surgical fix execution with timestamped backups
seo-geo-aeo-report-and-submit → Step 6–7: Delta report, GSC/IndexNow, memory, Telegram card
```

**Execution order:**
```
preflight → audit-wave → action-plan → qa-gate(1) → hitl-approval → fix-executor → qa-gate(2) → report-and-submit → [loop]
```

See `docs/AUTONOMOUS-LOOP-GRAPH.md` for the full gate flow with circuit breaker rules.

## Re-audit rules

- Compare dimension scores against the baseline in `audit-data.json`; report deltas.
- Judge performance by real-browser/CrUX FIELD data, never lab Lighthouse alone — lab CPU
  throttling amplifies intentional entrance animations into fake LCP regressions.
- Re-check Phase 0 items every time (placeholder content regrows; new pages ship
  untracked). Doorway similarity drifts as templates get reused — re-run
  `scripts/page_similarity.py` on page clusters.

## References

| File | Load when |
|------|-----------|
| `references/business_registry.md` | Always, Step 0 |
| `references/scoring_model.md` | Scoring / fallback specialist spec |
| `references/action_plan_taxonomy.md` | Building the action plan |
| `references/fix_execution_rules.md` | Before ANY site change |
| `references/geo_aeo_playbook.md` | llms.txt, entity schema, AI-citable pages |
| `references/dedupe_local_depth.md` | City/doorway page deduplication |
| `references/report_templates.md` | Writing artifacts |
| `docs/AUTONOMOUS-LOOP-GRAPH.md` | Autonomous loop graph, QA gates, HITL, rollback |

## Sub-Skill Skills

| Skill | Purpose |
|-------|---------|
| `seo-geo-aeo-preflight` | Site preflight checks |
| `seo-geo-aeo-audit-wave` | Parallel specialist audit + scoring |
| `seo-geo-aeo-action-plan` | Phase 0–3 classification + ACTION-PLAN.md |
| `seo-geo-aeo-qa-gate` | QA Gate 1 + Gate 2 + auto-rollback + circuit breaker |
| `seo-geo-aeo-hitl-approval` | Human approval gate (Telegram / CLI) |
| `seo-geo-aeo-fix-executor` | Gated surgical fix execution with backups |
| `seo-geo-aeo-report-and-submit` | Delta report, indexing pings, Telegram summary card |


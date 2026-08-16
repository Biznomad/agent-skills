# seo-geo-aeo-engine

Claude Code skill: end-to-end SEO/GEO/AEO engine for every portfolio business and client
site. Audit → weighted health score → phased action plan → gated fix execution →
re-audit deltas.

Extracted from the Two & Through full-site audit + fix cycle (2026-07-04): 9 parallel
specialist agents, 62 pages, baseline 59/100, same-week live fixes (fake-review removal,
single-entity schema, llms.txt, DNI-safe phone unification, doorway de-dupe, AI-citable
cost cluster).

## What's inside

```
SKILL.md                              # orchestrator workflow (modes: audit/fix/re-audit/status)
references/
  business_registry.md                # fleet pointer map + per-business guardrails
  scoring_model.md                    # dimensions, weights, grade bands
  action_plan_taxonomy.md             # Phase 0-3 + AI-doable vs OWNER tagging
  fix_execution_rules.md              # backups, validation, platform guardrails
  geo_aeo_playbook.md                 # llms.txt, entity schema, AI-citable pages, citations
  dedupe_local_depth.md               # doorway-page rescue methodology
  report_templates.md                 # artifact layout + skeletons
scripts/
  site_preflight.sh                   # redirects, headers, AI-bot access, llms.txt, sitemap, MX
  health_score.py                     # weighted score + snapshot deltas from audit-data.json
  page_similarity.py                  # pairwise seq + shingle similarity (doorway detection)
```

## Install

Clone into the Claude Code personal skills directory:

```bash
git clone git@github.com:Biznomad/seo-geo-aeo-engine.git ~/.claude/skills/seo-geo-aeo-engine
```

Invoke with `/seo-geo-aeo-engine <business-or-domain> [audit|fix|re-audit|status]` or just
ask for an SEO audit of any registered business.

## Notes

- Private/internal: the business registry contains portfolio-specific pointers (no secrets —
  credential paths only).
- Scripts are stdlib-only (Python 3, bash + curl/dig).

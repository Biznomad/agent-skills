---
name: seo-geo-aeo-preflight
description: Use when starting any SEO/GEO/AEO engine loop cycle, before running audit specialists, when a new business domain is being onboarded, or when checking AI crawler accessibility, robots.txt config, llms.txt presence, SSL, and HTTP redirect health for any portfolio or client site.
---

# SEO/GEO/AEO — Preflight

Run `scripts/site_preflight.sh <domain>` (located in `~/.agents/skills/seo-geo-aeo-engine/scripts/`) before ANY audit wave. Save output to `<audit-dir>/preflight.txt`.

## What it checks

| Check | Pass Criteria |
|---|---|
| HTTP → HTTPS redirect | 301 from http:// to https:// |
| www → apex redirect | Single canonical host |
| SSL validity | No cert errors, expiry > 30 days |
| Security headers | HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy present |
| robots.txt AI crawlers | GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended all allowed |
| llms.txt | File present at `/llms.txt`; score 0 if absent |
| Sitemap | URL resolves; URL count recorded |
| Advertised emails | MX records exist for every email shown on the page |

## Outputs

- `preflight.txt` — raw output saved to audit dir
- A pass/fail summary card posted to the loop's continuation context

## Fail behaviour

If ANY critical check fails (SSL expired, all AI crawlers blocked, homepage returns non-200), **halt the audit wave** and alert owner via Telegram before continuing. Soft failures (llms.txt absent, missing security header) are logged as findings but do not halt.

## Cross-reference

- Called by: `seo-geo-aeo-engine` (Step 1)
- Feeds into: `seo-geo-aeo-audit-wave`
- Business context required: load `references/business_registry.md` from `seo-geo-aeo-engine` skill before running

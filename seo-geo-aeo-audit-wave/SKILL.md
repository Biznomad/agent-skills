---
name: seo-geo-aeo-audit-wave
description: Use when running the parallel specialist audit for a business or client domain — spawning SEO, GEO, AEO, local, content, performance, SXO, visual, and sitemap agents concurrently, then merging dimension scores into a weighted health score JSON artifact.
---

# SEO/GEO/AEO — Audit Wave

Spawn ALL applicable specialists in ONE message so they run concurrently. Wait for all to return before proceeding to scoring.

## Core Specialists (always)

| Skill / Agent | Dimension |
|---|---|
| `seo-technical` | Crawl, redirects, security headers, canonicals, mobile |
| `seo-schema` | JSON-LD validity, entity architecture, FAQPage/Service coverage |
| `seo-geo` | AI crawler access, llms.txt quality, passage-level citability |
| `seo-local` | GBP status, NAP consistency, citation coverage |
| `seo-content` | Depth, duplication, E-E-A-T, intent gaps |
| `seo-performance` | CrUX field data first, lab second; LCP/INP/CLS |
| `seo-sxo` | SERP intent match, persona walkthrough, CTA clarity |
| `seo-visual` | Real-browser rendering, overlap bugs, tap targets |
| `seo-sitemap` | XML validity, lastmod, orphans, noindex discipline |

## Conditional Specialists

| Skill / Agent | Condition |
|---|---|
| `seo-ecommerce` | Platform is Shopify or has a product catalog |
| `seo-maps` | Brick-and-mortar or service-area business |
| `seo-drift` | A baseline `audit-data.json` snapshot already exists |
| `seo-google` | GSC/CrUX API token on file in registry |
| `seo-backlinks` | Authority deep-dive explicitly requested |

## Required Output Per Specialist

Each agent MUST return:
1. Dimension score 0–100 (integer)
2. Findings written to `findings/<dimension>.md` in the audit dir
3. JSON fragment: `{"dimension": "<name>", "score": <int>, "critical": [], "high": [], "medium": []}`

If a named specialist skill is unavailable, spawn a general-purpose agent with the coverage spec from `references/scoring_model.md`.

## Scoring

After all specialists return:
1. Merge all JSON fragments into `audit-data.json`
2. Run `scripts/health_score.py audit-data.json --profile <local-service|ecommerce>`
3. Record baseline date; never overwrite prior snapshots — append dated entries

## Scoring Discipline

- Score what IS, not what's planned — staged-but-unpublished fixes don't move the score
- A CRITICAL trust/legal finding (fake reviews, fabricated addresses) caps that dimension at 40
- Keep the SAME profile (`local-service` vs `ecommerce`) across all re-audits of a business

## Cross-reference

- Preceded by: `seo-geo-aeo-preflight`
- Feeds into: `seo-geo-aeo-action-plan`
- Weights/grade bands: `references/scoring_model.md` in `seo-geo-aeo-engine` skill

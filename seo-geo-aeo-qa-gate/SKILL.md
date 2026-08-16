---
name: seo-geo-aeo-qa-gate
description: Use before and after fix execution in the SEO/GEO/AEO engine loop — runs pre-execution non-degradation checks (Gate 1) and post-execution schema, HTTP, and tracking validation (Gate 2) with automatic rollback from timestamped backups on any failure. Use when you need quality assurance guardrails around site changes.
---

# SEO/GEO/AEO — QA Gate

Two mandatory gates bracket every fix batch. Neither is optional.

## Gate 1 — Pre-Execution (Before Human Approval)

Run BEFORE presenting the fix batch to the human for approval.

| Check | Tool / Method | Fail Action |
|---|---|---|
| Page similarity (doorway detection) | `scripts/page_similarity.py` — any cluster > 0.85 cosine score | Block fix, log finding, flag for dedupe |
| Owner directives check | Load registry row + business memory — scan for "never touch X" patterns | Remove violating items from batch |
| Syntax pre-check | JSON-LD: validate against schema.org; Liquid: `shopify theme check`; nginx: `nginx -t` | Block fix, log parse error |
| Proposed scope sanity | No fix touches files outside the declared audit dir + web root | Block entire batch if scope exceeded |

If Gate 1 passes → hand off to `seo-geo-aeo-hitl-approval`.
If Gate 1 fails → log failures, alert owner, do NOT present for approval.

## Gate 2 — Post-Execution (After Each Fix)

Run AFTER every individual fix. ALL checks must pass before moving to the next fix.

| Check | Pass Criteria |
|---|---|
| HTTP status | Page returns 200; no unintended redirect chains |
| JSON-LD schema | Parses without errors (local validator or Google Rich Results API) |
| Tracking & DNI | GTM fires; DNI script line present and unmodified; no pixel removed |
| Visual spot-check | Real-browser screenshot shows no broken layout, no overlapping elements |

## Auto-Rollback Protocol

1. On ANY Gate 2 failure → immediately restore from `.bak-pre-<slug>-<YYYYMMDDHHMMSS>`
2. Verify rollback restored the page (re-run Gate 2 checks)
3. Log failure with exact check that failed + timestamp
4. Alert owner via Telegram with inline keyboard: `[Rollback Confirmed]` `[Escalate to Review]`

## Circuit Breaker Rules

- **2 consecutive rollbacks** → freeze the engine entirely; require manual human unlock
- **Tracking code altered/removed** → emergency rollback + immediate Telegram alert regardless of other checks
- **Shopify live theme touched** → rollback + alert even if changes looked correct

## Cross-reference

- Gate 1 feeds into: `seo-geo-aeo-hitl-approval`
- Gate 2 follows: `seo-geo-aeo-fix-executor`
- Rollback backups written by: `seo-geo-aeo-fix-executor`
- Fix guardrails: `references/fix_execution_rules.md` in `seo-geo-aeo-engine` skill

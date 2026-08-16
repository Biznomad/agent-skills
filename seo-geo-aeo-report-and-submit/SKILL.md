---
name: seo-geo-aeo-report-and-submit
description: Use after SEO/GEO/AEO fixes have passed QA Gate 2 to generate a delta report with score changes, resubmit the sitemap via GSC API, ping IndexNow for Bing/Copilot discovery, refresh llms.txt if facts changed, update business memory and backlog, and post a completion summary card to the business Telegram channel.
---

# SEO/GEO/AEO — Report & Submit

Final stage of every loop cycle. Runs after all Gate 2 checks pass.

## 1. Delta Report

Compare the new `audit-data.json` snapshot against the previous baseline:
- Per-dimension score deltas (e.g. `schema: 62 → 74 (+12)`)
- Weighted health score delta
- Items fixed this cycle (with backup stamp timestamps)
- Items remaining in backlog by phase

Write `DELTA-REPORT-<YYYYMMDD>.md` to the audit dir.

## 2. Sitemap Resubmit

After any content or schema change:
1. Regenerate `sitemap.xml` with updated `<lastmod>` timestamps
2. If GSC API token is on file (registry row): submit sitemap via API
3. Per-URL "Request Indexing" has NO public API — leave as OWNER item in backlog

## 3. IndexNow Ping

If a standing IndexNow key file exists in the web root (registry row):
- POST the list of changed URLs to IndexNow API
- Confirms instant Bing/Copilot discovery
- Log the submitted URL list and HTTP response code in the delta report

## 4. llms.txt Refresh

If any of the following changed this cycle: services, pricing, phone, address, hours, citation profile URLs:
- Update `llms.txt` to reflect canonical current facts
- Re-submit to IndexNow
- Version-stamp the change in the file's header comment

## 5. Business Memory Update

1. Append a dated entry to the business memory file: fixes applied, new score, open backlog items
2. Update the business's row in `references/business_registry.md` if platform/deploy details changed
3. Append to shared session state (`SESSION_STATE.md`) per workspace conventions

## 6. Telegram Summary Card

Send to the business's registered Telegram channel. Must use inline keyboard buttons — NEVER plain text.

```
✅ SEO/GEO/AEO Engine — Cycle Complete
📍 <Business> | <domain>
📅 <date>

📊 Health Score: <old> → <new>/100 (+<delta>)

🔧 Fixed this cycle: <n> items
  ✓ <item 1>
  ✓ <item 2>

📋 Open Backlog: <n> items across Phase 1–3
⚠️  Owner Actions Required: <n> items

🔄 Next cycle: <scheduled-date>
```

Inline keyboard:
```
[📋 View Full Report]   [📝 View Open Backlog]   [🔁 Trigger Re-audit Now]
```

## 7. Sleep / Schedule Next Cycle

- Log the next scheduled trigger time
- If running under a cron: no action needed — the scheduler handles the next wake
- If running manually: suggest the next trigger to the user based on the cycle interval

## Cross-reference

- Preceded by: `seo-geo-aeo-fix-executor` + `seo-geo-aeo-qa-gate` (Gate 2)
- Loop restarts at: `seo-geo-aeo-preflight` on next trigger
- GEO/AEO measurement: track AI referrers (perplexity.ai, chatgpt.com, copilot, gemini) in analytics

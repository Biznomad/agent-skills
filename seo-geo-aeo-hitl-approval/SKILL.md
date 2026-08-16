---
name: seo-geo-aeo-hitl-approval
description: Use when the SEO/GEO/AEO engine has passed QA Gate 1 and needs human approval before executing any site changes — sends an approval card via Telegram inline keyboard or CLI prompt with proposed fixes, risk level, and projected score impact. Use when gating autonomous agent actions on human sign-off.
---

# SEO/GEO/AEO — Human-in-the-Loop Approval Gate

Always present for approval BEFORE executing any fix. Never auto-approve. Gate 1 (`seo-geo-aeo-qa-gate`) must pass first.

## Approval Card Format

Send one card per fix batch. Must include ALL of the following:

```
🔍 SEO/GEO/AEO Engine — Approval Required
📍 Business: <name> | <domain>
📅 Cycle: <date>

📊 Current Health Score: <n>/100 (<grade>)
📈 Projected Score After Fixes: <n+delta>/100

🔧 Fix Batch — Phase <X>
  1. [AI-doable] <item> | Risk: LOW/MED/HIGH | Est. +<n> pts
  2. [AI-doable] <item> | Risk: LOW/MED/HIGH | Est. +<n> pts
  ...

⚠️  OWNER Items (not included in this batch — your action required):
  - <item>: <handoff steps>

💾 Backup: Timestamped .bak files will be created before each change.
🔄 Rollback: Automatic on any post-fix check failure.
```

## Delivery Channels (in priority order)

1. **Telegram** — Send to the business's registered Telegram channel (from `references/business_registry.md`). Use inline keyboard buttons — NEVER plain text buttons.
2. **CLI prompt** — Fall back to a numbered list if Telegram is unavailable for this business.

## Telegram Inline Keyboard

```
[✅ Approve Phase 0 Only]   [✅ Approve Full Batch]   [❌ Reject / Modify]
```

- `Approve Phase 0 Only` → execute only Phase 0 (trust & safety) items
- `Approve Full Batch` → execute all AI-doable items in the batch
- `Reject / Modify` → store the rejection + any user feedback in business memory; exit this loop cycle

## Waiting Behaviour

- Wait up to **24 hours** for a response before timing out
- On timeout: log as "Pending — no human response" and skip to next scheduled cycle
- Do NOT proceed with execution if no explicit approval is received

## After Rejection

1. Store rejection reason in business memory file
2. Append OWNER feedback as comments in `ACTION-PLAN.md` backlog
3. Exit fix execution for this cycle — re-audit on next scheduled trigger

## Cross-reference

- Preceded by: `seo-geo-aeo-qa-gate` (Gate 1 must pass)
- Feeds into: `seo-geo-aeo-fix-executor` (on approval)
- Business Telegram channel: `references/business_registry.md` in `seo-geo-aeo-engine` skill

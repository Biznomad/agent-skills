---
name: seo-geo-aeo-fix-executor
description: Use after human approval is received in the SEO/GEO/AEO engine loop to surgically execute approved fix batches with timestamped backups before every file edit, followed by QA Gate 2 validation. Use when applying schema changes, content edits, configuration fixes, or GEO/AEO build work to any client or portfolio site.
---

# SEO/GEO/AEO — Fix Executor

Load `references/fix_execution_rules.md` from the `seo-geo-aeo-engine` skill BEFORE touching anything. These are non-negotiable.

## Pre-Fix Protocol (every file, every time)

1. Write timestamped backup: `.bak-pre-<slug>-<YYYYMMDDHHMMSS>` alongside the target file
2. Verify the backup was written and is byte-identical to the original
3. Keep backup files OUT of live config globs (e.g. nginx `include sites-enabled/*` will load `.bak` files — store in a `_backups/` subdir instead)
4. Only then apply the fix

## Fix Execution Order

Execute in Phase order within the approved batch:
- Phase 0 items first (trust & safety — always lowest risk, highest urgency)
- Phase 1 next
- Phase 2 last

After EACH fix → call `seo-geo-aeo-qa-gate` Gate 2. Do NOT batch multiple fixes before validating.

## Platform-Specific Rules

| Platform | Rule |
|---|---|
| **Shopify** | Edit unpublished/dev theme ONLY. Live theme publish requires explicit human confirmation AFTER a Gate 2 pass. |
| **nginx** | Run `nginx -t` before `nginx -s reload`. Never reload without a clean config test. |
| **Static HTML / Netlify** | Deploy to preview/staging URL first; Gate 2 checks run against preview. Production deploy = human approval step. |
| **GHL Funnels** | Changes via API or builder — no direct DB edits. Always preview before activating. |

## GEO/AEO Build Work

For llms.txt, entity schema, and AI-citable page builds, follow `references/geo_aeo_playbook.md`. Key rules:
- Publish llms.txt ONLY after NAP/identity unification is complete
- Per-page `LocalBusiness` nodes with invented local addresses → REMOVE, replace with `Service` + `provider: {"@id": ".../#business"}"`
- Every new page must inherit tracking/DNI chrome from an existing page, not be built from scratch

## Doorway/City Page Deduplication

Follow `references/dedupe_local_depth.md`. Run `scripts/page_similarity.py` BEFORE and AFTER on affected clusters to confirm similarity score dropped below threshold.

## On Any Gate 2 Failure

`seo-geo-aeo-qa-gate` will trigger rollback. The fix executor's job:
1. Confirm rollback completed (re-verify the `.bak-pre-` file was restored)
2. Log the failure with exact diff that caused it
3. Mark the item as BLOCKED in `ACTION-PLAN.md` backlog
4. Do NOT attempt the same fix again in this cycle — leave for human review

## Cross-reference

- Preceded by: `seo-geo-aeo-hitl-approval`
- QA validation by: `seo-geo-aeo-qa-gate` (Gate 2 after each fix)
- Feeds into: `seo-geo-aeo-report-and-submit`
- Platform guardrails: `references/fix_execution_rules.md` in `seo-geo-aeo-engine` skill

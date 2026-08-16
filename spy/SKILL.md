---
name: spy
description: >
  Pull every competitor's active Meta ads with hooks, CTAs, offers, format,
  and how long each has been running. Saves a ranked swipe file. Replaces
  manually scrolling Meta Ads Library. Alias for /ads-competitor scoped to
  Meta. Use when user says "/spy", "spy on competitors", "competitor ad
  swipe", "what ads are competitors running", "pull competitor ads", or
  is starting Phase 1 of /biznomad-meta-ads-team.
---

# /spy — Competitor Meta Ads Swipe

Thin alias that routes the request to the more-capable installed
`/ads-competitor` skill, scoped to Meta only, with output landing in the
standard Biznomad workflow path.

## What this skill does

Pulls every actively-running Meta ad from 3–5 named competitors:
- Verbatim hooks (first line / headline)
- CTAs
- Offers (lead promo, bundle, BOGO, discount %)
- Creative format (static / video / carousel)
- Days-running on standout ads (>30 days = likely winners)
- Pricing snapshot from competitor website

## Meta API access gate

Before debugging query parameters or rewriting the scraper, verify the token can call Meta's Ads Library endpoint. A token that works for `/me`, `/me/adaccounts`, or normal Marketing API reads may still fail on `/ads_archive` unless the app has Ads Library API access. Use `scripts/check_meta_ads_library_access.py` against the candidate `.env` files and inspect specifically for `/ads_archive` success.

If Meta returns code `10` / subcode `2332002` with "Application does not have permission for this action," the fix is app authorization at `https://www.facebook.com/ads/library/api`, not a code-level scraper fix. See `references/meta-ads-library-api-access.md` for the exact diagnostic pattern and token-search hygiene.

## Critical Meta API pitfall

Before rewriting scraper logic, verify the app/token actually has Meta Ads Library API access. A normal Meta Marketing API token can be present and still fail on `/ads_archive` with OAuthException code 10 / subcode 2332002: "Application does not have permission for this action" and Meta's instruction to use `facebook.com/ads/library/api`. If that appears, the fix is app authorization/app review for Ads Library API, not changing fields, keywords, ranking code, or rotating to another token from the same app.

Important distinction: `ads_read`, `ads_management`, `business_management`, Page scopes, and Instagram scopes are Marketing API permissions; Ads Library API is a separate app-level feature. If the user points to an app like SMMA Genie and says it already has the scopes, validate the app identity and granted scopes, then explain that those scopes still do not satisfy `/ads_archive` until the app has Ads Library API access. See `references/meta-ads-library-api-access.md` for the diagnostic pattern, SMMA Genie example, and safe token-audit workflow.

## Inputs needed (ask the user)

- 3–5 competitor brand names or Facebook page URLs
- Geo scope (default: US)
- Client name (if running inside `/biznomad-meta-ads-team` — sets output path)

## How to invoke

1. Invoke `/ads-competitor` with `platform: meta` and the named competitors.
2. If running inside `/biznomad-meta-ads-team`, save output to
   `./meta-ads-team/01-spy/swipe-file.md`. Otherwise prompt for output location.
3. Cross-reference any prior swipe file in the same directory for delta
   ("what changed since last scan").

## Inspired by

cindie.zhu's "Meta x Codex skills" reel — the `/spy` command in her
5-skill stack. Built as an alias since her version is gated behind her
DM install guide. See [[reference_biznomad_meta_ads_team_skill]] for the
full orchestrator that chains this with the other 4.

## Related

- `/ads-competitor` — the underlying skill
- `/competitive-ads-extractor` — alternate scraper (ComposioHQ)
- `/biznomad-meta-ads-team` — runs this as Phase 1 automatically
- `[[feedback_security_scan]]` — already satisfied for the underlying skill

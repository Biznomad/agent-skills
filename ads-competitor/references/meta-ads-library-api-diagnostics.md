# Meta Ads Library API diagnostics

Use this when a competitor-ad spy script has a Meta token but `/ads_archive` returns HTTP 400/401/403.

## Key distinction

Meta Marketing API access and ad-account permissions are not enough for public competitor ad research. The endpoint:

`https://graph.facebook.com/vXX.X/ads_archive`

requires Ads Library API access for the app/token. If the token is present but the app lacks this access, Meta returns an OAuth permission error even when the token works for other Meta Ads calls.

## Canonical failure observed

- Endpoint: `/v21.0/ads_archive`
- Query type: active `ALL` ads, US reached country, supplement keywords
- Token: present
- Response: HTTP 400
- Error: OAuthException code 10, subcode 2332002
- Message: `Application does not have permission for this action`
- User message: `To access the API, you'll need to follow the steps at facebook.com/ads/library/api.`

## Diagnostic sequence

1. Confirm token is present without printing it: log boolean + length only.
2. Make the smallest possible `/ads_archive` request with safe fields:
   - `id,page_id,page_name,ad_delivery_start_time`
3. If the same permission error appears, stop debugging fields/syntax. The blocker is app permission.
4. Tell the user to enable/apply for Ads Library API access at `facebook.com/ads/library/api` for the app behind the token.
5. After approval, rerun the scraper and only then debug field names, paging, ranking, or recreation logic.

## Competitor sniper pattern

A robust system should separate four stages:

1. Fetch: query Meta Ads Library by competitor page IDs and category keywords.
2. Rank: score likely winners by ad age/longevity, offer language, category relevance, concise copy, and snapshot availability.
3. Transform: create original brand-safe concepts from the strategic pattern; do not copy competitor wording or creative.
4. Compliance: for supplements, block disease/cure/treat/prevent claims and use support/routine language.

## Reporting rule

Do not say the spy system is broken generically. State the exact blocker: `Meta token exists, but the app/token lacks Ads Library API access.`

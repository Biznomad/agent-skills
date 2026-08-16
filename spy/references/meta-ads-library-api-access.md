# Meta Ads Library API access diagnostic

Use this when a competitor-spy or ad-swipe workflow calls Meta Graph API `/ads_archive`.

## Core rule

`ads_read`, `ads_management`, `business_management`, Page scopes, and Instagram scopes are normal Marketing API permissions. They do not prove the app has Ads Library API access.

Meta treats Ads Library API as a separate app-level feature/approval. A valid token can:

- succeed on `/me`
- succeed on `/me/adaccounts`
- show many granted scopes including `ads_read` and `ads_management`
- still fail on `/ads_archive`

## Failure signature

```text
OAuthException
code: 10
error_subcode: 2332002
message: Application does not have permission for this action
error_user_msg: To access the API, you'll need to follow the steps at facebook.com/ads/library/api.
```

This is an app-feature approval blocker. Do not burn time rotating equivalent tokens, testing every `ad_type`, or rewriting field lists/ranking logic.

## Verification pattern

Do not print token values. Report only redacted fingerprints, app name/app ID, token identity, and scope names.

1. Load candidate tokens from env/config files.
2. For each token, call:
   - `/{version}/app?fields=id,name`
   - `/me?fields=id,name`
   - `/me/permissions`
   - `/me/adaccounts?fields=id,name,account_status&limit=5`
3. Then call `/ads_archive` with a tiny query:
   - `search_terms=sea moss gel`
   - `ad_type=ALL`
   - `ad_active_status=ACTIVE`
   - `ad_reached_countries=["US"]`
   - `fields=id,page_id,page_name,ad_delivery_start_time,ad_snapshot_url`
   - `limit=1`
4. Success is an HTTP 200 response with `data` (possibly empty). Code `10` / subcode `2332002` means the app lacks Ads Library API access.

## SMMA Genie / Example Brand example

For example, a valid system-user token identifies as app `Example App` (`<APP_ID>`) and user `Example API User`. It has broad granted scopes, including `ads_read`, `ads_management`, `business_management`, and Page/Instagram scopes. It still returns subcode `2332002` on `/ads_archive` until Meta grants Ads Library API access to the app.

If the user says “SMMA Genie has the scopes,” confirm the distinction plainly: it has the Marketing API scopes; it still needs the Ads Library API app feature.

## Fix path

1. Prepare/submit Meta App Review or Ads Library API access request at `https://www.facebook.com/ads/library/api` for the app.
2. Use the app review package if available in the project (justification, screencast, internal-use explanation).
3. After approval, regenerate or retest the same system-user token.
4. Only wire the token into the spy pipeline once `/ads_archive` returns HTTP 200.

## Safety

Never paste or print access tokens. When auditing, use:

- token length
- first/last few characters as a redacted fingerprint
- app name/app ID
- granted permission names
- Meta error code/subcode/message

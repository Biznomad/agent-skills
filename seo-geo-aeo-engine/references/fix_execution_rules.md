# Fix Execution Rules

Load this file before ANY change to a client site. These rules exist because each one was
learned the expensive way.

## Approval gates

- Present each fix batch (grouped by phase) for approval with inline decision buttons
  before executing. Batch = one coherent change set with one rollback story.
- Live/production pushes ALWAYS need explicit confirmation naming the environment
  ("publish to LIVE theme?", "reload nginx on PROD?").
- OWNER decisions (canonical phone, appeal wording, account claims) block their dependent
  fixes — do not proceed on an assumed answer.

## Backups

- Per-file, timestamped, purpose-slugged: `file.html.bak-pre-<slug>-<YYYYMMDDHHMMSS>`.
- Take the backup BEFORE the first edit of the session, not per-edit.
- **Backup placement trap:** never leave `.bak` files inside directories loaded by glob
  includes — nginx `include sites-enabled/*;` will load stale `.bak` configs as LIVE
  config and cause conflicting-server-name behavior. Move them to a config archive dir.
- Bulk image/asset optimization: keep originals in a sibling `*.bak-perf-<stamp>` dir.

## Validation loop (after EVERY fix)

1. Page returns 200 and renders (fetch + real-browser spot check for visual changes).
2. Structured data still parses — extract and parse every JSON-LD block on changed pages.
3. Tracking survives: DNI still swaps numbers for ad-cookied visitors, pixels/GTM/analytics
   still fire, form/webhook endpoints unchanged.
4. nginx: `nginx -t` BEFORE reload; verify cert SANs cover every server_name you route.
5. On any failure: restore from backup immediately, then diagnose.

## Tracking preservation (DNI pattern)

When unifying phone numbers on a site with a call-tracking line: swap all on-page + schema
references to the canonical number, then add a small DNI script that swaps the DISPLAYED
number back to the tracking line only for visitors carrying an ad-click cookie (gclid etc.).
Result: organic + AI-referred callers ring the canonical line; paid attribution intact.
Mark the script with a stable comment marker so future audits can find it.

## Performance work

- Judge by FIELD data (CrUX, real-browser PerformanceObserver), never lab Lighthouse alone.
  Lab CPU throttling turns intentional entrance animations into fake 8s+ LCP numbers.
- Never degrade an owner-directed design element (hero animations, brand fonts) for a lab
  score. Non-destructive levers instead: self-host fonts + vendor JS, preload critical
  assets, shorten animation failsafe timers, lazy-load below-fold backgrounds
  (data-attr + IntersectionObserver), recompress images with originals backed up.

## Email / contact facts

Before publishing any contact fact (schema, llms.txt, footer): verify it. `dig MX` the
domain of every advertised email — advertising a dead mailbox is a trust hole for both
customers and AI answer engines.

## Don't rebuild existing engines

Before building any automation (review requests, follow-ups, posting), inventory the
business's server crons and scripts. Mature ops boxes have hundreds of scripts; the engine
you want probably exists and is stuck on ONE blocker (e.g. a review link that needs a
verified profile). Fix the blocker.

## Platform-specific

- **Shopify:** edit dev/unpublished themes only; validate Liquid schema before upload;
  mobile CSS in every section; live publish is a gated user decision.
- **Shopify noindex mechanics (learned 2026-07-17, corrected same day):** `seo.hidden=1`
  works on pages AND articles — platform injects `<meta name="robots"
  content="noindex,nofollow">` and removes the resource from the sitemap. Theme-level
  meta-tag noindex (e.g. a `custom.noindex` metafield the theme renders) does NOT remove
  articles from the sitemap — pair it with `seo.hidden` when the goal is full removal.
- **Verify the EXACT URL before diagnosing platform behavior.** A truncated handle from a
  display listing 404s and "proves" a fix isn't serving when it is. Always copy handles
  from API data, never from console printouts that may be width-truncated, and check the
  HTTP status alongside any grep of the response body.
- **Shopify themeDuplicate is ASYNC:** poll the theme's `processing:false` before
  uploading assets to a fresh duplicate, or the copy job overwrites your uploads.
- **Shopify CDN cache:** page HTML serves mixed stale/fresh edges for up to ~30+ minutes
  after publishes/metafield changes. Verify mutations via the Admin API (ground truth)
  plus patient polling; sitemaps regenerate much faster than page HTML.
- **Static + nginx:** deploy via the business's established transfer path (see registry);
  keep web-root file ownership/permissions as found.
- **Netlify:** verify which SITE the directory deploys to before `netlify deploy` — local
  `.netlify` state can point at the wrong site.
- **GHL funnels:** clone before editing; never modify a live funnel in place.

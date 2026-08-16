# Local-first production verification on Netlify

Use this when deploying a local-first web app where browser storage can mask whether production setup actually works.

## Durable lesson

A production deploy can be correct while a returning browser still shows stale localStorage/autosave state. Verify the first-run path separately from the returning-user path before telling the user the funnel/app is set up.

## Verification pattern

1. Build all production artifacts, not just the frontend:
   - frontend bundle
   - Netlify Functions / API TypeScript output
   - any client-side tracking pixel or embeddable script
2. Deploy to Netlify production or the intended preview URL.
3. Open a fresh URL with a cache-busting query string, e.g. `?fresh_verify=<timestamp>`.
4. Prefer a clean browser profile/context or explicitly clear site storage for the domain before checking first-run behavior.
5. Verify both paths:
   - first-run/no local state: expected seed/live data loads automatically
   - returning-user/local state: existing saved work is restored and not overwritten unexpectedly
6. If the app integrates server-side secrets, confirm the browser only sees derived data/status, never tokens.
7. Capture visible proof: page title/canvas name, connected integration status, counts/metrics shown, and any deploy URL/dashboard link.
8. Report any local-first caveat plainly: existing users may need to click an import/sync button or clear local storage if they want the new default seed to replace their saved canvas.

## Reporting format

Keep it crisp:

- Live URL
- Deploy URL/log link
- What auto-loads on a fresh visit
- What was verified visually or via automated browser check
- Local-first caveat, if stale browser storage can change what the user sees

## Pitfall

Do not claim production is set up merely because the build passed. For local-first apps, the decisive test is a fresh production visit plus confirmation that localStorage/autosave behavior does not silently hide the new deployment behavior.
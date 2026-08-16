# Backend readiness triage for Netlify deployments

Use this when a user asks whether a local app will function correctly on Netlify or whether it needs additional backend setup.

## Pattern

Do not answer from the frontend build alone. Check three layers:

1. Netlify routing/config
   - Read `netlify.toml`.
   - Confirm `build.command`, `build.publish`, and `build.functions`.
   - Confirm API redirects such as `/api/* -> /.netlify/functions/*`.

2. Serverless function runtime requirements
   - Inspect function handlers and shared clients.
   - Identify required environment variables from code, not just `.env.example`.
   - Separate optional env vars from hard requirements.
   - Common split:
     - Demo/heuristic/fallback functions may work with no secrets.
     - Persistence, ingest, auth, metrics often need database credentials/service keys.

3. Frontend integration state
   - Search the API client for stubs/feature flags such as `STUB = true`.
   - Verify whether browser calls actually hit `/api/...` or return local mock data.
   - Check whether authenticated endpoints require a bearer/JWT and whether the frontend sends it.

## Reporting format

Give a blunt deployment-readiness split:

- "Works on Netlify now" — static UI, demo data, fallback functions, public endpoints.
- "Needs backend setup for real product" — database migrations, env vars, auth/JWT, persistence, live metrics, paid AI key.
- State whether Netlify itself is enough, or whether a separate backend host is needed.

## Example conclusion

"For a live demo, deploy now. For real SaaS behavior, Netlify is enough as the host, but you still need Supabase configured, Netlify env vars set, frontend stubs removed, auth wired, and metrics/persistence connected. No separate Express server/VPS is required unless the serverless model becomes insufficient."

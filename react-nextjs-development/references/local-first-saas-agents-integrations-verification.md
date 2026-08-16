# Local-first SaaS-style agents + integrations verification pattern

Use this when turning a Vite/React local-first app into a functional SaaS-style tool with local automation agents, integration cards, Netlify Functions, and optional real-data imports.

## Durable pattern

1. Keep personal-use mode local-first first.
   - Persist canvases, agent configs, agent runs, and integration cards in browser storage.
   - Use deterministic local agents before requiring remote AI/API keys.
   - Keep sample/demo data explicitly labeled as sample; never imply invented metrics are live.

2. Treat agents and integrations as real domain objects, not decorative UI.
   - Agents need persisted config, enabled/paused state, trigger, scope, run button, and run history.
   - At least one agent should produce real recommendations from current canvas/import data.
   - Integrations need provider, status, serverManaged flag, dataProvides list, setupHint, and lastSync/summary.

3. Maintain env-var parity across handlers.
   - If a data import handler accepts fallback env vars, the integration status/health endpoint must check the same fallback names.
   - Example bug: Shopify import accepted `SHOPIFY_ACCESS_TOKEN`, but `/api/integrations` only checked `EXAMPLE BRAND_SHOPIFY_ACCESS_TOKEN`, so import worked while status said `needs_config`.
   - Fix class: centralize or mirror credential detection for import and status endpoints.

4. Runtime smoke-test both static build and live endpoints.
   - `npm run build`
   - web root returns 200
   - integration registry returns provider statuses
   - agent run endpoint returns deterministic fallback when AI key is absent
   - real-data endpoint returns expected summary when server-side credentials are present
   - planned connectors without credentials return `needs_config`, not crashes

5. Avoid unsafe shell probe shapes.
   - Do not pipe `curl` directly into an interpreter.
   - Safer probe pattern: `curl -o tmp.json -w '%{http_code}'`, then run Python/Node against the saved local file.

## Minimal smoke-test checklist

- Build passes for web, functions, and any pixel/bundle package.
- Pixel or embed snippet remains under its stated size budget.
- `/api/integrations` returns all provider cards with correct statuses.
- `/api/agents/run` returns `{ status: 'success', mode: 'heuristic', recommendations: [...] }` without an AI key.
- Real imports return non-null canvas/summary when credentials exist.
- Integration status agrees with real import capability.
- Netlify CLI auth/link status is checked separately from app build readiness.

## Netlify deployment distinction

A project can be build-ready but not deploy-ready if the folder is not linked to a Netlify site. Report these separately:

- Build/runtime readiness: local build and endpoint smoke tests pass.
- Netlify publication readiness: `npx netlify status` is authenticated and folder is linked, or the user has chosen to create/link a site.

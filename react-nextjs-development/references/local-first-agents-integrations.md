# Local-first Agents + Integrations Pattern

Use this when turning a React/Vite/Next app from a demo into a functional personal-use app with automation and connector scaffolding, while avoiding premature Supabase/auth/backend complexity.

## Durable pattern

1. Keep the user-visible app functional without cloud setup:
   - localStorage/IndexedDB persistence for app entities
   - debounced autosave
   - export/import for portability
   - deterministic local heuristics when AI/API keys are missing

2. Model automation as first-class persisted domain objects:
   - `AgentConfig`: id, name, type, enabled, trigger, scope, integrationIds, instructions, created_at, updated_at
   - `AgentRun`: id, agent_id, canvas_id/resource_id, status, started_at, finished_at, summary, recommendations/actions
   - Seed 2-3 useful default agents on first load; do not make the user start with a blank automation area.

3. Separate local execution from server execution:
   - Implement a local runner first for immediate value and offline/personal use.
   - Add a typed serverless `/api/agents/run` contract for future hosted execution.
   - Store recent run history locally; cap it (e.g. last 50) to avoid unbounded localStorage growth.

4. Treat integrations as capability/status cards, not just buttons:
   - provider, name, status, serverManaged, lastSyncAt, summary, dataProvides, setupHint
   - Make clear which integrations require server-side credentials.
   - Never expose Shopify/Meta/GA4/Klaviyo credentials in frontend env.

5. Wire imports to automation:
   - After Shopify/CSV/manual import, update integration status + lastSyncAt.
   - Trigger enabled `on_import` agents automatically.
   - Surface the latest agent insights in the UI so imports immediately produce recommendations.

6. CSV/manual import is an immediate usability bridge:
   - Support node metric rows and edge flow rows in one CSV.
   - Example headers: `node_label,node_type,visitors,events,conversions,path,event_key,source,target,count`
   - Rows with `node_label` create/update node metrics.
   - Rows with `source` and `target` create edge counts between existing labels.

7. Netlify/serverless deployment checklist:
   - Add function source file.
   - Add Netlify wrapper in `functions/`.
   - Add local dev-server route.
   - Add `netlify.toml` redirect.
   - Add typed frontend API client.
   - Add `.env.example` placeholders for server-only env vars.
   - Document route and credential behavior.

## TypeScript pitfalls seen in this pattern

- With strict TS, `lines[0]` from CSV parsing is `string | undefined` even after a length guard; assign to `headerLine` and explicitly guard before parsing.
- Mixed recommendation arrays can infer optional properties as required if all initial mapped entries include them. Explicitly type arrays such as `Array<{ node_id?: string; ... }>` before pushing entries without `node_id`.
- If local models add metrics to canvas nodes, update the shared `CanvasNode` type to include optional `metrics`; otherwise helper functions and CSV imports drift from the domain model.

## Verification

- Run the full monorepo build after all route/type/UI changes, not just the frontend package.
- If dev-server runtime verification hits `EADDRINUSE`, kill the process on the port and restart, but do not encode the port conflict as a durable tool failure.
- Verify at least: static page load, new API route returns JSON, CSV import path applies metrics, and a default agent run creates recommendations.

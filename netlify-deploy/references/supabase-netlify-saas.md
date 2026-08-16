# Supabase + Netlify SaaS readiness pattern

Use this when turning a Vite/React app deployed on Netlify into a real multi-user SaaS without a separate Express/VPS backend.

## Durable pattern

Netlify can host the static app and serverless API, while Supabase provides auth, Postgres, RLS, RPCs, and storage/persistence. The deciding question is not "does the frontend build?" but whether the product path has all five pieces wired end-to-end:

1. Browser auth
   - Add a browser Supabase client using `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`.
   - Provide sign up, sign in, sign out, session bootstrap, and `onAuthStateChange` handling.
   - Keep a clear no-credentials/demo state so local demos still work before SaaS setup.

2. JWT propagation to Netlify Functions
   - Frontend API client must fetch the active Supabase session and send `Authorization: Bearer <access_token>` on protected API calls.
   - Serverless functions should verify/use the JWT for user-scoped operations and reserve the service-role key for privileged database actions.

3. Cloud persistence model
   - Persist a full user-owned/workspace-owned resource graph, not just partial patches.
   - For canvas/graph products, implement full sync semantics: upsert submitted nodes/edges and delete orphaned records absent from the latest client graph. Otherwise deleted items reappear after reload.
   - Use real UUIDs (`crypto.randomUUID()` in the browser) when the database schema uses UUID primary keys.

4. Metrics and RPCs
   - Apply migrations in dependency order: base schema, event tables, RLS policies, metrics/RPC helpers.
   - Metrics endpoints should call user-scoped SQL/RPCs rather than trusting client-side aggregation for production dashboards.
   - Keep heuristic/demo insights as a fallback when AI provider keys are not configured, but label the gap clearly.

5. Netlify configuration
   - `netlify.toml` must point functions to compiled output if TypeScript functions are built separately, e.g. `packages/functions/dist/functions`, not the source directory.
   - Redirect `/api/*` to `/.netlify/functions/:splat`.
   - Required Netlify env vars commonly come in browser/server pairs:
     - `SUPABASE_URL`
     - `SUPABASE_ANON_KEY`
     - `SUPABASE_SERVICE_ROLE_KEY`
     - `VITE_SUPABASE_URL`
     - `VITE_SUPABASE_ANON_KEY`
   - Optional AI vars should not block demo deploy if heuristic fallback exists.

## Verification sequence

1. Build all workspaces locally (`npm run build` or repo-equivalent).
2. Run the Netlify dev stack if available and verify API redirects/functions locally.
3. Browser-test unauthenticated/demo mode: app loads, fallback insights work, and the UI clearly states SaaS setup requirements if env vars are absent.
4. After Supabase env vars and migrations are configured, test the production SaaS loop:
   - sign up
   - sign in
   - create/save resource
   - reload/open saved resource
   - delete an item, save, reload, confirm it stays deleted
   - refresh metrics
5. Deploy preview first unless the user explicitly wants production; then deploy `--prod` after the auth/persistence loop passes.

## Reporting language

Be blunt about the split:

- "Netlify is enough as the backend host" means serverless functions cover the API; it does not mean Supabase credentials/migrations are optional.
- "Demo works" is not "SaaS works." SaaS requires auth, cloud persistence, RLS/user scoping, metrics, and deployed env vars.

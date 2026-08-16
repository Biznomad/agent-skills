# Local-first browser persistence for personal-use React apps

Use this pattern when the user explicitly does not need multi-user SaaS, cross-device sync, or cloud auth yet. For personal MVPs, local-first often beats adding Supabase/Clerk/Neon too early.

## Fit

Good for:
- Single-user/personal tools.
- Netlify/Vite/React apps that should deploy with minimal infrastructure.
- Canvases, drafts, settings, small project data, and user-created JSON documents.
- Apps where export/import JSON is acceptable for backup and portability.

Not enough for:
- Team accounts or per-user cloud sync.
- High-volume analytics/event queries.
- Server-side authorization boundaries.
- Data that must survive browser clearing without user-managed backups.

## Implementation checklist

1. Keep the frontend functional without backend credentials.
2. Store the current document in localStorage or IndexedDB.
   - localStorage is fine for small JSON state.
   - IndexedDB is better for larger documents, binary assets, or many records.
3. Use a versioned key namespace, e.g.:
   - `app:autosave:v1`
   - `app:documents:v1`
   - `app:document:v1:<id>`
4. Maintain an index/list key for saved documents instead of scanning all localStorage keys in app code.
5. Add manual controls:
   - Save locally
   - New local document
   - Export JSON backup
   - Import JSON backup
6. Add debounced autosave after state changes and restore autosave on startup.
7. Preserve local-only runtime fields if they matter after reload. Example: canvas demo metrics or edge counts may not be part of a backend schema but should be serialized for local mode.
8. Validate imported JSON shape before loading it.
9. Update deployment docs and `.env.example` so users are not told backend env vars are required when they are optional.
10. Run a production build and browser smoke test:
    - load demo/create data
    - save locally
    - reload
    - verify restored state
    - run key feature such as AI insights
    - check browser console

## UX language

Use clear local-first copy:
- "Your data saves in this browser. Export JSON for backups or to move devices."
- Avoid scary SaaS/backend setup prompts for a personal/local-first mode.
- Be explicit that clearing browser data can remove local saves.

## Upgrade path

Keep the domain serializer/deserializer separate from persistence. That makes it easy to later replace localStorage with Supabase, Neon, Netlify Blobs, or another backend without rewriting UI state code.

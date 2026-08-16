---
name: netlify-deploy
description: Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netlify, including preview and production deploys.
---

# Netlify Deployment Skill

Deploy web projects to Netlify using the Netlify CLI with intelligent detection of project configuration and deployment context.

Related reference: `references/netlify-monorepo-production-smoke.md` captures a monorepo deploy pattern using `--filter`, explicit package publish paths, compiled functions, and post-deploy smoke tests to catch stale function bundles.

## Overview

This skill automates Netlify deployments by:
- Verifying Netlify CLI authentication
- Detecting project configuration and framework
- Linking to existing sites or creating new ones
- Deploying to production or preview environments

## Prerequisites

- **Netlify CLI**: Installed via npx (no global install required)
- **Authentication**: Netlify account with active login session
- **Project**: Valid web project in current directory
- When sandboxing blocks the deployment network calls, rerun with `sandbox_permissions=require_escalated`.
- The deployment might take a few minutes. Use appropriate timeout values.

## Authentication Pattern

The skill uses the **pre-authenticated Netlify CLI** approach:

1. Check authentication status with `npx netlify status`
2. If not authenticated, guide user through `npx netlify login`
3. Fail gracefully if authentication cannot be established

Authentication uses either:
- **Browser-based OAuth** (primary): `netlify login` opens browser for authentication
- **API Key** (alternative): Set `NETLIFY_AUTH_TOKEN` environment variable

## Workflow

### 1. Verify Netlify CLI Authentication

Check if the user is logged into Netlify:

```bash
npx netlify status
```

**Expected output patterns**:
- ✅ Authenticated: Shows logged-in user email and site link status
- ❌ Not authenticated: "Not logged into any site" or authentication error

**If not authenticated**, guide the user:

```bash
npx netlify login
```

This opens a browser window for OAuth authentication. Wait for user to complete login, then verify with `netlify status` again.

**Alternative: API Key authentication**

If browser authentication isn't available, users can set:

```bash
export NETLIFY_AUTH_TOKEN=your_token_here
```

Tokens can be generated at: https://app.netlify.com/user/applications#personal-access-tokens

### 2. Detect Site Link Status

From `netlify status` output, determine:
- **Linked**: Site already connected to Netlify (shows site name/URL)
- **Not linked**: Need to link or create site

### 3. Link to Existing Site or Create New

**If already linked** → Skip to step 4

**If not linked**, attempt to link by Git remote:

```bash
# Check if project is Git-based
git remote show origin

# If Git-based, extract remote URL
# Format: https://github.com/username/repo or git@github.com:username/repo.git

# Try to link by Git remote
npx netlify link --git-remote-url <REMOTE_URL>
```

**If link fails** (site doesn't exist on Netlify):

```bash
# Create new site interactively
npx netlify init
```

This guides user through:
1. Choosing team/account
2. Setting site name
3. Configuring build settings
4. Creating netlify.toml if needed

### 4. Verify Dependencies

Before deploying, ensure project dependencies are installed:

```bash
# For npm projects
npm install

# For other package managers, detect and use appropriate command
# yarn install, pnpm install, etc.
```

### 5. Deploy to Netlify

Choose deployment type based on context:

**Preview/Draft Deploy** (default for existing sites):

```bash
npx netlify deploy
```

This creates a deploy preview with a unique URL for testing.

**Production Deploy** (for new sites or explicit production deployments):

```bash
npx netlify deploy --prod
```

This deploys to the live production URL.

**Deployment process**:
1. CLI detects build settings (from netlify.toml or prompts user)
2. Builds the project locally
3. Uploads built assets to Netlify
4. Returns deployment URL

### 6. Report Results

After deployment, report to user:
- **Deploy URL**: Unique URL for this deployment
- **Site URL**: Production URL (if production deploy)
- **Deploy logs**: Link to Netlify dashboard for logs
- **Next steps**: Suggest `netlify open` to view site or dashboard

## Handling netlify.toml

If a `netlify.toml` file exists, the CLI uses it automatically. If not, the CLI will prompt for:
- **Build command**: e.g., `npm run build`, `next build`
- **Publish directory**: e.g., `dist`, `build`, `.next`

## Backend Readiness Triage

When the user asks whether a site will function correctly on Netlify or whether it needs more backend setup, do not stop at "the frontend builds." Check:

1. `netlify.toml` routing: build command, publish directory, functions directory, and `/api/*` redirects to Netlify Functions.
2. Function runtime dependencies: required environment variables, database clients, service-role keys, optional AI/provider keys, and fallback paths.
3. Frontend integration state: API client stubs, feature flags, mock data, auth token/JWT handling, and whether browser calls actually hit `/api/...`.

Report in two buckets: "works on Netlify now" versus "needs backend setup for real product." Be explicit whether Netlify itself is sufficient as the backend host or whether a separate server/VPS is actually needed. See `references/backend-readiness-triage.md` for the checklist and a concise example conclusion.

For Supabase-backed SaaS on Netlify, use `references/supabase-netlify-saas.md`. The important distinction: Netlify can be enough as the backend host, but SaaS still requires Supabase auth, migrations/RLS, JWT propagation to functions, cloud persistence, metrics/RPCs, and deployed browser/server env vars.

For local-first apps where browser storage/autosave can mask production behavior, use `references/local-first-production-verification.md`. Verify a fresh no-local-state visit separately from the returning-user path before claiming the live app is set up.

Common framework defaults:
- **Next.js**: build command `npm run build`, publish `.next`
- **React (Vite)**: build command `npm run build`, publish `dist`
- **Static HTML**: no build command, publish current directory

The skill should detect framework from `package.json` if possible and suggest appropriate settings.

## Example Full Workflow

```bash
# 1. Check authentication
npx netlify status

# If not authenticated:
npx netlify login

# 2. Link site (if needed)
# Try Git-based linking first
git remote show origin
npx netlify link --git-remote-url https://github.com/user/repo

# If no site exists, create new one:
npx netlify init

# 3. Install dependencies
npm install

# 4. Deploy (preview for testing)
npx netlify deploy

# 5. Deploy to production (when ready)
npx netlify deploy --prod
```

## Monorepo Artifact Deploys

When a monorepo has separate web and functions packages, do not assume a successful frontend deploy uploaded functions. Deploy the already-built artifacts explicitly and verify both sides:

```bash
npm run build --workspaces --if-present
npx netlify deploy --prod --site <SITE_ID> \
  --dir packages/web/dist \
  --functions packages/functions/dist/functions
```

After deploy, verify a live function endpoint with `curl` or a browser/network probe before telling the user production is fixed. A visible updated frontend is not proof that Netlify Functions were repackaged.

Prefer non-destructive artifact staging when command guards block broad cleanup commands. If the functions build output contains stale files, either fix the TypeScript output settings (for example `declaration: false`) or rebuild into a fresh temporary/staging directory rather than routing around a blocked `rm -rf`.

## Error Handling

Common issues and solutions:

**Monorepo prompt / CLI crash on workspace selection**
→ If Netlify CLI detects multiple workspaces and crashes while prompting, pass `--filter <workspace-name>` on commands that support it, e.g. `--filter @bizfunnel/web`. For commands that do not support `--filter` (such as `netlify status` in some CLI versions), target the site directly with `--site <site-id>` for deploy/env operations instead of relying on local linking.
→ Pitfall: with `--filter`, Netlify may resolve `--dir` / `--functions` inconsistently against the repo root, selected package, or resolved config. If `--dir dist` fails with `deploy directory .../repo/dist has not been found` while the resolved config says `packages/web/dist`, rerun with absolute paths: `npx netlify deploy --prod --site <SITE_ID> --filter @pkg/web --dir "$PWD/packages/web/dist" --functions "$PWD/packages/functions/dist/functions"`. Watch the deploy log: it may say `Functions folder ... doesn't exist` and then `Deploying functions from cache`. If you need a guaranteed fresh functions upload, use absolute functions paths plus `--skip-functions-cache`, or omit `--filter` by avoiding the workspace prompt another way, then verify the live function endpoint after deploy.

**"Incorrect function names" during deploy**
→ Check the configured functions directory for emitted non-function files such as `.d.ts` declarations. Netlify may try to package them as functions and reject names containing dots. For TypeScript-compiled functions, set `declaration: false` or rebuild into a clean staging/output directory so the functions directory contains only valid function `.js` entries plus allowed supporting files. Avoid broad destructive cleanup unless the user has approved the exact path.


**"Not logged in"**
→ Run `npx netlify login`

**"No site linked"**
→ Run `npx netlify link` or `npx netlify init`

**"Build failed"**
→ Check build command and publish directory in netlify.toml or CLI prompts
→ Verify dependencies are installed
→ Review build logs for specific errors

**"Publish directory not found"**
→ Verify build command ran successfully
→ Check publish directory path is correct

## Troubleshooting

### Escalated Network Access

If deployment fails due to network issues (timeouts, DNS errors, connection resets), rerun the deploy with escalated permissions (use `sandbox_permissions=require_escalated`). The deploy requires escalated network access when sandbox networking blocks outbound requests.

Example guidance to the user:

```
The deploy needs escalated network access to deploy to Netlify. I can rerun the command with escalated permissions—want me to proceed?
```

## Environment Variables

For secrets and configuration:

1. Never commit secrets to Git
2. Set in Netlify dashboard: Site Settings → Environment Variables
3. Access in builds via `process.env.VARIABLE_NAME`

## Tips

- Use `netlify deploy` (no `--prod`) first to test before production
- Run `netlify open` to view site in Netlify dashboard
- Run `netlify logs` to view function logs (if using Netlify Functions)
- Use `netlify dev` for local development with Netlify Functions

## Reference

- Netlify CLI Docs: https://docs.netlify.com/cli/get-started/
- netlify.toml Reference: https://docs.netlify.com/configure-builds/file-based-configuration/

## Bundled References (Load As Needed)

- [CLI commands](references/cli-commands.md)
- [Deployment patterns](references/deployment-patterns.md)
- [netlify.toml guide](references/netlify-toml.md)

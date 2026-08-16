# SaaS Design — seo-geo-aeo-engine → product
Date: 2026-07-12 · Status: DRAFT (owner review pending) · Working name: **"Citable"** (placeholder — naming undecided)

## What it is
Self-serve web product wrapping the proven audit engine: enter a domain → free instant
mini-audit → paid full audit (9-specialist wave, health score, phased action plan) →
subscription for continuous monitoring (score history, re-audit deltas, AI-citation
tracking across ChatGPT/Perplexity/Gemini/AI Overviews). The engine's fix-execution
capability is deliberately NOT self-serve — it's the Biznomad done-for-you upsell attached
to every report's "AI-doable" items.

Differentiator vs commodity SEO audit tools: the GEO/AEO surface (AI-visibility scoring,
llms.txt/entity/citability analysis, "is your brand cited by AI" tracking) plus an action
plan written like an operator, not a crawler dump — proven on real stores (TNT 59/100
baseline → fix cycle; HV 53/100 → same-week live fixes).

## Customers ("all of the above", sequenced)
1. **v1: SMB/e-com owners** — self-serve, the front door.
2. **v1 seed: Biznomad clients** — every AGaaS client gets an account (retention artifact,
   real usage data, testimonials).
3. **v2: Agencies** — white-label tier (their logo/domain on reports).
4. **v3: Shopify App** — distribution channel reusing the same API (Shopify billing per
   the no-Stripe-on-Shopify rule).

## Product tiers (numbers = placeholders, owner decision)
- **Free**: instant mini-audit — scripted checks only (site_preflight suite: redirects,
  security headers, AI-crawler access, llms.txt, sitemap, MX) + one AI-visibility spot
  check. Near-zero COGS. Email-gated full results = lead capture.
- **One-shot full audit**: ~$79. The 9-specialist audit + score + action plan, web report
  + PDF. No subscription required (validation + gift/agency-trial path).
- **Starter ~$49/mo**: 1 site, monthly re-audit, weekly AI-citation checks, score history.
- **Growth ~$149/mo**: 3 sites, weekly re-audits, competitor citation tracking.
- **Agency ~$399/mo**: 10 sites, white-label reports, client-facing share links.
- **Done-for-you**: "Fix this for me" button on every AI-doable item → Biznomad AGaaS
  pipeline (calendly/GHL intake). This is the strategic reason the SaaS exists.

## COGS reality (from today's real runs)
Full audit ≈ 9 specialist agents ≈ 0.8–1.2M tokens ≈ **$3–10 API cost** depending on
model mix (Sonnet-class workers, Haiku for mechanical passes). Mini-audit ≈ cents.
Subscription monitoring: citation checks are small prompts (~$0.10–0.50/site/week).
Margins work at the placeholder prices; enforce with per-tier audit credits.

## Architecture
```
[Next.js app (Netlify)] ── auth/billing/dashboard/reports
        │ REST
[API + queue (VPS, Postgres)] ── orgs/sites/audits/findings/scores/citations tables
        │ jobs
[Audit workers (VPS, Claude Agent SDK)] ── ports the skill's specialist specs to SDK
        │                                   subagents; same scoring_model.md weights
[Citation tracker] ── scheduled prompts across OpenAI/Anthropic/Gemini/Perplexity APIs,
                      extract cited domains (build minimal in-house; evaluate self-hosted
                      gego as accelerant — GPL fine server-side)
```
- **Single source of truth**: the skill repo's references/ (scoring model, coverage specs,
  taxonomy) become a shared package consumed by both the internal skill and the SaaS
  workers — one brain, two harnesses.
- **Sandboxing**: SaaS workers are READ-ONLY against customer sites (crawl + APIs only).
  No fix execution, no credentials from customers in v1.
- **Billing**: Paddle or LemonSqueezy as merchant-of-record (avoids Stripe per working
  rules; MoR handles global sales tax). OWNER DECISION.
- **Reports**: same artifact structure as the skill (score table, dimension findings,
  Phase 0–3 plan) rendered as web dashboard + shareable read-only link + PDF export.

## Build phases (validation-first, per practical-over-complex rule)
- **Phase 0 (1–2 wks): Wizard-of-Oz validation.** Landing page + free mini-audit (the
  preflight scripts as a hosted endpoint) + waitlist + "$79 full audit" checkout. Early
  full audits fulfilled by running the EXISTING skill manually. Proves willingness-to-pay
  before platform build. Netlify + one VPS endpoint. 
- **Phase 1 (2–4 wks): automated full audits.** Agent SDK workers + queue + report
  rendering + accounts. Biznomad clients seeded.
- **Phase 2: monitoring subscription.** Scheduler, citation tracker, score history,
  drift alerts (email + optional Telegram).
- **Phase 3: white-label + Shopify app channel.**

## Open decisions (owner)
1. Product name + domain (placeholder "Citable").
2. Price points (placeholders above).
3. Merchant of record: Paddle vs LemonSqueezy.
4. Brand relationship: standalone brand vs biznomad.io/product (recommend standalone
   product brand, "powered by Biznomad" for the DFY pipeline).
5. Phase 0 go — build the landing + mini-audit now?

## Risks
- **COGS discipline**: audit depth must be credit-gated; runaway re-audits kill margin.
- **Moat**: prompts are copyable; the moat is the action-plan quality, the fix-execution
  arm (agency), longitudinal score data, and speed of GEO methodology updates.
- **Platform ToS**: citation tracking must use official APIs (no scraping ChatGPT UI).
- **Support surface**: self-serve customers on damaged sites will ask questions — the
  free tier answer path should route to the DFY pipeline, not free consulting.

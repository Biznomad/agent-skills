# Action Plan Taxonomy

Every finding gets a phase, a tag, and a one-line "why it matters". Write the plan so a
non-technical owner can read it.

## Tags

- **AI-doable** — executable from this environment with backups and validation
  (server edits, schema, content builds, config).
- **OWNER** — needs the client's decision, credentials, physical access, or identity
  (canonical phone choice, citation account claims, PIN postcards, 2FA logins, appeals).

Never silently convert an OWNER item into an AI-doable one by working around an access
gate — bot-blocked platforms (Yelp/DataDome, Google login walls) stay OWNER items with a
handoff card.

## Phase 0 — Same day: trust & safety

Anything that misrepresents the business or breaks core conversion. Ship the same day.

- Fake/placeholder content visible to users: fabricated reviews, stock "testimonials",
  placeholder banners left in production (FTC exposure — remove, don't polish).
- Fabricated schema: per-city fake addresses, invented aggregateRating, wrong entity types.
- Conversion blockers: overlapping FABs covering call buttons/forms, broken tel: links,
  dead advertised emails (check MX records), broken booking flows.
- **OWNER decision that gates Phase 1:** canonical NAP — especially WHICH phone number is
  canonical when a tracking line exists (changes who rings; ask, never assume).

## Phase 1 — Week 1: identity unification

Make the business ONE consistent entity everywhere machines look.

- NAP unified sitewide: on-page + JSON-LD + title tags; tracking numbers preserved via DNI
  (dynamic number insertion keyed on ad-click cookies) so paid attribution survives.
- Single-entity schema rollout: one canonical `#business` node; location/service pages
  reference it via `Service` + `areaServed` — no duplicate LocalBusiness nodes.
- Security + redirect hygiene: www→apex 301, HSTS/XCTO/XFO/Referrer-Policy, one canonical
  protocol/host.
- llms.txt published (AFTER NAP unification — it must state the canonical facts).
- FAQPage schema on pages that already have FAQ content.
- Sitemap hygiene: real URL set, lastmod, funnel/utility pages noindexed and removed.
- OWNER: claim GBP-independent citations (Bing Places, Apple Business Connect, Facebook).

## Phase 2 — Weeks 2–3: money pages + speed

- Rebuild the primary money page to beat franchise-depth competitors (900+ words: process,
  pricing, same-day cutoffs, FAQ, locality proof).
- Build the cost/pricing cluster (see geo_aeo_playbook.md) — highest AI-citation ROI.
- De-duplicate doorway/city pages (see dedupe_local_depth.md).
- Performance: self-host fonts + vendor JS, modern image formats + lazy-load, defer
  third-party scripts. Respect owner directives on animations; judge by field data.
- SERP differentiators into titles/metas (e.g. "Book Online in 60 Seconds").
- Internal linking: homepage → hub → cluster (link equity must reach clusters via links,
  not just the sitemap).

## Phase 3 — Month 2: authority

- Real-review engine: point existing review-request automation at whichever platform can
  accept reviews NOW (Facebook/Yelp while GBP suspended); swap placeholders with real
  reviews as they arrive.
- Refresh GBP appeal AFTER identity fixes land (clean NAP story strengthens the appeal).
- Citations wired back: as each profile goes live, add URL to schema `sameAs`, llms.txt,
  and footer.
- Local links: chambers, Nextdoor, sponsorships, community pages.
- Measurement loop: GSC coverage weekly, analytics events per city/page, AI-referral
  traffic (perplexity/chatgpt/copilot referrers) tracked in analytics.

## Backlog discipline

`ACTION-PLAN.md` ends with an `## OPEN backlog` section. Every session that touches the
business updates it: done items get a date + backup stamp; new findings get a phase + tag.
The backlog is the single source of truth for "what's next" — status requests read it
instead of re-auditing.

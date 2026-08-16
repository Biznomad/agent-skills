# GEO/AEO Playbook

How to make a business citable by AI answer engines (ChatGPT, Perplexity, Claude, Google
AI Overviews, Bing Copilot) on top of classic organic.

## AI crawler access (table stakes)

Verify ALL of these fetch key pages with 200 and are not disallowed in robots.txt:
GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended,
Googlebot, Bingbot. `scripts/site_preflight.sh` checks robots rules; spot-check real
fetches with the bot User-Agent for the homepage + one money page.

## llms.txt

Plain-markdown file at `/llms.txt` summarizing the business for LLM consumers. Include:
what the business does, services with plain-language descriptions, PRICING (real numbers —
this is what gets cited), service area/cities, how to book, canonical NAP, company facts.
Rules:

- Publish only AFTER identity unification — it must state canonical facts (one phone,
  verified email, real address policy).
- Update whenever services/pricing/contact change; treat as a release artifact.
- Add live citation profile URLs (GBP, Bing Places, Facebook, Yelp) as they exist.

## Single-entity schema pattern

One business = one canonical node. Fragmented or fabricated entities poison AI trust.

- Canonical `LocalBusiness` (or correct subtype) node with stable `@id`
  `https://<domain>/#business` on the homepage: real address, `geo`, `logo`, hours,
  `OfferCatalog`, `telephone` = canonical number.
- City/service pages: `Service` nodes with `provider: {"@id": ".../#business"}` and
  `areaServed` — NEVER per-page LocalBusiness nodes with invented local addresses.
- No placeholder `sameAs` (empty social URLs), no invented `aggregateRating`, no
  incorrect types chosen for keyword reasons.
- `FAQPage` on every page with real Q&A content; questions phrased as users ask them.

## AI-citable page pattern (the cost-cluster play)

Answer engines cite pages that answer the question in the first passage. Highest-ROI
build: a pricing/cost guide cluster.

1. Parent guide: `/[service]-cost-[city]/` — opens with a direct-dollar answer in the
   first 100 words ("X costs $A–$B in CITY; most jobs land around $C"), then a price
   table with concrete examples, competitor/franchise comparison (sourced figures only),
   DIY math, FAQ with `FAQPage` LD.
2. Item children: `/[item]-removal-cost-[city]/` etc. — one distinct high-intent query
   each, direct-dollar opening, item-specific facts (regulations, disposal rules) that
   only a real operator would know.
3. Build children from an existing page's chrome so tracking/DNI/analytics ship intact.
4. Interlink: parent ↔ children with a marked link block; homepage/hub links to parent.
5. Every claim must be true to the business's actual pricing — AI engines get punished
   for citing pages that contradict the booking flow.

Content rules for citability everywhere: H2s that mirror real questions, one
straight-answer sentence immediately after each H2, specifics over adjectives (numbers,
counties, cutoff times), named-entity consistency with the canonical NAP.

## Index pings

- **GSC API** (webmasters scope token): sitemap submit works headlessly; URL Inspection
  data readable; per-URL "Request Indexing" is UI-only — OWNER item.
- **IndexNow:** place a standing key file `<key>.txt` in the web root once; POST URL lists
  on every content ship for instant Bing/Copilot discovery.

## Citations (GBP-independent identity)

When GBP is suspended or weak, build the entity graph elsewhere — AI engines triangulate:

- **Bing Places:** create MANUALLY (do not import from a suspended GBP). Expect postcard
  PIN verification to the real address (OWNER enters PIN). Description/hours often locked
  until verified — add after.
- **Apple Business Connect:** requires Apple ID 2FA — OWNER task with a handoff card.
- **Facebook page:** OWNER login required; once live it can also receive reviews.
- **Yelp:** hard-blocks automated browsers (DataDome) even on the homepage — don't fight
  it; OWNER claims by phone.
- Handoff card per platform: exact steps, prefilled canonical NAP, reply keywords so the
  owner can confirm completion from their phone.
- As each profile goes live: wire the URL into schema `sameAs` + llms.txt + site footer.

## Measuring GEO/AEO

- Track AI referrers in analytics (perplexity.ai, chatgpt.com, copilot, gemini).
- Periodically ask the target queries in ChatGPT/Perplexity and record whether the
  business is cited (the AI-citation audit dimension).
- CrUX field data for perf; GSC impressions for classic organic movement.

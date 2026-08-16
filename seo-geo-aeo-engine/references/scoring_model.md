# Scoring Model

## Dimensions and coverage specs

Each specialist scores its dimension 0–100. Coverage specs below double as the prompt spec
when spawning a general-purpose fallback agent.

| Dimension | Covers |
|-----------|--------|
| technical | Crawlability, indexability, redirects (www/apex, http→https), security headers (HSTS/XCTO/XFO/Referrer-Policy), canonical tags, URL structure, mobile viewport, JS rendering, server config hygiene |
| schema | JSON-LD validity, entity architecture (single canonical business node vs fragmented/fake per-page entities), correct types, FAQPage/Service/Offer coverage, no placeholder sameAs, aggregateRating substantiation |
| geo-aeo | AI crawler access (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot all 200 + robots.txt allowed), llms.txt presence/quality, passage-level citability (direct answers in first 100 words), question-mirroring headings, brand mention consistency |
| content | Depth vs competitors, thin/doorway pages, duplication across templates, E-E-A-T signals, title/meta quality + differentiators, internal linking, keyword/intent coverage gaps |
| performance | Field data (CrUX) first, lab second. LCP/INP/CLS, page weight, font loading strategy, image formats + lazy-loading, third-party JS deferral, self-hosted vendors |
| local | GBP status, NAP consistency (site vs schema vs citations), citations coverage (Bing Places, Apple, Facebook, Yelp), reviews velocity + response, local landing page quality, service-area schema honesty |
| sxo | SERP-backwards analysis: does the ranking page type match intent, persona walk-throughs, CTA clarity, booking-flow friction, trust elements visible above fold |
| visual | Real-browser rendering desktop + mobile, overlap/covering bugs (FABs over CTAs), tap-target sizes, broken layouts, placeholder/fake content visible to users |
| sitemap | XML validity, URL count vs reality, lastmod accuracy, funnel/utility pages noindexed and excluded, orphan pages, canonical alignment |
| ecommerce (cond.) | Product schema, feed health, collection page depth, faceted-nav crawl traps, marketplace visibility |
| maps (cond.) | Geo-grid rankings, GBP profile completeness, review intelligence, competitor radius |

## Weights

Weights must stay constant per business across re-audits (deltas depend on it).

| Dimension | local-service | ecommerce |
|-----------|--------------:|----------:|
| technical | 15 | 15 |
| schema | 10 | 10 |
| geo-aeo | 15 | 15 |
| content | 15 | 15 |
| performance | 10 | 10 |
| local | 15 | 0 |
| ecommerce | 0 | 15 |
| sxo | 10 | 10 |
| visual | 5 | 5 |
| sitemap | 5 | 5 |
| **Total** | **100** | **100** |

`scripts/health_score.py` implements these tables. Extra dimensions present in
`audit-data.json` but absent from the profile (e.g. maps, backlinks) are reported but not
weighted — note them in the report.

## Grade bands

| Score | Band | Meaning |
|-------|------|---------|
| 0–49 | CRITICAL | Trust/identity problems actively suppressing visibility |
| 50–69 | NEEDS WORK | Fundamentals present, entity/content/authority gaps |
| 70–84 | GOOD | Compete on content velocity + authority |
| 85–100 | STRONG | Maintain, monitor drift, expand clusters |

## Scoring discipline

- Score what IS, not what's planned. A staged-but-unpublished fix does not move the score.
- A dimension with a CRITICAL legal/trust finding (fake reviews, fabricated addresses)
  caps at 40 regardless of other checks.
- Record the baseline date in `audit-data.json`; every re-audit appends a dated snapshot
  rather than overwriting, so score history survives.

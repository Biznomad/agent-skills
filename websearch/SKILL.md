---
name: websearch
description: >
  Search the web and fetch pages through Decodo residential IPs. Use whenever you
  need current information, competitor research, market data, pricing, news, or a
  page that blocks datacenter traffic. Use when the user says: "search", "look up",
  "google", "find out", "what's the latest", "research", "check competitors",
  "who ranks for", or asks anything you cannot answer from memory.
version: 1.0.0
author: Biznomad
license: MIT
metadata:
  requires_env:
    - DECODO_SCRAPE_TOKEN
---

# websearch

Google search and page fetching that exits through **Decodo residential IPs**
(real consumer ISPs). Google returns normal results instead of a bot challenge,
and sites that block datacenter ranges answer normally.

This is the fleet's web-search path. The built-in `web` toolset is inert — it
wants EXA / Tavily / Firecrawl / Parallel keys that are not configured. Use this
instead.

## Search

```bash
python3 scripts/websearch.py "sea moss market size 2026"
python3 scripts/websearch.py "competitor pricing teeth whitening atlanta" --n 10
python3 scripts/websearch.py "query" --geo "United Kingdom"
```

Returns markdown: AI overview, organic results with URLs and snippets, knowledge
panel, and "people also ask". Typical latency is 3–5 seconds.

## Fetch a page

```bash
python3 scripts/websearch.py --url https://example.com/pricing
python3 scripts/websearch.py --url https://spa-site.com --js   # render JavaScript
```

Use `--url` when you already know the page. Use `--js` only for JavaScript-heavy
sites — it is slower.

## Flags

| Flag | Purpose | Default |
|---|---|---|
| `--geo` | Exit country | `United States` |
| `--n` | Max organic results | 8 |
| `--js` | Render JavaScript (URL fetch only) | off |
| `--json` | Raw JSON instead of markdown | off |
| `--timeout` | Seconds | 90 |

## Notes

- Every call spends Decodo scraping credits. Prefer one well-formed query over
  several vague ones; do not poll in a loop.
- `--geo` matters for local intent (rankings, pricing, availability differ by
  country). Leave it at `United States` unless the question is about another market.
- On a `DECODO_SCRAPE_TOKEN is not set` error the token is missing from that
  profile's environment — it belongs in `~/.hermes/.env` so every profile inherits it.
- For interactive work (clicking, forms, logins) use the `browser` toolset
  instead. This skill is for reading, not driving.

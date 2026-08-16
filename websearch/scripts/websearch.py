#!/usr/bin/env python3
"""websearch — web search and page fetch via Decodo's Scraping API.

Exits through Decodo residential IPs (real consumer ISPs), so Google and
bot-sensitive sites answer normally instead of serving a challenge. Replaces
the EXA/Tavily/Firecrawl keys the `web` toolset wants — you already pay for
Decodo, so this costs nothing extra.

  websearch.py "sea moss market size 2026"
  websearch.py "competitor pricing" --geo "United States" --n 10
  websearch.py --url https://example.com/pricing        # fetch a page's HTML
  websearch.py "query" --json                           # machine-readable

Env: DECODO_SCRAPE_TOKEN (Basic-auth token, 64 chars).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://scraper-api.decodo.com/v2/scrape"
DEFAULT_GEO = "United States"


def _post(payload: dict, token: str, timeout: int) -> dict:
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()[:300]
        sys.exit(f"Decodo API error {exc.code}: {body}")
    except urllib.error.URLError as exc:
        sys.exit(f"Network error reaching Decodo: {exc.reason}")


def _trim(text: object, limit: int) -> str:
    s = " ".join(str(text or "").split())
    return s if len(s) <= limit else s[: limit - 1] + "…"


def search(query: str, geo: str, n: int, token: str, timeout: int) -> dict:
    data = _post(
        {
            "target": "google_search",
            "query": query,
            "geo": geo,
            "parse": True,
        },
        token,
        timeout,
    )
    try:
        return data["results"][0]["content"]["results"]["results"]
    except (KeyError, IndexError, TypeError):
        sys.exit("Unexpected Decodo response shape — rerun with --json to inspect.")


def render(res: dict, query: str, n: int) -> str:
    out = [f"# Search: {query}\n"]

    info = res.get("search_information") or {}
    total = res.get("total_results_count")
    if total:
        out.append(f"_~{total:,} results_\n" if isinstance(total, int) else "")

    for ov in (res.get("ai_overviews") or [])[:1]:
        body = ov.get("content") or ov.get("text") or ""
        if body:
            out.append("## AI overview\n" + _trim(body, 700) + "\n")

    organic = (res.get("organic") or [])[:n]
    if organic:
        out.append("## Results\n")
        for i, r in enumerate(organic, 1):
            out.append(f"{i}. **{_trim(r.get('title'), 100)}**")
            out.append(f"   {r.get('url')}")
            desc = r.get("desc") or r.get("snippet")
            if desc:
                out.append(f"   {_trim(desc, 220)}")
            out.append("")

    kn = res.get("knowledge") or {}
    if kn.get("title"):
        out.append(f"## Knowledge panel\n**{kn['title']}** — {_trim(kn.get('description'), 300)}\n")

    rq = res.get("related_questions") or {}
    items = rq.get("items") if isinstance(rq, dict) else rq
    if items:
        out.append("## People also ask")
        for q in items[:5]:
            out.append(f"- {_trim(q.get('question') if isinstance(q, dict) else q, 120)}")
        out.append("")

    if not organic:
        out.append("_No organic results — try a broader query or a different --geo._")

    return "\n".join(out)


def fetch_url(url: str, geo: str, token: str, timeout: int, render_js: bool) -> str:
    payload = {"url": url, "geo": geo}
    if render_js:
        payload["headless"] = "html"
    data = _post(payload, token, timeout)
    try:
        content = data["results"][0]["content"]
    except (KeyError, IndexError, TypeError):
        sys.exit("Unexpected Decodo response shape — rerun with --json to inspect.")
    return content if isinstance(content, str) else json.dumps(content, indent=2)


def main() -> None:
    ap = argparse.ArgumentParser(description="Web search / page fetch via Decodo residential IPs")
    ap.add_argument("query", nargs="?", help="search query")
    ap.add_argument("--url", help="fetch this URL instead of searching")
    ap.add_argument("--geo", default=DEFAULT_GEO, help=f"exit country (default: {DEFAULT_GEO})")
    ap.add_argument("--n", type=int, default=8, help="max organic results (default: 8)")
    ap.add_argument("--timeout", type=int, default=90, help="seconds (default: 90)")
    ap.add_argument("--js", action="store_true", help="render JavaScript when fetching a URL")
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    args = ap.parse_args()

    token = os.environ.get("DECODO_SCRAPE_TOKEN", "").strip()
    if not token:
        sys.exit(
            "DECODO_SCRAPE_TOKEN is not set.\n"
            "It lives in the Hermes env — check ~/.hermes/.env or the profile .env."
        )

    if args.url:
        print(fetch_url(args.url, args.geo, token, args.timeout, args.js))
        return

    if not args.query:
        ap.error("provide a query, or --url to fetch a page")

    res = search(args.query, args.geo, args.n, token, args.timeout)
    if args.json:
        print(json.dumps(res, indent=2)[:200000])
    else:
        print(render(res, args.query, args.n))


if __name__ == "__main__":
    main()

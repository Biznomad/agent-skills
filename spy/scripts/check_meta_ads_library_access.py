#!/usr/bin/env python3
"""Check whether Meta access tokens can use the Ads Library API.

Reads plausible EAA-style tokens from env vars and optional .env files passed as
arguments. Prints fingerprints only; never prints full token values.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

TOKEN_KEYS = re.compile(r"(META|FACEBOOK|FB).*TOKEN", re.I)


def iter_tokens(paths: Iterable[str]) -> List[Tuple[str, str]]:
    found: List[Tuple[str, str]] = []
    for key, val in os.environ.items():
        if TOKEN_KEYS.search(key) and val.startswith("EAA") and len(val) > 80:
            found.append((f"env:{key}", val))
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        if not path.exists() or not path.is_file():
            continue
        for line_no, raw in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if "=" not in raw or raw.strip().startswith("#"):
                continue
            key, val = raw.strip().split("=", 1)
            key = key.replace("export ", "").strip()
            val = val.strip().strip('"').strip("'")
            if TOKEN_KEYS.search(key) and val.startswith("EAA") and len(val) > 80:
                found.append((f"{path}:{line_no}:{key}", val))
    dedup: Dict[str, str] = {}
    for source, token in found:
        dedup.setdefault(token, source)
    return [(source, token) for token, source in dedup.items()]


def graph_get(token: str, endpoint: str) -> dict:
    if endpoint == "me":
        url = "https://graph.facebook.com/v21.0/me?" + urllib.parse.urlencode({
            "access_token": token,
            "fields": "id,name",
        })
    elif endpoint == "adaccounts":
        url = "https://graph.facebook.com/v21.0/me/adaccounts?" + urllib.parse.urlencode({
            "access_token": token,
            "fields": "id,name,account_status",
            "limit": 5,
        })
    else:
        url = "https://graph.facebook.com/v21.0/ads_archive?" + urllib.parse.urlencode({
            "access_token": token,
            "search_terms": "sea moss",
            "ad_type": "ALL",
            "ad_active_status": "ACTIVE",
            "ad_reached_countries": json.dumps(["US"]),
            "fields": "id,page_id,page_name,ad_delivery_start_time,ad_snapshot_url",
            "limit": 1,
        })
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode())
        return {"ok": True, "keys": list(data.keys()), "count": len(data.get("data", [])) if isinstance(data.get("data"), list) else None}
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            err = json.loads(body).get("error", {})
        except Exception:
            err = {"message": body[:300]}
        return {
            "ok": False,
            "status": e.code,
            "code": err.get("code"),
            "subcode": err.get("error_subcode"),
            "message": err.get("message"),
            "user_msg": err.get("error_user_msg"),
        }


def main() -> int:
    tokens = iter_tokens(sys.argv[1:])
    print(f"plausible_meta_tokens={len(tokens)}")
    for idx, (source, token) in enumerate(tokens, 1):
        print(f"\nTOKEN_{idx} fp={token[:8]}...{token[-6:]} len={len(token)} source={source}")
        for endpoint in ["me", "adaccounts", "ads_archive"]:
            print(endpoint + ":", json.dumps(graph_get(token, endpoint), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

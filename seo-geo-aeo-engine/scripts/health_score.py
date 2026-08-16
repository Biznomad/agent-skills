#!/usr/bin/env python3
"""Compute the weighted SEO/GEO/AEO health score from audit-data.json.

Usage:
    health_score.py <audit-data.json> [--profile local-service|ecommerce] [--snapshot -1]

Reads the latest snapshot (or --snapshot index), applies the profile weights from
references/scoring_model.md, prints a score table + weighted total + grade band, and
reports deltas vs the previous snapshot when one exists. Stdlib only.
"""
import argparse
import json
import sys

WEIGHTS = {
    "local-service": {
        "technical": 15, "schema": 10, "geo-aeo": 15, "content": 15,
        "performance": 10, "local": 15, "sxo": 10, "visual": 5, "sitemap": 5,
    },
    "ecommerce": {
        "technical": 15, "schema": 10, "geo-aeo": 15, "content": 15,
        "performance": 10, "ecommerce": 15, "sxo": 10, "visual": 5, "sitemap": 5,
    },
}

BANDS = [(85, "STRONG"), (70, "GOOD"), (50, "NEEDS WORK"), (0, "CRITICAL")]


def band(score):
    return next(label for floor, label in BANDS if score >= floor)


def dim_score(entry):
    return entry["score"] if isinstance(entry, dict) else float(entry)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audit_json")
    ap.add_argument("--profile", default=None, choices=list(WEIGHTS))
    ap.add_argument("--snapshot", type=int, default=-1,
                    help="snapshot index to score (default: latest)")
    args = ap.parse_args()

    with open(args.audit_json) as f:
        data = json.load(f)

    profile = args.profile or data.get("profile")
    if profile not in WEIGHTS:
        sys.exit(f"error: unknown profile {profile!r}; pass --profile")

    snaps = data.get("snapshots") or []
    if not snaps:
        sys.exit("error: no snapshots in audit-data.json")
    snap = snaps[args.snapshot]
    prev = snaps[args.snapshot - 1] if len(snaps) > 1 and args.snapshot != 0 else None

    weights = WEIGHTS[profile]
    dims = snap.get("dimensions", {})
    total, weight_used = 0.0, 0

    print(f"Profile: {profile}   Snapshot: {snap.get('date', '?')}\n")
    print(f"{'Dimension':<14}{'Score':>6}{'Weight':>8}{'Delta':>8}")
    for dim, w in weights.items():
        if dim not in dims:
            print(f"{dim:<14}{'—':>6}{w:>8}{'':>8}  (MISSING — excluded)")
            continue
        s = dim_score(dims[dim])
        delta = ""
        if prev and dim in prev.get("dimensions", {}):
            d = s - dim_score(prev["dimensions"][dim])
            delta = f"{d:+.0f}"
        print(f"{dim:<14}{s:>6.0f}{w:>8}{delta:>8}")
        total += s * w
        weight_used += w

    extras = sorted(set(dims) - set(weights))
    for dim in extras:
        print(f"{dim:<14}{dim_score(dims[dim]):>6.0f}{'0':>8}{'':>8}  (unweighted)")

    if weight_used == 0:
        sys.exit("error: no scorable dimensions found")
    health = total / weight_used
    print(f"\nHEALTH SCORE: {health:.0f}/100  ({band(health)})", end="")
    if weight_used < 100:
        print(f"  [normalized — {100 - weight_used} weight missing]", end="")
    if prev:
        prev_dims = prev.get("dimensions", {})
        prev_total = sum(dim_score(prev_dims[d]) * w for d, w in weights.items() if d in prev_dims)
        prev_used = sum(w for d, w in weights.items() if d in prev_dims)
        if prev_used:
            print(f"  Δ {health - prev_total / prev_used:+.0f} vs {prev.get('date', 'prev')}", end="")
    print()


if __name__ == "__main__":
    main()

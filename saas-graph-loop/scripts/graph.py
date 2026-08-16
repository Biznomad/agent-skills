#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""graph.py — the build graph engine for saas-graph-loop.

The graph is the source of truth for what to build next. A loop that "replenishes
its backlog" guesses; this derives the frontier structurally from dependency edges,
so the answer is the same every time and never drifts.

Graph file: a single JSON doc (default ./saas-graph.json).

    {
      "product": "acme",
      "goal":    "shipped, first 10 paying customers",
      "nodes": {
        "billing": {
          "layer":  "build",              domain|build|gtm
          "title":  "Stripe subscriptions",
          "status": "todo",               todo|doing|done|blocked|dropped
          "needs":  ["auth"],             ids that must be done first
          "impact": 5, "reach": 4, "confidence": 4, "effort": 3,
          "phase":  "mvp",                spike|mvp|launch|scale
          "notes":  "", "evidence": ""
        }
      }
    }

Commands (all take --file, default ./saas-graph.json):

    init      --product NAME --goal TEXT
    add       ID --title T [--layer L] [--needs a,b] [--impact N] [--reach N]
                 [--confidence N] [--effort N] [--phase P] [--notes TEXT]
    link      ID --needs a,b            (replace deps)   |  --add-needs a,b
    status    ID --set STATE [--evidence TEXT]
    frontier  [--phase P] [--limit N] [--json]    unblocked + ranked; THE build queue
    critical                                      longest dependency chain to goal
    validate                                      cycles, dangling deps, orphans
    render    [--mermaid|--ascii]
    stats

Value = (impact + reach + confidence) / effort, each factor 1-5, rounded to 1dp.
Matches growth-loop's scoring shape so the two speak the same language.

Exit codes: 0 ok, 1 usage/not-found, 2 validation failed.
"""
import argparse
import json
import sys
from pathlib import Path

LAYERS = ("domain", "build", "gtm")
STATES = ("todo", "doing", "done", "blocked", "dropped")
PHASES = ("spike", "mvp", "launch", "scale")
FACTORS = ("impact", "reach", "confidence", "effort")


def load(p: Path):
    if not p.exists():
        sys.exit(f"no graph at {p} — run: graph.py init --product NAME --goal TEXT")
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, g):
    p.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def value(n):
    eff = max(1, int(n.get("effort", 3) or 3))
    got = sum(int(n.get(k, 3) or 3) for k in ("impact", "reach", "confidence"))
    return round(got / eff, 1)


def deps_done(g, nid):
    """True when every dependency of nid is done. Missing deps count as NOT done."""
    for d in g["nodes"].get(nid, {}).get("needs", []):
        if g["nodes"].get(d, {}).get("status") != "done":
            return False
    return True


def cycles(g):
    """Return the first cycle found as a list of ids, else []."""
    WHITE, GREY, BLACK = 0, 1, 2
    color = {k: WHITE for k in g["nodes"]}
    stack = []

    def walk(u):
        color[u] = GREY
        stack.append(u)
        for v in g["nodes"][u].get("needs", []):
            if v not in g["nodes"]:
                continue
            if color[v] == GREY:
                return stack[stack.index(v):] + [v]
            if color[v] == WHITE:
                hit = walk(v)
                if hit:
                    return hit
        color[u] = BLACK
        stack.pop()
        return None

    for k in g["nodes"]:
        if color[k] == WHITE:
            hit = walk(k)
            if hit:
                return hit
    return []


def frontier(g, phase=None):
    """Unblocked, unfinished nodes ranked by value desc. This is the build queue."""
    out = []
    for nid, n in g["nodes"].items():
        if n.get("status") in ("done", "dropped", "doing"):
            continue
        if phase and n.get("phase") != phase:
            continue
        if not deps_done(g, nid):
            continue
        out.append((nid, n))
    out.sort(key=lambda kv: (-value(kv[1]), kv[0]))
    return out


def longest_chain(g):
    """Longest dependency chain (the critical path). Memoized DFS over needs."""
    if cycles(g):
        return []
    memo = {}

    def depth(u):
        if u in memo:
            return memo[u]
        best = []
        for v in g["nodes"][u].get("needs", []):
            if v in g["nodes"]:
                cand = depth(v)
                if len(cand) > len(best):
                    best = cand
        memo[u] = best + [u]
        return memo[u]

    return max((depth(k) for k in g["nodes"]), key=len, default=[])


def cmd_init(a):
    p = Path(a.file)
    if p.exists() and not a.force:
        sys.exit(f"{p} exists — use --force to overwrite")
    save(p, {"product": a.product, "goal": a.goal, "nodes": {}})
    print(f"initialized {p} for {a.product!r}")


def cmd_add(a):
    p = Path(a.file)
    g = load(p)
    if a.id in g["nodes"] and not a.force:
        sys.exit(f"node {a.id!r} exists — use --force to overwrite")
    n = {"layer": a.layer, "title": a.title, "status": a.status,
         "needs": [x for x in (a.needs or "").split(",") if x.strip()],
         "phase": a.phase, "notes": a.notes or "", "evidence": ""}
    for k in FACTORS:
        n[k] = getattr(a, k)
    g["nodes"][a.id] = n
    save(p, g)
    print(f"+ {a.id}  [{a.layer}/{a.phase}]  value={value(n)}  needs={n['needs'] or '-'}")


def cmd_link(a):
    p = Path(a.file)
    g = load(p)
    if a.id not in g["nodes"]:
        sys.exit(f"no node {a.id!r}")
    cur = g["nodes"][a.id].get("needs", [])
    new = [x.strip() for x in (a.add_needs or a.needs or "").split(",") if x.strip()]
    g["nodes"][a.id]["needs"] = sorted(set(cur + new)) if a.add_needs else new
    save(p, g)
    print(f"{a.id} needs -> {g['nodes'][a.id]['needs'] or '-'}")


def cmd_status(a):
    p = Path(a.file)
    g = load(p)
    if a.id not in g["nodes"]:
        sys.exit(f"no node {a.id!r}")
    g["nodes"][a.id]["status"] = a.set
    if a.evidence:
        g["nodes"][a.id]["evidence"] = a.evidence
    save(p, g)
    unlocked = [k for k, n in g["nodes"].items()
                if a.id in n.get("needs", []) and n.get("status") not in ("done", "dropped")
                and deps_done(g, k)]
    print(f"{a.id} -> {a.set}")
    if unlocked:
        print("unlocked: " + ", ".join(sorted(unlocked)))


def cmd_frontier(a):
    g = load(Path(a.file))
    rows = frontier(g, a.phase)[: a.limit or None]
    if a.json:
        print(json.dumps([{"id": k, "value": value(n), **n} for k, n in rows], indent=2))
        return
    if not rows:
        print("frontier empty — nothing unblocked."
              " Either the phase is done or everything is waiting on a dependency.")
        return
    print(f"{'VALUE':>6}  {'ID':<26} {'LAYER':<7} {'PHASE':<7} TITLE")
    for k, n in rows:
        print(f"{value(n):>6}  {k:<26} {n.get('layer',''):<7} {n.get('phase',''):<7} {n.get('title','')}")


def cmd_critical(a):
    g = load(Path(a.file))
    chain = longest_chain(g)
    if not chain:
        sys.exit("cannot compute — graph has a cycle (run: graph.py validate)")
    print(f"critical path ({len(chain)} deep):")
    for i, k in enumerate(chain):
        n = g["nodes"][k]
        mark = {"done": "x", "doing": ">", "blocked": "!"}.get(n.get("status"), " ")
        print(f"  {'  ' * i}[{mark}] {k} — {n.get('title','')}")


def cmd_validate(a):
    g = load(Path(a.file))
    errs, warns = [], []
    cyc = cycles(g)
    if cyc:
        errs.append("cycle: " + " -> ".join(cyc))
    for k, n in g["nodes"].items():
        for d in n.get("needs", []):
            if d not in g["nodes"]:
                errs.append(f"{k}: needs unknown node {d!r}")
        if n.get("layer") not in LAYERS:
            warns.append(f"{k}: odd layer {n.get('layer')!r}")
        if n.get("status") not in STATES:
            warns.append(f"{k}: odd status {n.get('status')!r}")
        if n.get("phase") not in PHASES:
            warns.append(f"{k}: odd phase {n.get('phase')!r}")
        for f in FACTORS:
            v = n.get(f)
            if not isinstance(v, int) or not 1 <= v <= 5:
                warns.append(f"{k}: {f}={v!r} outside 1-5")
        if n.get("status") == "done" and not deps_done(g, k):
            errs.append(f"{k}: marked done but a dependency is not done")
    for w in warns:
        print("warn: " + w)
    for e in errs:
        print("ERROR: " + e)
    print(f"{len(g['nodes'])} nodes, {len(errs)} errors, {len(warns)} warnings")
    sys.exit(2 if errs else 0)


def cmd_render(a):
    g = load(Path(a.file))
    if a.mermaid:
        print("graph LR")
        for k, n in g["nodes"].items():
            shape = {"done": f'{k}["{n.get("title",k)}"]',
                     "doing": f'{k}("{n.get("title",k)}")'}.get(
                         n.get("status"), f'{k}["{n.get("title",k)}"]')
            print(f"  {shape}")
            for d in n.get("needs", []):
                print(f"  {d} --> {k}")
        done = [k for k, n in g["nodes"].items() if n.get("status") == "done"]
        if done:
            print("  classDef done fill:#1f8b4c,color:#fff,stroke:#0f5;")
            print("  class " + ",".join(done) + " done;")
        return
    by_layer = {}
    for k, n in g["nodes"].items():
        by_layer.setdefault(n.get("layer", "?"), []).append((k, n))
    for layer in LAYERS + ("?",):
        rows = by_layer.get(layer)
        if not rows:
            continue
        print(f"\n== {layer} ==")
        for k, n in sorted(rows):
            mark = {"done": "x", "doing": ">", "blocked": "!", "dropped": "-"}.get(
                n.get("status"), " ")
            dep = (" <- " + ",".join(n["needs"])) if n.get("needs") else ""
            print(f"  [{mark}] {k:<26} {value(n):>5}  {n.get('title','')}{dep}")


def cmd_stats(a):
    g = load(Path(a.file))
    n = g["nodes"]
    by = {}
    for v in n.values():
        by[v.get("status", "?")] = by.get(v.get("status", "?"), 0) + 1
    done = by.get("done", 0)
    pct = (100.0 * done / len(n)) if n else 0.0
    print(f"product: {g.get('product')}  goal: {g.get('goal')}")
    print(f"nodes: {len(n)}  " + "  ".join(f"{k}={v}" for k, v in sorted(by.items())))
    print(f"complete: {pct:.0f}%   frontier: {len(frontier(g))}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default="saas-graph.json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.set_defaults(fn=cmd_init)
    s.add_argument("--product", required=True); s.add_argument("--goal", default="")
    s.add_argument("--force", action="store_true")

    s = sub.add_parser("add"); s.set_defaults(fn=cmd_add)
    s.add_argument("id"); s.add_argument("--title", required=True)
    s.add_argument("--layer", default="build", choices=LAYERS)
    s.add_argument("--status", default="todo", choices=STATES)
    s.add_argument("--phase", default="mvp", choices=PHASES)
    s.add_argument("--needs", default=""); s.add_argument("--notes", default="")
    s.add_argument("--force", action="store_true")
    for f in FACTORS:
        s.add_argument(f"--{f}", type=int, default=3, choices=range(1, 6))

    s = sub.add_parser("link"); s.set_defaults(fn=cmd_link)
    s.add_argument("id"); s.add_argument("--needs"); s.add_argument("--add-needs")

    s = sub.add_parser("status"); s.set_defaults(fn=cmd_status)
    s.add_argument("id"); s.add_argument("--set", required=True, choices=STATES)
    s.add_argument("--evidence", default="")

    s = sub.add_parser("frontier"); s.set_defaults(fn=cmd_frontier)
    s.add_argument("--phase", choices=PHASES); s.add_argument("--limit", type=int)
    s.add_argument("--json", action="store_true")

    sub.add_parser("critical").set_defaults(fn=cmd_critical)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)

    s = sub.add_parser("render"); s.set_defaults(fn=cmd_render)
    s.add_argument("--mermaid", action="store_true"); s.add_argument("--ascii", action="store_true")

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

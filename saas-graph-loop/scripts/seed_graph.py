#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""seed_graph.py — bootstrap a greenfield SaaS build graph.

Every SaaS re-derives roughly the same skeleton: model the domain, prove the risky
bit, build auth -> core loop -> billing, then launch surfaces and GTM. This writes
that skeleton so a run starts from a real graph instead of a blank file, then gets
edited for the specific product.

    seed_graph.py --product acme --goal "10 paying customers" [--file saas-graph.json]
                  [--skip-gtm] [--skip-scale] [--force]

The seeded factors (impact/reach/confidence/effort) are DEFAULTS, deliberately
generic. Re-score them against the real product before trusting the frontier order —
the ranking is only as good as the scores. Node ids are stable, so `graph.py add`
extra product-specific nodes and link them in.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

# id, layer, phase, title, needs, (impact, reach, confidence, effort)
SEED = [
    # ---- spike: kill the product before building it -------------------------
    ("problem-evidence", "domain", "spike", "Evidence the problem is real and paid-for today", [], (5, 5, 3, 2)),
    ("competitor-scan", "domain", "spike", "Who solves this now and where they are weak", ["problem-evidence"], (4, 4, 4, 2)),
    ("domain-model", "domain", "spike", "Entities, relations, permissions (the domain graph)", ["problem-evidence"], (5, 5, 4, 3)),
    ("riskiest-spike", "build", "spike", "Throwaway spike of the single riskiest technical assumption", ["domain-model"], (5, 3, 3, 3)),
    ("stack-decision", "build", "spike", "Stack, hosting, and data store chosen and justified", ["riskiest-spike"], (4, 4, 4, 1)),

    # ---- mvp: the smallest thing someone would pay for ----------------------
    ("schema", "build", "mvp", "Schema + migrations generated from the domain model", ["domain-model", "stack-decision"], (5, 5, 5, 2)),
    ("auth", "build", "mvp", "Signup, login, session, password reset", ["stack-decision"], (5, 5, 5, 2)),
    ("permissions", "build", "mvp", "Authorization rules enforced server-side", ["auth", "schema"], (5, 4, 4, 3)),
    ("core-crud", "build", "mvp", "CRUD over the primary entity", ["schema", "permissions"], (4, 5, 5, 2)),
    ("core-workflow", "build", "mvp", "The one workflow that delivers the core value", ["core-crud"], (5, 5, 4, 4)),
    ("app-shell", "build", "mvp", "Nav, layout, empty and error states", ["auth"], (3, 5, 5, 2)),
    ("onboarding", "build", "mvp", "First-run path to first value (activation)", ["core-workflow", "app-shell"], (5, 5, 4, 3)),
    ("billing", "build", "mvp", "Plans, checkout, subscription lifecycle, webhooks", ["auth"], (5, 4, 4, 3)),
    ("transactional-email", "build", "mvp", "Verify, reset, receipt, lifecycle mail", ["auth"], (3, 4, 5, 2)),
    ("error-monitoring", "build", "mvp", "Error tracking + structured logs in prod", ["stack-decision"], (4, 3, 5, 1)),
    ("deploy-pipeline", "build", "mvp", "One-command deploy, migrations, rollback", ["stack-decision"], (5, 3, 4, 2)),
    ("backups", "build", "mvp", "Automated backups with a TESTED restore", ["deploy-pipeline", "schema"], (5, 2, 5, 2)),

    # ---- launch: surfaces a stranger meets ---------------------------------
    ("landing", "gtm", "launch", "Landing page: problem, proof, one CTA", ["problem-evidence"], (5, 5, 4, 2)),
    ("pricing-page", "gtm", "launch", "Pricing and packaging that matches billing", ["billing", "landing"], (5, 4, 3, 2)),
    ("legal", "gtm", "launch", "Terms, privacy policy, data handling", ["landing"], (3, 3, 5, 1)),
    ("analytics", "build", "launch", "Activation and conversion funnel instrumented", ["onboarding"], (4, 4, 4, 2)),
    ("support-channel", "gtm", "launch", "A real way for users to reach a human", ["landing"], (3, 4, 5, 1)),
    ("docs", "gtm", "launch", "Getting-started docs for the core workflow", ["core-workflow"], (3, 4, 4, 2)),
    ("seo-foundation", "gtm", "launch", "Titles, meta, sitemap, schema.org, llms.txt", ["landing"], (3, 5, 4, 2)),
    ("launch-readiness", "build", "launch", "Load, security, and a full e2e pass before opening", ["billing", "onboarding", "backups", "analytics"], (5, 3, 4, 3)),

    # ---- scale: only after real usage --------------------------------------
    ("first-customers", "gtm", "scale", "First 10 paying customers, by hand", ["launch-readiness", "pricing-page"], (5, 5, 3, 4)),
    ("feedback-loop", "gtm", "scale", "Structured channel from user pain to the graph", ["first-customers"], (5, 4, 4, 2)),
    ("usage-metering", "build", "scale", "Usage tracked and enforced against plan limits", ["billing", "analytics"], (4, 3, 4, 4)),
    ("admin-panel", "build", "scale", "Internal tooling for support and refunds", ["permissions"], (4, 2, 4, 3)),
    ("team-accounts", "build", "scale", "Orgs, seats, invites, roles", ["permissions", "billing"], (4, 3, 3, 4)),
    ("public-api", "build", "scale", "Documented API with keys and rate limits", ["permissions", "docs"], (3, 3, 3, 4)),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--product", required=True)
    ap.add_argument("--goal", default="shipped, first paying customers")
    ap.add_argument("--file", default="saas-graph.json")
    ap.add_argument("--skip-gtm", action="store_true")
    ap.add_argument("--skip-scale", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    p = Path(a.file)
    if p.exists() and not a.force:
        sys.exit(f"{p} exists — use --force to overwrite")

    rows = [r for r in SEED
            if not (a.skip_gtm and r[1] == "gtm")
            and not (a.skip_scale and r[2] == "scale")]
    keep = {r[0] for r in rows}

    nodes = {}
    for nid, layer, phase, title, needs, (im, re_, cf, ef) in rows:
        nodes[nid] = {"layer": layer, "title": title, "status": "todo",
                      "needs": [d for d in needs if d in keep],
                      "impact": im, "reach": re_, "confidence": cf, "effort": ef,
                      "phase": phase, "notes": "", "evidence": ""}

    p.write_text(json.dumps({"product": a.product, "goal": a.goal, "nodes": nodes},
                            indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"seeded {p}: {len(nodes)} nodes for {a.product!r}")

    graph = Path(__file__).with_name("graph.py")
    if graph.exists():
        subprocess.run([sys.executable, str(graph), "--file", str(p), "validate"], check=False)
        print()
        subprocess.run([sys.executable, str(graph), "--file", str(p), "frontier", "--limit", "5"],
                       check=False)
    print("\nNext: re-score factors against THIS product, then add product-specific nodes.")


if __name__ == "__main__":
    main()

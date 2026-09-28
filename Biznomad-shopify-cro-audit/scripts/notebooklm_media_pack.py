#!/usr/bin/env python3
"""Wave 5 — NotebookLM media pack for a Biznomad Shopify CRO audit.

Creates (or reuses) a NotebookLM notebook from the audit deliverables, generates an
infographic + video overview + audio overview, waits for them, and downloads them into
<audit-dir>/media/. Idempotent: state lives in <audit-dir>/media/notebook.json, so re-running
resumes (re-attaches to in-progress artifacts, downloads finished ones, skips done ones).

Usage:
  python3 notebooklm_media_pack.py <audit-dir> [--client "Client Name"] [--skip video,audio] [--no-wait]

Requires: `pip install notebooklm-py` and a one-time `notebooklm login`. Uses explicit notebook
ids everywhere (parallel-safe, never `notebooklm use`).
Exit codes: 0 ok · 1 error · 2 at least one artifact still generating (re-run later to download).
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

SOURCES = ["REPORT.md", "PUNCH-LIST.md", "CRO-SCORECARD.md", "P1-EXECUTION.md", "wave0-posthog.md"]
TIMEOUTS = {"infographic": 900, "audio": 1200, "video": 2700}
EXT = {"infographic": "png", "audio": "mp3", "video": "mp4"}
FOCUS = (
    "This is a Shopify store conversion-rate-optimization audit for {client}. Lead with the business "
    "impact: revenue at risk, the top P1 findings, what was already fixed, and what the owner still has "
    "to decide. Use the exact prices, percentages and page names from the report. Audience: the store "
    "owner, non-technical, about five minutes."
)


def sh(args, check=True, timeout=None):
    p = subprocess.run(["notebooklm", *args], capture_output=True, text=True, timeout=timeout)
    if check and p.returncode != 0:
        msg = (p.stderr.strip() or p.stdout.strip())[:400]
        raise RuntimeError(f"notebooklm {' '.join(args)} -> rc {p.returncode}: {msg}")
    return p


def jout(args, **kw):
    """Run with --json and unwrap the CLI's single-key envelope ({"notebook": {...}}, {"source": {...}}, {"artifact": {...}})."""
    p = sh(args + ["--json"], **kw)
    txt = p.stdout.strip()
    i = txt.find("{")
    d = json.loads(txt[i:]) if i >= 0 else {}
    if len(d) == 1 and isinstance(next(iter(d.values())), dict):
        d = next(iter(d.values()))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audit_dir")
    ap.add_argument("--client", default=None)
    ap.add_argument("--skip", default="", help="comma list of infographic,video,audio to skip")
    ap.add_argument("--no-wait", action="store_true", help="start generation and exit; re-run later to download")
    a = ap.parse_args()

    audit = Path(a.audit_dir).resolve()
    media = audit / "media"
    media.mkdir(exist_ok=True)
    state_f = media / "notebook.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {}
    client = a.client or state.get("client") or audit.parent.name.replace("-", " ")
    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    log = open(media / "media-pack.log", "a")

    def L(m):
        print(m, flush=True)
        log.write(time.strftime("%Y-%m-%dT%H:%M:%S ") + m + "\n")
        log.flush()

    def save():
        state_f.write_text(json.dumps(state, indent=1))

    sh(["status"])  # auth check; raises if not logged in

    if not state.get("notebook_id"):
        nb = jout(["create", f"CRO Audit — {client} — {audit.name}"])
        state.update({"notebook_id": nb["id"], "client": client, "sources": {}, "artifacts": {}})
        save()
        L(f"notebook created {nb['id']}")
    nid = state["notebook_id"]
    state.setdefault("sources", {})
    state.setdefault("artifacts", {})

    for name in SOURCES:
        f = audit / name
        if not f.exists() or name in state["sources"]:
            continue
        try:
            r = jout(["source", "add", str(f), "--notebook", nid])
            state["sources"][name] = r.get("id") or r.get("source_id")
            L(f"source {name} -> {r.get('id') or r.get('source_id')}")
        except Exception as e:  # keep going with the other sources
            L(f"source {name} FAILED: {e}")
        save()
    for sid in [s for s in state["sources"].values() if s]:
        sh(["source", "wait", sid, "-n", nid, "--timeout", "600"], check=False, timeout=660)

    focus = FOCUS.format(client=client)
    gens = {
        "infographic": ["generate", "infographic", focus, "--orientation", "portrait", "--detail", "detailed", "--style", "professional"],
        "video": ["generate", "video", focus, "--format", "explainer", "--style", "classic"],
        "audio": ["generate", "audio", focus, "--format", "brief", "--length", "default"],
    }
    for kind, cmd in gens.items():
        art = state["artifacts"].get(kind, {})
        if kind in skip or art.get("id") or art.get("downloaded"):
            continue
        try:
            r = jout(cmd + ["--notebook", nid, "--retry", "3"])
            aid = r.get("id") or r.get("artifact_id") or r.get("task_id")
            state["artifacts"][kind] = {"id": aid, "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
            L(f"{kind} generation started -> {aid}")
        except Exception as e:
            state["artifacts"][kind] = {"error": str(e)[:300]}
            L(f"{kind} generation FAILED to start: {e}")
        save()

    if a.no_wait:
        L("no-wait: exiting; re-run later to download")
        return 0

    rc = 0
    for kind in ("infographic", "audio", "video"):
        art = state["artifacts"].get(kind, {})
        if kind in skip or not art.get("id") or art.get("downloaded"):
            continue
        w = sh(["artifact", "wait", art["id"], "-n", nid, "--timeout", str(TIMEOUTS[kind])], check=False, timeout=TIMEOUTS[kind] + 60)
        if w.returncode == 2:
            L(f"{kind} still generating after {TIMEOUTS[kind]}s; re-run later to download")
            rc = 2
            continue
        if w.returncode != 0:
            L(f"{kind} wait failed: {w.stderr.strip()[:200]}")
            rc = 1
            continue
        out = media / f"{audit.name}-{kind}.{EXT[kind]}"
        d = sh(["download", kind, str(out), "-a", art["id"], "-n", nid], check=False, timeout=600)
        if d.returncode == 0 and out.exists():
            art["downloaded"] = str(out)
            L(f"{kind} -> {out} ({out.stat().st_size // 1024} KB)")
        else:
            L(f"{kind} download failed: {d.stderr.strip()[:200]}")
            rc = 1
        save()

    lines = ["# Media pack", f"Notebook: https://notebooklm.google.com/notebook/{nid}", ""]
    for kind, art in state["artifacts"].items():
        lines.append(f"- {kind}: {art.get('downloaded') or art.get('error') or 'pending (' + str(art.get('id')) + ')'}")
    (media / "MEDIA-PACK.md").write_text("\n".join(lines) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())

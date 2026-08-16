#!/usr/bin/env python3
"""Pairwise page-similarity matrix for doorway/duplicate detection.

Usage:
    page_similarity.py <page1> <page2> [...more]        # local HTML files or URLs
    page_similarity.py --list urls.txt                  # one file/URL per line

Metrics per pair (on extracted visible text, chrome-heavy tags stripped):
  seq     — difflib SequenceMatcher ratio (overall sameness)
  shingle — 8-word shingle Jaccard overlap (copied-block / doorway signal)

Flags: >0.85 seq = DOORWAY RISK; >0.60 seq = TEMPLATE-HEAVY; healthy = <0.60 seq
and <0.35 shingle. Stdlib only.
"""
import argparse
import difflib
import re
import sys
import urllib.request

SHINGLE = 8
UA = "Mozilla/5.0 (compatible; seo-geo-aeo-engine/1.0)"


def fetch(src):
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    with open(src, encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_text(html):
    # drop non-content + shared-chrome regions so shared nav/footer doesn't dominate
    html = re.sub(r"(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?is)<(nav|header|footer)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?is)<!--.*?-->", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"&[a-z#0-9]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def shingles(text, k=SHINGLE):
    words = text.split()
    return {" ".join(words[i:i + k]) for i in range(max(len(words) - k + 1, 0))} or {text}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def flag(seq):
    if seq > 0.85:
        return "DOORWAY RISK"
    if seq > 0.60:
        return "template-heavy"
    return "ok"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pages", nargs="*", help="HTML files or URLs")
    ap.add_argument("--list", help="file with one page path/URL per line")
    args = ap.parse_args()

    pages = list(args.pages)
    if args.list:
        with open(args.list) as f:
            pages += [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if len(pages) < 2:
        sys.exit("error: need at least 2 pages")

    texts, shingle_sets = {}, {}
    for p in pages:
        try:
            texts[p] = extract_text(fetch(p))
            shingle_sets[p] = shingles(texts[p])
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr)
    names = [p for p in pages if p in texts]
    if len(names) < 2:
        sys.exit("error: fewer than 2 pages loaded successfully")

    worst = []
    print(f"{'pair':<72}{'seq':>7}{'shingle':>9}  flag")
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            seq = difflib.SequenceMatcher(None, texts[a], texts[b]).ratio()
            sh = jaccard(shingle_sets[a], shingle_sets[b])
            label = f"{short(a)} vs {short(b)}"
            print(f"{label:<72}{seq:>7.2f}{sh:>9.2f}  {flag(seq)}")
            worst.append((seq, sh, label))

    worst.sort(reverse=True)
    n = len(worst)
    avg_seq = sum(w[0] for w in worst) / n
    avg_sh = sum(w[1] for w in worst) / n
    print(f"\npairs: {n}  avg seq: {avg_seq:.2f}  avg shingle: {avg_sh:.2f}")
    print(f"worst: {worst[0][2]}  seq {worst[0][0]:.2f} shingle {worst[0][1]:.2f}")
    risky = sum(1 for w in worst if w[0] > 0.85)
    if risky:
        print(f"⚠ {risky}/{n} pairs at DOORWAY RISK (>0.85 seq)")


def short(p, n=34):
    return p if len(p) <= n else "…" + p[-(n - 1):]


if __name__ == "__main__":
    main()

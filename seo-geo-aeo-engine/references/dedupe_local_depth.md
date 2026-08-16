# De-dupe & Local Depth

Rescue playbook for templated city/doorway pages — the pattern that turned 25 near-clone
city pages (85–89% similar) into locally-differentiated pages (~57% similar) in one pass.

## Measure first

Run `scripts/page_similarity.py` across the page cluster (files or URLs). It reports two
metrics per pair:

- **Sequence similarity** (difflib ratio on extracted text) — overall sameness.
- **Shingle overlap** (8-word shingle Jaccard) — copied-block detection; the doorway signal.

| Reading | Interpretation |
|---------|----------------|
| >85% seq | Doorway risk — search engines likely collapse/ignore the cluster |
| 60–85% seq | Template-heavy; differentiate the money sections |
| <60% seq AND <35% shingle | Healthy — shared chrome, unique substance |

Record before/after numbers in the audit dir (they're the proof of work).

## Local-depth section pattern (+300–400 words per page)

Insert ONE substantial hand-written block per city page, reusing existing styled classes
(no new CSS, no layout risk). Components:

1. **Unique local intro** — reference real neighborhoods, corridors, housing stock,
   student/military/film-industry turnover, whatever actually drives demand there.
2. **Service-area card** — the specific pickup zones/ZIPs covered from this page.
3. **Jurisdiction-correct facts card** — the regulatory details that differ by
   county/city (emissions rules, title/paperwork requirements, disposal ordinances).
   Build N variants for N jurisdictions and map pages correctly — wrong-county facts are
   worse than no facts.
4. **Two city-specific Q&As** — added to the page FAQ and its FAQPage LD.
5. **Why-us strip** — localized proof points (home-base city, response time to this area).

Writing rules: no spun text, no synonym-swapped paragraphs — write each city's block from
its actual facts. If there are no real local facts for a city, that page should probably
be consolidated, not padded.

## Hub-page de-dupe

Service pages that clone the main hub (e.g. estate-cleanouts vs junk-removal at 97%):
rewrite around the distinct JOB, not the shared service — different process, different
pricing structure, different audience section (e.g. an executor's guide: probate holds,
out-of-state coordination, realtor SLAs), service-specific FAQ. Target <45% seq vs hub.

## Builder mechanics

- Generate pages/sections with a builder script that clones an existing page's chrome
  (nav, tracking, DNI, analytics, animations) and injects the unique content — keep the
  builder in the audit dir or scratchpad and note its path in the plan.
- Per-file backups before modifying existing pages (see fix_execution_rules.md).
- After the pass: update sitemap lastmod, GSC resubmit, IndexNow ping.
- Homepage/hub must LINK to the cluster (marked link block) — link equity via sitemap
  alone doesn't flow.

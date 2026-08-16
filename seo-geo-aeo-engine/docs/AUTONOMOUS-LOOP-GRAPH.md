# Autonomous SEO/GEO/AEO Engine: Loop Graph & Human-in-the-Loop Gate Architecture

## 1. Autonomous Loop Graph (Mermaid)

```mermaid
flowchart TD
    A[Schedule / Cron Trigger] --> B[Step 0 & Preflight\nsite_preflight.sh]
    B --> C[Parallel Audit Wave\n9 Core + Conditional Specialists]
    C --> D[Compute Health Score\nhealth_score.py]
    D --> E[Classify Action Plan\nPhase 0-3 + AI-Doable Tagging]
    
    E --> F{QA Gate 1: Pre-Check\nNon-degradation & Similarity}
    F -- Fail --> G[Log QA Failure & Alert]
    F -- Pass --> H{Human Approval Gate\nTelegram / CLI Inline Buttons}
    
    H -- Rejected --> I[Store Feedback in Memory & Exit Loop]
    H -- Approved --> J[Create File Backups\n.bak-pre-YYYYMMDDHHMMSS]
    
    J --> K[Surgical Execution\nApply Approved Fixes]
    K --> L{QA Gate 2: Post-Check\nSchema, 200 OK, Tracking}
    
    L -- Fail --> M[AUTO-ROLLBACK\nRestore .bak File]
    M --> N[Alert Owner via Telegram\nCircuit Breaker Tripped]
    
    L -- Pass --> O[Deployment & Indexing\nGSC API + IndexNow Ping]
    O --> P[Generate Delta Report & Score Boost]
    P --> Q[Send Summary Card to Telegram]
    Q --> R[Sleep Until Next Loop Cycle]
```

---

## 2. 5-Stage Autonomous Execution Protocol

### Stage 1: Trigger & Preflight
- **Interval**: Weekly or Event-Driven (Git Push / Deploy).
- **Execution**: `scripts/site_preflight.sh <domain>`.
- **Outputs**: `preflight.txt` (HTTP codes, SSL, AI crawler accessibility, `llms.txt` presence, sitemap counts).

### Stage 2: Concurrent Specialist Audit & Scoring
- Specialist agents (`seo-technical`, `seo-schema`, `seo-geo`, `seo-local`, `seo-content`, `seo-performance`, `seo-sxo`, `seo-visual`, `seo-sitemap`) run in parallel.
- Score merged into `audit-data.json` via `scripts/health_score.py`.

### Stage 3: QA Gate 1 (Pre-Execution Inspection)
- **Check 1**: Page Similarity check (`scripts/page_similarity.py < threshold`).
- **Check 2**: Owner Directives check (e.g. "Do not touch hero video animation").
- **Check 3**: Syntax & Linting pre-check for Liquid/HTML/JSON-LD.

### Stage 4: Human Approval Gate (Telegram / CLI)
- **Channel**: Telegram Business Bot or CLI Prompt.
- **Message Content**: Proposed batch items, total score impact projection, risk assessment.
- **Buttons**:
  - `[Approve Phase 0 (Trust & Safety)]`
  - `[Approve All AI-Doable Fixes]`
  - `[Reject Batch / Request Modifications]`

### Stage 5: Gated Fix, QA Gate 2, & Auto-Rollback
- **Pre-Fix**: Write timestamped `.bak-pre-<slug>-<YYYYMMDDHHMMSS>` files.
- **Fix Execution**: Apply changes surgical edit by edit.
- **Post-Fix Verification**:
  - Valid JSON-LD schema parsing (Google Structured Data API / local validator).
  - HTTP 200 response check.
  - Tracking pixels & DNI lines verified intact.
- **Fail Action**: Instant automatic rollback from `.bak-pre-` backup on any test failure.

---

## 3. Circuit Breaker Rules

1. **Max Auto-Rollbacks**: If 2 consecutive fixes trigger rollbacks, freeze the engine and alert human.
2. **Shopify Guardrail**: Never touch live themes directly; edits execute on unpublished dev theme until human approves live push.
3. **Tracking Safety**: If Google Tag Manager or DNI tracking line is altered/broken, immediate emergency rollback.

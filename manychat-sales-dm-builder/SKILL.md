---
name: manychat-sales-dm-builder
description: Use when building, auditing, or documenting a ManyChat sales DM ecosystem for a client, especially Instagram/Facebook Click-to-DM, comment-to-DM, quiz/product finder, lead capture, support handoff, and draft-to-live workflows.
metadata:
  short-description: Build repeatable ManyChat sales DM funnels
---

# ManyChat Sales DM Builder

Use this skill to audit and build a client-ready ManyChat DM sales ecosystem. The default output should be a safe draft automation plus a launch checklist. Never publish or set live without explicit user approval.

## Operating Rules

- Build in draft mode first.
- Do not click `Set Live` unless the user explicitly approves that exact action.
- Do not refresh Facebook, Instagram, TikTok, or Google permissions unless explicitly approved.
- Do not reveal API tokens, page tokens, or secrets in chat or docs.
- Use ManyChat API only for tags/custom fields and read-only account checks. ManyChat flow creation/editing is UI-only.
- Before tag/custom-field setup, run the redaction-safe API access checker when available; never print raw tokens or account payloads.
- For tag/custom-field setup, prefer `scripts/run-manychat-tag-field-setup.mjs --dry-run` before `--apply`; require `APPROVE TAG FIELD DRY RUN` for the non-mutating check and `APPROVE TAG FIELD APPLY` before creating missing tags or fields.
- If ManyChat AI Builder starts producing trivia, appointment, or generic templates, switch to manual builder.
- Customer decisions must be button-first. Do not leave visible copy that says `reply`, `type`, `text`, or `send` a keyword when that choice should be a button or quick reply; reserve typed input for order numbers, checkout email/phone, or open support context.

## Discovery Checklist

1. Confirm client/account name and active channels.
2. Open `Automation` and identify the relevant folder.
3. Audit existing flows:
   - status: live, stopped, draft
   - triggers
   - runs
   - CTR
   - first message copy
   - branch buttons
   - capture points
   - support handoff
4. Note warnings:
   - channel permissions lost
   - wallet/billing warning
   - disabled triggers
   - broken links
5. Search client server/docs for prior funnel specs, product lists, offers, tags, and integration notes.
6. If the operator browser redirects to sign-in, the API token returns Unauthorized, or channel permissions are unhealthy, start with the generated live access unlock runbook and API access check.
7. If ManyChat's visible Google sign-in button focuses but does not open OAuth in the Codex built-in browser, use the generated direct `/auth/google?return=...` fallback route and let the human operator complete credentials/MFA/consent.
8. After OAuth succeeds, use the generated post-login resume checklist before touching live canvas controls so workspace, draft state, warnings, and first proof are captured.

## Recommended Sales Ecosystem

Core flows:

- `ROUTER-v2`: front door for organic DM, keyword, comment, story, and paid DM traffic.
- `PRODUCT-FINDER-v2`: quiz/product match flow.
- `CAPTURE-OFFER-v2`: email/SMS capture and first-order code.
- `AD-ROUTER-v2`: Click-to-DM ad entry point.
- `COMMENT-TO-DM-v2`: reel/post comment keyword entry.
- `ABANDONED-CART-DM-v2`: cart recovery where compliant and integrated.
- `POST-PURCHASE-v2`: review, replenishment, cross-sell.
- `SUPPORT-HANDOFF-v2`: order/help triage and live chat assignment.
- `REACTIVATION-v2`: opted-in winback.

## Tag And Field Setup

Create these categories when useful:

- source tags: ad, comment, story reply, DM keyword, ref URL, QR, organic
- intent tags: product finder, best sellers, bundle, reviews, support, order status, wholesale, abandoned cart
- goal tags: energy, immunity, digestion, skin, stress/sleep, general wellness
- format tags: gel, gummies, raw, bundle, unsure
- lifecycle tags: new lead, warm lead, hot lead, customer, repeat, VIP, replenishment, winback
- support tags: support open, human needed, order status, refund, product question, resolved

Use custom fields for:

- primary goal
- preferred format
- quiz answer value driver
- recommended product
- coupon code
- cart URL
- cart value
- last purchase date/product
- support issue
- support order number

## Product Photos

Use product photos in decision moments, not everywhere.

Best placements:

- quiz result/product recommendation
- best sellers branch
- bundle comparison
- social proof/review module
- cart recovery
- post-purchase usage instructions
- replenishment reminders

Avoid product photos in:

- consent prompts
- support triage
- every smart-delay reminder
- very short re-entry nudges

Image block pattern:

```text
{PRODUCT_NAME}

Best for: {USE_CASE}.

- {POINT_1}
- {POINT_2}
- {POINT_3}

{CTA}
```

## Health Knowledge Layer

Use a knowledge layer when the client sells wellness, supplements, herbs, nutraceuticals, or health-adjacent products.

Rules:

- The bot is educational, not medical.
- Never diagnose, treat, cure, mitigate, or prevent disease in DM copy.
- Ask safety questions before product suggestions when the user mentions ailments, symptoms, medication, pregnancy, breastfeeding, children, thyroid, autoimmune, liver, kidney, surgery, allergies, or side effects.
- Route red flags and high-risk questions to emergency care, clinician/pharmacist guidance, or human handoff.
- Use research sources to explain evidence limits, not to force a sale.
- Recommend products only for general wellness goals and format preferences.

Recommended source hierarchy:

- NCCIH herb/supplement safety pages
- NIH Office of Dietary Supplements fact sheets
- FDA supplement and claim guidance
- FTC health product advertising guidance
- PubMed systematic reviews and clinical reviews
- Client product labels, COAs, and lab tests

For NotebookLM:

1. Create one notebook per client knowledge base.
2. Add only curated sources.
3. Store a source manifest with URLs and rationale.
4. Ask NotebookLM for cited summaries.
5. Convert the answer into short DM-safe language.
6. Preserve evidence limitations and safety warnings.

## Manual Build Workflow

1. Create a new automation in the client folder.
2. Choose `Start from a blank canvas`.
3. Select the primary channel, usually Instagram.
4. Rename immediately with a draft-safe name:
   `{CLIENT}-ROUTER-v2-CLEAN-DRAFT`
5. Add a concise first message:
   `Welcome to {BRAND}. What can I help you with today?`
6. Add button-first support copy:
   `Tap the path that fits best. Support is here too if you need order help.`
7. Add 3 primary routes:
   - `Find My Match`
   - `Shop Best Sellers`
   - `Bundle Save`
8. Connect each button to a separate message step.
9. Write branch copy in one clean pass. Avoid repeated replacement attempts if the editor is appending text.
10. Add at least one Quick Reply to the first message if using Instagram Ads trigger.
11. Add actions/tags after message structure is stable.
12. Add triggers last.
13. Preview/test.
14. Request explicit approval before publishing.

## Branch Copy Template

Router:

```text
Welcome to {BRAND}. What can I help you with today?

Tap the path that fits best. Support is here too if you need order help.
```

Find My Match:

```text
Quick Match: what are you focused on right now?

Choose the closest goal below and I will point you to the best option and bundle.
```

Best Sellers:

```text
Our best sellers are the easiest place to start.

Top picks:
1. {PRODUCT_1}
2. {PRODUCT_2}
3. {BUNDLE_1}

Want a first-order code or help choosing? Tap the next step below.
```

Bundle:

```text
Bundle Save picks:

{BUNDLE_1}: {SHORT_REASON}
{BUNDLE_2}: {SHORT_REASON}
{BUNDLE_3}: {SHORT_REASON}

Pick the bundle path that feels closest, or compare first.
```

Support:

```text
Support triage: what do you need help with?

Choose the closest option below so we can route you faster.

If it is about an order, the order-help path will ask for your order number and checkout email or phone privately.
```

## Click-To-DM Ad Viewer Strategy

Do not promise automatic DMs to passive ad viewers. Use this compliant pattern:

1. Build Meta custom audience from ad/video viewers.
2. Retarget them with a Click-to-DM ad.
3. CTA example: `DM MATCH to find your best {PRODUCT_CATEGORY}`.
4. In ManyChat, use `Instagram Ads` or `Facebook Ads` trigger.
5. Ensure first message has at least one Quick Reply.
6. In Ads Manager, select the saved ManyChat automation for the ad.
7. Tag the contact as paid DM source.

## Evergreen Loop Strategy

Do not build an infinite promotional DM loop. Build an evergreen re-entry system.

Inside the 24-hour window:

- immediate response
- one helpful smart-delay nudge after 5-10 minutes
- one value/FAQ nudge after 2-4 hours
- one final useful reminder around 20-23 hours

Outside the 24-hour window:

- continue through opted-in SMS/email
- use Click-to-DM retargeting ads
- use story/comment/ref URL re-entry
- use post-purchase, review, replenishment, or support events
- use allowed ManyChat/Meta re-engagement features only when applicable

Suppress promotions when:

- support is open
- refund/return issue is active
- customer recently complained
- customer opted out
- no valid messaging window exists

## 100+ Node Ecosystem Pattern

Do not make one giant unreadable automation unless the client explicitly needs it. Prefer modular automations:

- Entry routers
- Product finder
- Product result cards
- Offer capture
- Best sellers
- Bundle engine
- Social proof
- Objection handling
- Cart recovery
- Post-purchase
- Replenishment
- Re-entry
- Support
- Analytics/admin

For very advanced builds, create a node map before building. Target 100+ logical modules across the OS, not necessarily 100 nodes on one canvas.

When the client explicitly wants a 150+ node-style build inside one ManyChat draft, expand each high-intent step with secondary content blocks:

- Keep the first block focused on the immediate intent and primary CTA.
- Add a second Text block for non-buyers who need comparison, value framing, safety, proof, or support.
- Put three decision buttons on that second block.
- Route each decision button to a new message step.
- Populate the new steps immediately before creating more branches.
- Keep product-photo cards on product, comparison, bundle, review, cart, and replenishment nodes.

Example secondary decision block:

```text
Not ready to shop yet? I can help you compare first.

Pick the next thing you want to see:
```

Example buttons:

- `Compare G vs Gel`
- `Best Value Bundle`
- `Ingredient Safety`

ManyChat UI note: button title replacement may not persist with direct fill. Use keyboard replacement: click field, `Meta+A`, `Backspace`, type title, choose next-step action, `Done`.

## Consultative Sales Pattern

For higher-trust brands, add a help-first branch before the hard product routes:

- `Find My Match`
- `Ask Wellness Q`
- `Shop Best Sellers`
- `Bundle Save`
- `Support`

The `Ask Wellness Q` branch should:

- answer general education questions
- ask one clarifying question
- check safety flags
- use citations internally
- route to product only when safe and contextually useful

Preferred answer shape:

```text
I can help with general wellness education. I cannot diagnose or treat symptoms in DM.

Here is the short version: {EVIDENCE_BACKED_POINT}

Before I suggest a routine, any medication, thyroid, pregnancy/nursing, allergy, or other safety concern?
```

## Common ManyChat Pitfalls

- AI Builder may force sales quizzes into trivia format.
- Instagram Ads trigger requires at least one Quick Reply in the first message.
- Button blocks may be limited; use 3 primary routes plus keyword fallback when needed.
- Some editor fields append text instead of replacing during automation. If this happens, create a fresh clean draft and type once.
- Channel permissions warnings can block or confuse trigger setup.
- Selecting a trigger may create an unsaved trigger state; save it before navigating away, or intentionally abandon it.

## Launch Gate

Before publishing, verify:

- flow name is correct
- flow is in the right folder
- first message has quick reply if ad-triggered
- all branches are connected
- tags/actions are present
- support handoff works
- links are final
- compliance language is acceptable
- preview passes
- completion audit separates proven work from live ManyChat gates
- completion audit references the gated tag/custom-field helper, not the low-level setup script
- launch gate status report is current and matches the live evidence registers
- live account evidence register records proof for account-side gates
- live session run sheet embeds a one-page command script and action-time approval prompts before any upload, Test Request, token check, trigger QA, permission refresh, or Set Live action
- live action approval prompts exist before any upload, Test Request, token check, trigger QA, permission refresh, or Set Live action
- live approval ledger exists to track row-level approval status without granting blanket approval or storing secrets
- final gate closure packet lists the remaining blockers, exact first live actions, proof commands, and stop conditions
- live gate cockpit exists as the single-screen live-session control surface, reflects the current blockers, and points to the next gated action
- live evidence capture kit defines acceptable proof, redaction rules, and register update commands
- visible decision copy is button-first; typed keyword copy is hidden fallback only
- user explicitly approves `Set Live`

## Client Package Generator

When the user wants to replicate a DM sales OS for another client, prefer a structured client config over freehand docs.

Use this pattern:

1. Copy `client-configs/example-client.json`.
2. Fill in:
   - client and brand name
   - ManyChat workspace
   - primary flow name
   - product names, URLs, positioning, and local image paths
   - core sales routes
   - support routes
   - live order lookup endpoint if available
   - launch gates
3. Run:

```bash
node scripts/generate-client-dm-os.mjs client-configs/<client>.json generated-client-packages
```

4. Verify generated package:
   - `CLIENT_LAUNCH_COMMAND_CENTER.md`
   - `CLIENT_LAUNCH_BRIEF.md`
   - `CLIENT_DEPLOYABILITY_REPORT.md`
   - `CLIENT_RELEASE_NOTES.md`
   - `CLIENT_EVIDENCE_PACKET_INDEX.md`
   - `CLIENT_LAUNCH_READINESS_REPORT.md`
   - `CLIENT_TECHNICAL_DEPLOYMENT_RUNBOOK.md`
   - `CLIENT_HANDOFF_INDEX.md`
   - `CLIENT_LAUNCH_GATE_STATUS.json`
   - `CLIENT_LAUNCH_GATE_STATUS.md`
   - `CLIENT_LAUNCH_PACKET.md`
   - `CLIENT_LAUNCH_QA_CHECKLIST.md`
   - `CLIENT_DEPLOYMENT_EVIDENCE_MATRIX.md`
   - `CLIENT_OPERATOR_CANVAS_QA_WORKSHEET.md`
   - `CLIENT_COMPLETION_AUDIT.md`
   - `CLIENT_LIVE_ACCOUNT_EVIDENCE_REGISTER.json`
   - `CLIENT_LIVE_ACCOUNT_EVIDENCE_REPORT.md`
   - `CLIENT_LIVE_ACCESS_UNLOCK_RUNBOOK.md`
   - `CLIENT_API_ACCESS_CHECK.md`
   - `CLIENT_POST_LOGIN_RESUME_CHECKLIST.md`
   - `CLIENT_LIVE_EVIDENCE_UPDATE_GUIDE.md`
   - `CLIENT_PACKAGE_SAFETY_CHECK.md`
   - `CLIENT_BUTTON_FIRST_COPY_CHECK.md`
   - `CLIENT_BUTTON_FIRST_LIVE_CANVAS_PATCH_LIST.md`
   - `CLIENT_BUTTON_FIRST_LIVE_CANVAS_PATCH_REGISTER.json`
   - `CLIENT_BUTTON_FIRST_LIVE_CANVAS_PATCH_REPORT.md`
   - `CLIENT_BUTTON_PARITY_QA_WORKSHEET.md`
   - `CLIENT_NODE_BUTTON_MATRIX.md`
   - `CLIENT_LIVE_CANVAS_AUDIT_REGISTER.json`
   - `CLIENT_LIVE_CANVAS_AUDIT_REPORT.md`
   - `CLIENT_LIVE_NODE_DIRECTORY.json`
   - `CLIENT_LIVE_NODE_DIRECTORY.md`
   - `CLIENT_IMAGE_PREVIEW_QA_REGISTER.json`
   - `CLIENT_IMAGE_PREVIEW_QA_REPORT.md`
   - `CLIENT_PRODUCT_IMAGE_QUICK_REFERENCE.md`
   - `CLIENT_EXTERNAL_REQUEST_QA_REGISTER.json`
   - `CLIENT_EXTERNAL_REQUEST_QA_REPORT.md`
   - `CLIENT_EXTERNAL_REQUEST_REPAIR_SHEET.md`
   - `CLIENT_EXTERNAL_REQUEST_MAPPING_QUICK_REFERENCE.md`
   - `CLIENT_ORDER_LOOKUP_BRANCH_DECISION_CARD.md`
   - `CLIENT_EXTERNAL_REQUEST_SAFE_TEST_RUNBOOK.md`
   - `CLIENT_LIVE_ACTION_APPROVAL_PROMPTS.md`
   - `CLIENT_LIVE_APPROVAL_LEDGER.md`
   - `CLIENT_LIVE_APPROVAL_LEDGER.json`
   - `CLIENT_FINAL_GATE_CLOSURE_PACKET.md`
   - `CLIENT_FINAL_LIVE_GATE_EXECUTION_PLAN.json`
   - `CLIENT_FINAL_LIVE_GATE_EXECUTION_PLAN.md`
   - `CLIENT_LIVE_LAUNCH_REHEARSAL_AGENDA.md`
   - `CLIENT_ACCOUNT_OWNER_LIVE_SESSION_PREP.md`
   - `CLIENT_LIVE_SESSION_INVITE.md`
   - `CLIENT_LIVE_SESSION_MINUTES_TEMPLATE.md`
   - `CLIENT_LIVE_ACCESS_AND_CREDENTIALS_CHECKLIST.md`
   - `CLIENT_ROLE_BASED_LAUNCH_SIGNOFF_PACKET.md`
   - `CLIENT_MANYCHAT_BROWSER_OPERATIONS_RUNBOOK.md`
   - `CLIENT_LIVE_GATE_PROOF_RECEIPT_TEMPLATE.md`
   - `CLIENT_LIVE_GATE_COCKPIT.md`
   - `CLIENT_FINAL_LAUNCH_UNLOCK.md`
   - `CLIENT_API_TOKEN_INTAKE_CHECKLIST.md`
   - `CLIENT_LIVE_EVIDENCE_CAPTURE_KIT.md`
   - `CLIENT_TRIGGER_QA_REGISTER.json`
   - `CLIENT_TRIGGER_QA_REPORT.md`
   - `CLIENT_TRIGGER_QA_QUICK_REFERENCE.md`
   - `CLIENT_PAID_TRAFFIC_AUTODM_RUNBOOK.md`
   - `CLIENT_SET_LIVE_ERROR_REGISTER.json`
   - `CLIENT_SET_LIVE_ERROR_TRIAGE.md`
   - `manychat_external_request_config.md`
   - `preview/index.html`
   - copied `assets/` images

5. Validate the consolidated launch gate status before handoff:

```bash
node scripts/generate-manychat-launch-gate-status.mjs
node scripts/validate-manychat-launch-gate-status.mjs
node scripts/validate-manychat-launch-gate-status.mjs generated-client-packages/<client>/CLIENT_LAUNCH_GATE_STATUS.json
```

Also validate the final live-session cockpit whenever it is generated:

```bash
node scripts/validate-manychat-live-gate-cockpit.mjs
node scripts/validate-manychat-final-launch-unlock.mjs
node scripts/validate-manychat-api-token-intake-checklist.mjs
node scripts/print-manychat-live-session-brief.mjs
node scripts/validate-manychat-live-session-brief.mjs
node scripts/validate-manychat-live-evidence-update-guide.mjs
node scripts/validate-manychat-live-session-control-stack.mjs
node scripts/generate-manychat-live-session-control-stack-report.mjs
node scripts/validate-manychat-live-session-control-stack-report.mjs
node scripts/validate-manychat-live-session-minutes-template.mjs
node scripts/validate-manychat-live-access-credentials-checklist.mjs
node scripts/validate-manychat-role-based-launch-signoff-packet.mjs
node scripts/validate-manychat-browser-operations-runbook.mjs
node scripts/validate-manychat-live-gate-proof-receipt-template.mjs
node scripts/test-manychat-evidence-timestamp-safety.mjs
node scripts/validate-manychat-paid-traffic-autodm-runbook.mjs
node scripts/validate-manychat-agent-macro-pack.mjs
```

6. Browser-QA the generated preview before presenting it to the client.

The generated live access unlock runbook should be used first whenever the operator browser redirects to sign-in, the API token returns Unauthorized, or channel permissions are not healthy. The generated API access check should be run before tag/custom-field setup so token validity is proven without printing secrets or raw account payloads. After OAuth succeeds, use the generated post-login resume checklist before touching live canvas controls. The generated launch gate status report should be treated as the deployment scoreboard and updated after each proof register changes. The generated launch command center should be validated with `scripts/validate-manychat-launch-command-center.mjs` so its current blocker list never drifts from the launch gate status. The generated client launch brief should be validated with `scripts/validate-manychat-client-launch-brief.mjs` and opened first with stakeholders so readiness, blockers, owners, proof commands, and the exact next approval are visible without implying live approval. The generated deployability report should be validated with `scripts/validate-manychat-client-deployability-report.mjs` so package-ready, evidence-ready, and live-approved are kept separate and the current launch verdict remains tied to gate proof. The generated client release notes should be validated with `scripts/validate-manychat-client-release-notes.mjs` so the current handoff version, proof commands, blockers, and next live action remain tied to the package without embedding stale secrets or customer data. The generated evidence packet index should be validated with `scripts/validate-manychat-client-evidence-packet-index.mjs` so every launch requirement maps to proof artifacts, validation commands, live gate evidence, and approval boundaries before client handoff. The generated launch readiness report should be validated with `scripts/validate-manychat-client-launch-readiness-report.mjs` so the current go/no-go summary reflects launch gates and does not confuse package-ready with live-ready. The generated technical deployment runbook should be validated with `scripts/validate-manychat-technical-deployment-runbook.mjs` so backend order lookup operations, health checks, rollback, External Request wiring, and secret boundaries are client-facing without exposing tokens or customer data. The generated live session run sheet should be validated with `scripts/validate-manychat-live-session-run-sheet.mjs` so every remaining live action has a one-page command script, inline exact approval text, stop conditions, and safe proof commands before handoff. The generated live session brief should be generated with `scripts/generate-manychat-live-session-brief.mjs`, validated with `scripts/validate-manychat-live-session-brief-files.mjs`, printed with `scripts/print-manychat-live-session-brief.mjs`, and validated with `scripts/validate-manychat-live-session-brief.mjs` before any live session so the client package and operator terminal both show the current gate order, exact next approval, hidden-token helper, and no-permission-refresh/no-Set-Live boundary. The generated live launch rehearsal agenda should be validated with `scripts/validate-manychat-live-launch-rehearsal-agenda.mjs` so owners can rehearse exact approval boundaries, evidence commands, no-data proof rules, and stop conditions before touching live controls. The generated live approval ledger should be validated with `scripts/validate-manychat-live-approval-ledger.mjs` so every gated action stays row-level, pending until exact approval, and redaction-safe without storing secrets or customer data; use `scripts/update-manychat-live-approval-ledger.mjs` to record approved, used, expired, or denied row status without losing it on package regeneration. Validate the live session control stack with `scripts/validate-manychat-live-session-control-stack.mjs`, generate `CLIENT_LIVE_SESSION_CONTROL_STACK_REPORT.md` with `scripts/generate-manychat-live-session-control-stack-report.mjs`, and validate it with `scripts/validate-manychat-live-session-control-stack-report.mjs` so the next-action helper, final execution plan, approval prompts, approval ledger, evidence capture kit, and client copies stay synchronized before handoff. The generated completion audit should be validated with `scripts/validate-manychat-completion-audit.mjs` so package-ready and live-approved are never conflated while launch gates remain blocked, and so its evidence path stays on `scripts/run-manychat-tag-field-setup.mjs` instead of the low-level setup script. Validate client launch language with `scripts/validate-client-launch-language-safety.mjs` before handoff so client-facing markdown cannot claim ready-to-deploy, launch-approved, or traffic-safe language while required gates remain blocked. The generated final launch unlock should be validated with `scripts/validate-manychat-final-launch-unlock.mjs` so the operator closeout sheet always names the next gate, step action, exact approval request, and blocker IDs before a launch session. The generated live gate operator runbook should be generated with `scripts/generate-manychat-live-gate-operator-runbook.mjs` and validated with `scripts/validate-manychat-live-gate-operator-runbook.mjs` so the account owner can see the exact approval, Codex action, redacted proof, and stop rules on one page. The generated client package manifest should be validated with `scripts/validate-client-package-manifest.mjs` so every listed file hash, byte count, package fingerprint, and Start Here order is independently proven before handoff. The generated client handoff archive should be generated with `scripts/generate-client-handoff-archive.mjs` and validated with `scripts/validate-client-handoff-archive.mjs` so the client-facing folder can be handed off as one deterministic bundle without hiding launch blockers. The generated live evidence guide should be used to update account-side proof without exposing tokens, page secrets, customer emails, customer phone numbers, customer addresses, or payment data; validate it with `scripts/validate-manychat-live-evidence-update-guide.mjs` so source and client evidence instructions keep the hidden helper path and do not reintroduce stale direct-token setup examples. Run `scripts/test-manychat-evidence-timestamp-safety.mjs` before launch handoff or after editing evidence helper scripts so ISO timestamps remain accepted on temp register copies without triggering false phone/PII findings or mutating source live evidence. Use the generated tag and custom-field dictionary with `scripts/run-manychat-tag-field-setup.mjs --dry-run` before any `--apply`; the dry-run helper requires `APPROVE TAG FIELD DRY RUN`, apply requires `APPROVE TAG FIELD APPLY`, and both read the token from a hidden terminal prompt. Use the generated External Request repair sheet, mapping quick reference, branch decision card, and safe-test runbook before clicking `Test Request`; safe fake QA values should be used first so response mapping proof does not expose real customer data. Validate the mapping quick reference with `scripts/validate-manychat-external-request-mapping-quick-reference.mjs` before handoff so every response mapping row, failed-row command, and stop condition stays aligned with the QA register. Validate the order lookup branch decision card with `scripts/validate-manychat-order-lookup-branch-decision-card.mjs` before handoff so found/tracking, found/processing, mismatch, not-found, lookup-error, and human-fallback outcomes stay button-first, privacy-safe, and aligned with External Request proof. Use the generated product image quick reference before uploading or previewing product images; validate it with `scripts/validate-manychat-product-image-quick-reference.mjs` so Send Message #24 repair, packaged upload assets, button-continuity proof, and device-preview commands stay aligned with the image QA register. Use the generated trigger QA quick reference before attaching or testing ad, comment, keyword, or fallback entry points; validate it with `scripts/validate-manychat-trigger-qa-quick-reference.mjs` so internal-test approval, passive-viewer compliance, first-button proof, and source/route proof stay aligned with the trigger QA register. Validate the paid traffic AutoDM runbook with `scripts/validate-manychat-paid-traffic-autodm-runbook.mjs` so ad viewers stay in compliant Click-to-DM, comment-to-DM, story reply, ref URL, or opted-in re-entry paths instead of passive direct DMs. Validate the agent macro pack with `scripts/validate-manychat-agent-macro-pack.mjs` so human support and sales-assist responses keep order privacy, safety escalation, discount boundaries, support-first tone, and low-pressure conversion language intact. Use the generated live action approval prompts at action-time before uploads, `Test Request`, API-token checks, tag/custom-field setup, trigger test traffic, permission refreshes, or `Set Live`; record only row-level status in the generated live approval ledger and never treat one approval row as approval for another action. Use the generated final gate closure packet as the one-page gate summary, use the generated final live gate execution plan JSON/MD as the structured action order for the last live-account session, use the generated live launch rehearsal agenda before the final live session to rehearse owner roles and stop rules without approving live actions, use the generated next live gate action JSON/MD as the single current action with exact approval text, keep the generated live gate operator runbook open as the account-owner approval and proof guide, keep the generated live session brief open as the client-facing launch-session boundary, keep the generated live gate cockpit open as the single-screen live-session control surface, use `scripts/print-manychat-live-session-brief.mjs` as the command-side current-state brief, use the generated final launch unlock as the operator closeout sheet for the next exact gate, and use the generated live evidence capture kit to decide what proof is acceptable, what must be redacted, and which update command records the proof. The generated safety, button-first checks, live canvas patch list, live canvas patch register, live canvas patch report, button parity QA worksheet, node/button matrix, live canvas audit register, live node directory, image preview QA register, External Request QA register, trigger QA register, paid traffic AutoDM runbook, and Set Live error triage register should be reviewed before client handoff. Use the paid traffic AutoDM runbook to keep ad viewers in a compliant Click-to-DM/comment-to-DM retargeting path instead of promising direct DMs to passive ad viewers. Use `scripts/update-manychat-button-first-patch-register.mjs` to mark individual button-first patch items `patched_pending_qa`, `verified`, or `not_applicable` after the live ManyChat card has been updated and previewed with redacted proof. Use `scripts/generate-manychat-launch-gate-status.mjs` and `scripts/validate-manychat-launch-gate-status.mjs` after any proof update so the client-facing launch gate table stays current. Use `scripts/update-manychat-live-canvas-audit.mjs` to mark individual live canvas nodes/cards `verified`, `failed`, or `not_applicable` after reviewing them in ManyChat. Use the live node directory to walk every numbered `Send Message` node in large builds, and use `scripts/update-manychat-live-node-directory.mjs` to record per-node proof safely. Use `scripts/update-manychat-image-preview-qa.mjs` to record device-preview proof for product image rendering. Use `scripts/update-manychat-external-request-qa.mjs` to record method, URL, header, body, response mapping, branch, and privacy proof for live order lookup. Use `scripts/update-manychat-trigger-qa.mjs` to record ad, comment, and keyword trigger proof. Use `scripts/update-manychat-set-live-errors.mjs` to record Set Live validator attempts and pointed errors after explicit approval to run the validator. The generator is a scaffold, not a substitute for live ManyChat QA. The final live gates remain API/token access, channel permissions, button-first live card patch verification, External Request wiring, product image device preview, trigger QA, and Set Live validation.

Validate wellness and health-claim language with `scripts/validate-manychat-health-claim-safety.mjs` before handoff so customer-facing source and client artifacts cannot drift into unguarded supplement, disease, cure, treatment, prevention, or guaranteed-outcome claims. Include that validator alongside the client launch-language scan, package safety scan, launch brief, deployability report, release notes, evidence packet index, launch readiness report, acceptance checklist, role signoff packet, and reusable skill verification.

Use `scripts/generate-manychat-external-request-fake-qa-fixture.mjs` and `scripts/validate-manychat-external-request-fake-qa-fixture.mjs` whenever the live order lookup External Request still needs a safe ManyChat response sample. The generated fake QA fixture, `CLIENT_EXTERNAL_REQUEST_FAKE_QA_FIXTURE.md`, should sit beside `CLIENT_EXTERNAL_REQUEST_SAFE_TEST_RUNBOOK.md` and define the exact fake contact field values, request body, expected safe `not_found` response, forbidden proof contents, mapping checklist, and redacted evidence commands before anyone clicks `Test Request`.

Regenerate the launch evidence worklist with `scripts/generate-manychat-launch-evidence-worklist.mjs` before client handoff and validate it through `scripts/validate-client-launch-package-sync.mjs`. The product image QA rows in `CLIENT_LAUNCH_EVIDENCE_WORKLIST.md` should name the packaged ManyChat upload assets, such as `generated-client-packages/example-brand/assets/black-gold-gummies-manychat-upload.jpg`, instead of pointing operators at source-only `product_images/` paths during the live session.

Use `scripts/validate-manychat-account-owner-live-session-prep.mjs` before a final live-account session. The generated account-owner prep sheet, `CLIENT_ACCOUNT_OWNER_LIVE_SESSION_PREP.md`, should sit beside `CLIENT_NEXT_LIVE_GATE_ACTION.md`, `CLIENT_API_TOKEN_INTAKE_CHECKLIST.md`, `CLIENT_LIVE_GATE_COCKPIT.md`, `CLIENT_FINAL_LIVE_GATE_EXECUTION_PLAN.md`, and `CLIENT_LIVE_APPROVAL_LEDGER.md`, and should tell the account owner what to have ready, the exact next approval text, hard boundaries, and stop conditions without exposing secrets or implying approval for any other action.

Use `scripts/validate-manychat-live-session-invite.mjs` before sending a launch-session scheduling note. The generated live session invite, `CLIENT_LIVE_SESSION_INVITE.md`, should give the account owner a ready-to-send subject, attendees, agenda, prep links, exact approval text, closeout commands, and no-secret calendar-note rules without approving token use, Test Request, uploads, trigger tests, permission refreshes, traffic, or `Set Live`.

Use `scripts/validate-manychat-live-session-minutes-template.mjs` before a gated live-account session. The generated live session minutes template, `CLIENT_LIVE_SESSION_MINUTES_TEMPLATE.md`, should capture session header, opened source docs, exact approval read aloud, approval log, work performed, evidence captured, stop conditions, closeout commands, and carry-forward blockers without storing secrets, customer data, or blanket approval.

Use `scripts/validate-manychat-live-access-credentials-checklist.mjs` before a gated live-account session. The generated live access and credentials checklist, `CLIENT_LIVE_ACCESS_AND_CREDENTIALS_CHECKLIST.md`, should name ManyChat, ManyChat API token, Shopify/order lookup, n8n endpoint, Meta/IG test account, product image asset, and support/sales owners; confirm no-secret credential handling; and prevent tokens, customer data, OAuth/MFA details, or broad credential approvals from being copied into docs, screenshots, chat, or calendar notes.

Use `scripts/validate-manychat-role-based-launch-signoff-packet.mjs` before first traffic or final go/no-go review. The generated role-based launch signoff packet, `CLIENT_ROLE_BASED_LAUNCH_SIGNOFF_PACKET.md`, should keep business, build, technical/order lookup, support/sales, traffic, and compliance/safety owners signing only their lane while preserving live-gate blockers, exact approval boundaries, safety scans, package proof, and `NO_GO` status until every required gate is verified or not applicable.

Use `scripts/validate-manychat-browser-operations-runbook.mjs` before operating ManyChat in the Codex built-in browser or any shared operator browser. The generated browser operations runbook, `CLIENT_MANYCHAT_BROWSER_OPERATIONS_RUNBOOK.md`, should convert the current live gates into browser preflight checks, exact-action boundaries, External Request mapping steps, product image preview steps, trigger QA steps, stop conditions, and redacted proof commands without implying approval for live actions.

Use `scripts/validate-manychat-live-gate-proof-receipt-template.mjs` after adding or regenerating receipt documentation. The generated proof receipt template, `CLIENT_LIVE_GATE_PROOF_RECEIPT_TEMPLATE.md`, should give operators a redaction-safe client receipt format for each closed live gate, including approval source, register update, validator result, package closeout result, carry-forward blocker, and final launch receipt fields without storing secrets or customer data.

Use `scripts/generate-manychat-order-lookup-branch-decision-card.mjs` and `scripts/validate-manychat-order-lookup-branch-decision-card.mjs` whenever the live order lookup External Request still needs outcome-branch QA. The generated order lookup branch decision card, `CLIENT_ORDER_LOOKUP_BRANCH_DECISION_CARD.md`, should sit beside the External Request repair sheet, mapping quick reference, safe-test runbook, and fake QA fixture, and give operators one-screen outcome logic for found/tracking, found/processing, mismatch, not-found, lookup-error, and human-fallback paths. Treat missing button continuity, promo-first support copy, real-customer test data, unsaved mapping rows, or private order data in proof as stop conditions.

Use `scripts/generate-manychat-e2e-scenario-matrix.mjs` and `scripts/validate-manychat-e2e-scenario-matrix.mjs` before launch rehearsal. The generated E2E scenario matrix, `CLIENT_E2E_SCENARIO_MATRIX.md`, should prove button-first sales paths, service/order lookup paths, safety handoff, discount boundaries, lifecycle nudges, trigger entry, product images, and redacted proof rules as full customer journeys before final launch approval.

Use `scripts/generate-manychat-pilot-ramp-plan.mjs` and `scripts/validate-manychat-pilot-ramp-plan.mjs` before first traffic. The generated pilot ramp plan, `CLIENT_PILOT_RAMP_PLAN.md`, should name business, traffic, support, and technical owners; define day-0 through day-7 traffic phases; list stop conditions; and give rollback actions that pause traffic before changing live flow behavior.

Use `scripts/generate-manychat-operator-training-guide.mjs` and `scripts/validate-manychat-operator-training-guide.mjs` before client handoff or first traffic. The generated operator training guide, `CLIENT_OPERATOR_TRAINING_GUIDE.md`, should train support, sales, paid traffic, technical/order lookup, and business owners on Inbox triage, concise sales assist, discount restraint, order lookup privacy, wellness safety handoff, pilot operations, and end-of-shift proof rules.

Use `scripts/generate-manychat-conversation-qa-rubric.mjs` and `scripts/validate-manychat-conversation-qa-rubric.mjs` before pilot launch. The generated conversation QA rubric, `CLIENT_CONVERSATION_QA_RUBRIC.md`, should give support and sales owners a 100-point review system, critical-fail rules, review cadence, coaching actions, and stop-score thresholds for real DM conversations.

Use `scripts/generate-manychat-sla-escalation-matrix.mjs` and `scripts/validate-manychat-sla-escalation-matrix.mjs` before pilot launch. The generated SLA escalation matrix, `CLIENT_SLA_ESCALATION_MATRIX.md`, should name client/business, support, sales, traffic, technical/order lookup, and safety owners; define response targets; describe pause rules; and prevent promo pressure during support, privacy, or wellness-safety issues.

Use `scripts/generate-manychat-iteration-backlog.mjs` and `scripts/validate-manychat-iteration-backlog.mjs` before launch handoff and weekly optimization. The generated iteration backlog, `CLIENT_ITERATION_BACKLOG.md`, should convert QA findings, customer confusion, sales opportunities, support load, creative/image needs, and measurement gaps into approved change requests instead of ad hoc live edits.

Use `scripts/generate-manychat-personalization-map.mjs` and `scripts/validate-manychat-personalization-map.mjs` before scaling traffic or optimizing campaigns. The generated personalization map, `CLIENT_PERSONALIZATION_MAP.md`, should translate quiz answers, ad/source context, Shopify lifecycle signals, price friction, support state, and safety context into button-first next-best actions without over-personalizing or exposing private data.

Use `scripts/generate-manychat-reentry-compliance-map.mjs` and `scripts/validate-manychat-reentry-compliance-map.mjs` before enabling lifecycle, nurture, replenishment, retargeting, or re-entry paths. The generated re-entry compliance map, `CLIENT_REENTRY_COMPLIANCE_MAP.md`, should keep the evergreen loop messaging-window aware, opt-in based, non-spammy, and clear about when to use automated DM, human Inbox, paid Click-to-DM/comment/story/ref URL re-entry, or owned-channel email/SMS.

Use `scripts/generate-manychat-emergency-rollback-runbook.mjs` and `scripts/validate-manychat-emergency-rollback-runbook.mjs` before live traffic. The generated emergency rollback runbook, `CLIENT_EMERGENCY_ROLLBACK_RUNBOOK.md`, should give traffic, support, technical/order lookup, and client owners a one-page kill-switch order for wrong routes, order privacy risk, External Request failures, product image failures, support/safety incidents, permission warnings, and Set Live issues.

Use `scripts/generate-manychat-launch-day-war-room.mjs` and `scripts/validate-manychat-launch-day-war-room.mjs` before first traffic. The generated launch-day war room board, `CLIENT_LAUNCH_DAY_WAR_ROOM.md`, should give client/business, support, sales, traffic, technical/order lookup, and safety owners a timed command surface for first-hour proof, owner coverage, stop conditions, redacted evidence commands, and day-1 closeout.

Use `scripts/generate-manychat-live-launch-rehearsal-agenda.mjs` and `scripts/validate-manychat-live-launch-rehearsal-agenda.mjs` before a final live-account session. The generated live launch rehearsal agenda, `CLIENT_LIVE_LAUNCH_REHEARSAL_AGENDA.md`, should give owners a 45-minute dry rehearsal for exact action approvals, hidden token handling, External Request fake QA, product image repair, trigger QA, evidence commands, and stop rules without approving any live action.

Use `scripts/generate-manychat-sales-concierge-playbook.mjs` and `scripts/validate-manychat-sales-concierge-playbook.mjs` before the sales pilot. The generated sales concierge playbook, `CLIENT_SALES_CONCIERGE_PLAYBOOK.md`, should guide human or AI-assisted sales agents through product-fit decisions, objection handling, bundle/value-first discount discipline, agentic next-best-action cues, and human takeover triggers.

Use `scripts/generate-manychat-attribution-tracking-plan.mjs` and `scripts/validate-manychat-attribution-tracking-plan.mjs` before scaling traffic. The generated attribution tracking plan, `CLIENT_ATTRIBUTION_TRACKING_PLAN.md`, should map ManyChat source tags, UTM-bearing links, Shopify discount usage, assisted revenue, source quality, support load, and redacted evidence commands without storing customer private data.

Use `scripts/generate-manychat-operator-drill-pack.mjs` and `scripts/validate-manychat-operator-drill-pack.mjs` before pilot traffic. The generated operator drill pack, `CLIENT_OPERATOR_DRILL_PACK.md`, should rehearse sales, support, order lookup, privacy, wellness safety, trigger routing, product images, and re-entry moments so the team proves button-first customer handling before traffic.

Use `scripts/generate-manychat-operator-drill-evidence.mjs`, `scripts/update-manychat-operator-drill-evidence.mjs`, and `scripts/validate-manychat-operator-drill-evidence.mjs` to record the result of those role-play drills. The generated `CLIENT_OPERATOR_DRILL_EVIDENCE_REPORT.md` and `CLIENT_OPERATOR_DRILL_EVIDENCE_REGISTER.json` should show passed, failed, retry-required, or not-applicable outcomes with redacted proof before first traffic; drill completion is never approval to click `Set Live`, run `Test Request`, upload images, refresh permissions, or use a fresh API token.

Use `scripts/generate-manychat-replication-playbook.mjs` and `scripts/validate-manychat-replication-playbook.mjs` before packaging reusable client handoffs. The generated `CLIENT_REPLICATION_PLAYBOOK.md` should document clone phases, config replacement rules, evidence maps, custom-skill update steps, and non-negotiable live-action approval boundaries so this DM OS can be adapted to another ecommerce client without copying stale Example Brand proof.

## Final Live Gate Evidence Pattern

For any client build that is structurally complete but still waiting on live ManyChat proof, create a final live gate packet:

- `CLIENT_LIVE_ACTION_APPROVAL_PROMPTS.md`: exact approval language for uploads, External Request `Test Request`, fresh API-token checks, trigger QA, permission refresh, and `Set Live`.
- `CLIENT_LIVE_APPROVAL_LEDGER.md` and `CLIENT_LIVE_APPROVAL_LEDGER.json`: row-level approval status ledger for the gated live actions; it never grants blanket approval and must not contain secrets or customer data.
- `CLIENT_FINAL_GATE_CLOSURE_PACKET.md`: the one-page closure cockpit listing blocker status, next live action, proof command, and stop condition.
- `CLIENT_FINAL_LIVE_GATE_EXECUTION_PLAN.json` and `CLIENT_FINAL_LIVE_GATE_EXECUTION_PLAN.md`: structured final-session execution order with gate dependencies, approval prompt references, steps, evidence update commands, and stop conditions.
- `CLIENT_NEXT_LIVE_GATE_ACTION.json` and `CLIENT_NEXT_LIVE_GATE_ACTION.md`: the single next action to request, including exact approval text and the matching proof command.
- `CLIENT_LIVE_GATE_OPERATOR_RUNBOOK.md`: the one-page action-time operator runbook that separates account-owner approval, Codex action, redacted proof capture, and stop rules for the live session.
- `CLIENT_LIVE_SESSION_BRIEF.md`: the client-facing launch-session boundary that restates current blockers, exact next approval text, command path, action boundaries, and stop conditions.
- `CLIENT_ACCOUNT_OWNER_LIVE_SESSION_PREP.md`: the account-owner prep sheet that states what to have ready, the exact next approval, hard boundaries, and stop conditions before the session.
- `CLIENT_LIVE_SESSION_INVITE.md`: the ready-to-send scheduling note with attendees, agenda, prep links, exact approval text, and no-secret calendar-note rules.
- `CLIENT_LIVE_SESSION_MINUTES_TEMPLATE.md`: the redaction-safe session record for action approvals, work performed, evidence accepted, stop conditions, closeout commands, and carry-forward blockers.
- `CLIENT_LIVE_ACCESS_AND_CREDENTIALS_CHECKLIST.md`: the no-secret access readiness sheet for ManyChat, Shopify/order lookup, n8n, Meta/IG, internal test accounts, product assets, and support/sales coverage.
- `CLIENT_ROLE_BASED_LAUNCH_SIGNOFF_PACKET.md`: the role-by-role go/no-go packet that keeps each owner accountable without overriding launch gates or exact approvals.
- `CLIENT_MANYCHAT_BROWSER_OPERATIONS_RUNBOOK.md`: the in-browser operator checklist for API-token proof, External Request mappings, product image previews, trigger QA, stop rules, and redacted proof commands.
- `CLIENT_LIVE_GATE_PROOF_RECEIPT_TEMPLATE.md`: the client-safe proof receipt template for recording approval source, register update, validator result, package closeout, and final launch receipt fields after each closed gate.
- `CLIENT_LIVE_GATE_COCKPIT.md`: the single-screen operator control surface that keeps blockers, next action, approval boundaries, safe test values, image upload target, trigger rules, and evidence commands visible during the live session.
- `CLIENT_FINAL_LAUNCH_UNLOCK.md`: the operator closeout sheet listing the non-negotiable approval boundary, next live gate, blocker IDs, exact approval request, and validation command.
- `CLIENT_API_TOKEN_INTAKE_CHECKLIST.md`: the safe first-gate checklist for fresh ManyChat API token handling, including the no-storage rule, approval prompt, hidden local token helper, redacted checker command, and evidence fields.
- API token intake checklist: use it before any fresh ManyChat token is entered, prefer `scripts/run-manychat-api-token-check.mjs` so the token is read from a hidden terminal prompt instead of shell history, and record only redacted proof.
- `CLIENT_LIVE_EVIDENCE_CAPTURE_KIT.md`: proof matrix, redaction rules, register update commands, and stop conditions.

Evidence discipline:

- Never treat a screenshot or note as launch proof until the matching register update command is run and validated.
- Use the final live gate execution plan as the machine-readable and human-readable source for the live-session action order.
- Use the next live gate action file when asking the operator for the next exact approval so the request names the action, destination, data path, and stop condition without creating blanket approval.
- Use the live gate operator runbook as the human-facing action-time guide so the account owner can see what they approve, what Codex will do, what proof will be recorded, and when everyone must stop.
- Use `scripts/print-manychat-live-session-brief.mjs` as the command-side current-state brief before a live session so archive proof, open gates, exact approval text, hidden-token helper, and live-action boundaries are visible in one safe terminal output.
- Use the live approval ledger to record row-level status only; a yes to one row never approves any other row. Update the ledger with `scripts/update-manychat-live-approval-ledger.mjs` so approved/used/expired/denied state survives regeneration.
- Validate the final launch unlock with `scripts/validate-manychat-final-launch-unlock.mjs` before handoff so the next approval request cannot drift from the live gate cockpit.
- Keep the live gate cockpit open during the live session so the operator does not have to jump between several files while a permission warning, upload, Test Request, trigger QA, or token check is on screen.
- For fresh ManyChat API tokens, run `scripts/print-manychat-next-live-action.mjs`, run `scripts/print-manychat-live-session-brief.mjs`, follow `CLIENT_API_TOKEN_INTAKE_CHECKLIST.md`, prefer `scripts/run-manychat-api-token-check.mjs` for hidden local token entry, pass the token only as `MANYCHAT_API_TOKEN`, and record only redacted proof.
- Never store raw tokens, shared secrets, customer emails, customer phones, addresses, tracking numbers, payment data, private order URLs, or selected-contact identifiers in docs.
- For External Request proof, use a fake QA lookup first, then use the order lookup branch decision card to verify customer-facing outcomes; stop if the selected contact is real, private order data appears, a mapping row is unsaved, or a branch lacks a next-step button.
- For image proof, require rendered image preview; URL text or placeholders remain failed.
- For trigger proof, use internal test accounts only and keep passive ad viewers in compliant Click-to-DM/comment-to-DM/re-entry paths.
- After every live proof update, rerun the package preparation command and keep launch `NO-GO` until source and client launch gate files show zero blockers.

## Manual Build Recipe: 150+ Node DM Sales OS

When a client explicitly asks for a very large DM ecosystem, build in clusters. Do not create empty branches just to increase the node count. Each cluster should add real sales utility and at least one return path.

Recommended cluster order:

1. Router and product finder
2. Best sellers and product cards
3. Product comparison and bundle/value framing
4. Safety and human handoff
5. Offer/code/save-match paths
6. Objection handling
7. Routine builder
8. Social proof
9. Wellness education
10. Support/order help
11. Replenishment/reorder
12. Review/referral
13. Ad-to-DM entry paths
14. Comment/story automation entry paths
15. Winback and browse loops

For every new branch:

- Fill the message copy immediately.
- Add no more than three decision buttons per block.
- Route at least one button back to products or comparison.
- Route at least one button to human/safety support when appropriate.
- Verify `Saved` before leaving the node.

### Safe Wellness Copy Rules

Use general, careful language:

- "can be part of a general wellness habit"
- "choose the format you can repeat"
- "check with a licensed professional"
- "I cannot diagnose or treat symptoms in DM"

Avoid:

- treatment, cure, prevention, disease, or symptom-resolution claims
- guaranteed outcomes
- replacing professional care

### Browser Automation Workarounds

If ManyChat rejects direct `fill()` or `type()` calls:

1. Click the field.
2. Press `Meta+A`.
3. Press `Backspace`.
4. Enter text one character at a time with keypress events.
5. Wait for `Saved`.

If the `Select Existing Step` target is off-screen:

1. Open the step picker.
2. Scroll inside the picker.
3. Re-query visible rows.
4. Click the visible row.
5. Click `Done`.

If an image URL saves but renders as a URL/placeholder, do not treat it as a finished product-photo node. Replace with an uploaded/rendered image before launch.

### Support Cluster Pattern

For ecommerce DM ecosystems, add a support menu as a second block on the human-help node.

Support menu buttons:

- `Order Help`
- `Shipping Help`
- `Return Issue`

Build each support node with:

- one clear intake ask
- one route back to product options
- one route to human follow-up
- one route to adjacent support context when useful

Order-help intake should request order number and checkout email. Shipping copy should avoid hard promises and point to checkout for live shipping details. Return/issue copy should request order number, checkout email, issue description, and a clear photo for damaged/wrong items.

### Routine Retention Pattern

For ecommerce wellness DM ecosystems, add routine-retention as a second block on the routine builder node.

Menu buttons:

- `7 Day Starter`
- `Gel Ideas`
- `Stay Consistent`

Build each retention node with:

- one practical habit-building message
- one buying/product-card route
- one comparison or human-help route
- one save-match or routine-loop route

Recommended routing:

- `7 Day Starter` -> `Gummy Start`, `Gel Ritual`, `Save Plan`
- `Gel Ideas` -> `Gel Card`, `Compare First`, `Ask Human`
- `Stay Consistent` -> `Save Match`, `Product Options`, `Routine Builder`

The purpose is to keep the DM useful and active without spam. Make the cadence feel like a helpful concierge: simple next step, practical choice, then loop back into the sales/support system. For supplement or wellness brands, avoid medical claims and route safety questions to a human or licensed professional.

### Engaged Price-Help Discount Pattern

Use discounts as a warm-lead assist, not as the default opener.

Good trigger points:

- ad click/ad match path
- price objection
- not-ready loop
- save-match loop
- repeat comparison behavior

Recommended core node:

```text
Price help path:

Totally fair. If price is the only thing holding you back, start with the current code or the best-value bundle.

No pressure. You can also compare first if you want to feel sure before buying.
```

Recommended buttons:

- `Show Code` -> offer/code node
- `Best Value` -> bundle/value node
- `Compare First` -> comparison node

Keep the conversation short and button-led. Do not promise a fixed discount unless the live offer is verified. Always leave one non-purchase route so the customer feels guided, not forced.

### Customer Retention / Reorder / Referral Pattern

Use this for customers who have already bought, reached support, saved a match, or shown routine interest. It should feel like a concierge loop, not a spam loop.

Add a customer menu to the support/human hub or post-purchase branch:

```text
Already bought from us? I can help with the next step.

Choose what you need:

REORDER - get back to your usual product.
TRY NEW - compare another format or bundle.
REVIEW / REFER - share feedback or send a friend.
```

Recommended buttons:

- `Reorder` -> reorder node
- `Try New` -> cross-sell/comparison node
- `Review / Refer` -> review/referral node

Build the reorder node with:

- concise restock copy
- one button back to the product they likely bought
- one button to the other core product
- one button to bundle/value

Build the try-new node with:

- one-line positioning for each format
- buttons to each product card or bundle card
- no long education unless the customer requests it

Build the review/referral node with:

- `Shop Again` -> reorder node
- `Refer Friend` -> referral/product-share node
- `Need Help` -> support/human hub

Build the referral node as a product-path chooser unless a verified referral reward exists. Do not invent referral rewards, discounts, or review incentives.

Rules:

- Attach this branch after support, routine, or existing-customer context.
- Keep messages short and button-led.
- Always provide a support/human exit.
- Never publish until all links, product images, offers, and compliance-sensitive claims are verified.

### Save-Match Re-Entry Hub Pattern

Use this on save-match, not-ready, and offer-capture fallback nodes. This is how to create an evergreen-feeling system without sending endless automated promotional DMs.

Add this menu:

```text
Want useful check-ins instead of random promos?

Pick what you actually want:

ROUTINE TIPS - simple ways to stay consistent.
REORDER REMINDER - help remembering when to restock.
NEW DROPS - product launches and best-value deals.
```

Recommended buttons:

- `Routine Tips` -> routine tips node
- `Reorder Reminder` -> reorder reminder node
- `New Drops` -> new drops/deals node

Build `Routine Tips` with:

- one short habit-building message
- `7 Day Starter` or equivalent starter plan
- `Stay Consistent` or equivalent retention loop
- `Product Options` to return to buying paths

Build `Reorder Reminder` with:

- a reminder that long-term follow-up should happen through an opted-in channel
- `Reorder Now`
- `Best Value`
- `Ask Human`

Build `New Drops` with:

- concise copy that asks for email/phone for launch/deal updates
- `Best Sellers`
- `Best Value`
- `Ask Human`

Rules:

- Do not create fake engagement traps just to keep the DM window open.
- Do not promise unlimited IG/Messenger reminders.
- Keep long-term nurture tied to explicit email/SMS opt-in, Shopify events, review/replenishment events, or click-to-DM re-entry.
- Every re-entry node needs a useful next step and a support/human exit.

### Product Image Upload QA Pattern

Use this whenever pasted product image URLs show as placeholders instead of rendered images.

Steps:

1. Download the verified product images locally.
2. Optimize any file above the visible ManyChat upload limit.
3. Open the target product-card node.
4. Add or select an `Image` block.
5. Use `Upload image or paste URL` and choose the local file.
6. Wait for `Saved`.
7. Verify the phone preview renders the actual product image.

Guardrails:

- Do not launch with image URL strings, empty upload prompts, or broken image blocks.
- If the automation environment cannot control native file upload, document the handoff and the exact local file path.
- In Codex's in-app browser, authenticated ManyChat editing works, but programmatic file upload may not be available. Use manual file-picker upload in the logged-in browser or an authenticated browser tool that supports file upload.
- Prefer the Codex built-in browser for live ManyChat sessions when the user asks for it; do not switch to regular Chrome unless the operator explicitly requests that browser for the current action.
- Use one approved operating browser per live action so proof screenshots, saved state, and rollback notes remain traceable.
- Keep product photos on decision nodes: product cards, comparison, bundle/value, review/social proof, cart recovery, and replenishment.

### Checkout / Cart Rescue Pattern

Use this for warm leads who are close to buying but stuck at checkout. Attach it to price-help, offer-code, checkout-started, or abandoned-cart paths.

Entry copy:

```text
Almost ready but stuck at checkout?

I can help with the common blockers: finding your cart, choosing the best-value option, or getting human help before you order.
```

Recommended buttons:

- `Find My Cart` -> cart recovery node
- `Best Value` -> bundle/value node
- `Checkout Help` -> support/human hub

Build `Find My Cart` with:

- short guidance to reopen checkout from the product page when no cart URL is available
- `Product Options`
- `Shipping Help`
- `Cart Support`

Build `Cart Support` with:

- one short prompt asking what happened
- examples: cart disappeared, code not working, checkout error, shipping question
- product name request
- `Show Discount`
- `Product Options`
- `Human Help`

Rules:

- Never ask for card numbers, passwords, or sensitive payment information in DM.
- If a real Shopify cart URL exists, use it; otherwise route to product options and human support.
- Keep this branch concise. It is for removing friction, not starting a long sales pitch.

### Live Shopify Order Lookup Pattern

Use this when the client wants customers to check order/tracking status inside DM without exposing Shopify Admin credentials to ManyChat.

Architecture:

- Never paste Shopify Admin tokens into ManyChat.
- Deploy a middleware endpoint on Cloudflare Worker, VPS, or another HTTPS backend.
- The middleware receives order number and email/phone, verifies identity against Shopify, and returns only DM-safe fields.
- Require a shared request secret header, such as `x-manychat-secret`.
- Return no full address, payment data, complete customer profile, or private order details.

Required ManyChat fields:

- `hv_order_number`
- `hv_order_email_or_phone`
- `hv_support_issue_type`
- `hv_order_lookup_status`
- `hv_order_name`
- `hv_order_created_at`
- `hv_order_fulfillment_status`
- `hv_order_financial_status`
- `hv_tracking_company`
- `hv_tracking_number`
- `hv_tracking_url`
- `hv_order_status_url`
- `hv_order_next_action`
- `hv_order_customer_message`

Support path:

1. Ask for order number.
2. Ask for email or phone used at checkout.
3. Run External Request.
4. Branch by `hv_order_lookup_status` and `hv_order_next_action`.
5. Validate the outcome branches with `CLIENT_ORDER_LOOKUP_BRANCH_DECISION_CARD.md` before launch proof.

Recommended External Request body:

```json
{
  "order_number": "{{hv_order_number}}",
  "email_or_phone": "{{hv_order_email_or_phone}}",
  "issue_type": "{{hv_support_issue_type}}",
  "subscriber_id": "{{contact.id}}"
}
```

Branching:

- `found` + `send_tracking`: send `{{hv_order_customer_message}}` with `Track Package`, `Delivery Issue`, `Human Help`.
- `found` + `set_processing_expectation`: send `{{hv_order_customer_message}}` with `Shipping Question`, `Change Address`, `Human Help`.
- `mismatch`: do not reveal order data. Offer `Try Again` and `Human Help`.
- `not_found`: ask them to double-check details. Offer `Try Again` and `Human Help`.
- `error`: route to human help and mark the conversation open.

Verification cases before launch:

- real fulfilled order with matching verifier
- real unfulfilled order with matching verifier
- real order with wrong verifier
- fake order
- service unavailable/error branch

For Example Brand specifically:

- Public endpoint: `https://n8n.example-brand.com/manychat/order-lookup/lookup-order`
- Health check: `https://n8n.example-brand.com/manychat/order-lookup/health`
- Middleware service on the client VPS: `manychat-order-lookup.service`
- Shared header value lives in `/etc/manychat-order-lookup.env`

### Lifecycle / Retention Cluster Pattern

Use after the core sales, support, and checkout-rescue routes are stable. Attach from the customer/support hub, reorder keyword, customer trigger, or post-purchase trigger.

Entry copy:

```text
Customer lifecycle menu:

If you already ordered or plan to reorder, I can keep this organized.

POST PURCHASE - how to use it and what to expect.
REPLENISHMENT - reorder timing and restock help.
VIP / WINBACK - best value, referral, and comeback paths.
```

Recommended entry buttons:

- `Post Purchase`
- `Replenishment`
- `VIP / Winback`

Build `Post Purchase` with:

- `How To Use` -> routine selector
- `Shipping Help` -> shipping/support route
- `Review / Refer` -> review/referral route

Build the routine selector with:

- `Gummy Routine`
- `Gel Routine`
- `Storage Tips`

Routine safety rules:

- Use label-directed guidance.
- Do not say the product diagnoses, treats, cures, or prevents a condition.
- Route pregnancy, nursing, medication, allergies, thyroid concerns, and medical-condition questions to a clinician/pharmacist.
- If product quality looks or smells off, tell the customer not to use it and route to support.

Build `Replenishment` with:

- `Running Low`
- `Still Have Some`
- `Try New Routine`

Build `Running Low` with:

- `Reorder Now`
- `Best Value`

Build `VIP / Winback` with:

- `Comeback Deal`
- `VIP Bundle`
- `Refer Review`

Discount/value rules:

- Do not hardcode a percentage unless the client confirms the live offer.
- Route price-sensitive, engaged users to the current code or bundle-value node.
- Keep copy short and supportive. Guide toward the sale; do not force the sale.

Retention rules:

- Do not build an unsolicited endless DM loop.
- Use customer-initiated replies/buttons, click-to-DM re-entry, allowed message tags/windows, or opted-in email/SMS.
- For reminders outside the DM window, ask for opted-in email/phone and route through the appropriate channel.

### Launch Structural QA Pattern

Before calling a ManyChat sales DM ecosystem ready:

- Open the Starting Step and every numbered step.
- Confirm every button destination has useful copy.
- Confirm there are no blank child nodes.
- Confirm there are no empty upload prompts.
- Confirm product image blocks render as actual photos in preview/device test.
- Confirm Instagram Ads first message has a Quick Reply when required.
- Confirm safety routes avoid medical claims and hand off to human/clinician guidance.
- Confirm discount copy uses the current approved offer.
- Confirm tags/actions/custom fields exist, or document API-token blockage.
- Confirm the automation still says `DRAFT` until the user explicitly approves launch.

### Set Live Validator Audit Pattern

When the user approves launch or explicitly asks to fix Set Live errors:

- Click `Set Live` once and let ManyChat open the failing node.
- Read the exact validator error before editing.
- Fix only the pointed issue, then wait for `Saved`.
- Rerun `Set Live` and repeat until there are no node-level errors.
- Keep an audit log of node, error, root cause, and fix.

Common validator blockers:

- `Please specify what happens when this button is pressed`: open the marked button and either route it to the correct existing step or set a verified website URL.
- `Please enter a URL`: open the marked website button and add the correct product, policy, or collection URL.
- `Please add text or remove the text block`: fill the empty text block with concise useful copy or remove it.
- `Please add Subject`: add a subject to an email step, even if the email step is unattached.
- `keyboard cannot be empty`: inspect the email design/button block, add a real CTA label, and set a website URL or remove the button.

If ManyChat publishes successfully:

- Verify the top status changed to `LIVE`.
- Verify the save state says `Saved`.
- Document any persistent account notices separately, such as Facebook page `Refresh Permissions`.
- Do not click `Refresh Permissions` unless the user explicitly authorizes it.

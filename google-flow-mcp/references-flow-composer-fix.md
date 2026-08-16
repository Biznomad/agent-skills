# Flow Composer Fix Notes

## What works
- Browser relay attachment works with:
  - `target: "node"`
  - `profile: "ace-chrome"`
- Tabs, snapshots, navigation, button clicks, project opening, and account verification work.
- Google Ultra session is visible in Flow.

## Current blocker
The Flow prompt composer is not exposed like a normal DOM input/control to the current browser automation layer.

Observed behavior:
- Accessibility snapshot exposes a `textbox` with placeholder-like text: `What do you want to create?`
- Direct `click` on ARIA refs can work for buttons but not reliably for the composer.
- Direct `type` / `fill` against the composer ref fails because the underlying locator is not resolved as a normal editable element.
- DOM probing does not reveal a standard `contenteditable`, text input, textarea, Lexical, ProseMirror, or obvious editor node.
- The page is a Next.js app and likely uses a custom/virtualized editor surface.

## Likely fixes
1. Add lower-level CDP text insertion support in browser relay for the focused element.
2. Expose richer selector/introspection for virtualized editors.
3. Inject a page-specific shim that targets the actual React/editor instance once identified.
4. Fall back to OS/native input automation if browser relay typing cannot reach the virtual editor.

## Recommendation
Do not claim Flow composer automation is complete until one of the above is implemented and tested end-to-end.

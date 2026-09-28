# Client-sharing scope

The current repository files were reviewed on 2026-09-28 UTC.

## Changes

- Replaced identified store domains, Shopify application/variant/selling-plan IDs, advertising account IDs, internal endpoints, service names, and personal machine paths with configurable examples.
- Removed private client audit results and product-roadmap details.
- Replaced agency package pricing with configuration placeholders and generalized scheduling links.
- Normalized example API tokens and design-file identifiers; retained public authorship, licenses, vendor documentation, and Biznomad branding.
- Removed generated coverage databases and added ignore rules for credentials, coverage data, and client audit outputs.

## Verification and limits

Reviewed the tracked text files with targeted client/domain/identifier searches and Gitleaks. The remaining scanner matches were reviewed as documentation placeholders, design-variable names, package metadata, or password-test examples; no live credential was confirmed. This is a bounded review, not a guarantee that no sensitive information can exist. Bundled binary assets were inventoried; Office-document XML and compressed text were checked for known client identifiers. Fonts, preview images, and the template PDF were not exhaustively content-audited.

Git history was scanned separately and still contains earlier unsanitized details. A normal commit does not erase those older versions. For client sharing, use the ZIP download of the current main branch, which excludes Git history. Do not describe a full Git clone as history-sanitized until the old history has been replaced.

## Rechecking

Run `gitleaks dir . --redact` for the current files and `gitleaks git . --redact` for history. Review findings instead of treating known documentation placeholders as working credentials. Keep scan reports private and keep client data outside skill folders.

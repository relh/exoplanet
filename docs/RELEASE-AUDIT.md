# Publication cleanup — 20 October 2026

**Sensitive-content cleanup and publication verification passed.** The research, scientific findings, author attribution and ordinary project provenance remain intact. The owner authorized publication after verification. No candidate submission or external outreach is performed.

## What was removed

A sanitized copy of all 678 existing commits was prepared and checked, removing only sensitive operational details:

- Whole host-process snapshots in two frozen-plan records, including unrelated project names, host services, session identifiers and application arguments.
- The machine identity in an archived assessment and its duplicate text/ZIP exports. Exact word matching preserves unrelated scientific strings.
- The private dashboard listener address from every historical text version, including a bare JSON listener field.
- Credential, signature and related authentication query parameters from saved signed archive URLs, including nested ZIP copies. Scientific object identities, metadata and raw-content hashes remain.

All 678 original commits and their sanitized equivalents are retained in the private research archive. The public release starts from a clean current snapshot, with all current research files preserved and no original history attached. Thirty-six historical blobs changed during the audit. [release-history-redactions.json](release-history-redactions.json) records the categories and original/sanitized SHA-256 and Git object hashes. [release-commit-map.txt](release-commit-map.txt) maps the original commits to the sanitized private history. The [initial audit](RELEASE-AUDIT-INITIAL.md) remains a historical record of the problems before cleanup.

## Attribution and provenance retained

The owner explicitly permits public research findings and identifiable attribution. Richard Higgins and the supplied contact email remain in commit metadata and may be used in the manuscript. Benign local project/cache paths and scientific tracebacks remain: they are provenance, rather than credentials or unrelated private-project details. The sensitive process snapshots were the only identified source of unrelated project and session information.

Original project code and documentation use the [MIT license](../LICENSE). [DATA-SOURCES.md](DATA-SOURCES.md) records survey credits and distinguishes third-party terms from the project license.

## Original research archive

Before any transformation, a complete private Git bundle was created and successfully verified. Its SHA-256 is recorded in the redaction manifest. The original remote repository is retained as a separate private archive. The publication repository is newly created at the familiar project URL from the sanitized current snapshot, rather than exposing the old repository’s retained, unreachable objects. The files were transferred in verified batches and assembled into an independent root commit. Its Git tree exactly matches the audited local snapshot (`264117dd493bc0ee043fc943c631685c7d7d7f61`). Original sensitive blob IDs and the original main commit return 404 in the new repository. The original archive remains private. A failed temporary template copy is separate from the publication repository.

No raw research download, observation, scientific array or figure was deleted. Measurements, numerical JSON values outside the omitted process fields, physical conclusions, failures and source-data hashes are unchanged. The original frozen bytes remain in the private archive. Existing historical hash fields continue to refer to those original bytes; the redaction map supplies the sanitized equivalent when such a file was edited. **Sanitized plans are not newly frozen experiments.** Historical verifiers that require exact original text bytes may need that translation or the private original; they must not silently claim a new pre-access freeze.

Current dashboard archives are regenerated from sanitized source files and have matching export provenance. An unsigned archive URL may require a fresh link from the provider; it is not a claim of directly accessible anonymous download.

## Verification

The full sanitized history and nested archives are scanned again for the identified machine/address/session/private-project patterns and signed download credentials. A fresh secret scan is classified against the earlier public archive IDs and scientific labels, without disabling generic secret detection. [release-verification.json](release-verification.json) records the exact counts and scope: all 678 commits and 111,628 unique blobs passed the targeted sensitive-content review. All 1,318 remaining generic scanner detections exactly match previously classified public identifiers, scientific labels and filenames; no signed AWS access-ID findings remain.

Transform verification passed 7,462 checks of original/replacement hashes, unchanged numerical JSON fields and unchanged numerical/figure ZIP members. Current checks pass 125 documentation links, 608 dashboard source/export/archive assertions and the transit presentation verifier for all 4,045 observations and 19 source hashes. There is no scientific reanalysis, observation access or candidate promotion in this cleanup.

## Scope limits

This is a targeted secrets and operational-privacy cleanup, not an anonymity exercise or a blanket certification of all scientific or redistribution claims. Figure pixels were not exhaustively OCR-reviewed. Ignored raw caches, local private backups and protected agent histories are not part of the publication repository. They remain untouched and must not be uploaded. No live user credential was identified in the audited findings; expired signed URLs were nevertheless stripped.

**The owner explicitly authorized the final visibility change after these checks.**

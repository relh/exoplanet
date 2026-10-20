# Public-release audit — 20 October 2026

**Decision: keep the repository private.** Private operational information is present in current research artifacts and recoverable Git history. The documentation cleanup does not clear that history for publication.

## Scope

Baseline: `77d0af27d8babc9506e3dd69803171da9acfa7ec` on `main`, synchronized with origin before edits. The checkout is not shallow. The remote advertises only `main`; there are no tags or additional branches.

- Reviewed all 675 commits, their messages and author/committer metadata, and 111,616 unique reachable blobs. The baseline contains 116,392 tracked files.
- Ran `gitleaks detect --source . --log-opts='--all --full-history' --redact` and classified every detection.
- Searched historical content for host identities, personal paths, network addresses, emails and operational details. Inspected current URL hosts and sensitive filenames.
- Read all 1,812 historical ZIP/NPZ blobs recursively: 11,683 archive members, including 797 text members. No object-dtype NumPy arrays or archive-read errors were found; no pickle or downloaded code was executed. Ran a separate secret scan on extracted text.
- Inspected textual metadata in 1,219 historical PNG blobs. Every text field was a software identifier; no privacy matches were found there. Raster content was not OCR-scanned or individually reviewed for this audit.
- GitHub reports a private repository with no issues/PRs, releases, Actions runs/artifacts or Pages deployment. Discussions are disabled. Wiki access returned “repository not found”; its contents could not be independently inspected.

This covers reachable Git history and the listed repository surfaces. It does not certify unreachable server objects, every pixel of a figure, external accounts, ignored caches or third-party redistribution rights. Local untracked research progress files were left untouched and excluded from the cleanup commit.

## Findings

| Finding | Evidence | Release implication |
|---|---|---|
| Host process snapshots | `results/new-epochs-5546257-20261012/plan.json` and `results/new-epochs-80387959-20261012/plan.json` | Included host details, session arguments and an unrelated project path. Current snapshots are omitted; historical originals remain private. |
| Machine identity | An archived model assessment, its dashboard text copy and ZIP member, plus a process snapshot | Current copies have been generalized or redacted. Previous Git versions still disclose the original identity. |
| Personal filesystem paths | 2,729 baseline tracked files; 2,385 unique historical blobs contain the local user's home path | Mostly provenance/cache references and tracebacks. These remain a publication blocker; blanket replacement could break hashes and historical verifiers. |
| Private dashboard address | README versions, dashboard instructions and the integration verification record | Removed from current docs and generalized in the current verification record. Historical versions retain it. |
| Author identity | All 675 baseline commits carry an identifiable name and personal-domain email | Publishing this history would disclose them. A release needs an explicit disclosure decision or reviewed replacement history. |
| Signed archive links | 624 scanner occurrences representing 310 unique LCO/S3 URLs, also copied into a dashboard archive | URLs expired on 15 October 2026 at 23:27:42–46 UTC. These are public-archive response artifacts, not a confirmed user secret; their credential/signature parameters still need a deliberate publication policy. |
| Missing license | No repository license file | A license must be selected before this can be released as open-source software. Survey and third-party attribution obligations require separate consideration. |

The main secret scan returned 1,942 detections. All 1,318 generic-key findings are public archive identifiers, scientific model/control labels or public filenames. The other 624 are the expired signed-link occurrences above. The archive scan returned 930 duplicate findings: 306 archive identifiers and the same 624 signed-link occurrences. There are no unclassified findings in these reports and no confirmed live user credential. This is not proof that all possible secrets are absent. One custom archive network-pattern match was a software version, not an address.

## Cleanup and evidence integrity

README, the resumption guide and dashboard instructions were shortened while retaining scientific caveats, failed controls, closed-queue state and holdout rules. Private hosting details were removed. Machine references were removed from current text and the regenerated dashboard archive. New repository guidance prohibits committing host-wide process lists and personal operational details.

[privacy-edits.json](privacy-edits.json) records original Git blob IDs and original/edited SHA-256 hashes for the four edited evidence records. Only the two process fields, one machine-name phrase and the private listener value changed. Scientific plan fields, frozen timestamps, measurements, decisions and original result hashes remain unchanged. **These edits are not new pre-access freezes.** Existing result hashes continue to identify the original frozen bytes retained in private history. Dashboard export hashes identify the edited display copies.

Checks passed 126 local documentation links/anchors and 251 privacy/provenance assertions covering current machine-name absence, unchanged scientific plan fields, privacy-edit hashes, dashboard archive/source equality and export provenance. The existing transit verifier passes all 4,045 exported observations and 19 source hashes. No scientific algorithm was modified or new observation opened.

[release-scan-summary.json](release-scan-summary.json) retains aggregate scan counts, classifications and hashes of the local scanner reports, without copying their private identifiers into these docs.

The first exporter attempt selected Python 3.14 and failed because the locked `batman-package` distribution has no compatible wheel. Re-running with installed Python 3.12 succeeded; setup instructions now select that interpreter explicitly. Historical scientific verification records were not rewritten to imply new validation.

## Before publication

1. Select a license and decide whether the historical author identity may be disclosed.
2. Choose a separately sanitized public snapshot or an explicitly authorized history rewrite. A clean publication repository can preserve the existing private research archive; do not force-push replacement history without a reviewed plan and verified backup.
3. Sanitize paths, process details, private endpoints and signed-link parameters across the chosen publication contents, nested archives and any retained history. Preserve original/new hashes and explain provenance substitutions.
4. Repeat content, history, archive and secret checks against the exact publication commit, then make the visibility change only if the findings are resolved.

No visibility change, history rewrite, force push, external submission or outreach was performed. The requested cleanup is pushed to the existing private repository.

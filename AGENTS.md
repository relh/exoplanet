# Repository guidance

Before changes, run `git status --short --branch` and `git fetch origin`.
Never implicitly merge or rebase work. The owner authorized the audited public
release; keep raw caches, private backups and original sensitive history private.
See `docs/RELEASE-AUDIT.md` for the publication cleanup and retained provenance.

Retain research evidence; raw downloads belong in ignored `data/`, with URLs and
SHA-256 hashes in committed run manifests. Never execute downloaded shell scripts.
Do not describe a periodogram peak as a planet discovery. Catalog non-matches are
not proof of novelty. Keep failed checks and limitations in reports. No external
candidate submission or contacting astronomers without explicit user instruction.

Run `uv run pytest` for scientific algorithm changes. Use deterministic synthetic
injection tests. Keep catalog errors explicit, not equivalent to no known match.

Before resuming scientific work, read `GOAL.md` and `CHECKED-RESULTS.md`, then
inspect the linked current evidence and live processes. Keep README organized by
relevance; update existing candidate rows instead of appending a running journal.
Retain invalidated interpretations, failed checks and their reasons in linked
assessments and the checked-results index. Qualitative likelihood labels are not
calibrated probabilities. See GOAL.md for holdout and queue-resumption rules.

Use `CODE-ORGANIZATION.md` for module placement and parallel ownership. The user
authorizes sensible sub-agent investigations; assign disjoint result directories
and avoid shared cache downloads or changing scientific src under a live queue.
Generic followup autoopens reserved data: complete its documented preflight first.
Record only relevant research-job state in new manifests. Do not commit full host
process lists, personal paths, machine names, private network addresses or session
arguments. Privacy edits to frozen evidence need original/new hashes and an
explicit amendment; they do not create a new pre-access freeze.

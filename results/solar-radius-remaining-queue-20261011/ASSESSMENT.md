# Remaining frozen solar-radius queue

Prepare all5,132 remaining entries, ranks1872–7003, as ten512-target batches and one12-target batch. The original ranking, targets, discovery sectors, reserved sectors and screening gates are unchanged. All discovery and reserved caches were absent at preparation. This queue is independent of the running ranks1360–1871 batch.

Two workers run each batch sequentially. Each completed batch receives a terminal audit of selection membership, code/raw hashes, FITS identities, outcomes and untouched reserved sectors. Results remain screening leads until separately reviewed. The queue stops rather than overwriting an existing output, on a failed subprocess, on a failed audit, or when available disk falls below60GiB. A stopped/interrupted queue requires explicit state inspection before recovery; a stale running manifest is not proof of a live process.

The selection and all outcomes must remain available even if no signal passes. The earlier shallow-injection limitations still apply. These5,132 searches are planned work; completion must be established from their individual manifests and terminal audits, not this document or the parent queue plan.

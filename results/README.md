# Research evidence

This directory preserves individual experiments, including plans, measurements, source snapshots, failures and verification. **Reports describe the state at the time they were written.** Older references to active queues, pending tests or next steps may be superseded; they are not instructions to restart work.

## Start here

| Question | Current reference |
|---|---|
| What did the search find? | [Main results and candidate table](../README.md) |
| What was checked or invalidated? | [Evidence index](../CHECKED-RESULTS.md) |
| Is the work complete, and how can it be extended? | [Goal and resumption guide](../GOAL.md) |
| How is the search accounted for? | [Completion audit](scoped-completion-20261012/ASSESSMENT.md), [solar ledger](solar-radius-lead-audit-20261011/audit.json), [weak-seed ledger](weak-seed-audit-20261011/audit.json) |
| How should a new experiment be organized? | [Code and research workflow](../CODE-ORGANIZATION.md) |

The [earlier vetting plan](remaining-vetting-audit-20261012/ASSESSMENT.md) records the rationale for the final tests; its pending-work statements are historical. Consult the current evidence index for their outcomes.

## Reading a run

Start with its `ASSESSMENT.md`, then inspect the plan, measurements and provenance it references. A `verification.json` describes checks within a stated scope; it does not prove astrophysical validity. Some runs use different filenames, documented in their reports.

Raw downloads live in ignored data directories. Committed manifests record their sources, retrieval times and hashes. Source snapshots and historical scripts belong to the evidence: do not overwrite or reorganize them. A historical verifier may assert that reserved observations were absent at that time; inspect it before rerunning against a later cache.

Current summaries take precedence over older prose, while the original measurements and failed checks remain available. Add a new, linked assessment when evidence changes an interpretation.

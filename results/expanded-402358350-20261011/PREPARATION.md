# TIC402358350: prepared sector54 expansion, not executed

This directory contains a prepared experiment, not new scientific results. The parent4944–5455 batch was still running during preparation. No additional observation was opened, and there is no execution record or expanded timing fit yet.

`run.py` requires both an explicit `--execute` and the coordinator-inspected SHA-256 of the successful terminal batch verification. Before its first archive fetch it checks that audit, completed512-target accounting, selection hash and identities, dispositions, source snapshot hashes, queue-audit provenance and this target's screening pass. It checks sector54 and81 light-curve caches are absent. The coordinator must also inspect historical evidence and actual process state; cache absence alone is not a claim of blindness.

Once authorized after the terminal audit, the script first evaluates sector54 at the previously frozen40/41 primary1.5-day and sensitivity2.5-day clocks, preserving the unchanged original discovery clock too. No54 timing optimization precedes those saved measurements. It reports timing uncertainty, coverage and expected sensitivity, including inconclusive or failed outcomes.

Only after both original predictions are saved does54 explicitly join40/41 as training. Both predefined windows refine the same original discovery period-family neighborhood using the original discovery baseline to preserve search width. Inclusion of54 does not depend on its producing a favorable nominal recovery. The resulting clocks, correlated profile pairs and raw provenance are frozen for81. The script does not open81 under any path; its absence is rechecked during processing.

This is a separately planned expansion, allowed by the earlier protocol's explicit provision for a new plan before81. It preserves the original40/41 predictions. Future81 analysis must retain both the original timing-inconclusive forecast and the expanded-training prediction, and must not promote a profile maximum to nominal recovery. Source ambiguity remains. If a retrieval, preprocessing or fitting error occurs after launch, its execution state is retained and automatic continuation over partial output is forbidden.

Preparation validation is limited to Python compilation and inspection against the actual running manifest's schema, including `selection_path`. No command that opens observations has been run. Scientific reconstruction and provenance verification are required after the experiment actually executes; this prepared state must not be described as a passed scientific experiment.

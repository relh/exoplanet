# Sector 49 long-injections: partial run

The process exited 1 after eight of twelve planned trials. The first two metadata-ranked stars (320209338, 288452774) completed their trials. The third, TIC 165463961, had unusable QLP flux and failed before any baseline or injection; its four trials were unperformed. No substitute star was chosen and no completed trial was restarted. process-status.json records the terminal failure; audit.json reads retained progress and its terminal=false refers to absence of a successful results.json, not a still-running process.

Both completed-star baseline arrays exactly matched production at both detrending windows. All eight performed periods lie inside the actual search grid. 8/8 recovered period, 8/8 matched phase, and 2/8 passed the unchanged noncrowding screen, all with matching phase. Passing (TIC, period, Earth radius): [(320209338, 5.73, 3.0), (288452774, 5.73, 3.0)].

No Earth-radius trial passed. Two stars and one phase/duration per period group do not establish completeness; missing trials are not recovery failures. Existing variability and noise were retained.

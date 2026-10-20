# TIC 346786364: incomplete screening, no usable full recovery

The original QLP58 run did not complete screening. Unlike a zero-flux product,
it contains 5,652 usable native flux/error pairs and 1,952 ten-minute bins. The
1.5-day detrending window succeeds, but all ten contiguous segments are too short
for the required 2.5-day alternative window. The longest span is 2.197 days;
segment_audit.py reproduces these eligibility checks without relaxing gates.

The partial BLS result (P=0.573400128 days, depth about 55%, formal SNR 34.49)
is retained in the original error record. It is not a screened planet candidate.
An initial diagnostic assertion incorrectly assumed failure in the first window;
inspection of the saved partial result identified the second-window failure,
which the completed audit now verifies. No original result was altered.

All other available sectors, 18 and 85, are reserved and remain unopened. A
separate same-epoch SPOC request returned HTTP 404. The star is excluded from
completed usable-search counts; incomplete screening is not a nondetection.

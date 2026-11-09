# Marisa Chargeshot: complete beam and side-volley native C++

The original nine-function `cs_mari` physical owner now expresses all four
12-sample Chargeshot history traversals, the three separate hardware GRCG
beam bands, and the two independent five-bullet Gauge side volleys as natural
`for` loops. The 11-to-1 history shift keeps its descending signed index;
collision still samples only 0, 4 and 8 and breaks before the next step.
Beam tile selection, original Y shifts, byte-frame increments, burst speed
mutation, warning order and hardware calls remain unchanged.

The first broad trial `af1134b` was not exact because the Hyper history loop
still had a duplicated `++i` in the body; after correcting that specific
source mistake, successive `af1134c` (history and collision), `af1134d`
(all three GRCG passes), `af1134e` (both Gauge volleys) and current `af1134f`
reproduced **all 1,509 CODE bytes**, 152 ordered native fields, nine PUBLICs,
full Japanese MAIN image and ordered MZ relocations in two independent
original TC4/TLINK rounds each.

Proof: `.analysis/work/exatt-layout-af1134f/report.json`.

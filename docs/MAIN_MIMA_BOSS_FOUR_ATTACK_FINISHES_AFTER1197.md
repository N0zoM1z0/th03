# Mima BOSS: native endings of four attack families

The spread, random-bomb, trailing-shot and moving-orbit controllers now exit
on unfinished frames before changing attack mode or resetting the frame
counter. Their earlier warning, bullet and palette operations still execute
in the original order, including RNG draws, trail toggles and the distinct
six-frame pellet cadence. All four checks are natural C++ returns.

Incremental original TC4/TLINK receipts `af1197a` (spread), `af1197b`
(random bomb), `af1197c` (trail) and `af1197d` (orbit) each matched the
complete 1,922 CODE bytes, 277 ordered native fields, nine PUBLICs and the
Japanese MAIN loaded image and relocations in both compiler rounds.

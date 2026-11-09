# Rikako Extra Attack: native homing controller and full entity traversals

The full five-function `ex_rika` owner now uses natural `for` loops for both
first-free allocators, the 14-slot sprite renderer, and the complete homing,
collision, flying and arrival state machine. Both early `continue` paths
(inactive slot and clipping) join one original signed-index/near-pointer
advance after their state effects. The update's signed register index is
scoped to its `for` header; its per-frame byte mutations and signed angle
quotient remain unchanged.

Original Turbo C++/TLINK stages `af1124a` through `af1124d` matched all 702
CODE bytes, 46 ordered native fields, five PUBLICs and the Japanese MAIN
image/relocations in two independent rounds each. Final source evidence:
`.analysis/work/exatt-layout-af1124d/report.json`.

An isolated `af1124e` attempt narrowed the target angle's lifetime inside
the homing branch; its original compiler CODE differed, so that candidate
was rejected.

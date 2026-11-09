# Kotohime Extra Attack: natural control of all physical entity passes

The complete eight-function `ex_koto` owner now uses `for` loops for its
first-free allocation, 4- and 10-wave bullet groups, 10-slot beam/flying/event
state update, and render scan. The live update's free-slot `continue` reaches
one shared index/global-pointer advance; the byte event counter and RNG calls
remain in their original order. The signed update index is safely scoped to
its `for` header without changing the original compiler output.

Original TC4/TLINK stages `af1121a` through `af1121d` each matched the
1,054-byte CODE owner, 100 ordered native fields, eight PUBLICs, and full
Japanese MAIN image/relocations in two independent rounds. Final receipt:
`.analysis/work/exatt-layout-af1121d/report.json`.

A further attempt `af1121e` to turn the two direction-to-angle-delta `if`
blocks into ternaries changed original CODE and was rejected. Keep those
branches rather than relying only on semantic equivalence.

# TH03 MAIN — complete Fireball owner: traversals and chain parameters (af1108e)

The original 1,555-byte `e_fireb` physical owner contains the first-free
Fireball allocator, flight/fall/explosion animation and collision, all 24
entity updates, chained Extra Attack rewards and rendering. The forward
allocator/update/render walks and backward explosion-hit scan now use natural
prefix updates for their actual near pointers. The explosion renderer's
coordinate values initialize directly at first use, after sprite sizing.
Semantic constants describe the original spawn size, generation limit, two
chain-charge thresholds, gauge bonus and transfer score without changing
the native integer divisions or timing.

Original Turbo C++ 4.02 independent two-round native checks passed for
`af1108c` (all pointer progressions), `af1108d` (explosion-placement locals),
and final `af1108e` (named chain semantics). Every one of the 1,555 original
CODE bytes, all 115 ordered native fields, ten PUBLICs, full normal Japanese
MAIN image and all 1,553 ordered MZ relocations match the original.
Source-bound original compiler evidence:
`.analysis/work/exatt-layout-af1108e/report.json`.

Two isolated wider lifetime experiments failed native CODE equality:
`af1108a` moved the explosion sprite's byte cel scratch into its branch;
`af1108b` moved the allocator's signed index declaration to its `for` header.
Both were rejected. The original uninitialized chain-slot behavior is
intentionally untouched: initializing it would be a gameplay fix, not exact
reconstruction. These are local original-source improvements, not Factory
canonical packed-product acceptance.

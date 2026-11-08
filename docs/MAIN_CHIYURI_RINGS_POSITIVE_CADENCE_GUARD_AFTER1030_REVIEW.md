# TH03 MAIN Chiyuri Rings: positive cadence guard

The 208-byte `chiyuri_pattern_rings()` leaf now scopes its attack body under
the positive firing condition:

```cpp
if((boss_frame % chiyuri_ring_interval) == 1) {
    // center warning, finish transition, ring and optional pellet burst
}
```

This replaces the inverse early-return guard with a positive cadence scope.
The warning bomb still precedes the finish transition, the main 32-ring is
still emitted before the level-eight pellet gate, and the four auxiliary
pellets retain their original coordinate and call order.

Stage `af1030i` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030i/report.json`

SHA-256: `e9c5ca692fe55573c16339ca1f0b72a7c6260d8182818f92d542ae4e1416744f`

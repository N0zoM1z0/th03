# TH03 MAIN Kotohime Radial Burst: scoped register locals and natural while loops

The complete 302-byte `kotohime_pattern_radial_burst()` now expresses its
nested projectile traversal as two pre-tested C++ `while` loops. The original
register roles remain explicit: `center_i` is the outer DI index and
`bullet_i` is the inner SI index. Both natural `index < count` tests and
prefix increments compile to the original native instructions.

The scratch lifetimes now follow the actual traversal:

```cpp
register int center_i = 0;
while(center_i < kotohime_orbit_count) {
    register int x;
    register int y;
    register unsigned char center_angle;

    // compute one center and store its polar coordinates
    register int bullet_i = 0;
    while(bullet_i < kotohime_burst_count) {
        // compute one spread angle/speed and emit
        bullets_add();
        ++bullet_i;
    }
    ++center_i;
}
```

The center coordinates and byte angle live only for one outer iteration;
the inner register index is initialized at the start of each center's burst.
This preserves the target's top-tested loop entry, DI/SI register allocation,
signed 16-bit multiply/divide order, byte-angle truncation, both `polar()`
calls, coordinate-store order, inner angle/speed calculations and
`bullets_add()` order.

The source was explored in separate original-compiler trials: outer and inner
`index < count` forms; prefix increments; both `while` loops; register
qualification for the center angle and coordinates; moving scratch locals
into the per-center block; and initializing each loop index at its natural
scope. Every step retained the complete original owner. The final maintained
source/comment revision was rebuilt at stage `af1031h`.

Stage `af1031h` rebuilt the complete `ba_koto` physical owner in two
independent original TC4 4.02 rounds. All 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1031h/report.json`

SHA-256: `ac2a3e4e901b11d52690bc27718657fa88346e53cffc08cb9b06f631f1d96aa5`

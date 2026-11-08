# TH03 MAIN Kotohime Radial Burst: outer-first register declarations

The 302-byte radial burst now declares its nested loop indices in the same
outer-to-inner order as their traversal:

```cpp
register int center_i;
register int bullet_i;
for(center_i = 0; kotohime_orbit_count > center_i; center_i++) {
    // one radial center
    for(bullet_i = 0; kotohime_burst_count > bullet_i; bullet_i++) {
        // local spread
    }
}
```

This is a natural source ordering for the two nested traversals. The original
TC4 allocation remains DI for `center_i` and SI for `bullet_i`, and the
signed 16-bit multiply/divide, byte-angle truncation and projectile order are
unchanged.

Stage `af1029l` rebuilt the complete `ba_koto` physical owner in two
independent original Turbo C++ 4.02 rounds. All 1,840 CODE bytes, 262 ordered
native fields and eleven PUBLIC offsets match. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1029l/report.json`

SHA-256: `62ad2ce45c32c675ce1652e3b6dd307a6b009cfb516270d2277ecf598bbcbe1a`

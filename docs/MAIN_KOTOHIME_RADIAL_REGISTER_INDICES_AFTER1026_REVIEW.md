# TH03 MAIN Kotohime Radial Burst: explicit register loop indices

The two nested radial traversal indices are now explicitly declared as
register locals:

```cpp
register int bullet_i;
register int center_i;
for(center_i = 0; kotohime_orbit_count > center_i; center_i++) {
    // compute one center and emit its local burst
    for(bullet_i = 0; kotohime_burst_count > bullet_i; bullet_i++) {
        // angle, speed and bullets_add()
    }
}
```

The target disassembly uses DI for the outer center index and SI for the inner
bullet index. Declaring both locals `register` makes those lifetimes explicit
in the source while preserving the two natural loops, their signed 16-bit
multiply/divide calculations, byte-angle truncation, and projectile call order.

Stage `af1026i` rebuilt the complete `ba_koto` owner in two independent
original Turbo C++ 4.02 rounds. All 1,840 CODE bytes, 262 ordered native fields
and eleven PUBLIC offsets match. Both normal MAIN links reproduce the original
Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1026i/report.json`

SHA-256: `3209edcbd2b482854e9c41c486e8c4689b7c403ebca92cb1a81bf1a57f9ae854`

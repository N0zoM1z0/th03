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

## Additional radial-branch and coordinate-type experiments

The following natural alternatives were compiled against the same complete
`ba_koto` owner and rejected because the complete CODE payload differed:

- `af1026b`: move the expansion/movement path to an early-return guard and
  leave release as the fallthrough path.
- `af1026c`: invert the expansion/release branches without an early return.
- `af1026e`: replace the two `int` coordinate locals with a `PlayfieldPoint`
  and copy the complete point to `bullet_template.center`.
- `af1026f`: use the same local `PlayfieldPoint` but copy its X and Y fields
  individually into the bullet template.

All four source experiments were reverted. The original expansion/release
branch and separate integer coordinate temporaries remain. The successful
`register int` index declarations are independent of those rejected trials.

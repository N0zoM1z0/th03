# TH03 MAIN Kotohime Radial Burst: natural loops, release guard and arithmetic

The complete 302-byte `kotohime_pattern_radial_burst()` now uses scoped,
pre-tested `for` loops for its two nested projectile traversals:

```cpp
for(register int center_i = 0; center_i < kotohime_orbit_count; ++center_i) {
    register int x;
    register int y;
    register unsigned char center_angle;
    center_angle = boss_move_phase +
        ((center_i * KOTOHIME_FULL_TURN_STEPS) / kotohime_orbit_count);
    x = polar(boss_center_x, boss_effect_radius, CosTable8[center_angle]);
    y = polar(boss_center_y, boss_effect_radius, SinTable8[center_angle]);
    bullet_template.center.x.v = x;
    bullet_template.center.y.v = y;

    for(register int bullet_i = 0; bullet_i < kotohime_burst_count; ++bullet_i) {
        bullet_template.angle =
            ((bullet_i * KOTOHIME_BURST_HALF_TURN_STEPS) / kotohime_burst_count) +
            center_angle + KOTOHIME_BURST_CENTER_ANGLE_OFFSET;
        bullet_template.speed.v = KOTOHIME_BURST_SPEED_BASE +
            ((bullet_i * KOTOHIME_BURST_SPEED_SCALE) / kotohime_burst_count);
        bullets_add();
    }
}
```

The loop headers retain DI for the outer index and SI for the inner index.
`bullet_i` is initialized once per center, and the coordinate/angle scratch
remains scoped to one outer iteration. The signed 16-bit multiply/divide
order, byte-angle truncation, polar-call order, coordinate stores and bullet
emission order are unchanged.

The release check is now a positive completion branch:

```cpp
if(KOTOHIME_RING_RELEASE_AFTER < boss_render_frame) {
    // radial volley and SELECT transition
} else {
    return;
}
```

This preserves the byte postfix increment and the non-release early return.
The shared aimed/radial warning-radius increment is now named
`KOTOHIME_RING_WARNING_EXPAND_STEP` rather than a repeated literal `8`.

The center angle and speed expressions use the natural base-first additions:
`boss_move_phase + orbit_angle` and `KOTOHIME_BURST_SPEED_BASE + speed_step`.
Both operand orders compile to the same complete owner.

A natural `boss_move_phase -= 4` replacement for the AL-mediated byte update
was also tested and rejected because it changes complete CODE. Stage af1056b
also tried a shared `register unsigned char phase` local initialized from
`boss_move_phase`, incremented by `(unsigned char)0xFC`, and stored back; the
complete `ba_koto` CODE comparison differed in the first round. Both variants
were restored, and the original AL load/add/store sequence remains.

Stage `af1033y` rebuilt the complete `ba_koto` physical owner in two
independent original TC4 4.02 rounds. All 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033y/report.json`

SHA-256: `11606da3926cd36593629424ce9d5f63ead29c7e5bd19f1258f26e1eb389b498`


## Current-source loop lifetime revalidation (af1068e)

The current maintained radial traversal was re-tested with both indices
initialized in their own natural `for` headers and coordinate/angle scratch
scoped to one outer iteration:

```cpp
for(register int center_i = 0;
    center_i < kotohime_orbit_count;
    ++center_i) {
    register int x;
    register int y;
    register unsigned char center_angle;
    // compute center_angle and the two polar coordinates
    for(register int bullet_i = 0;
        bullet_i < kotohime_burst_count;
        ++bullet_i) {
        // angle, speed and bullets_add()
    }
}
```

This is a current-source revalidation rather than a transfer of the earlier
`af1031h` or `af1037r` results. It preserves DI for the outer index and SI for
the inner index, resets the inner index for each center, and narrows the
coordinate/angle scratch lifetime to one center. Signed 16-bit multiplication
and division, byte-angle truncation, polar-call order, coordinate-store order,
projectile angle/speed expressions, and `bullets_add()` order are unchanged.

Stage `af1068e` rebuilt the complete `ba_koto` owner in two independent
original TC4 4.02 rounds: all 1,840 CODE bytes, 262 ordered native fields and
eleven PUBLIC offsets match. Both normal Japanese MAIN links reproduce the
loaded image and ordered relocations.

Protected report: `.analysis/work/exatt-layout-af1068e/report.json`

SHA-256: `a51759a9529f0da12dc9dd9cded1492aedf828405599ddafefc354876a25669c`

### Additional current-source negative control

Stage `af1068g` tried assigning each `polar()` result directly into
`bullet_template.center.x.v` and `.y.v`, removing the `x` and `y` scratch
locals. The first complete `ba_koto` CODE comparison differed, so the
experiment was restored. Keep the separate coordinate temporaries.


## Alternate current-source nested while form (af1068w)

A second natural loop spelling was also tested against the current complete
`ba_koto` owner. It moves the outer and inner register indices to their
respective scopes, initializes each at zero, and advances each index at the
end of its loop body:

```cpp
register int center_i = 0;
while(center_i < kotohime_orbit_count) {
    // per-center scratch and polar coordinates
    register int bullet_i = 0;
    while(bullet_i < kotohime_burst_count) {
        // angle, speed and bullets_add()
        ++bullet_i;
    }
    ++center_i;
}
```

Stage `af1068w` also reproduced all 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets in two original TC4 4.02 rounds. Both normal
Japanese MAIN links reproduce the original loaded image and ordered
relocations. The maintained source retains the `for`-header form from
af1068e because it gives each index the narrower loop lifetime; this `while`
form is a verified alternative, not a failed experiment.

Report: `.analysis/work/exatt-layout-af1068w/report.json`

SHA-256: `fb0e5d33f26e95e1269447a9bf851eaafd91d2836aa07c11bc54b3906638f1b2`

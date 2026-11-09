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

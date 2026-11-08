# TH03 MAIN Mima renderer: Trail tail guard and Particle phase comparisons

The 305-byte `mima_render_main()` now expresses the final Trail dispatch as
a positive early-return guard after the Particle, Expand and Flash paths:

```cpp
if(MIMA_RMODE_TRAIL != boss_render_mode) {
    return;
}
boss_render_frame = 0;
goto render_mode_2;
```

The shared Trail-to-Particle label remains intact. The reset still happens
only for Trail, before entering the shared Particle/carrier draw sequence.
The other modes already return from their own branches; the final guard
preserves the original fall-through behavior for normal mode and unknown
mode values.

The Particle carrier's nested frame thresholds now use constant-first
comparisons:

```cpp
if(MIMA_RENDER_PARTICLE_CEL_FIRST <= boss_render_frame) {
    sprite_offset += 4;
    if(MIMA_RENDER_PARTICLE_CEL_SECOND <= boss_render_frame) {
        boss_render_mode = MIMA_RMODE_EXPAND;
    }
}
```

The Particle, Expand and Flash mode equality checks use variable-first
comparisons. The two nested thresholds, carrier offset adjustment, Expand
transition, byte-frame postfix increment and Trail label/goto remain in their
original order.

Experiments against the complete physical owner:

- `af1034g`: invert the final Trail check into an early return; exact.
- `af1034h`: move both Particle threshold constants to the left; exact.
- `af1034i`: move Particle/Expand/Flash mode values to the right of the
  variable; exact.
- An empty `if(frame < FIRST) { } else { ... }` rewrite changed CODE.
- A ternary `sprite_offset += (frame >= FIRST) ? 4 : 0` rewrite changed CODE.
  The nested positive threshold guards remain the natural exact form.

Stage `af1034i` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1034i/report.json`

SHA-256: `d605803ae02600deb7b908dac7393dfd209723e60a9ccbb9e6afebcac9d27707`

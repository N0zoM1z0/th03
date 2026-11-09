# TH03 MAIN Yumemi: update truth tests and four-phase arrival scratch lifetimes (af1069l)

This pass reopens two substantial functions in the complete 2,358-byte
`ba_yumem` physical owner: the 368-byte `gba_boss_update_yumemi()` controller
and the 404-byte `yumemi_render_arrival()` four-phase raster renderer.

## Full update controller

The six level-derived parameter assignments remain in their original order.
The update-start result is now tested as a natural truth value:

```cpp
if(boss_update_start()) {
    // six level-derived parameters
}
```

The active-player mismatch still returns before PID selection, target update
or frame advancement. The opposite-player PID is now declared and initialized
inside the active path, after that early return:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
register pid_t pid_other = (1 - pid_current);
bullet_template.pid = pid_other;
boss_target_update();
boss_frame++;
```

The unsigned-word frame clock uses postfix increment. The effect-radius and
render-frame countdown guards now use natural truth tests:

```cpp
if(boss_effect_radius) {
    boss_effect_radius -= YUMEMI_EFFECT_RADIUS_DECAY;
}
if(boss_render_frame) {
    boss_render_frame--;
}
```

The byte postfix decrement remains untouched. INTRO sound/finish ordering,
mode switch, EXPLODE early return, origin updates, effect countdown, collision
map, hitbox setup and HP/hit-test tail remain in their original order.

## Four-phase arrival renderer

The shared `phase` scratch is now local to each of the three phases that need
it. Each branch declares and initializes its own byte value from the original
phase boundary:

```cpp
} else if(YUMEMI_ARRIVAL_PHASE2_END > boss_frame) {
    register unsigned char phase = boss_frame - YUMEMI_ARRIVAL_PHASE1_END;
    // original first closing raster
} else if(YUMEMI_ARRIVAL_PHASE3_END > boss_frame) {
    register unsigned char phase = boss_frame - YUMEMI_ARRIVAL_PHASE2_END;
    // original first opening raster and extra sprite
} else if(YUMEMI_ARRIVAL_PHASE4_END > boss_frame) {
    register unsigned char phase = boss_frame - YUMEMI_ARRIVAL_PHASE3_END;
    // original final opening raster
}
```

The first phase still has no phase-byte temporary. Its two-stage signed
`* 8` then `* 16` scaling, four inclusive raster conditions, signed 8-pixel
steps, clipping bounds, sprite order and phase-three extra sprite are
unchanged. The overlap-register XOR/interrupt protocol remains symbolic
assembly because the target instruction encoding is observable.

## Negative controls

- Moving `left` and `right` into each phase block changed the complete owner
  (`af1069m`); keep both register locals at function scope.
- Moving the `top` declaration to its first use after the sprite-size call
  changed the complete owner (`af1069n`); keep the original top declaration
  and assignment order.
- The phase-byte lifetime change itself passes when tested with the current
  update-controller changes; it is not inferred from the earlier af1048
  arrival experiments.

## Complete original-owner verification

Stage `af1069l` rebuilt the complete `ba_yumem` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,358 CODE bytes, 343 ordered
native fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1069l/report.json`

SHA-256: `b6d2f059081a14dee97a8228974df4f072ce53297aaffeb4a1a1f03391afc4b2`

Source SHA-256: `12e78d6dde750864df4e00f7b3893f2154c47413182d3524850cf228dd8100f1`

## Joint current-source integration

Stage `af1069o` rebuilt `ba_yumem` and `ba_chiyu` together in two independent
original TC4 rounds: 5,012 CODE bytes, 724 ordered native fields and 21 PUBLIC
offsets match. Both complete normal Japanese MAIN links reproduce the original
loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1069o/report.json`

SHA-256: `149d2e29ea2acc3d1cf976d3280d3a740a1cb3ccd5d093273f930e3038c9c553`

This is scoped local original-toolchain evidence, not a Factory Oracle
receipt, canonical packed-file acceptance or whole-product ownership claim.

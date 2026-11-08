# TH03 MAIN Mima Spread: positive fire-window guard

The 214-byte `mima_pattern_spread()` leaf now uses a positive fire-window
condition around its complete firing and finish path:

```cpp
if(boss_frame < MIMA_SPREAD_INITIAL_SETUP_END) {
    // initialize Particle mode and angles
    return;
}

if(boss_frame >= MIMA_SPREAD_FIRE_BEGIN) {
    // even-frame main volley and optional six-frame pellet pair
    // finish transition
}
```

The initial setup still returns immediately after setting Particle mode,
frame zero and the two initial angles. Frames between setup and fire are now
naturally represented by a false positive guard instead of an inverse
`return`. The even-frame bullet, conditional six-frame pellet pair, sound
ordering, angle increments and finish transition remain unchanged.

The compiler alternatives were isolated: first replacing the `else if`
with an independent early-return `if`, then replacing that return with the
positive fire-window guard. Both source variants produced the complete
original owner. The final maintained/indented source was rebuilt at
`af1031m`.

Stage `af1031m` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1031m/report.json`

SHA-256: `aa056e10aa64c3b29cd47efa5767a05b9cd9df4bae6b9695d5de05f98be5f796`

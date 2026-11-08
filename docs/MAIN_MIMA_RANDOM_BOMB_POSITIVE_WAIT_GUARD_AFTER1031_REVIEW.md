# TH03 MAIN Mima Random Bomb: positive post-warning wait guard

The 262-byte `mima_pattern_bomb_random()` leaf now scopes the live barrage,
ring, sound and finish logic under a positive wait-window condition:

```cpp
if(boss_frame > MIMA_RANDOM_BOMB_BULLET_WAIT_END) {
    // four-frame bullet/pellet pair, frame-0x40 ring, sound and finish
}
```

The earlier warning-mode transition and the three exact marker-frame bombs
remain outside this guard. The marker branch still returns immediately after
`bomb_center_add()`, preserving the original setup and call ordering. The
positive condition is equivalent to the former `if(frame <= wait_end) return`
but expresses the active attack window directly.

The trials were isolated. Removing the marker branch's own `return` changed
CODE and was reverted. Replacing the initial warning/early-return chain with
a combined positive `(warning || frame >= fire_begin)` guard also changed
CODE and was reverted. The positive wait-window guard itself, with the
original marker return and warning chain retained, is native-exact.

Stage `af1031s` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1031s/report.json`

SHA-256: `f751d73d93399f3b726980cb831a4b72b16fac38eba106fa946b9ba35d49f91d`

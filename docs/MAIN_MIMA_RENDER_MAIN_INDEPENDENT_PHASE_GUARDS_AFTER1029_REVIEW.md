# TH03 MAIN Mima renderer: independent early-return phase guards

`mima_render_main()` now expresses its render-mode dispatch as independent
`if` statements after the initial hit branch:

```cpp
if(boss_hit) {
    // draw damaged sprite
    return;
}
if(MIMA_RMODE_PARTICLE == boss_render_mode) {
    // shared Particle/Trail carrier path
    return;
}
if(MIMA_RMODE_EXPAND == boss_render_mode) {
    // draw expanded sprite
    return;
}
if(MIMA_RMODE_FLASH == boss_render_mode) {
    // draw flash sprite
    return;
}
if(MIMA_RMODE_TRAIL == boss_render_mode) {
    boss_render_frame = 0;
    goto render_mode_2;
}
```

Each preceding branch already returns, so the independent guards retain the
same mutually exclusive mode partition and leave the Particle/Trail shared
label and its byte-frame postincrement intact. This makes the early-return
structure explicit without replacing the target's important Trail-to-Particle
goto or merging the two modes.

Stage `af1029g` rebuilt the complete `ba_mima` physical owner in two
independent original Turbo C++ 4.02 rounds. All 1,922 CODE bytes, 277 ordered
native fields and nine PUBLIC offsets match. Both normal MAIN links reproduce
the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1029g/report.json`

SHA-256: `56390f88e7e177f52d3c4a4b132e68afa35fe30a802be763b25dbc8b62700e5e`

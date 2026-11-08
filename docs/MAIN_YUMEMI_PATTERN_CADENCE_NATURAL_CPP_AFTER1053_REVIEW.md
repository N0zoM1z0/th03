# TH03 MAIN Yumemi pattern cadence and phase comparisons: natural C++ after1053

This pass continues the full ten-function Yumemi BOSS source through its
ring, aimed, chase and rain attack controllers.

## Natural remainder and phase tests

The ring's unsigned-word four-frame firing cadence now uses a direct
remainder truth test:

```cpp
if(!(boss_frame % YUMEMI_RING_FIRE_PERIOD)) {
    // one ring volley, then the original angle/speed updates
}
```

The aimed attack's warning phase and the chase attack's beam phase now put
the named phase constant first:

```cpp
if(YUMEMI_AIMED_WARNING_PHASE ==
    (boss_frame % YUMEMI_AIMED_WARNING_PERIOD)) { ... }
if(YUMEMI_CHASE_BEAM_PHASE ==
    (boss_frame % YUMEMI_CHASE_BEAM_PERIOD)) { ... }
```

The aimed two-frame fire cadence and the variable unsigned-word rain
interval also use natural remainder truth tests. These changes preserve the
original modulo periods, phase values, attack timing and the order of sound,
RNG, bomb, bullet and movement calls. The chase's two consecutive
`boss_move_sine()` calls and its original SEEK/TRACK transition remain
separate.

Together with the preceding cross-ring pass, all four pattern families now
have natural modulo/remainder conditions where verified, and the cross-ring
producer keeps its four separate random angle draws and four bullet additions
in the original order.

## Complete original-owner verification

Stage `af1053h` rebuilt the complete 2,358-byte `ba_yumem` physical object in
two independent original Turbo C++ 4.02 rounds. All 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The other 98
original game objects and CRT were reused; no full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1053h/report.json`

SHA-256: `275dd3171104ce4dbe2c1d30b1278cbb4bbd7df5718dd8d4a041a4471de315ad`

This is natural-C++ recovery inside the already source-owned Yumemi object,
not new unique CODE ownership, raw vendor OMF packet identity or canonical
packed-game acceptance.

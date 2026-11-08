# TH03 MAIN Yumemi attack modulo and phase comparisons: natural C++ after1053

This follow-up expands the Yumemi pattern recovery through the ring, aimed,
chase and rain leaves. It keeps the existing attack timing constants and
separate state-machine bodies while making modulo and phase predicates more
idiomatic.

## Exact pattern predicates

- Ring fire: `!(boss_frame % YUMEMI_RING_FIRE_PERIOD)`.
- Aimed warning phase: `YUMEMI_AIMED_WARNING_PHASE == (boss_frame % YUMEMI_AIMED_WARNING_PERIOD)`.
- Aimed fire: `!(boss_frame % YUMEMI_AIMED_FIRE_PERIOD)`.
- Chase beam phase: `YUMEMI_CHASE_BEAM_PHASE == (boss_frame % YUMEMI_CHASE_BEAM_PERIOD)`.
- Variable rain cadence: `!(boss_frame % yumemi_rain_interval)`.

The cross-ring cadence was already converted to the same remainder truth
form in the preceding after1052 pass. These predicates retain the exact
unsigned-word periods, warning/fire phase, attack frame windows and original
RNG/bomb/bullet ordering. The chase continues to call `boss_move_sine()`
twice as two separate operations; the SEEK/TRACK transition and the two
player-coordinate member copies remain separate.

## Negative control: aggregate player-point assignment

A natural-looking replacement of the two player-coordinate assignments:

```cpp
boss_aux_point.x = players[bullet_template.pid].center.x;
boss_aux_point.y = players[bullet_template.pid].center.y;
```

with:

```cpp
boss_aux_point = players[bullet_template.pid].center;
```

changes complete `ba_yumem` CODE. The same aggregate replacement was tested
independently in both the aimed and chase leaves and rejected. Keep the two
component assignments so the original TC4 copy/code-generation sequence is
preserved.

## Complete original-owner verification

Stage `af1053j` rebuilt the complete 2,358-byte `ba_yumem` physical object in
two independent original Turbo C++ 4.02 rounds. All 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The other 98
original game objects and CRT were reused; no full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1053j/report.json`

SHA-256: `8d0fc9a8680f015423df8d1bd7e6f69dac3495e601f74c0c6a38c443a49b7907`

This is natural-C++ recovery inside the already source-owned Yumemi object,
not new unique CODE ownership, raw vendor OMF packet identity or canonical
packed-game acceptance.

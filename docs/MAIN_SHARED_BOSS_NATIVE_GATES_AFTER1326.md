# Shared major BOSS: exact edge, hit and pattern-count transitions

The shared BOSS producer owns the 24-sprite explosion ring and the
seven-function movement, spawn and pattern controller in two original
physical objects. The current source now states the left/right motion
boundaries as inclusive comparisons with `boss_center_x` on the left.
The descending state preserves its original downward step, enemy-active
flag store, and out-of-bounds exit. The explosion ring likewise compares
its grown radius directly to the original reward threshold.

`boss_hittest_end()` now checks positive HP and the already-exploding
mode independently before updating BOSS lifecycle state. The target
position remains fixed once the mode is DESCEND. `boss_pattern_next()`
continues to consume one RNG draw per rejected nearby attack; once the
original postincrement exceeds the selected pattern count, it directly
sets DESCEND mode. The original RNG `do/while` and the 32-byte `REP MOVSW`
template initialization are unchanged.

The source-bound original TC4/TLINK stage `af1326i` reproduces both
physical BOSS owners: **949 CODE bytes, 106 literal ordered native fields,
and eight PUBLICs**, two independent native compiler rounds and full
normal Japanese MAIN links. The bounded integration check `af1326h`
recompiled both shared BOSS units plus the newly source-bound VRAM plane
initializer and current Marisa BOSS, matching **2,421 CODE bytes, 309
ordered fields, and 18 PUBLICs** in both complete links.

A rejected original TC4 trial `af1326b` replaced the RNG rejection
`do/while` with an apparently equivalent infinite loop and opposite
comparison tests. Its different signed/unsigned register promotions and
branch directions shortened the controller from 601 to 600 CODE bytes.
The original loop remains intact. No filler, target patches or full cold
replay were used to obtain exactness.

Read-only verification of the current shared owner:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1326i
```

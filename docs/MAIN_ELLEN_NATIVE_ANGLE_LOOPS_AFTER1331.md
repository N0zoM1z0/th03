# Ellen BOSS: exact Extra Attack angles and intro flicker

The complete Ellen BOSS now uses natural byte-angle `+=` in both radial
Extra Attack bursts. Each burst still draws its own RNG word and divides
its 256-unit full turn by the original byte count on every iteration;
the angle changes *after* the far Extra Attack call. The paired-pellet
attack's separate 0x10-byte angle advance also accepts compound `+=` in
the current TC4 source. The intro sprite flicker is now an explicit
nested global-frame and intro-window gate, preserving earlier strip draws.

The original TC4 4.02 source-bound stage `af1331h` reproduces **all 1,675
physical CODE bytes**, 213 ordered OMF native fields and nine PUBLICs in
two independent rounds. The related `af1331i` stage jointly recompiles
Ellen, Bullet and both shared BOSS objects: **5,309 CODE bytes, 515 fields,
37 PUBLICs** and both complete normal Japanese MAIN links and ordered
MZ relocations match the original.

Compiler counterexamples matter here: `af1331d` made the spread-angle
advance compound `+=` and shortened the physical BOSS from 1,675 to
1,671 bytes, with 212 instead of 213 ordered fields. `af1331f` made
`boss_render_frame += 3` compile to a different memory ADD, also shrinking
the owner to 1,671 bytes. `af1331g` merged four render-strip decrements
with their negative tests and shrank CODE to 1,667 bytes. These changes
were individually rejected. Equal-looking C++ syntax in another BOSS
cannot substitute for the real owner-specific compiler proof.

Read-only verification of current native source:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1331h af1331i
```

## 2026-11-11: source-exact late volley and strip-phase control

`ellen_pattern_extra()` now gates the final signed -2 radial Extra Attack
volley with a positive comparison against its original final frame. The
large DI/SI-local angular loop stays in that guarded scope, with the
original one RNG draw, signed mode argument, divide-per-iteration angle
step and final SELECT transition. The warning phase and first positive
radial burst are unaffected. `ellen_pattern_spread()` now uses explicit
zero/nonzero unsigned-word two-frame firing conditions and a positive
finish phase at the existing `done` label. It retains `fire_single` and
the exact sound/fire/angle-increment order. The pellet controller also
commits its mode reset under a positive terminal-frame condition.

The intro renderer now short-circuits odd global frames and the first
0x40 intro ticks in a single ordered condition, *after* its three
original strip draws. This preserves all four eight-sprite radial
families and their byte-angle progression.

Complete-owner stages `af1353a` (intro), `af1353b` (spread cadence),
`af1353c` (spread completion), `af1353d` (final Extra Attack) and
`af1353e` (pellet completion) passed two original TC4 4.02 rounds.
The current `af1353e` proves **1,675 CODE bytes, 213 ordered native
fields and 9 PUBLICs**. A five-object consumer check `af1353f`
recompiled Ellen BOSS, Ellen Extra Attack, Bullet and both shared BOSS
objects: **6,438 CODE bytes, 594 ordered fields and 43 PUBLICs**
with complete normal Japanese MAIN links and ordered MZ relocations
exact. No new Factory packed-file acceptance is asserted.

Current source receipt: `.analysis/work/exatt-layout-af1353e/report.json`,
SHA-256 `fedf221acaab1f6011a0d992e862f475a6a71eb19be8b9d884371e944d797171`.
Joint receipt: `.analysis/work/exatt-layout-af1353f/report.json`,
SHA-256 `e51c8d102b876bed9dc8b8fdfde5bf47add5b1910fbc38c199ef7dc18f90525f`.

## 2026-11-11: pre-tested loops across both large BOSS subsystems

Five real loops in the maintained Ellen BOSS now use pre-tested `while`
forms: the eight-shot spread volley; the first and last radial Extra
Attack rings; and both levels of the four-by-eight intro sprite raster.
Each loop retains the original counter initialization, the emitter call,
then its signed-index increment and byte-angle update. The two Extra
Attack loops still perform signed word division at every step, advance
the angle after each far call and draw exactly one initial RNG value per
burst. The intro's outer loop advances the separate group angle and
sprite bank only after all eight sprites of that group.

Both spread and pellet controllers also return directly on unfinished
frames, allowing the original terminal state assignments to stand after
the guard. The spread's `fire_single` and `done` labels remain: removing
their control transfer by reversed tests (`af1360a`) or natural case
fallthrough (`af1360b`) changed TC4's jump layout. Replacing Extra
Attack's three warning comparisons with a `switch` (`af1360e`) likewise
changed CODE and was reverted.

Incremental native stages `af1360c` and `af1360d` proved terminal exits;
`af1360f`, `af1360g`, `af1360h`, `af1360i` and `af1360j` proved each
loop transformation. Current-source `af1360k` recompiles the complete
**1,675-byte Ellen BOSS**, with 213 ordered native fields and nine
PUBLICs, twice using the original Turbo C++ 4.02 toolchain. The
seven-object consumer check `af1360l` recompiles Ellen BOSS, Ellen
Extra Attack, Bullet, both shared BOSS objects, Polar and sound:
**6,584 CODE bytes, 612 ordered fields and 46 PUBLICs**. Both normal
Japanese MAIN links and ordered relocations match.

Owner receipt: `.analysis/work/exatt-layout-af1360k/report.json`, SHA-256
`ebeff3da0d49da0050974eca0bc0f0941ec67d9292bdee44a0bdc124f0e11069`.
Joint receipt: `.analysis/work/exatt-layout-af1360l/report.json`, SHA-256
`71f7463a11f195ce8da2aff747e2fc7bca92eb4cdef7a49ed4b91acc7f13db6d`.

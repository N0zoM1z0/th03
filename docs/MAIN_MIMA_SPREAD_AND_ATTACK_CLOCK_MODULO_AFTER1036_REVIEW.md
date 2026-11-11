# TH03 MAIN Mima Spread and attack clocks: natural modulo and byte-angle updates

The 214-byte `mima_pattern_spread()` now uses constant-first phase guards,
ordinary unsigned-word comparisons and compound byte-angle increments:

```cpp
if(MIMA_SPREAD_INITIAL_SETUP_END > boss_frame) {
    // particle setup
    return;
}

if(MIMA_SPREAD_FIRE_BEGIN <= boss_frame) {
    if(0 == (boss_frame % MIMA_FIRE_EVEN_PERIOD)) {
        // main volley
        mima_spread_angle += MIMA_SPREAD_ANGLE_STEP;
        if(
            (boss_frame < mima_pellet_until) &&
            (0 == (boss_frame % MIMA_SPREAD_PELLET_PERIOD))
        ) {
            // opposite pellet pair
        }
        mima_pellet_angle += MIMA_PELLET_ANGLE_STEP;
    }
    if(MIMA_SPREAD_FIRE_END_AFTER < boss_frame) {
        // SELECT transition
    }
}
```

The initial setup still returns before the fire window. The main volley remains
even-frame only, the optional side pellets remain on the six-frame unsigned
word cadence, both byte-angle updates remain after their original bullet
operations, and the finish transition remains after the firing block.

The same natural modulo spelling now replaces all three power-of-two masks
across Random Bomb and Orbit:

```cpp
0 == (boss_frame % MIMA_RANDOM_BOMB_FIRE_PERIOD) // period 4
0 == (boss_frame % MIMA_FIRE_EVEN_PERIOD)        // period 2
```

The expressions are unsigned-word timer modulo operations. Original TC4
optimizes them to the same native mask instructions. The zero comparison is
constant-first. This is supported by complete-owner comparison, not merely
by algebraic equivalence.

Stage `af1036i` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1036i/report.json`

SHA-256: `976d02bb1afbaeb6457ab83dafb77d26d072dbbac692b0097375eaae06811171`

## Related negative control

Replacing the unsigned division by four in the level-derived random count
with `gba_boss_level >> 2` changed complete CODE (af1035q). Keep the named
integer division; do not generalize the modulo-to-mask optimization into a
claim that every division can become a shift.

## 2026-11-11: whole Mima BOSS current-source gate recovery

`mima_pattern_spread()` now expresses the optional pellet volley as a single
ordered short-circuit condition: first the unsigned-word expiry check, then
the unsigned-word six-frame remainder. The two pellets still fire at their
original angles and speed, and the angle update still occurs after the
optional volley on each eligible main-attack tick. All four other even/four-
frame attack clocks in `mima_pattern_spread`, `mima_pattern_bomb_random`, and
`mima_pattern_orbit` now state an explicit zero-remainder predicate. The
original word division, RNG use, sounds and state transitions are unchanged.

An independent trial `af1351e` replaced the trail-phase group selection with
an equivalent conditional expression. TC4 emitted **1,918 instead of 1,922
CODE bytes**; the compiler-visible branch layout differs, so that variant
was discarded. The successful current `af1351b` stage compiled the entire
**1,922-byte Mima BOSS** twice, matching all **277 ordered native fields**,
**9 PUBLICs**, and both normal Japanese MAIN links. It is independently
jointly linked with the two shared BOSS objects at `af1351f` (**2,871 CODE
bytes, 383 ordered fields, 17 PUBLICs**).

Current source receipt: `.analysis/work/exatt-layout-af1351b/report.json`,
SHA-256 `59de33d539412208037239c6265331278db7c3327865ac4cd5929130387b7c2e`.
Joint receipt: `.analysis/work/exatt-layout-af1351f/report.json`,
SHA-256 `760a257f1db1ac33f7e997be1d12c0ab995b2ea068c45f3934cce88d0df5a65d`.

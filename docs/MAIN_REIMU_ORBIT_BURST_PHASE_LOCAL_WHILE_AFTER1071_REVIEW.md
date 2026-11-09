# TH03 MAIN Reimu Orbit Burst: three phase-local natural while loops (af1071q)

The complete 443-byte `reimu_pattern_orbit_burst()` leaf now uses three
separate natural `while` loops, one for each original attack phase. Each phase
owns its own signed index and byte-angle scratch in the narrowest useful
scope. The original phase gates, return points, ring cadence, stored point
arrays and Extra Attack release order remain intact.

## Phase-local C++ shape

The expansion phase now uses:

```cpp
int i = 0;
while(i < reimu_orbit_count) {
    unsigned char angle;
    angle = static_cast<unsigned char>(
        ((i << 8) / reimu_orbit_count) + reimu_orbit_angle
    );
    // original X and Y polar calls and array writes
    ++i;
}
```

The hold and release phases each declare their own `int i = 0` and their own
`unsigned char angle` inside their respective blocks. This removes both
function-scope scratch variables. The index remains signed: `i << 8` is
performed before signed division by `reimu_orbit_count`, then the orbit base
angle is added and explicitly truncated to one byte. Do not move the division
before the shift or change the signed intermediate.

The expansion radius still uses `TO_SP(boss_frame) * 2`, preserving the
original two-stage fixed-point scaling. The hold phase retains the constant
48-pixel radius, writes both stored coordinate arrays before advancing the
index, and updates the global byte orbit angle after the loop. The release
phase emits `reimu_extra_add()` in stored-index order and only then resets the
mode, frame and render mode.

## Natural control-flow and arithmetic variants retained

The current source also uses these independently verified natural forms:

- Variable-first frame gates: `boss_frame == REIMU_ORBIT_INIT_FRAME`,
  `boss_frame < REIMU_ORBIT_EXPAND_END`,
  `boss_frame < REIMU_ORBIT_RELEASE_FRAME`, and
  `boss_frame == REIMU_ORBIT_RELEASE_FRAME`.
- Explicit unsigned-byte self-addition:
  `reimu_orbit_angle = reimu_orbit_angle + REIMU_ORBIT_ANGLE_STEP;`
- Explicit ring cadence zero test: `round_frame_mod16 == 0`.
- Early return for non-ring frames before the unchanged ring projectile
  template and RNG sequence.
- Prefix `++i` at the end of each while body. Postfix was also tested in the
  while bodies and matched; prefix is the maintained spelling.
- Ordinary `int` and `unsigned char` locals without `register` both match.

## Rejected alternative

Splitting each byte-angle calculation into an assignment followed by compound
addition:

```cpp
angle = reimu_orbit_angle;
angle += (i << 8) / reimu_orbit_count;
```

changed the complete physical owner (`af1071h`). Keep the single quotient-first
assignment with explicit byte truncation.

## Complete original-owner verification

Stage `af1071q` rebuilt the complete `ba_reimu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,020 CODE bytes, 270 ordered
native fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1071q/report.json`

SHA-256: `428aff902834728c9e76b0a3b609f18365a04c493fc407ee3813b3cdf0408492`

Source SHA-256: `36f53d1f70947ebceca8fd67aea64a5424e8c7ae74f5dfbff9a4177269635988`

## Joint current-source integration

Stage `af1071r` rebuilt Reimu, Yumemi and Chiyuri together in two independent
original TC4 rounds: 7,032 CODE bytes, 994 ordered native fields and 30 PUBLIC
offsets match. Both complete normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1071r/report.json`

SHA-256: `38e27eb2acb2293e369d5a2057b227498181d16cc48872b5d7df611e03915e9a`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

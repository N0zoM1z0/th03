# TH03 MAIN Reimu Orbit Cloud: phase-local byte-angle state (af1072u)

The 339-byte `reimu_pattern_orbit_cloud()` leaf no longer carries one
function-scope `unsigned char angle` across two independent uses. The first
angle lifetime now covers only the direction-adjusted cloud shot pair; the
second covers only the center-orbit Y calculation after the speed update.
Both blocks declare their own byte scratch. This is a genuine lifetime
recovery: the angle is recomputed for the center orbit and never needs to
survive across the intervening acceleration logic.

## First angle phase and two-projectile emission

```cpp
{
    unsigned char angle;
    angle = static_cast<unsigned char>(boss_frame) * REIMU_CLOUD_ANGLE_FRAME_STEP;
    if(reimu_direction != 0) {
        angle = 0 - angle;
    }
    if(0 == (boss_frame % reimu_cloud_interval)) {
        // original first pellet-cloud projectile
        bullets_add();
        bullet_template.angle = ((angle << 1) + REIMU_CLOUD_OPPOSITE_ANGLE);
        angle = angle + REIMU_CLOUD_OPPOSITE_ANGLE;
        // original second pellet-cloud projectile
        bullets_add();
    }
}
```

The variable unsigned-word interval remains modulo; it is not a constant
period and cannot be replaced by a low-bit mask. The two cloud projectile
centers still use the original `polar()` table lookups and radius. The first
angle is based on the byte-cast frame, multiplied by the named frame step, and
negated with implicit byte truncation when the direction flag is nonzero.
The second projectile adds the named half-turn to the local byte angle only
after writing the opposite projectile angle.

The initial frame setup remains before both scopes: anchor X/Y, direction RNG
and initial cloud speed are preserved in order. The variable-interval test
still gates both emissions together.

## Acceleration and center-orbit phase

The fixed period-two speed update is now expressed as a low-bit test:

```cpp
if((boss_frame & (REIMU_CLOUD_ACCEL_PERIOD - 1)) == 0) {
    reimu_cloud_speed++;
}
```

The byte-field postfix increment is intentional. Prefix increment, compound
`+= 1`, and explicit `speed = speed + 1` were all re-tested and changed the
complete original owner.

The center orbit gets a fresh byte angle after acceleration:

```cpp
{
    unsigned char angle;
    angle = static_cast<unsigned char>(boss_frame) * REIMU_CLOUD_ANGLE_FRAME_STEP;
    angle = angle + REIMU_CLOUD_ANGLE_ROTATION;
    boss_center_y = polar(
        boss_aux_point.y.v, REIMU_CLOUD_CENTER_ORBIT_RADIUS, SinTable8[angle]
    );
}
```

The finish transition is variable-first (`boss_frame >= REIMU_CLOUD_FINISH_FRAME`).
The orbit center is updated before the finish check, as in the original.

## Additional exact natural-expression trials

The following forms all match the complete `ba_reimu` owner in two original
TC4 rounds:

- `if(boss_frame == REIMU_CLOUD_START_FRAME)` and
  `if(boss_frame >= REIMU_CLOUD_FINISH_FRAME)`.
- `if(reimu_direction != 0)`.
- `if(0 == (boss_frame % reimu_cloud_interval))` for the dynamic interval.
- `if((boss_frame & (REIMU_CLOUD_ACCEL_PERIOD - 1)) == 0)` for the fixed
  period-two acceleration.
- `static_cast<unsigned char>(boss_frame) * REIMU_CLOUD_ANGLE_FRAME_STEP`
  for the frame-derived byte angle.
- `angle = 0 - angle` for direction reversal, relying on assignment's byte
  truncation.
- `angle = angle + REIMU_CLOUD_OPPOSITE_ANGLE` and
  `angle = angle + REIMU_CLOUD_ANGLE_ROTATION` for the two byte additions.
- `angle << 1` for both projectile angle doublings.

Negative controls: unary `-angle` changed CODE; selecting `-2`/`2` through a
ternary changed CODE; prefix or explicit arithmetic speed increments changed
CODE. The maintained source keeps the passing explicit forms and postfix byte
increment.

## Complete original-owner verification

Stage `af1072u` rebuilt the complete `ba_reimu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,020 CODE bytes, 270 ordered
native fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1072u/report.json`

SHA-256: `9bb56bb1b81c8bfd74caf86153bb38a4d9eab258182e0eead803f05c5f6c5641`

Source SHA-256: `b51cd8e17ceda2f5e2cd7cb6ecaff226a975619fab33ac59db68f8a7a7c84fd9`

## Joint current-source integration

Stage `af1072v` rebuilt Reimu, Yumemi and Chiyuri together in two independent
original TC4 rounds: 7,032 CODE bytes, 994 ordered native fields and 30 PUBLIC
offsets match. Both complete normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1072v/report.json`

SHA-256: `6892e75dc0c0628e7cbb4d8f7875a460b785cd345a5c9e02357be4c582235920`

This is scoped original-toolchain evidence, not a Factory Oracle receipt,
raw vendor OMF identity claim, or canonical packed-file acceptance.

# TH03 MAIN Reimu: Orbit Burst, Orbit Cloud and Update natural C++ recovery

This pass continues three substantial parts of the complete 2,020-byte Reimu
BOSS: the 443-byte three-phase Orbit Burst controller, the 339-byte Orbit
Cloud controller and the 296-byte far Update controller.

## Orbit Burst: three phases and shared signed-angle arithmetic

The three frame phases now use constant-first comparisons. Since each of the
first two phase bodies already returns, the nested `else if` chain is now
three independent guards. This makes the state progression explicit while
preserving the original expansion, held-radius ring firing and release-time
Extra Attack ordering:

```cpp
if(REIMU_ORBIT_EXPAND_END > boss_frame) {
    // expand the orbit, advance its angle, return
}
if(REIMU_ORBIT_RELEASE_FRAME > boss_frame) {
    // hold the orbit, optionally fire a ring, advance its angle, return
}
if(REIMU_ORBIT_RELEASE_FRAME == boss_frame) {
    // release each stored point as an Extra Attack
}
```

The local angle is now a register-qualified byte and all three radial loops
use postfix `i++`. The angle distribution keeps signed `i * 256` before
integer division and applies the current byte angle after division:

```cpp
angle = reimu_orbit_angle +
    (REIMU_ORBIT_ANGLE_UNITS * i) / reimu_orbit_count;
```

The expansion radius now expresses the native two-stage scale through the
project's subpixel macro:

```cpp
TO_SP(boss_frame) * 2
```

The order matters: the single `boss_frame * 32` expression changes CODE, as
does `TO_SP(boss_frame * 2)`. `TO_SP(boss_frame) * 2` is the natural form
that reproduces the original instructions. The two global unsigned-byte
orbit-angle updates also accept compound `+=` in this owner.

## Orbit Cloud: byte-angle and timer arithmetic

The shared 48-pixel center trajectory now has a named
`REIMU_CLOUD_CENTER_ORBIT_RADIUS`, used for both the initial anchor offset
and the center's later polar movement. The distinct 32-pixel projectile
orbit radius remains `REIMU_CLOUD_ORBIT_RADIUS`.

The start and finish frame tests are constant-first. The unsigned-word
projectile interval and two-frame acceleration cadence now use natural
remainder truth tests:

```cpp
if(!(boss_frame % reimu_cloud_interval)) { ... }
if(!(boss_frame % REIMU_CLOUD_ACCEL_PERIOD)) { ... }
```

Both frame-derived byte angles use constant-first multiplication with an
explicit C++ byte conversion. The negative direction still uses explicit
subtraction followed by byte truncation, now written with `static_cast`:

```cpp
angle = REIMU_CLOUD_ANGLE_FRAME_STEP *
    static_cast<unsigned char>(boss_frame);
angle = static_cast<unsigned char>(0 - angle);
```

Both local byte-angle rotations accept compound `+=`. The cloud-speed
increment remains postfix; prefix `++reimu_cloud_speed` changes CODE.

## Update controller

The complete 296-byte `gba_boss_update_reimu()` now uses a register-qualified
`pid_other`, postfix BOSS-frame increment, constant-first level formulas,
and constant-first INTRO/SELECT mode and frame comparisons. The positive
launched-player scope, INTRO return, mode dispatch, collision map and hitbox
lifetime remain unchanged.

## Negative controls

The following alternatives were compiled and rejected against the complete
original owner:

- `boss_frame * 32` instead of `TO_SP(boss_frame) * 2` changes CODE.
- `TO_SP(boss_frame * 2)` also changes CODE.
- `static_cast<unsigned char>(-angle)` changes CODE; retain the explicit
  `static_cast<unsigned char>(0 - angle)` byte-wrap expression.
- Prefix `++reimu_cloud_speed` changes CODE; retain postfix increment.

The compiler accepted both postfix and prefix loop increments in earlier
independent Reimu work; this pass uses postfix in the three Orbit Burst loops.
The exact current source, rather than a historical note, is the basis for the
verification below.

## Complete-owner verification

Stage `af1044m` rebuilt the complete `ba_reimu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,020 CODE bytes, 270 ordered
native fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1044m/report.json`

SHA-256: `7b4ffab9145a0b13cc8983b1e87ffd593cd37893a52995cf45e284f068f751bd`

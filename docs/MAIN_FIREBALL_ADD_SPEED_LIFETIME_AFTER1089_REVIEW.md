# TH03 MAIN Fireball: first-use speed lifetime in the 329-byte allocator (af1089k)

The complete far-cdecl `fireballs_add()` allocator now declares its randomized
speed scratch at the first assignment that produces the initial transfer
speed:

```cpp
fireball_p->center.x.v = origin_center_x;
fireball_p->center.y.v = origin_center_y;
fireball_p->pid = origin.pid;

subpixel_length_8_t speed = (
    to_sp(1.25f) +
    (round_speed / 2) +
    randring2_next16_ge_lt_sp(0.0f, 2.0f)
);
```

This is later than the free-slot guard and later than the fireball's initial
center/PID stores. The local remains live for the later fall-speed calculation
and `vector2_between_plus()` call; the first randomized value is still clamped,
stored as `fall_velocity_y`, and used for the same original transfer/fall
behavior. No RNG call or projectile-state mutation was reordered.

The allocator retains its compiler-sensitive `for` / `continue` / `return`
shape and its original signed index and near-pointer progression. The
`pid_target`, origin-center and screen-X scratch lifetimes are intentionally
not moved: tested alternatives changed the complete physical object.

## Explored alternatives

- Moving `pid_target` below the first-free-slot guard changed CODE (`af1089a`).
- Moving `screen_x` to its first assignment changed CODE (`af1089c`).
- Moving `origin_center_y` or `origin_center_x` below the free-slot guard
  changed CODE (`af1089d`, `af1089e`).
- Moving the allocator index into its `for` header changed CODE (`af1089f`).
- Moving the explosion renderer's byte `cycle` local into its middle frame
  branch changed CODE (`af1089i`).

The successful speed-local declaration is deliberately kept distinct from
those rejected lifetime changes.

## Complete original-owner verification

Stage `af1089j` rebuilt the complete Fireball physical owner in two
independent original Turbo C++ 4.02 rounds. All 1,555 CODE bytes, 115 ordered
native fields and ten PUBLIC offsets match. The original one-byte DATA and
one-byte BSS carriers are preserved, and both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The source
overlay checked the maintained `fireball.cpp` producer.

Report: `.analysis/work/exatt-layout-af1089j/report.json`

SHA-256: `ea52d4b059f6dd3d966419101f1906696c2b30431b905fbb2782d95da6ac9bb5`

Current `fireball.cpp` SHA-256:
`46354748fbc825592ed1801d446b1f0e60bb7efabd08912c3f529dfa35936294`

## Ten-owner integration

Stage `af1089k` rebuilt the current Fireball owner together with `bullet`,
`ba_mima`, `ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`, `ex_reup`
and `hitcirc` in two independent original TC4 rounds: 16,635 CODE bytes,
1,947 ordered native fields and 94 PUBLIC offsets match. Both normal Japanese
MAIN links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1089k/report.json`

SHA-256: `2b732ac99f269133adcbf848539d64b99aa5a79c2332a57649434c81476b010e`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

# TH03 MAIN Chiyuri Update: natural arithmetic, pointer indexing and local lifetimes

The complete 613-byte `gba_boss_update_chiyuri()` controller now uses a
larger set of natural C++ spellings while retaining the original full-owner
TC4 output. The work covers level setup, INTRO/SELECT transitions, paired
center selection, mode selection, render cadence and the palette/collision
suffix.

## Level-derived parameter setup

The five additive expressions now put their fixed bases first:

```cpp
chiyuri_cardinal_speed = 0x30 + gba_boss_level;
chiyuri_ring_speed = 0x34 + gba_boss_level;
chiyuri_trail_speed = 0x38 + (2 * gba_boss_level);
chiyuri_fan_speed = 0x10 + gba_boss_level;
chiyuri_fan_count = 0x0C + (gba_boss_level / 2);
```

The cardinal/ring interval formulas retain their existing base-minus-level
and base-minus-level/4 order. No shared cached level local is introduced;
prior attempts to cache the seven values changed complete CODE.

## Active-player path and frame control

- `pid_other` is now a `register pid_t`, declared before the register byte
  `random_i`.
- The unsigned-word BOSS clock uses postfix `boss_frame++`.
- INTRO completion, INTRO cross-effect, and SELECT timer comparisons put
  their fixed frame constants first.
- The render-cadence boolean is now `0 == (round_or_result_frame &
  (CHIYURI_RENDER_ANIM_PERIOD - 1))`.
- The SELECT palette-cycle comparison is constant-first.

The byte `boss_pattern_i++`, byte `boss_move_phase--`, byte render-frame
mask, byte `boss_render_mode--`, and collision/hitbox tail retain their
original operation forms and order.

## INTRO cross-effect coordinates

The four cross-effect center coordinates use constant-first offsets:

```cpp
(-TO_SP(56)) + boss_center_x
TO_SP(56) + boss_center_x
(-TO_SP(56)) + boss_center_y
TO_SP(56) + boss_center_y
```

All four original `bomb_center_add()` calls and their order remain intact.

## SELECT paired-center indexing and random mode

The five-way random selector now uses multiplication rather than a shift:

```cpp
random_i = 2 * randring_far_next16_mod(5);
boss_center_x = *(chiyuri_boss_x_words + random_i);
boss_center_y = *(chiyuri_boss_y_words + random_i);
```

The random call is still evaluated once, and the same doubled byte index
selects the same pair of word-array entries. Pointer arithmetic plus
indirection replaces array-subscript syntax without changing the complete
owner. The random mode expression is now base-first:

```cpp
boss_mode = CHIYURI_MODE_CARDINAL_0 + randring_far_next16_and(0x0F);
```

The pattern-counter increment and descent override remain in their original
order.

The palette countdown call uses constant-first multiplication:

```cpp
bomb_palette_step(16 * boss_move_phase, pid_other);
```

The byte decrement and nested nonzero guard remain unchanged.

## Negative controls

The following alternatives were tested against the complete owner and
rejected because their CODE payload differed:

- Reverse `boss_pattern_i > boss_pattern_count` to
  `boss_pattern_count < boss_pattern_i`.
- Replace `1 - pid_current` with either `pid_current ^ 1` or
  `!pid_current`.
- Move `pid_other` into the launched-player block as an initialized local.
- Put `random_i` before `pid_other` in the register declaration order.
- Expand `boss_hp -= boss_hit` to `boss_hp = boss_hp - boss_hit`.

Keep the original pattern-counter comparison, `1 - pid_current`, outer
`pid_other` declaration, `pid_other`-before-`random_i` declaration order,
and HP compound subtraction.

## Complete-owner verification

Stage `af1038w` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1038w/report.json`

SHA-256: `e6789c68d298a7b4d1d789adf7128f69265ae55b265f9b340f30e7fac7d8940f`

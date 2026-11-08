# TH03 MAIN Mima renderers: natural coordinate and sprite-bank arithmetic

This pass continues both the 305-byte `mima_render_main()` and the 223-byte
Pascal `mima_render_split()` leaves in the complete `ba_mima` physical owner.

## Main renderer

The main sprite origin now uses the shared project pixel conversion and
constant-first half-sprite placement:

```cpp
left = -MIMA_RENDER_MAIN_LEFT_HALF +
    playfield_fg_x_to_screen(boss_center_x, pid_other);
top = -MIMA_RENDER_MAIN_TOP_HALF + TO_PIXEL(boss_center_y);
```

The damaged sprite bank, Particle sprite bank, Particle carrier bank and
Flash sprite bank all use the named offset before the common BOSS sprite
base:

```cpp
MIMA_DAMAGED_SPRITE_OFF + boss_sprite_offset
MIMA_PART_SPRITE_OFF + boss_sprite_offset
MIMA_PART_CARRIER_OFF + boss_sprite_offset
```

Both Particle and Flash sprite X positions use
`MIMA_PART_SPRITE_LEFT + left`. The Particle/Trail shared label, nested
constant-first frame thresholds, carrier offset adjustment, byte-frame
postincrement, Trail reset and early-return dispatch remain unchanged.

## Split renderer

The split renderer uses the same base-first main-sprite origin calculation:

```cpp
base_left = -MIMA_RENDER_MAIN_LEFT_HALF +
    playfield_fg_x_to_screen(boss_center_x, pid_other);
base_top = -MIMA_RENDER_MAIN_TOP_HALF + TO_PIXEL(boss_center_y);
```

The original `register int split_distance = distance` remains before the
register X scratch, preserving the SI/DI lifetime recovered in af717a. The
three original hardware mask writes (`0xAAAA`, `0x5555`, `0xFFFF`), first
polar/draw pair, byte-angle compound half-turn, second polar/draw pair and
mask restore remain in their original order.

## Complete-owner verification

Stage `af1042i` rebuilt the complete `ba_mima` physical owner in two
independent original Turbo C++ 4.02 rounds. All 1,922 CODE bytes, 277 ordered
native fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1042i/report.json`

SHA-256: `8aa737452563b540198d6b8dd4ae08305380a13938d3526123288b3cfc4ca6b0`

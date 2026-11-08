# TH03 MAIN Chiyuri renderers: natural coordinate and sprite arithmetic

This pass covers the complete `ba_chiyu` physical owner while improving all
four Chiyuri render leaves: the 178-byte ring renderer, 205-byte main
renderer, 91-byte INTRO renderer and 97-byte monochrome renderer.

## Ring renderer

The 16-sprite ring now uses natural base-first arithmetic for its radius,
sprite bank and animation offset:

```cpp
radius = CHIYURI_RING_RADIUS_SCALE * boss_effect_radius;
sprite_offset = CHIYURI_RING_SPRITE_OFFSET + boss_sprite_offset;
sprite_offset += CHIYURI_RING_SPRITE_ANIM_SCALE * boss_render_frame;
```

The loop keeps its original pre-tested `for` traversal and byte-angle state,
but uses postfix `i++` and constant-first angle advancement. Its X scratch
was hoisted from the loop body to the function scope without changing the
signed-index/coordinate register assignment. The screen center is expressed
as a negative half-sprite width plus the single playfield conversion:

```cpp
left = -(CHIYURI_RING_SPRITE_WIDTH / 2) +
    playfield_fg_x_to_screen(left, pid_other);
```

The signed Y conversion now uses the shared project macro:

```cpp
top = TO_PIXEL(top);
```

`TO_PIXEL(v)` expands to the existing signed `v >> SUBPIXEL_BITS` operation;
this is not a division rewrite and retains the original negative-coordinate
rounding behavior. The earlier compound `top >>= 4` attempt changed TC4 CODE
and remains rejected.

## Main renderer

The main sprite's horizontal and vertical placement now use base-first
coordinate expressions and the common pixel conversion macro:

```cpp
left = -CHIYURI_RENDER_MAIN_LEFT_HALF +
    playfield_fg_x_to_screen(boss_center_x, (1 - pid_current));
top = -CHIYURI_RENDER_MAIN_TOP_OFF + TO_PIXEL(boss_center_y);
```

The animation offset is expressed as the named sprite base plus the
constant-first frame scale:

```cpp
sprite_offset += CHIYURI_RENDER_ANIM_SPRITE_BASE +
    (CHIYURI_RENDER_ANIM_PERIOD * boss_render_frame);
```

The original hit sprite path, `boss_hit` early return, zero-frame return,
monochrome threshold chain and sprite emission order remain unchanged.

## INTRO renderer

All three signed-word frame comparisons now put their phase constants first:

- Last-frame render gate: `CHIYURI_INTRO_RENDER_LAST_END > boss_frame`
- First raster phase: `CHIYURI_INTRO_RENDER_FIRST_END > frame`
- Second raster phase: `CHIYURI_INTRO_RENDER_SECOND_END > frame`

The signed `frame` local remains separately declared and assigned after the
round-frame early return. All three radius formulas retain signed `frame << 3`.
The three byte `boss_move_phase` changes retain their original AL-mediated
load/add/store sequences; direct C++ `+=` or subtraction changed CODE in
previous independent trials. Ring rendering remains after all phase updates.

## Monochrome renderer

The monochrome sprite uses the same natural placement forms as the main
renderer, including the named main-left half-width and top offset, and
`TO_PIXEL(boss_center_y)`. The original monochrome/color interrupt sequence,
color argument, sprite call and reset interrupt are unchanged.

## Negative controls

The following apparently natural alternatives were tested and restored:

- `left = CHIYURI_RENDER_HIT_LEFT_OFF + left` changed complete CODE; retain
  `left += CHIYURI_RENDER_HIT_LEFT_OFF`.
- `top = CHIYURI_RENDER_HIT_TOP_OFF + top` changed complete CODE; retain
  `top += CHIYURI_RENDER_HIT_TOP_OFF`.
- Initializing the INTRO `frame` local in its declaration changed complete
  CODE; retain the separate assignment after the early-return gate.
- Replacing the existing signed `TO_PIXEL`-equivalent conversion with
  compound `>>=` changed complete CODE.

## Complete-owner verification

Stage `af1041j` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1041j/report.json`

SHA-256: `f2573e2b16667070a7d63d65245e69d6862a7a732cd61263c048e7a2cf365a2f`

# TH03 MAIN: natural Kotohime and Chiyuri ring renderers

The complete Kotohime and Chiyuri BOSS objects now use natural C++ loop
headers in their ring renderers, with the original TC4 4.02 CODE and
ordered OMF fields preserved. Their main renderers also use natural
byte-truth tests and mutually exclusive normal/monochrome state selection.

## Kotohime ring renderer

kotohime_render_ring() replaces its manually initialized while with:

    for(i = 0; i < count; ++i) {
        register screen_x_t left;
        unsigned char angle;
        angle = (((i * KOTOHIME_FULL_TURN_STEPS) / count) + boss_move_phase);
        // original polar geometry, screen conversion and sprite16_put
    }

The loop retains its original register int i. The per-iteration screen-X
temporary and byte angle are now scoped to the iteration; the signed
16-bit multiply/divide still precedes angle truncation, and the Y coordinate
conversion remains the original assigned right shift.

kotohime_render_main() now spells its byte-valued state naturally:

    if(boss_hit) {
        sprite_offset += 0x10;
    }
    sprite16_put(left, top, sprite_offset);

    if(boss_render_mode) {
        kotohime_render_ring(kotohime_orbit_count);
    }

Both truth tests reproduce the original complete physical object.

## Chiyuri 16-sprite orbit renderer

chiyuri_render_ring() now puts both original update operations in the
for-header, in their original order:

    for(
        i = 0, angle = boss_move_phase;
        i < CHIYURI_RING_SPRITES;
        ++i, angle = angle + CHIYURI_RING_SPRITE_ANGLE_STEP
    ) {
        register screen_x_t left;
        // original polar geometry, screen conversion and sprite16_put
    }

The signed index advances before the byte-angle assignment, matching the
former body sequence. The left screen coordinate is now iteration-local.
The top coordinate remains function-local: moving it into the loop, with
or without register, changed complete CODE. The named byte assignment
must remain angle = angle + STEP; the earlier compound enum-valued
angle += STEP alternative changed CODE.

## Chiyuri main renderer

The normal sprite path always returns, so the monochrome state ladder is
now explicitly its else-if continuation. Three byte tests also use
natural truth expressions:

    if(!boss_render_mode) {
        // normal sprite path; every route returns
    } else if(boss_render_mode >= CHIYURI_MONO_COLOR6_LATE_STEP) {
        chiyuri_render_mono(6);
    }

    if(boss_hit) {
        // damaged sprite
    }

    if(!boss_render_frame) {
        return;
    }

These forms preserve the zero-valued NORMAL state, the damaged-sprite
branch and the zero animation-frame early return.

## Compiler experiments and boundaries

- Kotohime af1008a tried a loop-local for(int i = ...) index; complete
  CODE changed. Af1008b retained the original register index in a natural
  for-header and matched.
- Kotohime af1008c moved the byte angle into the loop body; exact.
  Af1008d also moved the register screen-X temporary into the loop; exact.
  Moving the top coordinate into the loop, with either ordinary or
  register declaration (af1008e/af1010e), changed complete CODE.
  Removing register from the loop index (af1009b) also changed CODE.
- Chiyuri af1008f used a simple for-header but left the byte-angle update
  in the body; complete CODE changed. Af1009a moved both the initial byte
  angle and the original ordered index/angle updates into the for-header;
  exact. Af1009c moved the register screen-X temporary into the loop;
  exact. Moving top into the loop (af1009d/af1010b), removing register
  from the index (af1012e), or declaring a loop-local index (af1012f)
  changed complete CODE.
- Chiyuri af1009f attempted to share the two horizontal speed passes under
  an outer pass loop; the added direction branch changed complete CODE.
  Af1010a's separate block-local indices also changed complete CODE.
- Chiyuri af1010f made the monochrome ladder an else-if; exact.
  Af1011a changed boss_hit != 0 to boss_hit; af1011b changed the
  zero-valued normal-mode comparison to !boss_render_mode; af1011c
  changed the zero animation-frame comparison to !boss_render_frame.
  All three complete-object comparisons passed.

## Complete original-object and integration results

The final source set was checked together at af1012c, then integrated with
all nine major BOSSes and the three collision owners at af1012d.

| Scope | CODE bytes | Ordered OMF FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: |
| Complete Kotohime ba_koto | 1,840 | 262 | 11 |
| Complete Chiyuri ba_chiyu | 2,654 | 381 | 11 |
| Two-owner simultaneous scope | 4,494 | 643 | 22 |
| Twelve-owner simultaneous scope | 18,792 | 2,546 | 91 |

Both independent original Turbo C++ 4.02 rounds rebuild the complete
physical owners and execute the normal MAIN TLINK. The af1012d twelve-owner
links reproduce the complete 124,642-byte Japanese MAIN loaded image and
all 1,553 ordered MZ relocations. The other 87 original game objects and
Borland CRT were reused; no full cold replay was run.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1012c \
      --units ba_koto,ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1012d \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1012d

Protected reports:

- .analysis/work/exatt-layout-af1012c/report.json,
  SHA-256 52cf69d8820923652b4ef41d08f3b9a02dda6ea898a38effd8a588c12b93e6cb
- .analysis/work/exatt-layout-af1012d/report.json,
  SHA-256 3b719bd58e0fa975a2df6c9d9ea49c0768e16948f8bea555120dfc7d104621c3

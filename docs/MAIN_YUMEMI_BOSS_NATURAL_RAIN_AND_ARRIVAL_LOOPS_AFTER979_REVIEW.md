# TH03 MAIN Yumemi BOSS: natural rain and four-phase arrival loops

The complete ten-function Yumemi BOSS now expresses its twelve-drop rain
volley and four-phase entrance raster traversal as ordinary C++ for loops.

The rain attack preserves one independent playfield-X RNG draw and one
independent byte-angle RNG draw for each drop, followed by exactly one
bullet emission. Its loop now makes the original twelve-iteration count,
signed index and postfix update explicit in the loop header:

    for(i = 0; i < YUMEMI_RAIN_DROPS_PER_WAVE; i++) {
        bullet_template.center.x.v =
            randring_far_next16_mod(TO_SP(PLAYFIELD_W));
        bullet_template.angle =
            randring_far_next16_and(YUMEMI_RAIN_RANDOM_ANGLE_MASK) +
            YUMEMI_RAIN_RANDOM_ANGLE_BIAS;
        bullets_add();
    }

The four entrance phases likewise use for headers for their existing
left-to-right or right-to-left 8-pixel raster walks. The first two retain
left <= right; the last two retain left >= right. Their original
register-local coordinates, clipping bounds, sprite draw order, inclusive
last pixel and per-iteration step remain unchanged. TC4 emits the exact
original instructions for all four converted loops.

The same current source also names the template INTRO/NONE state, the chase
SEEK/TRACK byte values, all six round-start level formulas, and the ring
speed byte's natural addition assignment. The chase's !boss_move_phase
test was independently changed to an explicit comparison against the named
SEEK state. The main renderer's hit byte uses an explicit nonzero predicate.

A separate trial changing the unsigned 16-bit boss_effect_radius -= 8
to boss_effect_radius = boss_effect_radius - 8 failed the complete object
comparison; the original compound decrement is retained. The signed ring
angle's compound update and the byte render-frame postfix decrement also
remain in their original forms.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af979a --units ba_yumem
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af979a

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire ten-function, 2,358-byte original Yumemi BOSS. Both preserve
all 343 literal ordered OMF FIXUPP fields and ten PUBLIC offsets;
both complete normal MAIN links reproduce the 124,642-byte Japanese
loaded image and all 1,553 ordered MZ relocations. The other 98
original game objects and Borland CRT were reused; no full cold replay.

Protected current-source report:
.analysis/work/exatt-layout-af979a/report.json, SHA-256
5c7c99e5d98807825788fbd30878fd82505954e68334f617a6879c2f7aac7d09.

# TH03 MAIN Chiyuri BOSS: natural multiplicative ring geometry

The complete Chiyuri ring renderer now expresses its two power-of-two
geometry scales as ordinary C++ multiplication rather than shifts:

    radius = boss_effect_radius * CHIYURI_RING_RADIUS_SCALE;
    sprite_offset += boss_render_frame * CHIYURI_RING_SPRITE_ANIM_SCALE;

The named scales are 16 for the signed subpixel radius and 4 for the
sprite-frame bank. This keeps the original signed 16-bit multiplication
results, byte render-frame promotion, sprite offset addition and all
sixteen polar draw/update iterations. The source names the *scale* instead
of a shift count, which makes the geometry relationship more direct.

The same complete BOSS source retains the lifecycle-state improvements:
named INTRO initialization, explicit nonzero hit/movement-phase predicates
and explicit zero animation-frame check. The four attack families, collision
scheduler, GRCG intro and all sprite renderer leaves are compiled together.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af973b --units ba_chiyu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af973b

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire eleven-function, 2,654-byte original Chiyuri BOSS. Both preserve
all 381 literal ordered OMF FIXUPP fields and eleven PUBLIC offsets;
both complete normal MAIN links reproduce the 124,642-byte Japanese
loaded image and all 1,553 ordered MZ relocations. The other 98 original
game objects and Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af973b/report.json, SHA-256
2b41bf9a0c0fc3bca5b88b9bc8c02b0ac27e73559b225beaa7ed7574772d3bb4.

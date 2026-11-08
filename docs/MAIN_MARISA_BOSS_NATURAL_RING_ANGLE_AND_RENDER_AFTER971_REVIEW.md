# TH03 MAIN Marisa BOSS: natural ring-angle assignment and render predicates

The complete Marisa ring controller now uses ordinary C++ addition and
assignment for the second projectile's byte angle:

    bullet_template.angle =
        bullet_template.angle + (MARISA_RING_FULL_TURN / marisa_ring_count);

This is the runtime signed 16-bit 256 / byte_count quotient followed by
the original byte addition and truncation. The quotient remains after
the first ring projectile is emitted, and the second cloud projectile still
uses the original angle. The original IDIV, ADD AL,[angle], and byte store
are unchanged.

The main renderer also now expresses the hit byte as boss_hit != 0 and
compares its attack render state against MARISA_RENDER_MODE_ATTACK rather
than the literal 1. These edits were tested together with the angle
assignment in the complete physical BOSS.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af971b --units ba_maris
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af971b

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire nine-function, 1,431-byte original Marisa BOSS. Both preserve
all 199 literal ordered OMF FIXUPP fields and nine PUBLIC offsets;
both complete normal MAIN links reproduce the 124,642-byte Japanese
loaded image and all 1,553 ordered MZ relocations. The other 98
original game objects and Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af971b/report.json, SHA-256
14348b7868d9a8af655daf93999adbf3d4fcdd13dfb756568d8d7f4a72cd23d6.

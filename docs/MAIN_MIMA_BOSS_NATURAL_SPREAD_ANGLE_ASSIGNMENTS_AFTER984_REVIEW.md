# TH03 MAIN Mima BOSS: natural spread and pellet byte-angle assignments

Both mutable byte-angle accumulators in `mima_pattern_spread()` now use
ordinary C++ addition and assignment:

    mima_spread_angle = mima_spread_angle + MIMA_SPREAD_ANGLE_STEP;
    mima_pellet_angle = mima_pellet_angle + MIMA_PELLET_ANGLE_STEP;

These are independent byte-valued angle fields, and TC4 emits the exact
original CODE for both natural assignments. The first update remains after
the paired horizontal-symmetric bullet emissions; the second remains after
the optional medium-pellet pair. The original 16-bit frame gates, byte
truncation, projectile ordering and all nine BOSS functions are unchanged.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af984b --units ba_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af984b

Two independent original Turbo C++ 4.02 rounds recompiled the complete
1,922-byte `ba_mima` physical object, preserving all 277 ordered OMF
FIXUPP fields and nine PUBLIC offsets. Both normal MAIN links reproduce
the 124,642-byte Japanese loaded image and all 1,553 ordered MZ
relocations. The other 98 original game objects and Borland CRT were reused.

Protected current-source report:
`.analysis/work/exatt-layout-af984b/report.json`, SHA-256
`01f13a472e8979f2a4b67f35a8c38e38d5c1672bb391632873fb24f80147ad75`.

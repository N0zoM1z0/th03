# TH03 MAIN HitCircle: natural lifetime and renderer for headers

Both HitCircle traversal loops now use complete C++ `for` headers with
prefix updates of the signed index and near record pointer:

    for(i = 0; i < HITCIRCLE_COUNT; (++i, ++p))
    for(i = 0; i < HITCIRCLE_ENEMY_COUNT; (++i, ++p))

The loop-local index initialization moved into each header without changing
TC4 output. The lifetime loop still advances all thirteen physical records
(12 enemy and 1 player) after each age update. The renderer still draws only
the twelve enemy slots in order and leaves `p` pointing at the separate
player record for the later white monochrome draw.

The comma-expression order is significant. Reversing it to `(++p, ++i)`
changes the complete physical object. Keep index-before-pointer order.
The byte age postfix increment, age expiry check, separate player draw and
original sprite16 hardware-register calls remain unchanged.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af985b --units hitcirc
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af985b

Two independent original Turbo C++ 4.02 rounds recompiled the complete
445-byte `hitcirc` physical object, preserving all 30 ordered OMF FIXUPP
fields and four PUBLIC offsets. Both normal MAIN links reproduce the
124,642-byte Japanese loaded image and all 1,553 ordered MZ relocations.
The other 98 original game objects and Borland CRT were reused.

Protected current-source report:
`.analysis/work/exatt-layout-af985b/report.json`, SHA-256
`000fc1edb8af9c71f4daa3c91f14a9c64825f8fb4b06e89c1b25853d804641a1`.

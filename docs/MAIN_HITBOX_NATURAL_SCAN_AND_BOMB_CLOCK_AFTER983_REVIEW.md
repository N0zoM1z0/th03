# TH03 MAIN Hitbox: natural pair-scan increments and bomb clock

The complete `hitbox_hittest()` source now uses prefix increments for both
parts of its shot-pair scan header:

    for(i = 0; i < SHOTPAIR_COUNT; (++i, ++p)) {

The signed index and near pointer still advance after each body, including
all early `continue` paths. TC4 emits the original scan instructions for
this prefix form. Reversing the comma-expression to `(++p, ++i)` changes the
complete physical object's CODE, so index-before-pointer order is required.

The alternate-frame bomb damage gate now uses the natural unsigned-word
low-bit test:

    (round_or_result_frame & (HITBOX_BOMB_DAMAGE_PERIOD - 1)) == 0

The period is two. This expression emits the exact original CODE, just as
the modulo/remainder form did. The special segment-local explosion call
(`NOP; PUSH CS; CALL near`) and the far Chargeshot callback branch remain
unchanged.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af983c --units hitbox
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af983c

Two independent original Turbo C++ 4.02 rounds recompiled the complete
266-byte `hitbox` physical object, preserving all 33 ordered OMF FIXUPP
fields and its PUBLIC offset. Both normal MAIN links reproduce the original
Japanese loaded image and all 1,553 ordered MZ relocations. The other 98
original game objects and Borland CRT were reused.

Protected current-source report:
`.analysis/work/exatt-layout-af983c/report.json`, SHA-256
`43e49a19a772b27a0c2ceb4122d5566ca4ee47110ba7552beceba23bea9e7a55`.

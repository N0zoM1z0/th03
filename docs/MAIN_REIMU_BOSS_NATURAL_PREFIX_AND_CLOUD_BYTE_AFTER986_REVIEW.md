# TH03 MAIN Reimu BOSS: prefix orbit loops and explicit cloud-byte wrap

All five repeated loops in the complete Reimu BOSS now use prefix index
increments. This includes the three Orbit Burst phases, the live orbit
renderer and the eight-sprite intro renderer. The intro still uses a
comma-expression so its signed index advances before the byte angle:

    for(i = 0; i < REIMU_INTRO_SPRITE_COUNT;
        ++i, angle += REIMU_INTRO_ANGLE_STEP) {

TC4 emits the original instructions for prefix increment in every loop.
The three attack loops retain signed `i * 256` before integer division,
byte-angle truncation, polar-call order and the release-time Extra Attack
calls.

The cloud-orbit direction test is now explicit, and the negative angle is
written with an explicit byte conversion:

    if(reimu_direction != 0) {
        angle = (unsigned char)(0 - angle);
    }

The explicit cast documents the original modulo-256 byte wrap and is
native-exact. Replacing the expression with unary `-angle` alone changed
the complete object; the subtraction plus byte cast is the natural form
that preserves TC4 output.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af986a --units ba_reimu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af986a

Two independent original Turbo C++ 4.02 rounds recompiled the complete
2,020-byte `ba_reimu` physical object, preserving all 270 ordered OMF
FIXUPP fields and nine PUBLIC offsets. Both normal MAIN links reproduce
the 124,642-byte Japanese loaded image and all 1,553 ordered MZ
relocations. The other 98 original game objects and Borland CRT were reused.

Protected current-source report:
`.analysis/work/exatt-layout-af986a/report.json`, SHA-256
`95dca00485bf6eec6b02c95caa377fe7264be5e0727270c6b72122e26553102c`.

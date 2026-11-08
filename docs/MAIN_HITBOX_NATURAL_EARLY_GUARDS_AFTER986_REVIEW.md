# TH03 MAIN Hitbox: split the collision early guards

The first two exits in `hitbox_hittest()` are now separate natural C++
guard clauses:

    if(hitbox.origin.center.y.v < to_sp(0.0f)) {
        return 0;
    }
    if(defeat_flag == DF_BANNER) {
        return 0;
    }

TC4 emits the original branch layout and complete CODE for this split form.
The order remains significant: the negative-Y test executes before the
round banner check. The rest of the full shotpair/explosion/Chargeshot/Bomb
collision routine is unchanged, including its near-pointer scan, byte damage
accumulation and segment-local explosion-call ABI.

Two other fresh experiments were negative controls. Reversing the scan
header's prefix comma-expression to `(++p, ++i)` changed the complete object;
keep index-before-pointer order. Replacing `NOP; PUSH CS; CALL near` plus
`damage += _AL` with a direct `damage += explosions_hittest()` call also
changed CODE, so retain the original explicit far/near bridge.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af986b --units hitbox
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af986b

Two independent original Turbo C++ 4.02 rounds recompiled the complete
266-byte `hitbox` physical object, preserving all 33 ordered OMF FIXUPP
fields and its PUBLIC offset. Both normal MAIN links reproduce the original
Japanese loaded image and all 1,553 ordered MZ relocations. The other 98
original game objects and Borland CRT were reused.

Protected current-source report:
`.analysis/work/exatt-layout-af986b/report.json`, SHA-256
`f9fb84eddb743fa3f2ff961eb11e87362ec1ba5ef09703310f25d1ec1755d2e5`.

# TH03 MAIN Kana BOSS: natural staged-volley updates and for loop

The sixteen-pellet middle stage in Kana's full staged-ring attack now uses
ordinary C++ assignment for both mutable byte fields and a natural for loop:

    for(i = 0; i < KANA_MIDDLE_PELLET_COUNT; ++i) {
        bullets_add();
        bullet_template.angle =
            bullet_template.angle + KANA_STAGED_PELLET_ANGLE_STEP;
        bullet_template.speed.v =
            bullet_template.speed.v + KANA_STAGED_PELLET_SPEED_STEP;
    }

This preserves the original per-pellet order: emit using the current angle
and speed, advance the angle by six, advance speed by three, then increment
the signed loop index. The count remains sixteen. The loop's initializer,
test, and increment are now expressed in one C++ for statement rather than
a separate initialization and while body.

The successful trial is important because it is distinct from the
already-proven compound assignments: the new ordinary byte assignment
form is verified for both the angle and speed fields in the same loop.
Turbo C++ also emits the same complete loop control flow for the for form.
The original random cloud, staged ring timing, collision scheduler and full
sixteen-sprite Intro renderer are compiled as part of the same nine-function
BOSS.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af974c --units ba_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af974c

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire nine-function, **1,874-byte** original Kana BOSS. Both preserve
all **274 literal ordered OMF FIXUPP fields and nine PUBLIC offsets**;
both complete normal MAIN links reproduce the **124,642-byte Japanese
loaded image** and all **1,553 ordered MZ relocations**. The other 98
original game objects and Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af974c/report.json, SHA-256
ac9f32893af05350b6880577f39229e1e8a3e4dc06b2746d324706aa084dc206.

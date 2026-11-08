# TH03 MAIN Reimu BOSS: natural orbit, renderer and intro loops

All five repeated loops in the complete Reimu BOSS now use natural C++
for headers. The three Orbit Burst phases, the live orbit-sprite renderer
and the eight-sprite intro renderer all preserve the original signed
16-bit index and postfix update.

The Orbit Burst conversion retains the original signed i * 256 before
integer division by the orbit count, byte-angle truncation, two polar
lookups and per-index release calls. The renderer loop retains signed
array indexing and sprite draw order.

The intro renderer needed a more careful transformation. Its original
body increments the signed index before advancing the byte angle. A
plain for(i = 0; i < count; ++i) moved the index update after the angle
update and changed the original CODE. The exact natural form is:

    for(
        i = 0;
        i < REIMU_INTRO_SPRITE_COUNT;
        i++, angle += REIMU_INTRO_ANGLE_STEP
    ) {

This comma-expression preserves the original index-then-angle update order.
The final postfix form was independently rebuilt after a prefix-increment
trial also passed.

The template now names its center, velocity, HP and sprite-bank layout.
The scheduler and render-mode transitions use INTRO/SELECT and
NONE/ORBIT names; the main renderer's hit byte is explicitly nonzero.
The cloud attack's local byte half-turn now uses ordinary assignment:

    angle = angle + REIMU_CLOUD_OPPOSITE_ANGLE;

A direct assignment rewrite of the global cloud-speed increment did not
match the original complete object, so the original postfix increment
remains.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af982c --units ba_reimu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af982c

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire nine-function, 2,020-byte Reimu BOSS, preserving all 270
literal ordered OMF FIXUPP fields and nine PUBLIC offsets. Both complete
normal MAIN links reproduce the 124,642-byte Japanese loaded image
and all 1,553 ordered MZ relocations. The other 98 original game
objects and Borland CRT were reused; no full cold replay.

Protected current-source report:
.analysis/work/exatt-layout-af982c/report.json, SHA-256
a64963c61d23a637578f0e008bf1da8c02294b728282f0c6be51edf8785c9db7.

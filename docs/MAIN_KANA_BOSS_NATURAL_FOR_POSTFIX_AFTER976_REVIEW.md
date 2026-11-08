# TH03 MAIN Kana BOSS: postfix increment in the staged pellet for loop

The sixteen-pellet staged-ring loop now uses postfix increment in its for
header:

    for(i = 0; i < KANA_MIDDLE_PELLET_COUNT; i++) {

The loop index is a signed int and its previous value is not consumed by
the increment expression. Turbo C++ 4.02 therefore emits the same original
loop-control CODE for postfix and prefix increment. This is a narrowly
measured result for this loop; it does not justify changing the separate
byte counters or pointer postfix operations elsewhere in MAIN.

The body retains the natural byte assignments proven in af974c:
emit the projectile, add six to the byte angle, add three to the speed,
then advance the index. The full nine-function Kana BOSS, including all
four attack families, cloud RNG sequence, collision controller, main
renderer and sixteen-sprite intro renderer, was recompiled together.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af976a --units ba_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af976a

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire nine-function, 1,874-byte original Kana BOSS. Both preserve all
274 literal ordered OMF FIXUPP fields and nine PUBLIC offsets; both
complete normal MAIN links reproduce the 124,642-byte Japanese loaded
image and all 1,553 ordered MZ relocations. The other 98 original game
objects and Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af976a/report.json, SHA-256
45c0d81edc7473d3014ff4343c7049c867cd117cdd8d2dd7fb49bb0756c96fd3.

# TH03 MAIN Yumemi BOSS: rain-loop prefix increment

The twelve-drop rain volley now uses prefix increment in its natural
for-loop header:

    for(i = 0; i < YUMEMI_RAIN_DROPS_PER_WAVE; ++i) {

The preceding source-current af979a proof used postfix increment. This
independent full-object trial shows that TC4 emits the same original CODE
for prefix and postfix increment on this signed 16-bit loop index. Each
iteration still draws the playfield X coordinate and byte angle separately,
emits one bullet, then advances the index.

The full ten-function BOSS remains intact, including all attack controllers,
the 12-drop RNG sequence, collision scheduler, effect renderer and four
arrival raster loops.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af983a --units ba_yumem
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af983a

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire ten-function, 2,358-byte Yumemi BOSS, preserving all 343 literal
ordered OMF FIXUPP fields and ten PUBLIC offsets. Both complete normal
MAIN links reproduce the 124,642-byte Japanese loaded image and all
1,553 ordered MZ relocations. The other 98 original game objects and
Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af983a/report.json, SHA-256
53a363645f48f4b17ef8cae6c119812b4fa6737504fc8249f88a2bd581645c9b.

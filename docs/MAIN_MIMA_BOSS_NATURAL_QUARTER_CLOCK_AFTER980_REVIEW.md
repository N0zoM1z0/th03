# TH03 MAIN Mima BOSS: natural four-frame random-bomb clock

The random-bomb attack's unsigned 16-bit four-frame gate now uses a low-bit
mask:

    if((boss_frame & (MIMA_RANDOM_BOMB_FIRE_PERIOD - 1)) == 0) {

The original period is four, so this selects frames whose low two bits are
zero. Unlike the six-frame spread-pellet clock, this period is a power of
two and TC4 emits the original word test/mask sequence. The bullet/pellet
spawn order and the independent ring-frame event remain unchanged.

This complements the three even-frame gates already naturalized in the
spread, random-bomb sound and orbit controllers. The complete nine-function
Mima BOSS was recompiled, not just the random-bomb leaf.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af980f --units ba_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af980f

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire nine-function, 1,922-byte Mima BOSS, preserving all 277 literal
ordered OMF FIXUPP fields and nine PUBLIC offsets. Both complete normal
MAIN links reproduce the 124,642-byte Japanese loaded image and all
1,553 ordered MZ relocations. The other 98 original game objects and
Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af980f/report.json, SHA-256
c53ba6e23cda9bdc02a0ce238aa6ed074b615e0760e87a679f1ff32155046fae.

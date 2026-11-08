# TH03 MAIN Kana BOSS: named template, level parameters and renderer geometry

The complete nine-function ba_kana owner now names the original template
layout, render-state protocol, attack sound, seven level-derived parameters
and both large renderers' sprite geometry.

The template leaf identifies Kana's initial center, velocity, HP, sprite
bank and player-two offset. All attack entry/exit points use the shared
INTRO/SELECT scheduler IDs and NORMAL/EXPANDING/WARNING render states.
The full update names each independent level formula: accelerated-ring
count, slow/middle/fast staged-ring counts, cloud interval/count and
rotating-ring speed. The six attack sound calls use the original SFX ID.
The main renderer explicitly tests the byte hit flag for nonzero.

The renderer pass names the main-sprite placement, hit sprite offset,
warning sprite bank and its four animation steps, plus the intro sprite
bank, frame geometry and half-tile placement. It preserves the original
two-stage intro radius/frame multiplications, signed polar coordinates,
byte angle truncation, and the sixteen-sprite call/update order.

The full BOSS still contains all four attack families, the 16-pellet
staged volley, both unsigned-word modulo clocks, the random-cloud RNG
sequence, collision/hit controller and complete main/intro rendering.
The cloud's hardware-sensitive SUB AL,10h, binary zero-minus intro angle,
and signed rotating-angle compound update remain explicit because
different natural spellings have already failed genuine TC4 comparisons.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af966a --units ba_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af966a

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire **1,874-byte original Kana BOSS** and linked each through the
complete normal MAIN response. Both reproduce all **274 literal ordered
OMF FIXUPP fields and nine PUBLIC offsets**, the full original Japanese
MAIN loaded image (**124,642 bytes**) and all **1,553 ordered MZ
relocations**. The other **98 original game objects and original Borland
CRT** were reused; no full cold replay.

Protected source-current report:
.analysis/work/exatt-layout-af966a/report.json, SHA-256
da17ec634a93ca022f7270d58aeb53d350f05b3b5b1610c4acf4c14e07520bb2.

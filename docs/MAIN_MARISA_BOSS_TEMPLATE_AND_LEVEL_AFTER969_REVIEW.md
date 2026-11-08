# TH03 MAIN Marisa BOSS: natural template, state and level parameters

The complete nine-function ba_maris owner now uses semantic C++ values for
its original template layout, render states, scheduler transition and all
six round-start attack parameters.

The template leaf names Marisa's initial center, velocity, HP, sprite bank
and player-two bank offset. Its initial scheduler/render states now use the
same INTRO and NORMAL values as the full BOSS dispatcher. The spread, wide
column and narrow column controllers use the shared ATTACK render state;
all five attack-completion/intro transitions use SELECT.

The full update names the original level multiplier and each independent
base value: spread bullet speed, low cloud count, cloud speed, ring speed,
ring count and high cloud count. Both original doubled formulas remain
multiplication by two; the separate integer/byte conversions and round-start
update boundary are unchanged.

The complete BOSS still includes the four-frame spread attack, two distinct
wide/narrow paired-column controllers, 32-frame ring attack, full
update/collision scheduler, normal/flicker renderer and two-sided split-mask
intro renderer. The original signed 16-bit ring-count division, RNG draw
order, two sprite masks and register-local split offset remain intact.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af969a --units ba_maris
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af969a

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire 1,431-byte original Marisa BOSS, preserving all 199 literal
ordered OMF FIXUPP fields and nine PUBLIC offsets. Both complete normal
MAIN links reproduce the 124,642-byte Japanese loaded image and all
1,553 ordered MZ relocations. The other 98 original game objects
and original Borland CRT were reused; no full cold replay.

Protected current-source report:
.analysis/work/exatt-layout-af969a/report.json, SHA-256
ac37d9c2b6f5877c19e0aa15af96eee017ddddd4fa1ddeafe089ed4a8e97e3c2.

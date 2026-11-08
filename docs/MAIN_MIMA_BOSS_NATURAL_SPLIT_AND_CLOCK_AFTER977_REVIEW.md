# TH03 MAIN Mima BOSS: natural split-angle, even-frame clock and level setup

The complete nine-function Mima BOSS now expresses its split renderer's
opposite-half angle as ordinary C++ addition and assignment:

    angle = angle + MIMA_RENDER_SPLIT_OPPOSITE_ANGLE;

The byte angle still advances only after the first masked sprite has been
drawn, so the second polar calculation sees the original angle plus 0x80.
This was checked independently first in af977a, then in the combined
af977c/af977d source.

All three even-frame gates in the spread, random-bomb and orbit attack
controllers now use the unsigned-word low-bit condition:

    (boss_frame & (MIMA_FIRE_EVEN_PERIOD - 1)) == 0

The period is two, and the original global frame is unsigned 16-bit.
The complete TC4 object proves that this expression emits the same CODE
as the prior modulo-and-zero test at all three attack sites.

The template now uses the named INTRO scheduler state and its own
declared NORMAL render-state value. All seven round-start level formulas
have named divisors, multipliers and bases, and the main renderer explicitly
tests the hit byte as nonzero. Integer widths, division, assignment
truncation, round-start update timing, signed orbit steering, the trail
byte-narrowed modulo, and the original mode-5 goto/label renderer remain
unchanged.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af977d --units ba_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af977d

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire nine-function, **1,922-byte** original Mima BOSS. Both preserve all
**277 literal ordered OMF FIXUPP fields and nine PUBLIC offsets**; both
complete normal MAIN links reproduce the **124,642-byte Japanese loaded
image** and all **1,553 ordered MZ relocations**. The other 98 original
game objects and Borland CRT were reused; no full cold replay.

Protected current-source report:
.analysis/work/exatt-layout-af977d/report.json, SHA-256
7daf60464eb63bb7bf3ec43cd7f2f9d2a73cf86b9e72a3c5acacc8dd79f762a3.

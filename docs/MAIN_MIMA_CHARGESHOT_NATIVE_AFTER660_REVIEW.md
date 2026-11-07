# Mima complete charged-shot and Gauge C++ source, original native after660

This genuinely source-rooted Turbo C++/TLINK pair compiles all ten
functions of the original Mima charged-shot physical producer
(`cs_mima`), including the long fifteen-shot movement/clip/update,
hitbox renderer, arrival/activation helper, and two full Gauge attacks.
Its CODE is 1,338 bytes in the frozen original MAIN.

The original Mima Gauge angle step was an opaque 8-bit
`249 : 7` conditional. Actual modified-source TC4.02 compiles
the natural signed value `-7 : 7` into **identical original
machine code**, preserving the 8-bit wrap and RNG draw
(`af660b`). The *other* branch testing
`mima_gauge_angle_step > 7` must stay an unsigned byte
comparison. Rewriting it to a signed `< 0` comparison
changed native CODE (`af660c`), so that alternative was
rejected rather than patched.

The source now also checks the real physical **10-byte**
charged-shot record size: one-byte active and auxiliary fields,
16-bit X at +02, Y at +04, velocity X at +06 and velocity Y
at +08. Fifteen 10-byte slots per player, thirty total,
the original six-angle cycle, four-frame release cadence,
sixty-frame final release boundary and last-slot termination
behavior are compiler-time named phases. The alternating
8-/16-frame Gauge ring pulses and finish after frame 64
retain their exact original order and numeric values.

Native final stage:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af660d --units cs_mima
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af660d

Both independent original Turbo C++ 4.02 compiler and full normal
MAIN TLINK rounds match all **1,338 CODE bytes, 150 literal
ordered FIXUPP fields, ten PUBLICs**, original OMF segment
metadata, full normal MAIN executable and path-normalized MAP,
Japanese program image and its 1,553 ordered MZ relocations.
Independent standard MZ serialization matches the exact original
130,882-byte Japanese MAIN.EXE.

Preserved original-source and writer evidence:
`.analysis/work/exatt-layout-af660d/report.json`
SHA-256 `5314f7e8a5a29ad46fd98203d465ad377cd840ed33fff05c1dbc8202846bd1d9`.
Only the one selected original project object was recompiled;
the other 98 original project objects and startup/CRT libraries
were reused, not cold replayed. The current modified source is
confirmed from genuine native OMF COMENT dependency paths.

The original game CODE in this scope was already tracked; this
is source/ABI recovery rather than new canonical packed-file
Factory credit, historical vendor raw OMF packet equality,
or real PC-98 runtime certification.

# Reimu major BOSS: exact C++ orbit angles and sprite loop (after691)

This source-native proof covers the **complete 9-function
Reimu BOSS physical Turbo C++ owner**, not a detached
angle calculation. It contains the large BOSS state
dispatcher, full cloud/aimed/orbit/mirrored attacks
and original rendering helpers.

All **three** full orbit burst angle distribution
expressions now use natural signed C++:
    ((i * 256) / reimu_orbit_count) + reimu_orbit_angle
instead of `(i<<8)`, preserving the original
16-bit multiply **before the integer division**
and the original one-byte angle truncation.
The real current-source Turbo C++ 4.02 `af691a`
native pair reproduced the exact original entire
2,020-byte CODE payload and ordered fixups.

All four physically related BOSS orbit loop
increments can use ordinary `++i`. An attempt
to also replace the cloud's
`reimu_cloud_speed++` with prefix increment
changed actual original CODE (`af691b`).
The latter is deliberately restored and left
in postfix form; the complete source with only
the successful four-loop changes passed
`af691c`. The eight-point sprite render
leaf's polar loop also uses the natural `++i`
style while preserving the original call
order and signed pixel math (`af691d`).

Final source-/packed-header-OMF-dependency-attested
two-round original compiler and full MAIN TLINK:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af691e --units ba_reimu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af691e

Both native original Turbo C++ 4.02 rounds reproduce
**all 2,020 CODE bytes, 270 literal ordered
native FIXUPPs, nine PUBLIC offsets**, original
OMF segment definitions, whole normal MAIN
EXE/MAP, Japanese loaded program, all 1,553
ordered relocations and independently serialized
original 130,882-byte Japanese MAIN.EXE.

Proof:
`.analysis/work/exatt-layout-af691e/report.json`,
SHA-256 `ffbd73d1ed66389430acefa1cab04f8432cc5f9aea2767cecffc48bab9d0c2c4`.
The compiler actually consumed modified maintained
BOSS C++ and its current packed template header.
Only one complete original physical BOSS object
was freshly compiled twice, reusing 98 other
project objects and CRT. No full cold replay.

These are existing source-owned target bytes,
not newly accepted Factory canonical packed-game
bytes, historical original raw OMF packet identity
or real PC-98 hardware proof.

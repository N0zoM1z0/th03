# Rikako full BOSS orbit and entity ring: native signed C++ after692

This is a genuine whole-original-TU proof for the
1,677-CODE-byte Rikako BOSS controller, including
two long radial attacks, the remaining attacks,
the major scheduler and both renderers.

Two fully distinct 256-step angular distribution
loops now use natural signed C++ `i * 256`
instead of `i << 8` in the original physical
`rikako_pattern_orbit_spread` and
`rikako_pattern_entities_and_pellets`.
Both retain original signed integer division
*after* multiplication and byte-angle truncation.
The fresh `af692a` current-source-bound TC4 pair
verified every CODE byte and ordered native field.

The same two attack generators and their distinct
pellet loop, plus both sprite renderers, now use
natural `++i` instead of `i++`. The full
new original-native proof `af692b` reproduces
all original code and link relocations.

The entity release routine contains a seemingly
redundant `angle = randring_far_next16()`
immediately before a loop overwrites `angle`.
It is not safe dead code: the call advances the
game's global RNG sequence and therefore changes
subsequent gameplay if removed. The unchanged
draw and original call position are preserved.

Final source/template-OMF-COMENT-attested two-round
original Turbo C++ 4.02/TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af692c --units ba_rikak
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af692c

Both full native compiler rounds reproduce all
**1,677 original CODE bytes, 215 literal ordered
FIXUPP fields and eight PUBLIC offsets**, original
OMF segments, normal full MAIN EXE and MAP, Japanese
loaded program, 1,553 literal ordered relocations
and independently serialized original 130,882-byte
Japanese MAIN.EXE.

Preserved source/output/native writer evidence:
`.analysis/work/exatt-layout-af692c/report.json`,
SHA-256 `718d4e332ac4ae13ded7e0fab540af97db6629650cfefdbc3e11ac3711fc3ba0`.
Only the one affected original physical BOSS source was
freshly compiled; the other 98 project objects and
CRT inputs were reused. No full cold replay and no
new canonical packed-game Factory bytes are claimed.

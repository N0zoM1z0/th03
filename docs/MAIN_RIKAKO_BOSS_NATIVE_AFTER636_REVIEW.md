# Rikako BOSS: signed turn dynamics and three full attack phases (after636)

The original Rikako BOSS translation unit includes the complete large
`gba_boss_update_rikako` scheduler, three substantial attack routines,
sprite renderers and its own initial state. This is a full physical
1,677-CODE-byte object, not a test of an isolated leaf helper.

Three independent original bit-mask checks used to advance the signed
spin state every eight frames: one for an orbiting wide spread, one for
entity/pellet release and one for the alternating burst. Genuine 16-bit
Turbo C++ compiles the natural expression `boss_frame % 8 == 0`
to the same original bitwise instructions in all three contexts.

The alternating burst previously staged a signed +1/-1 adjustment in
AL, added the signed `boss_spin_delta`, and wrote AL back. The final
source can state the same 8-bit update directly:

    boss_spin_delta += ((boss_spin_delta > 2) ? -1 : 1);

The `boss_spin_delta != 2` and every-eight-frame gates remain in
place. The independent stages `af636a` (three cadence changes),
`af636b` (ternary via AL) and `af636c` (direct signed C++) each
compiled the entire original-byte-matching BOSS object.

The mode dispatcher now identifies the actual Rikako-specific
mapping of all 18 scheduler values to orbit spread, extra entities
and pellets, or alternating bursts. Original orbit warning/fire
frames 0x10/0x28, entity pellet launch 0x40, signed turn period eight
and alternating volley remainders 1/5/9/13 are named compile-time
C++ enums, preserving the initial RNG draw even when its angle is
later overwritten in the entity launch path. No added DATA or
new state object was introduced.

The final current-source/OMF-dependency-attested compiler and normal
MAIN TLINK pair:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af636d --units ba_rikak
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af636d

Both rounds reproduce **all 1,677 CODE bytes, 215 literal ordered
FIXUPP fields, eight PUBLIC offsets** and original segment definitions.
The full normal 99-object MAIN link and normalized complete MAP match
the historical source-native parent; the original Japanese program
image, **1,553 ordered MZ relocations** and separate exact 130,882-byte
Japanese MAIN.EXE serialization also match.

Retained proof:
`.analysis/work/exatt-layout-af636d/report.json`,
SHA-256 `202d328c9ccd91ab66d00ddcb544b320a3fbd0c7a72860922eb785d2313a5d84`.
The per-round real source, raw OBJ/EXE/MAP, native compiler/writer logs
and original linker responses are preserved. Only Rikako's native
object was recompiled, with no whole cold replay.

These are existing original game CODE bytes; this work advances
maintained natural source and ABI faithfulness, not newly accepted
packed-file Factory bytes, historic raw vendor OMF packet identity
or untested real PC-98 behavior.

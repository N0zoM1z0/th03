# Player explosion/axis effects: actual original C++ producer after668

This is a real first v2 source-OMF-dependency-attested compiler
proof for the five-function `effects` physical original project
object, previously outside the 38-unit BOSS/charged-shot source
probe. Its original `PLAYER_M_TEXT` CODE contribution is 628
bytes and it lives in the historical MAP as
`src/main/player/effects.cpp`, not `th03/effects.cpp`.
The v2 native writer/reviewer now preserves that actual module
name when normalizing complete linked MAIN MAPs.

The original complete source contains three small explosion
and warning-quad spawners, the multi-effect lifetime update,
and the larger GRCG circle/quad hardware renderer. Real 16-bit
TC4.02 compiled the unchanged-source control `af668a`
byte-for-byte equal to the historical physical original.

Two separate active-effect tests in the lifetime updater and
hardware renderer now use natural C++ truthiness:
    if(effect->kind) { ... }

The actual enum FREE value is zero, and the complete original
native source emits identical CODE from this simpler
expression. The two-round control `af668c` confirmed exact
original bytes, including all literal 16-bit fixups.
The original physical `player_effect_t` remains 10 bytes
with 12 source-owned logical slots, signed radius delta
and a character-dependent angle.

The original initialization/lifetime behavior is not
silently changed. Negative native controls found that
collapsing the age increment into an if preincrement
(`af668b`) and similarly merging the cursor increment
and circular-buffer wrap (`af668d`) both change original
TC4 CODE. These semantic-looking rewrites were rejected.
The separate original byte updates remain, and the
renderer continues to use arithmetic right shift for
the circle's potentially negative odd Y coordinate, while
polygon vertices use C++ division with truncation toward zero.

Final source-bound, original Turbo C++ 4.02 and full normal
MAIN TLINK acceptance:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af668e --units effects
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af668e

Both rounds reproduce all **628 original CODE bytes, 33 literal
ordered FIXUPP fields, five PUBLIC offsets, complete OMF
segments**, whole normal MAIN EXE and path-normalized full MAP,
the original Japanese loaded program image, 1,553 literal ordered
MZ relocations and independent full original 130,882-byte
Japanese MAIN.EXE serialization.

Retained original compiler/linker and source proof:
`.analysis/work/exatt-layout-af668e/report.json`,
SHA-256 `015762e51ba4f143fec8c8ef277c0f4c51608c732e7fbbd74969a3dd12ddf5ba`.
The compiler actually consumed the edited source (emitted
OMF COMENT dependency), not an old TH03WORK copy. Only the one
affected original TU was newly compiled twice, reusing
other 98 project objects and startup/CRT libraries.

This is maintainable natural C++ within previously accounted
original CODE. It is not new canonical Factory packed-file
credit, original historical vendor OMF packet identity or
physical PC-98 device behavior proof.

# Kana/Kotohime complete Bomb controllers: native pixel geometry after684

These are two whole original Turbo C++ Bomb translation units in
MAIN_05_TEXT, not fragments of their render helper. The Kana
Bomb contributes 526 CODE bytes / 53 ordered fixups / one PUBLIC;
Kotohime contributes 528 CODE bytes / 50 ordered fixups /
one PUBLIC. Both physical original objects are CODE-only:
the original Kana one-byte rotation angle and Kotohime
two-byte explosion Y are owned by an **external frozen
Bomb data carrier** and must not be allocated again.
The scoped original-current-source TC4 wrapper now supplies
`TH03_BOMB_EXTERNAL_STORAGE` for both, with actual OMF
source dependency checks. The unchanged four-bomb control
`af681b` proved the proper physical original ABI before edits.

Kana's major two-ended rotating explosion now emits both
screen-space polar positions through natural
`(x * 16), (y * 16)`, replacing manual `x<<4, y<<4`
in two successive mirror/reflection passes. All four
individual source expressions retain the original signed
pixel-to-subpixel behavior. A real independent two-round
compiler/full MAIN link `af684a` produced exact original
machine code. Kana's final 8-bit fade also now uses
`255 - frame * 8` instead of an authored left shift;
the same expression was independently tested in Kotohime
(`af684b`).

Kotohime's three-column explosion row is naturally
expressed in real playfield units:
`for(; x <= TO_SP(288); (x += TO_SP(96), ++i))`.
Its 96-pixel stride, 288-pixel final X and byte-palette
fade match original instructions (`af684c`, `af684e`).
The original `i` increment, bomb explosion Y lifetime,
screen flash, and 64/128-frame state transitions remain
in exactly the original order. **The late Kotohime branch
reads an uninitialized stack `color`** before doubling it.
This is genuine target behavior, not portable defined C++:
we do not zero-initialize that variable or change the
runtime before the original read.

Negative control: replacing the Kana Bomb shake test
`(frame & 3) < 2` with a seemingly equivalent
unsigned `frame % 4 < 2` **changed** original TC4
CODE (`af684d`). The real mask, rather than the
original-unequal candidate, is retained.

Final current-source/OMF-dependency-attested two-round
original Turbo C++ 4.02 and complete MAIN TLINK:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af684f --units b_kana,b_koto
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af684f

Both rounds reproduce the complete **1,054 original CODE
bytes, 103 literal ordered native FIXUPP fields, two
PUBLIC offsets**, original OMF segment and BSS metadata,
full normal MAIN EXE and path-normalized MAP, the Japanese
loaded program, 1,553 ordered MZ relocations, and
independently serialized exact original
130,882-byte Japanese MAIN.EXE.

Native compiler/OBJ/MAP/EXE writer receipt:
`.analysis/work/exatt-layout-af684f/report.json`,
SHA-256 `85346fc0c67ff06252b60b5b0a20d5d0deec18829b2974925f4061fc903f7220`.
Only the affected two complete original TU sources were
recompiled twice; 97 other original project objects and
startup/CRT libraries were reused, no full cold replay.

These were previously source-owned original CODE bytes.
This is natural-source and physical ABI progress, not new
canonical Factory packed-game acceptance, historic vendor
raw OMF packet-byte identity or PC-98 runtime proof.

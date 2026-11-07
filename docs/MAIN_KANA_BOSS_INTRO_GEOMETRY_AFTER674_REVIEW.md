# Kana full major BOSS: original native C++ intro geometry and animation (after674)

The complete original Kana BOSS physical Turbo C++ producer contains
nine functions with the major scheduler, four full attack pattern
families, sprite rendering and a large spinning sixteen-point
introductory ring renderer, owning **1,874 original CODE bytes**.

The maintained `kana_render_intro` now generates its entire radial
distance using natural 16-bit C++ multiplication while preserving
the original two-stage operation:
    radius = (0xC80 - ((boss_frame * 2) * 16));

Original TC4 lowers the `* 16` to precisely the original
left shift; the genuine source-bound full-object native
control `af674a` matches every CODE byte/fixup.

The same function's animated sprite offset originally used
right/left shifts and a bitmask:
    ((((boss_frame >> 2) & 3) << 5) * 0x28)

It now uses readable unsigned arithmetic preserving the
original operator tree:
    ((((boss_frame / 4) % 4) * 32) * 0x28)

Independent actual original compiler/TLINK controls
`af674b`, `af674c` and `af674d` proved the
unsigned division, modulo and multiplication steps
respectively all preserve original 16-bit x86 instructions.

A further test collapsing the two multiplications into
`((boss_frame / 4) % 4) * 1280` changed actual native
CODE (`af674e`). The preserved two-stage natural
C++ source is therefore **not** a cosmetic compiler-agnostic
simplification. Original signed AX/sprite positioning and
all circle loop drawing order are untouched. The exact
SUB AL,10h in a separate full Kana cloud BOSS attack
remains inline assembly because equivalent byte arithmetic
would emit the wrong native opcode (older native controls).

Final genuine source/header-OMF-attested two-round original
Turbo C++ 4.02 compiler and full normal MAIN TLINK:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af674f --units ba_kana
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af674f

Both rounds reproduce **all 1,874 original CODE bytes,
274 literal ordered native FIXUPP fields, nine PUBLIC offsets**,
complete OMF segment metadata, whole original normal
MAIN EXE/path-normalized MAP, the Japanese loaded program,
1,553 ordered MZ relocations and separately serialized
original 130,882-byte Japanese MAIN.EXE.

Native source/OBJ/EXE/MAP and writer evidence:
`.analysis/work/exatt-layout-af674f/report.json`
SHA-256 `5a448d9c2852fc3636fedda056302f9d2a08030d8768df29e9880832c304695e`.
Only the affected full Kana BOSS object was recompiled
twice; the other 98 original game objects and libraries
were reused without full cold replay.

All target CODE here was previously source-owned. This is
original-byte-exact maintained C++ progress, not new
canonical Factory packed-game credit, raw historical
vendor OMF packet identity or PC-98 runtime evidence.

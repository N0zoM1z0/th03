# Reimu major BOSS: natural arrival radius and two native-exact animation leaves (after676)

This current-source original Turbo C++ 4.02 native proof covers
the complete nine-function, **2,020-CODE-byte** Reimu major BOSS
producer, including the long update and attack pattern controllers
plus both independent sprite renderers.

In `gba_boss_render_reimu`, the original introductory sprite
orbit radius `0xC80 - (boss_frame << 5)` now uses ordinary
C++ `0xC80 - (boss_frame * 32)`, with exactly the original
compiler-emitted shift instructions (`af676a`). This single-stage
case is distinct from the large orbit burst's earlier two-stage
`(boss_frame*16)*2` expression: collapsing that separate
two-stage arithmetic to `boss_frame*32` changed the original
code in after666, so its operation order remains.

Both sprite leaf renderers, the normal orbit display and the
major BOSS intro, now use natural explicit unsigned C++:
`static_cast<unsigned int>(anim) % 4` in all four four-frame
cel tests, and `static_cast<unsigned int>(anim) % 2` for
the two alternate sprite choices. The original bitwise
`anim & 3` and `anim & 1` tests were independently
proven to compile from these expressions to **identical
native TC4 opcode bytes** (`af676b`, `af676c`).
No mask register/CPU flag semantics have been guessed.

Current exact physical source bound to actual TC4 object:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af676d --units ba_reimu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af676d

Both original Turbo C++ compiler/full normal MAIN TLINK
rounds reproduce **all 2,020 original CODE bytes, 270
literal ordered native FIXUPP fields, nine PUBLIC offsets**,
complete original OMF segments, normal whole MAIN EXE/MAP,
Japanese loaded program, all 1,553 ordered MZ relocations
and separately serialized original 130,882-byte Japanese
MAIN.EXE. Actual modified source and BOSS template header
dependencies are independently OMF-COMENT-attested.

Native original source/output evidence:
`.analysis/work/exatt-layout-af676d/report.json`,
SHA-256 `e0c24e240ed014409e6a49c75d8b3114fd10e34b5ff2319fecd18c4f106914ef`.
Only one complete original BOSS TU was freshly compiled
twice; other 98 physical project objects and startup/
CRT libraries remained untouched, without full cold replay.

All target bytes were previously tracked source-owned CODE.
This is real compiler-exact natural C++ progress,
not new canonical Factory packed-game byte credit,
historical vendor raw OMF identity or PC-98 runtime proof.

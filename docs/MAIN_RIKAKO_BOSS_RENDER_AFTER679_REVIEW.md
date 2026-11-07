# Rikako complete BOSS: original 16-bit intro geometry and sprite phase C++ after679

Rikako's physical complete BOSS producer includes the long major
attack dispatcher, three substantial attack families, ring/rotor
sprite rendering and intro drawing. The original full source owns
**1,677 CODE bytes**, 215 literal ordered native fixup sites and
eight PUBLIC offsets.

In the full 16-sprite `rikako_render_intro` body, the historically
staged radius `0xC80 - ((boss_frame * 2) << 4)` now reads as
**two natural C++ multiplies in the original operation order**:

    radius = (0xC80 - ((boss_frame * 2) * 16));

Genuine original Turbo C++ 4.02 full-object native control
`af679a` proves this expression lowers to identical original
machine code. The next two intro clocks now use natural
`round_or_result_frame % 2` and `boss_frame % 2`,
still preserving original timing and frame skipping (`af679b`).

Both i%4 uses in `rikako_render_main` now express the four-way
sprite selector with explicit unsigned C++ remainder, not hand
`i & 3` masks (`af679c`). Intro's eight-bit angle step
now uses natural `(unsigned char)boss_frame * 4` in place
of manual left shift, preserving the original byte truncation
and instruction stream (`af679d`). Each compiler test covers the
**entire physical original BOSS object**, not an isolated leaf.

Two tempting refactors were rejected after direct native
byte comparison: replacing the intro's binary `0-angle`
by unary `-angle` (`af679e`) and flattening the
two-stage radius to `frame*32` (`af679f`). Both changed
original TC4 output. The intended two-stage source semantics
and original zero-minus form remain. The original signed
AX pixel-conversion and register assignment are preserved.

Final changed-source/OMF-COMENT-attested actual original
Turbo C++ 4.02 and full normal MAIN TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af679g --units ba_rikak
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af679g

Both native rounds reproduce the full original **1,677 CODE bytes,
215 ordered literal FIXUPPs, eight PUBLICs**, complete OMF
segment metadata, the normal whole MAIN EXE/path-normalized
MAP, the original Japanese loaded program and all 1,553
MZ relocations. Independent standard MZ serialization
produces the exact 130,882-byte Japanese MAIN.EXE.

Native source and raw writer evidence:
`.analysis/work/exatt-layout-af679g/report.json`,
SHA-256 `e1adf2e1384936b70b849ad76f5b8c926e66ed09a813e98c7743ee1cf29757d9`.
Only this affected original BOSS translation unit was
compiled twice; the other 98 project objects and CRT
were reused without a full cold replay.

These are already tracked original CODE bytes, not new
canonical Factory packed-game byte credit, historical
vendor raw OMF packet-byte identity or PC-98 runtime proof.

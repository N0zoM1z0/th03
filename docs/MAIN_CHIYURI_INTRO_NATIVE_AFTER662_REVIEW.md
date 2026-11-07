# Chiyuri BOSS entrance: natural signed radius geometry (after662)

This proof recompiles the entire original 11-function Chiyuri
BOSS translation unit (2,654 original CODE bytes), not only a
render leaf. Its `chiyuri_render_intro` uses three distinct
32-frame radius phases that originally spell each pixel displacement
as `(frame << 3)`.

Genuine original 16-bit Borland Turbo C++ 4.02 instead emits
the same original left-shift bytes from the natural C++:
    boss_effect_radius = (0x100 - (frame * 8));
    boss_effect_radius = (0x200 - (frame * 8));
    boss_effect_radius = (0x300 - (frame * 8));

Only one branch executes per frame, preserving the original
0x20 and 0x40 transitions, the render call position and all
signed 16-bit widths. The independently source-bound full
BOSS object `af662a` confirms this codegen equality.

The nearby 8-bit boss rotation updates are **not** interchangeable
with ordinary high-level addition/subtraction under this compiler:
direct `boss_move_phase += 4` (prior `af651a`),
`boss_move_phase = boss_move_phase + 4` (`af662b`),
and `boss_move_phase -= 4` (`af662c`) all changed native
CODE. The original explicit AL load/ADD/store sequences are
retained. No target-byte patching or fake padding was used.

The current final original source/header-OMF-attested dual
Turbo C++/full MAIN TLINK rounds:
    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af662d --units ba_chiyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af662d

Both fresh physical source compilations reproduce all **2,654
original CODE bytes, 381 literal ordered FIXUPP fields, 11
PUBLIC offsets**, complete OMF segment metadata and original
full normal MAIN executable/MAP. The original Japanese program
image, all 1,553 ordered MZ relocations, and independently
serialized full 130,882-byte Japanese MAIN.EXE remain exact.

Preserved evidence:
`.analysis/work/exatt-layout-af662d/report.json`
SHA-256 `4db97e0005cf9c6a26727fd8f4bd933f605e4775696a04fc5788443ba0a0f1e2`.
Both compiler/linker writer rounds and genuine source/OMF
dependency paths are retained. The other 98 original
project objects and startup libraries were reused;
no full cold replay was run.

This is original-native maintainable C++ over already tracked
BOSS CODE bytes, not newly accepted canonical packed-game
Factory credit, historical raw vendor OMF packet identity
or PC-98 runtime validation.

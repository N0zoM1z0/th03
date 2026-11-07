# Mima complete three-function Bomb: original native physical columns (after689)

The original `bm_mima` physical Turbo C++ producer contains
the complete bomb update state machine, the per-column sprite
render helper and the large three-stage GRCG/palette/screen
effect. The unchanged-source dual-native `af688a` control
established the complete physical baseline before any edits.

The maintained long bomb function uses natural C++ typed
unsigned `frame%2==0` for its two-frame sound and
palette cadence, and natural `255-frame*8` for the
late-stage byte fade (native exact `af689a`).

In the 8-column sprite rendering leaf, the original
first-uninitialized-column sentinel is now directly
`if(!mima_bomb_column_p->sprite_offset) break`,
with natural `++i` iteration; TC4 emits the exact
original instructions for both edits (`af689b`).
Crucially this is a **break on the first empty column**,
not a scan that skips over inactive columns.

Real original Turbo C++ 4.02 compile-time assertions
now bind the physical four-byte column stride and
sprite offset +02. Compiler-time names identify the
eight columns/player, eight-frame sequential launch
cadence, and original 80/144 frame stage boundaries.
The actual original release and Palette/Pascal calls
and all original RNG consumption are retained.

Final modified-source/OMF-dependency-attested original
TC4 compiler plus full normal MAIN TLINK:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af689c --units bm_mima
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af689c

Both complete native rounds reproduce **all 833 original
CODE bytes, 93 ordered literal FIXUPP fields, three
PUBLIC offsets**, original OMF segments, normal complete
MAIN EXE, path-normalized MAP, Japanese loaded program,
1,553 ordered MZ relocations and independently
serialized original 130,882-byte Japanese MAIN.EXE.

Preserved real writer/source evidence:
`.analysis/work/exatt-layout-af689c/report.json`;
SHA-256 `0f9ce6edb81707daf5509559b439b8909ded2098da4484ad5f9c8a40147b6d6a`.
Only this one physical original TU was compiled twice,
with 98 other original project objects and CRT reused.
No full cold replay; no new canonical Factory packed-game
credit or historical raw OMF packet equality is claimed.

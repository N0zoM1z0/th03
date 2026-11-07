# Marisa complete Bomb: byte-exact native palette waves and physical source (after688)

The full original Marisa Bomb state machine is one complete
449-CODE-byte original `bm_mari` translation unit, placed in
HITBOX_TEXT. It is not a fragment: the source controls GRCG
background fill, early RGB palette ramp, the 64-frame animated
MRS/screen-shake and RNG explosion, the final sprite rendering,
and fade completion.

The new original-source-rooted v2 unchanged-source control
`af688a` compiled three physical original Bomb producers
Marisa/Mima/Reimu together, matching all 2,207 original
CODE bytes and preserving original MAIN image/MAP. This
isolated current Marisa source before edits.

In the complete maintained C++ Bomb source, original
`color = 0-(frame<<2)` and `255-(frame<<3)` are now
natural `color = 0-(frame*4)` and `255-(frame*8)`.
A genuine TC4 original-native full-object control `af688b`
proves the same CODE and 16-bit fixup fields. The odd-frame
sound gate `frame&1` uses natural typed
`static_cast<unsigned int>(frame)%2`, proven
byte-exact in `af688c`. The first 64-frame ramp,
next 64-frame sprite/shift effect, and the original
8-frame RNG explosion period have compiler-time named
C++ phases without additional DATA/BSS.

Two Marisa Bomb screenshake/sprite phase tests
`(frame&3)<2` were experimentally converted to
unsigned `frame%4<2`, which **changed native
CODE** (`af688d`). The original byte-mask forms
were restored. The 16-bit BX hardware fill input,
far Pascal boolean stack carrier and original
negative Y arithmetic shift are likewise preserved.

Final genuine modified-source OMF-COMENT-attested original
Turbo C++ 4.02/TLINK two-round proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af688e --units bm_mari
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af688e

Both rounds reproduce **449 original CODE bytes,
50 ordered literal native FIXUPP fields, one PUBLIC
offset**, complete original OMF segments, full normal
MAIN EXE and path-normalized MAP, Japanese program
image and all 1,553 ordered relocations, and separately
serialized exact 130,882-byte original Japanese MAIN.EXE.

Native proof: `.analysis/work/exatt-layout-af688e/report.json`,
SHA-256 `1986fa60452ce266c8c2088709f7dcff7c0a2e73072e4858d2c413527e5a82fc`.
Only this one original physical object was recompiled twice,
reusing the other 98 original project objects and CRT.
The target bytes were already tracked; no whole cold replay,
historical raw OMF packet byte identity or new canonical
Factory packed-game acceptance is claimed.

# TH03 MAIN polar geometry and CFG resident loader: native direct source proof (after729)

Two additional original physical source TUs were investigated using their
*real original* `obj/th03` linker slots and current maintained source,
not merely the original object labels in a historical MAP:

- `polar` — `src/main/math/polar.cpp`, complete **26-byte SHARED CODE**
  with one `polar(center, radius, ratio)` PUBLIC and zero original OMF
  fixup fields. Called extensively by the nine major BOSS geometry,
  bullets, player motion, and background effects.
- `cfg_lres` — `src/main/formats/cfg_lres.cpp`, complete **49-byte
  CFG_LRES_TEXT CODE** with six ordered original native OMF fixup fields
  and one resident-pointer-loader PUBLIC. The original near return,
  segmented resident pointer, stack-local configuration and original
  CFG filename initialization are preserved.

We extended the scoped original TC4 compiler/linker/reviewer to name both
complete physical source objects, original response slots and original
three-segment CODE/DATA/BSS MAP records. The unchanged-source `af729a`
control compiled both source objects together, reproducing original native
segments, fixup metadata, PUBLICs and the complete normal MAIN image/MAP.

## Native-exact natural C++ recovery and negative control

The **mathematically important** `polar` leaf retains the original 16-bit
signed radius, **32-bit signed product**, fixed Q8 arithmetic right shift
and 16-bit returned coordinate. We introduced a named compile-time
`POLAR_FRACTION_BITS = 8` and rewrote the return naturally as

    return center + ((static_cast<long>(radius) * ratio) >> POLAR_FRACTION_BITS);

This swaps only the two operands of the final signed-long sum, not the
multiplication, arithmetic shift, conversion width, or grouping. The
changed-source `af729b` original TC4 **fully matched** the original
physical CODE and all 99-object normal MAIN linking in two rounds.

We also tried explicitly naming a `register long scaled` intermediate
while preserving that expression's mathematical order (`af729c`). It
changed original CODE and was **rejected**; the final maintained source
is again precisely the tested `af729b`. The failed compiler source and
object stage remain retained; no target bytes were patched.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af729b --units polar,cfg_lres
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af729b

Both genuine original 16-bit TC4 4.02 / normal TLINK rounds match **75
complete original CODE bytes, six literal ordered native FIXUPP fields,
two PUBLICs**, both objects' complete segment declarations, entire
normal source-native MAIN/MAP, original Japanese **124,642-byte loaded
program** and all **1,553 ordered MZ relocations**. Independent standard
MZ serialization reproduces the exact original **130,882-byte MAIN.EXE**.
Only these **two** original source objects were rebuilt, and 97 other
project objects plus original CRT were reused. No full cold replay.

Source-bound proof: `.analysis/work/exatt-layout-af729b/report.json`,
SHA-256 `769f5366522af2b551a482ef77ee45d07930f4828223f2994079b8fca8df3f58`.
The 2 original native compiler rounds, source snapshots, OMF dependency
comments, linker responses, compiler writer logs and complete original
OBJ/EXE/MAP/MZ comparisons remain retained. This establishes new
**currently source-attested physical units**, not newly accepted canonical
Factory packed-file bytes, original vendor raw OMF packet identity or
whole-game source ownership; avoid double-counting historical coverage.

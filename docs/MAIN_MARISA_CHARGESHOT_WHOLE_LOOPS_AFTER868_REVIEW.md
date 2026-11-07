# TH03 MAIN after868: complete Marisa Chargeshot/Gauge native C++ history loops

The physical `cs_mari` original Turbo C++ 4.02 owner contains **nine
functions and 1,509 original initialized CODE bytes**: 12-sample beam
creation, Hyper activation, backward-shifted trajectory update, three-
sample hit test, three independently patterned GRCG render bands and
two 5-projectile Gauge volley branches with the true byte-valued
counter. All the changed loops were compiled as the **complete original
physical unit**, not synthesized helper functions or modern-only code.

## Maintained natural C++ recovery

All **nine independent source loops** now use ordinary typed C++
`while` with the original index/physical near-pointer ordering: two
12-sample initializers, a backward history shift from sample 11 to 1,
three hit samples 0/4/8 with original `break` behavior, three visually
distinct GRCG tile bands (11..7, 6..4, 3..1), and two five-shot Gauge
volley emitters. The initial head is updated **after** historical samples
shift, retaining the real 24-subpixel Y trail delay and unconditional
12-history initialization. The three GRCG bands reset `previous_x` and
use the original independent tile-pattern selection before checking X.
The renderer's **signed arithmetic `>>5`** stays a shift, not signed
`/32`; those differ on negative odd coordinates.

Named physical geometry now captures the original 16-pixel beam center
Y offset, signed 24-subpixel trail delay, GRCG vertical shift 5, display
clip Y=8 and left/right beam-edge offsets -2/+1. The actual byte frame
postincrement, 32-bit GRCG tile words, far-Pascal Gauge callbacks and
per-volley literal `speed.v -= 6` are retained when the real compiler
says they are codegen-sensitive.

## Actual original Turbo C++ source trials

- `af868a`: history backward shift becomes natural `while`; complete
  original TC4/normal MAIN TLINK byte-exact in both independent rounds.
- `af868b`: both 12-point initializers become natural `while`, still
  whole original CODE/fixups/normal MAIN exact twice.
- `af868c`: all **three distinct GRCG tile-band render loops** become
  natural `while`, retaining original signed Y and postcall X checks;
  original object still exact in both rounds.
- `af868d`: both original five-shot Gauge emitters become natural `while`;
  complete original source remains byte-identical in two native rounds.
- `af868e`: the sparse 0/4/8 sample collision scan also becomes `while`,
  preserving the original `break` and skip; still full native-exact.
- `af868f`: independently challenged the original literal byte-memory
  Gauge `speed.v -= 6` with a named same-valued enum in both emitters.
  Genuine original TC4 produced **1,503 CODE bytes** rather than
  original **1,509**. Restored both literal source updates.
- `af868g`: independently challenged the mutable charged beam
  `p->frame++` with prefix `++p->frame`. Real TC4 produced **1,514
  CODE bytes**, not 1,509; the original byte postfix remains.
- `af868h`: exact native confirmation of named original geometry and
  reverted byte-sensitive updates, both compiler/link rounds passed.
- Final `af868i`: current source comments, exact GRCG call formatting
  and all nine natural loops recompiled in **two genuine original
  TC4 4.02 and complete normal MAIN TLINK rounds** with byte equality.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af868i --units cs_mari
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af868i
```

Both final genuine original compiler/linker rounds match **all 1,509
original CODE bytes, 152 literal ordered native OMF FIXUPP fields and
9 PUBLIC offsets**, complete original source dependency/segment ABI,
full normal MAIN EXE/MAP, all **124,642 original Japanese loaded program
bytes and 1,553 ordered MZ relocations**. Independent standard MZ
serialization matches all **130,882 original Japanese MAIN.EXE bytes**,
without claiming historical TLINK header byte construction. The **98
other unchanged original game project objects and CRT were reused**;
no full cold replay, patched target/OBJ or fabricated byte buffers.

Protected current-source-bound two-round genuine compiler/TLINK report:
`.analysis/work/exatt-layout-af868i/report.json`, SHA-256
`8fde1aba730031f05ed29f0ba53c0d99abc820847101d214bae2fc77ca6b7168`.
This is improved maintained original C++ for a **historically
source-covered physical owner**, not additional unique CODE byte credit,
raw historical vendor OMF packet identity or canonical Factory packed-
file acceptance.

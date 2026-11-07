# TH03 MAIN after848: complete Yumemi major BOSS natural raster control

The entire original `ba_yumem` physical Turbo C++ owner (ten functions,
**2,358 original CODE bytes**) was compiled from the *maintained current
source*, not isolated from the real BOSS update, RNG and sprite call
ordering. The full `yumemi_render_arrival()` **four-stage 112-pixel
sprite raster** now expresses its two increasing and two decreasing
8-pixel sweeps as ordinary `while` loops. The original upper/lower
signed inequalities and end-of-loop register changes remain exact.

The BOSS main renderer's zero effect/gauge check now naturally uses
`!(boss_effect_radius || boss_render_frame)` for the original two
empty conditions. Chase-mode left/right borders and cross-ring four
signed displacement directions, plus source BOSS origin offsets, are
named as real 16-bit subpixel constants. None alters the original
four separate random angle calls, script transition deadlines or
screen-clip/reset ordering.

## Actual original native C++ experiments

- `af848a`: first typed `for` raster changed to `while` and passed both
  complete original TC4 4.02/compiler and normal MAIN TLINK rounds.
- `af848b`: **all four entrance loops** changed to signed-step
  `while` loops; the entire physical BOSS remains original CODE exact.
- `af848c`: new De Morgan Boolean render condition remained exact.
- `af848d`: attempted to invert the positive chase-X interval into
  an earlier negative range exit. This logical rewrite **failed** the
  original full CODE comparison, even though initialized length remained
  2,358. Its original branch shape was restored.
- Final **`af848e`** names original chase/volley geometry, preserves
  the BOSS scheduler and restores exact branch shape. Two genuine
  original TC4/normal TLINK rounds pass for the final current source.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af848e --units ba_yumem
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af848e
```

Both full original compiler/link rounds reproduce **all 2,358 original
CODE bytes, 343 literal ordered OMF FIXUPP fields, 10 PUBLIC offsets**,
original source/segment ABI and complete normal MAIN EXE/MAP. The
resulting **124,642-byte Japanese loaded game** and all **1,553
ordered original MZ relocations** match; independent standard MZ
serialization recreates all **130,882 original Japanese MAIN.EXE bytes**.
Only this physical BOSS owner was rebuilt, **98 other original game
objects and CRT reused unchanged**, no full-project cold replay.

Protected source-bound report and both genuine original writer rounds:
`.analysis/work/exatt-layout-af848e/report.json`, SHA-256
`dd986eb7749a072ba964d77d757d1d7e84ef93b6871ea29ec5e2a3797a62ac4c`.
This is **current original-source recovery for historically covered CODE**,
not additional unique CODE ownership, vendor raw OMF packet identity,
canonical Factory packed-game acceptance, or historical original-text
provenance. Rejected codegen experiments are retained as negative control.

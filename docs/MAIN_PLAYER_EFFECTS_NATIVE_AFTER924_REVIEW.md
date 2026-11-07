# TH03 MAIN after924 — full player effects update and original GRCG polygon engine

The complete original five-function `effects` physical Turbo C++ 4.02
source contains three separate explosion/center/axis effect spawners,
the entire effect pool's age/radius update and its full PC-98 GRCG
rasterizer (circles and true four-edge quadrilaterals). The pool's
historical DATA/BSS ownership and all actual RNG/palette/hardware calls
remain unchanged.

The full effect-pool **age/radius update** and the large full-pool
**render dispatcher** now use natural `while`, retaining the original
signed index and near-pointer updates after each record or sprite.
All active tests naturally spell `kind != PLAYER_EFFECT_FREE`. Both
original byte-angle updates can naturally use explicit named C++
assignments: the polygon's +64 rotation and alternating physical
slot +/-8 rotation. The latter emits exactly the original machine
code despite earlier failed direct enum-valued compound `+=` trials.
The inner four-vertex `while` retains separate signed-division
positions, exact polar calls and draw ordering.

Genuine original TC4 experiments:

- `af924a/b`: complete age updater and substantial GRCG render dispatcher
  changed from `for` to natural `while`, exact native CODE/TLINK twice.
- `af924c`: both active-effect `if(kind)` became `if(kind != FREE)`,
  whole original object and normal MAIN exact twice.
- `af924d`: changing all three physical byte ring cursors to prefix
  generated **640** CODE bytes vs original **628** (first diff
  CODE segment 4 offset 4); original postfix retained.
- `af924e`: quad byte-angle `angle += 64` became natural explicit
  `angle = angle + named_step`, byte-exact in both TC4/TLINK rounds.
- `af924f`: byte effect age `age++` to prefix emitted **633** vs
  original **628** CODE (first diff segment 4 offset 255).
- `af924g`: per-pool-entity alternating +/-8 byte angle also accepts
  `angle = angle + (parity ? named_step : -named_step)` exactly.
- `af924h`: negative-sensitive circle Y `>>1` to `/2` emitted **631**
  vs original **628** CODE (first diff segment 4 offset 317).
- `af924i`: radius compound `+=` to explicit signed assignment also
  emitted **631** vs original **628** CODE (first diff offset 255).
- Final `af924j`: both independent original TC4/full normal MAIN
  TLINK rounds recompiled all current C++ with rejected forms restored.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af924j --units effects
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af924j
```

The independent original rounds match **628 CODE bytes, 33 literal
ordered native OMF FIXUPPs, five PUBLICs**, historical source/segments
and ABI, complete normal MAIN EXE/MAP, **124,642 Japanese loaded bytes
and 1,553 original ordered MZ relocations**. Reviewed independent
standard DOS MZ serialization matches all 130,882 original Japanese
MAIN.EXE bytes, not necessarily historical vendor header serialization.
**98 other original game objects and original CRT reused**, no cold
replay, target patching, machine-code padding or object spoofing.

Protected genuine current-source-bound original writer receipt:
`.analysis/work/exatt-layout-af924j/report.json` SHA-256
`c7baa26845440c640c7c3686c7a596bf77bbacf4feeca20b1f6272a8af002656`.
Already source-covered historical CODE; natural C++ improvement is not
new distinct game bytes or canonical Factory packed-file acceptance.

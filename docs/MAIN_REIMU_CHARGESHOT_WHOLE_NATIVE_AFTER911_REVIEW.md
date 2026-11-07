# TH03 MAIN after911 — entire Reimu Chargeshot/Gauge, real six-slot hit scan

This is a genuine rebuild of the **complete original `cs_reimu` physical
Turbo C++ 4.02 source**: 24-slot reset, four-shot spiral creation and
seven history samples per shot, Hyper first-free-slot allocation,
12-projectile deceleration/homing/clip update, GRCG sprite rendering,
*only six* physical hit-test slots, and original mirrored Gauge attacks.
The original 32-byte projectile stride and externally owned DGROUP
state remain original. This is not a modern isolated function stub.

The original reset, four-shot spawn and its nested seven-history-point
initialization, full 12-projectile update and reverse 6..1 history shift,
true six-slot two-continue hit test, and full 12-shot monochrome/color
render all use **native-exact natural `while`**. Each early continue
preserves the original near-pointer/index step and the original PC-98
DX-zero GRCG sprite boundary. The original four-shot byte angle `+=0x20`
can naturally become `angle = angle + REIMU_CHARGE_LAUNCH_ANGLE_STEP`
without changing native CODE. The separate Gauge byte interval permits
`if(!remainder)`. Original -24-pixel clipping, 20-pixel hit margin,
48×48 sprite and screen placement have named original constants.

Actual genuine original compiler experiments:

- `af911a`: natural reset, four-shot launcher and seven-point history
  initializer, complete source and full normal MAIN exact twice.
- `af911b`: attempted to turn the Hyper first-free-slot
  `for/continue/break` into `while`, generating **1,450 vs original
  1,448 CODE bytes** (first difference CODE segment 4 offset 169).
  Restored original allocator shape.
- `af911c`: entire update and 6..1 backward history shift as native
  `while`, original CODE/FIXUPPs/whole MAIN exact twice.
- `af911d`: full actual *six-slot* hit-test with two explicit `continue`
  pointer advances as natural `while`, still original exact.
- `af911e`: full twelve-slot mono/color render as natural `while`;
  real sprite hardware service and near call ABI unchanged.
- `af911f`: original byte spiral `angle+=0x20` rewritten using natural
  explicit byte assignment and a named step, native exact twice.
- `af911g`: natural zero remainder on the true Gauge byte clock exact.
- `af911h`: original byte projectile frame postfix changed to prefix
  generated **1,453 vs 1,448 CODE bytes**, first mismatch CODE segment
  4 offset 298. Original postfix retained.
- `af911i`: named real clip/hit/sprite geometry, original exact twice.
- Final `af911j`: current full original owner and source-specific
  semantics recompiled twice using actual TC4 4.02 and the complete
  normal MAIN TLINK in original project slots.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af911j --units cs_reimu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af911j
```

Both independent compiler/linker rounds match **all 1,448 original
CODE bytes, 138 literal ordered OMF FIXUPPs and 10 PUBLIC offsets**,
source/segment/16-bit ABI, complete normal MAIN EXE/MAP, **124,642
Japanese loaded bytes and 1,553 ordered original MZ relocations**.
Independent standard DOS MZ serialization matches all 130,882 original
Japanese MAIN.EXE bytes, not raw historical vendor header serialization.
**98 other original game project objects and CRT reused**, no cold replay,
patched target/OBJ, synthetic code buffer or padding.

Current-source-bound original compiler report:
`.analysis/work/exatt-layout-af911j/report.json`, SHA-256
`04eb0667fdb43d436f5beb0895ba92dbee630f466696a50ebe9ba82e66ac47fd`.
Previously source-owned original CODE. This is improved maintainable
native C++ fidelity, not new distinct code credit, vendor OMF packet
identity or canonical Factory packed-game acceptance.

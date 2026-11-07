# TH03 MAIN after912 — complete Yumemi Extra Attack, native beam/flight control

The complete five-function original `ex_yume` Turbo C++ 4.02 physical
source owns two distinct allocators, the full 16-entity beam/flight
collision/update controller, elaborate EGC/GRCG beam renderer with four
perimeter loops, and the 16-entity dispatch renderer. The 32-byte real
projectile pool and shared flight functions remain externally owned;
this is a whole real original object, not a convenient mock renderer.

Both original first-free allocators (eight ordinary and slots 8..15
special), the **full 16-entity update with two independent early
`continue` paths**, and the entire 16-entity render dispatcher now
use natural C++ `while`. Each advance of the signed index and near
entity pointer occurs at precisely the original point after the
physical flight/collision/beam calls. Explicit source `state ==
YUME_EXATT_FREE` matches the original inactive truth test. Four
existing native-exact 16-pixel horizontal/vertical beam-perimeter
loops preserve all original GRCG clip and hardware register calls.

Real original compiler-positive and negative experiments:

- `af912a`: both real original slot allocators converted to `while`,
  original whole owner and normal Japanese MAIN exact twice.
- `af912b`: substantial full beam/hitbox/flying/arrival update converted
  to `while` with two correct early-continue index/pointer advances,
  exact original CODE and full normal TLINK twice.
- `af912c`: 16-entity full render dispatcher converted to native
  `while`, preserving all original near calls and sprite order.
- `af912d`: changed mutable byte `p->frame++` to prefix; actual TC4
  generated **1,701** vs original **1,696 CODE bytes** (first diff
  CODE segment 4 offset 1358). Original postfix restored.
- `af912e`: rewrote two signed screen-coordinate `top / 2` expressions
  to `top >> 1`. The real compiler emitted **1,690** instead of
  1,696 CODE bytes (first diff CODE segment 4 offset 261), and signed
  negative rounding is also different. Original division restored.
- `af912f`: natural explicit original free-state equality in both
  allocators and large update preserves exact original CODE twice.
- Final `af912g`: entire current maintained source and codegen comments
  compiled in two independent genuine original TC4 4.02 plus complete
  normal MAIN TLINK rounds, native exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af912g --units ex_yume
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af912g
```

Both independent original compiler/linker rounds match all **1,696 CODE
bytes, 87 literal ordered original OMF FIXUPP fields, five PUBLIC
offsets**, original physical segment/source ABI, complete normal MAIN
EXE and normalized MAP, **124,642 Japanese loaded program bytes and
all 1,553 ordered MZ relocations**. Independently reviewed standard
DOS MZ serialization reproduces all **130,882 original Japanese
MAIN.EXE bytes**, not historical vendor TLINK header identity.
**98 other original game project objects and CRT were reused**;
no full cold replay, target/OBJ patches, synthetic CODE or padding.

Protected genuine source-bound TC4/normal TLINK writer receipt:
`.analysis/work/exatt-layout-af912g/report.json`, SHA-256
`6331eee117391e06a12bf8e8c10a2e71af6d63837e82107d55ae1499bee67c3e`.
Historically source-covered bytes: native C++ improvement is **not
additional distinct original CODE ownership, vendor raw packet
identity or canonical Factory packed-file acceptance**.

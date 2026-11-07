# TH03 MAIN after885 — complete Marisa Extra Attack control as native C++ loops

The full five-function original physical `ex_maris` Turbo C++ 4.02 owner
contains the ordinary and BOSS-special fourteen-slot allocators,
three-phase 16×16 beam/flying sprite renderer, the complete
movement/beam-collision/arrival controller and fourteen-slot render
traversal. The 32-byte entities and shared flight/draw functions stay
in their own real historical original objects.

## Genuine natural C++ control and original geometric meaning

The two fourteen-entity allocators, the entire render dispatcher and
the long main updater now use natural C++ `while` loops with the
original signed 16-bit index and near pointer changes. In particular,
the update's **three original `continue` exits** — inactive entity,
expired beam and arriving flying entity — each advance *both* the
original signed index and near pointer before the next iteration.
The normal state/animation path does the same after its original byte
`frame++`. The six distinct beam sprite cels and original sprite
helpers are retained in their historical near/far ABI.

The exact X-target RNG range 0x1200, initial speed 0x6E, 0x1700 active
beam bottom/arriving Y, upward 0x100 step and signed -0x100 clamp,
4-pixel collision stripe, signed height `/32` and 0x1820 spawn marker
are now meaningful original compile-time C++ constants. The signed
height divisor deliberately uses integer division; a shift would
change negative values and original TC4 codegen.

## Actual original compiler experiments

- `af885a`: both full original allocators changed to natural `while`,
  two independent genuine TC4/full normal MAIN TLINK rounds exact.
- `af885b`: fourteen-slot render dispatcher also changed to `while`,
  still entire original CODE/FIXUPPs/normal MAIN exact twice.
- `af885c`: substantial update with all **three explicit `continue`
  pointer/index paths** changed to `while`, completely native exact.
- `af885d`: signed `height / 32` replaced by `height >> 5` generated
  **673** initialized CODE bytes vs original **676** (first difference
  CODE segment 4 offset 409), also changing negative rounding. Rejected.
- `af885e`: changed byte `p->frame++` to prefix, producing **681**
  original-CODE candidate bytes vs original **676**, rejected.
- `af885f`: named real launch/collision/beam coordinates and maintained
  original signed division and byte postfix, two native rounds exact.
- Final `af885g`: final current source/comments, recompiled through
  actual original TC4 4.02 and normal complete MAIN TLINK twice.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af885g --units ex_maris
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af885g
```

Both independent genuine original compiler/full normal MAIN linker
rounds reproduce all **676 original CODE bytes, 35 literal ordered
native OMF FIXUPP fields and 5 PUBLIC offsets**, source/segment/ABI,
complete original normal MAIN EXE/MAP, **124,642 Japanese loaded program
bytes and 1,553 ordered MZ relocations**. Independently checked
standard DOS MZ serialization reproduces all **130,882 original Japanese
MAIN.EXE bytes**; historical vendor header identity is not claimed.
**98 unchanged original project objects and CRT reused**, no full cold
replay, patched original target or synthetic CODE/NOP padding.

Protected original-source-bound native writer report:
`.analysis/work/exatt-layout-af885g/report.json` SHA-256
`445c260eab20e74e18295705da39924e7d871cfa937620fd97772af562fbf96b`.
The physical original owner had historical CODE-source coverage already.
This advances exact maintainable C++ and 16-bit compiler certainty,
**not new unique original CODE or canonical Factory packed-file credit**.

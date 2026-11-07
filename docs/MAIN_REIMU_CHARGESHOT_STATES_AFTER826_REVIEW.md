# TH03 MAIN after826: complete Reimu Chargeshot/Gauge state recovery

The original physical `cs_reimu` is **one ten-function 1,448-byte CODE
module**, not ten interchangeable standalone leaf compilers. The full
current maintained `src/main/player/chargeshot_reimu.cpp` now names
all three **byte-valued projectile states**: inactive (0), braking (1),
and homing/Hyper (2). This covers source-native reset, four-way spawn,
Hyper slot selection, seven-position history update, travel/acceleration,
six-slot collision, full 12-slot render, and both Gauge controllers.

These are original physical 32-byte structs with **seven history X/Y
samples**, 12 updated/rendered charged shots per player and **only six
collision-tested slots**, a real original quirk. The source does **not**
repair this behavior. Their original seven-position shift, slowing-to-
tracking transition and separate alternate-hit-frame schedule stay in
exactly the original order. The 32-frame Gauge ring period, phase 16 and
byte-derived Gauge initialization now have explicit semantic names, while
keeping the actual 16-bit word/byte evaluation and original RNG cadence.
The original signed 16-bit animation `phase` is still masked via `&3`.

## Genuine TC4 C++ alternatives and negative controls

- `af826a` tried `phase %= 4` on the signed 16-bit animation carrier.
  The entire original CODE payload **failed** comparison: signed
  division's codegen cannot be substituted for the original mask.
- `af826b` challenged it with an explicit unsigned cast before `%4`.
  This also **failed** whole-original CODE equality; the original
  mask stays. Neither result is counted as accepted native evidence.
- `af826c` introduced the real three-state lifecycle and explicit
  Gauge clocks, but replacing the original `angle += 0x20` with an
  enum-valued 0x20 changed Turbo C++'s byte-local update: the original
  reuses AL, while the alternate compiles into a direct memory `ADD`.
  It was rejected without byte padding, restoring the literal update.
- The corrected `af826d` and final **`af826e`** both passed two genuine
  original TC4 and normal TLINK rounds. The final additionally omits an
  unnecessary explicit cast around the already unsigned 16-bit frame
  clock for the alternate collision hit test.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af826e --units cs_reimu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af826e
```

Each native round confirms **all 1,448 original CODE bytes, 138 literal
ordered native OMF FIXUPP fields and ten PUBLIC offsets**, complete
original physical source/segment geometry, full normal Japanese MAIN
EXE/MAP, all **124,642 Japanese loaded program bytes** and **1,553
ordered MZ relocations**. Independent standard MZ serialization matches
all **130,882 bytes** of the pinned Japanese MAIN.EXE. The original
**98 other game objects and CRT are reused unchanged**: no full cold
replay. The actual compiler-source-binding check and independent review
are retained at `.analysis/work/exatt-layout-af826e/report.json`, SHA-256
`7976a6ba23b2264b317399ee0461313db97b57ab19fca88ab1f4a23bde027e70`.

This module already had historical native source ownership; these bytes
are **not new independent coverage**. Packet-identical vendor OMF,
whole-game current native source ownership and canonical packed-file
Factory acceptance are separate, unproved gates.

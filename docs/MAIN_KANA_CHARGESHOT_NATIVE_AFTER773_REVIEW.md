# TH03 MAIN Kana Chargeshot: complete four-trail/GRCG and Gauge source native after773

The original complete physical `cs_kana` Turbo C++ source contains
**nine functions** with **1,291 initialized CODE bytes, 117 literal
ordered original OMF FIXUPP fields and 9 PUBLICs**. It owns Kana's
four independent 13-sample beam trails (54-byte per-trail records),
charge creation, signed vector-based motion, reverse collision traversal,
GRCG overlap sprite rendering and the full 64-frame left/right Gauge
projectile sweep. This is a full original physical module proof, not a
small isolated leaf.

## Natural C++ reconstruction actually accepted

All four original `group++, p++` beam-trail iteration sites now use
signed local prefix `++group` without disturbing near pointer
postincrement. Sample initialization uses `++i`, and the 4-trail
GRCG render loop uses a named `KANA_CHARGE_TRAILS` count and `++i`.
The original signed reverse sample history loop remains separate
(`--point`), preserving all 13 historical coordinates and the original
12/8/4/0 render sample slots. Active state 1 and released state 2 are
explicit enum values, and the early charge/hit return and Gauge
activation helpers use naturally evaluated byte-truth tests. Original
RNG, 16-bit subpixel math, GRCG overlap setup/cleanup and Gauge state
expiration after 128 ticks are preserved, with no bug fixes.

## Real original compiler tests: two important rejected simplifications

- `af773a`: natural loop and state changes, the entire 1,291-byte original
  physical CODE plus full original normal MAIN linking passed both
  original Turbo C++ 4.02 compiler rounds.
- `af773b`: attempted to replace the 8-bit Gauge sweep's `% 64` with
  a theoretically equivalent `& 63` mask. TC4 CODE changed, so the
  original unsigned-byte modulo remains necessary for source exactness.
- `af773c`: attempted `_DX = 0` instead of the original GRCG overlap
  setup `asm xor dx, dx`. Original CODE differed; the explicit hardware
  register zeroing instruction was restored rather than spoofing its
  output or assuming the compiler would use XOR.
- `af773d`: final live maintained source, now with named 4-trail
  renderer bound and notes explaining the original CPU encodings, was
  independently compiled and fully linked **again**, with both rounds
  matching original bytes and native metadata.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af773d --units cs_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af773d

Both actual original TC4 compiler and TLINK rounds reproduce **1,291
original CODE bytes, 117 ordered literal original OMF FIXUPP fields,
all 9 PUBLIC offsets**, original segment/ABI and compiler-emitted
source COMENT fields, full normal MAIN EXE and MAP, Japanese 124,642-byte
loaded game and all 1,553 original MZ relocation words. Separately
verified standard MZ serialization reproduces the complete original
130,882-byte Japanese MAIN.EXE. 98 other project objects and original
Borland CRT were **reused**, not cold-rebuilt. Negative trial writer
outputs remain retained, without object byte patching.

Current-source proof `.analysis/work/exatt-layout-af773d/report.json`,
SHA-256 `5d5e3d642af4fd240656026f17e32e1799f8f4cfccc400f14b3bf6f59a7412b8`.
This is natural current-source recovery for already owned original CODE,
not new Factory canonical packed-game credit, vendor raw OMF packet
identity or all-product source ownership.

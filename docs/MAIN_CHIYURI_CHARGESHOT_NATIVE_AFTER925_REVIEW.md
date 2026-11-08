# TH03 MAIN after925 — full Chiyuri Chargeshot/Gauge state, hit and warning ABI

The original nine-function `cs_chiyu` physical Turbo C++ 4.02 unit
contains eight staggered 6-byte shots per player, full reverse-flight
and arrival updating, a hit test with five separate early-continue paths,
original 32×48 sprite drawing, and paired Gauge warning/shot control.
All projectile/Gauge arrays stay externally owned. The original quirk
of resetting **only the first physical slot sixteen times** remains;
repairing that source behavior would not reproduce the historical game.

The four original zero-age activity guards now naturally use explicit
`age == CHIYURI_CHARGE_INACTIVE_AGE`, and the two far Gauge entrypoints
use `gba_flag_active != GBAF_NONE`. The Gauge initialization enum
comparison may naturally put `flag_expected` first. The 24-pixel
Gauge warning X increment now uses a named constant while retaining
true original 16-bit compound memory and local-word updates. The full
original update, five-skip collision scan and reverse sprite renderer
retain their already native-exact `while` and near pointer order.

Independent genuine original TC4 codegen experiments:

- `af925a`: all four inactive age checks and two Gauge guards became
  explicit enum/zero comparisons, entire owner/normal MAIN exact twice.
- `af925b`: replacing the byte animation `anim &1` with `%2`
  generated **1,020 CODE** vs original **1,011**, first mismatch
  segment 4 offset 274. Original mask restored.
- `af925c`: byte `hits++` to prefix produced **1,016** vs 1,011,
  first difference segment 4 offset 362. Postfix restored.
- `af925d/e`: substituting explicit `word=word+named` for both the
  Gauge warning memory and local X increments failed; after restoring
  memory compound, the local explicit assignment alone still emitted
  **1,013** vs 1,011. Restored both compound operations.
- `af925f`: the actual 16-bit Gauge global X memory compound `+=`
  accepts a *named* 24-pixel compile-time constant, original exact.
- `af925g`: naming the local X compound step and swapping Gauge
  initialization equality operands also preserves every original byte.
- `af925h`: byte projectile age postfix decrement to prefix emitted
  **1,015** vs original **1,011**, first difference segment 4 offset
  121. Original postfix retained.
- Final `af925i`: source-current comments and all accepted natural C++
  compiled in two independent original TC4 4.02 and complete normal
  MAIN TLINK rounds, entire physical object byte-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af925i --units cs_chiyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af925i
```

Both genuine original compiler/normal linker rounds match **1,011
original CODE bytes, 96 literal ordered OMF FIXUPP fields, nine PUBLIC
offsets**, actual source/segments and 16-bit ABI, full normal MAIN
EXE/MAP, **124,642 Japanese loaded bytes and 1,553 original ordered
MZ relocations**. Independent standard MZ serialization recreates
all 130,882 original Japanese MAIN.EXE bytes (not historic vendor
header writer proof). **98 other original project objects and CRT reused**,
no full cold replay, target byte patches or synthetic NOP padding.

Protected current-source-bound actual TC4/TLINK proof:
`.analysis/work/exatt-layout-af925i/report.json` SHA-256
`ccc70a588e76df52ec03a050e96a5cd7732dc1a762543cd82e28c59eb0fc453a`.
Historically source-covered CODE; no new distinct original bytes or
canonical Factory packed-game acceptance credit.

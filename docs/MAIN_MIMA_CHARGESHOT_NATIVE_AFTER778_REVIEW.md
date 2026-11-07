# TH03 MAIN Mima Chargeshot: complete 30-projectile update, collision and Gauge native source after778

The complete original `cs_mima` physical Turbo C++ owner contains **ten
functions**, including a 30-slot reset pool, 15 charged projectiles per
player in a six-angle sequence, timed emission, per-frame velocity/
clip update, full 15-entity hit scan, projectile sprite renderer, and
8/16-frame double-ring Gauge barrage/expiration logic. The original
physical OMF owns **1,338 initialized CODE bytes, 150 ordered literal
FIXUPP fields and 10 PUBLICs** in the original 16-bit code group.

## Natural maintained source reconstruction

All five original 15/30-slot creation, reset, hit, update and render
loops now naturally use `++i` for the signed local counter while
preserving the original near-pointer postfix increments, six-angle
`i % 6` emission sequence, original frame/RNG consumption and ordered
player ownership. The original unused or surprising storage fields
are untouched. The original byte-valued 0/1 inactive/active states are
now compile-time names, and active/zero tests in the large movement,
collision, render and Gauge routines are ordinary C++ Boolean checks.
The complete 16-bit subpixel geometry, group flags, sprite angles and
signed `i % 3` rendering pattern remain intact.

## Exact native TC4 4.02 codegen tests of three clocks

Three separate experiments **challenged** natural bit masks against
original unsigned-byte period operations; all are real original full
physical compiler objects, not inferred from earlier docs:

- `af778a`: attempted masking the **4-frame release**, **8-frame
  Gauge ring** and **16-frame additional ring** together. The complete
  CODE shrank from 1,338 to 1,320 bytes and failed OMF exactness.
- `af778b`: restored just the three `%` operations while retaining all
  natural loops/state/Boolean edits. Both native compiler/full MAIN
  linker rounds matched all original byte/OMF fields again.
- `af778c`: isolated `frame % 4` to `frame & 3` in the timed release.
  The original CODE changed. Rejected.
- `af778d`: independently tested `% 8` to `& 7` on the active Gauge
  ring. The original CODE changed. Rejected.
- `af778e`: independently tested `% 16` to `& 15` for the second Gauge
  ring. The original CODE changed. Rejected.
- `af778f` and final **`af778g`** restored all three necessary original
  byte-modulo forms, documented the compiler-sensitive differences and
  actually recompiled the final maintained source twice. All original
  CODE/OMF/full normal MAIN fields matched both rounds.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af778g --units cs_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af778g

Each of the two genuine Turbo C++ 4.02 and full normal TLINK MAIN rounds
reproduces **all 1,338 original CODE bytes, 150 ordered native OMF
FIXUPP fields, 10 PUBLIC offsets**, complete original segment layouts
and emitted current-source COMENT dependencies. The full 99-project-
object normal MAIN EXE and path-normalized MAP, original Japanese
**124,642-byte loaded program and 1,553 ordered MZ relocations** match.
Independent standard DOS MZ serialization reproduces the complete
**130,882-byte original Japanese MAIN.EXE**. The other 98 original
project objects and Borland CRT were reused; no full cold replay,
original target substitution or code patching.

Current source-native receipt:
`.analysis/work/exatt-layout-af778g/report.json`, SHA-256
`aa743ab91869467db44e6e204bcf6c46a50159f18609ac57c645c2da8a7e024c`.
Negative trial compiler objects and logs remain protected, and none is
counted as accepted. This is meaningful maintainable C++ source
recovery for **already source-owned original bytes**, not additional
canonical Factory packed-game accepted units, historical vendor raw
OMF packet identity or entire product acceptance.

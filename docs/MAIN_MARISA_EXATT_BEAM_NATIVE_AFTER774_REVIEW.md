# TH03 MAIN Marisa Extra Attack: original-native 14-slot beam lifecycle after774

The complete original `ex_maris` physical 16-bit Turbo C++ module owns
**five functions**: the two 14-slot Extra Attack producers, the
substantial beam/column sprite renderer, the 14-slot update and collision
controller, and its renderer dispatcher. This is a full **676-byte
original CODE owner** with **35 ordered native OMF FIXUPP fields and
5 PUBLIC offsets** in `P_EXATT_TEXT`; the existing shared 32-byte
entity storage remains separately owned.

## Natural C++ reconstruction tested on the whole source

The maintained source now names the fourteen real entity slots,
free/beam/flying/appearing states (0/1/2/3) and distinct original beam
sprite and collision life phases: 0x30, 0x60, 0x66, 0x6C, 0x72, 0x64
and terminal 0x78. These timing boundaries are **not merged**: sprite
sheet selection, vertical motion, the X-column collision strip, and
bomb center additions remain in their original per-frame order.
All four signed local entity scans naturally use `++i`, while their
near-pointer postincrements remain as originally compiled. Inactive
state and shared flight update results use ordinary Boolean checks,
without changing RNG consumption, per-entity frame increments,
near/far Pascal callback parameters or the original sprite clip
selection (`pid_current == 1`, not generic truthiness).

Two deeper expression simplifications were independently rejected:

- `af774b` changed original signed 16-bit `collmap_tile_h.v = height / 32`
  into arithmetic shift `height >> 5`. Real TC4 generated different
  complete CODE. For negative heights the expressions can also differ
  in signed truncation semantics, so the original integer division
  remains necessary.
- `af774c` replaced original mutable 8-bit `p->frame++` with
  `++p->frame`, also changing original CODE. The original postfix
  frame mutation is retained, without repairing unrelated game quirks.

The first changed-source `af774a` trial passed the whole five-function
original unit; `af774d` independently recompiled the **final current
maintained source** with the negative-control comments and original
signed division/postincrement intact. Both real original TC4 4.02 and
full normal MAIN TLINK rounds were byte exact:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af774d --units ex_maris
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af774d

All **676 original CODE bytes, all 35 literal ordered original OMF
FIXUPP fields, all five PUBLIC offsets**, original segment/ABI and
source COMENT dependencies match. Both source-native normal MAIN EXE
and path-normalized MAP reproduce the original Japanese **124,642-byte
loaded program and all 1,553 ordered MZ relocations**. Independent
standard DOS MZ serialization reproduces the complete original
**130,882-byte Japanese MAIN.EXE**. The other 98 original project
objects and CRT were reused unchanged; no full cold replay, fabricated
CODE bytes or output patching.

Final source-native receipt:
`.analysis/work/exatt-layout-af774d/report.json`, SHA-256
`3294114c6bee629adb6a0ef2c43ae3940f5dbc22942341cb6128afd9f870a1d3`.
The failed original native compiler trials are retained as evidence.
This recovers natural source behavior from already owned original bytes;
**no additional canonical Factory packed-game acceptance**, historical
vendor raw OMF packet identity or 99-TU source ownership is claimed.

# TH03 MAIN Chiyuri Chargeshot/Gauge: full native loop and byte-frame C++ after771

The original complete 16-bit `cs_chiyu` Turbo C++ physical module owns
**nine functions**: eight-projectile creation, full countdown/update,
individual sprite leaf, reverse hit scanning and renderer, and mirrored
Gauge bombs and bullet volleys. It contains **1,011 original initialized
CODE bytes, 96 literal ordered OMF FIXUPP fields and nine PUBLICs**.
No original function was compiled as an invented standalone snippet.

## Verified natural C++ recovery

The maintained source now naturally increments the signed local `i` in
all **five** original array/renderer/update/scanner loops, preserving
near-pointer `p++`, `p--` and the original reverse physical slot order.
Original inactive-age equality checks use the byte's zero truth value.
The creator copies the underlying 16-bit Subpixel `.v` coordinates
instead of relying on implicit wrapper conversions, and both Gauge
activation helpers naturally test a nonzero flag. The original
unsigned-byte `% 2` sprite animation check and odd-tick Gauge bullet
check are **native-exact** as direct byte `& 1` tests.

The original **16-slot reset routine deliberately fails to advance its
pointer**: it clears the same first projectile's age 16 times. That
quirk is in the original Japanese game and was **not fixed**. All
three countdown/initialization paths retain their original byte
postincrements and decrements, shot enabling, hitbox/collision order and
original 6-byte projectile storage stride.

## Actual original compiler experiments and negative control

- `af771a`: first changed-source native TC4 4.02 source scope with
  signed local prefix loops, active-zero checks and direct 16-bit field
  loads. Both complete original compiler and full normal MAIN link
  rounds passed.
- `af771b`: changed animation byte `%2` to `&1` and again passed.
- `af771c`: additionally changed the original 8-bit Gauge clock's
  `% CHIYURI_GAUGE_BOMB_PERIOD` (period 16) to a direct `&15` mask,
  along with gauge shot parity. The entire physical CODE **differed**,
  despite equivalent unsigned arithmetic. Rejected as a combined trial.
- `af771d`: restored the original `%16` and retained the natural
  byte `&1` Gauge parity test; both native rounds were again exact.
- `af771e`: added source comments distinguishing these two separate
  codegen cases and independently recompiled the final maintained
  source in two original TC4/TLINK rounds. All original object and
  linker fields matched again.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af771e --units cs_chiyu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af771e

Both rounds match **all 1,011 original CODE bytes, all 96 ordered literal
OMF FIXUPP fields, all 9 PUBLIC offsets**, original segment layout and
native compiler source-dependency COMENT records. Full normal 99-object
MAIN EXE/normalized MAP, Japanese 124,642-byte loaded program and all
1,553 ordered MZ relocations match. An independently validated
standard DOS MZ serializer reproduces every byte of original Japanese
130,882-byte MAIN.EXE. Other 98 original project objects and CRT reused;
no full cold replay, artificial byte padding or target patching.

Current source-native receipt `.analysis/work/exatt-layout-af771e/report.json`
SHA-256 `03e829d5c6102d4edd5a71fc141d840e644746dd976e713ec68b4ccec3962688`.
Rejected `af771c` source and writer logs remain preserved. These are
improved natural C++ semantics for already source-owned original CODE,
**not** new Factory canonical packed-file accepted credit, historical
vendor raw OMF packet equality or entire product acceptance.

# TH03 MAIN after852: whole Mima Extra Attack native unsigned modulo

The original physical `ex_mima` is a **727-CODE-byte, four-function
Turbo C++ 4.02 source owner**: spawn, per-entity renderer, the long
bounce/fly/collision/acceleration update and multi-entity render loop.
This code uses **six of the sixteen 32-byte entity slots per player**;
current source retains the original shared 16-slot storage carrier and
now asserts the original 32-byte `exatt_entity_t` ABI width at compile
time without allocating or changing object DATA/BSS.

## Native recovery of the originally unsigned parity calculation

The original update copies a 16-bit elapsed duration into a **signed
local `int`**. Its original `duration & 1` acceleration gate nevertheless
uses the *low unsigned word bit*. The maintained natural C++ now states
that precisely as

```
static_cast<unsigned int>(duration) % MIMA_EXATT_HALF_FRAME_COUNT
```

where the period is two. Genuine original TC4 4.02 emits **identical
original machine code**, including the 8-bit `p->speed` compound mutation.
The alternative signed `duration % 2` is *not* original-exact and, for
negative 16-bit duration values, would give the wrong remainder.
The source also names the original 0x1200 random target range, 0x5A
initial speed, 16-unit collision stripe and radius, and the 8-subpixel
collision rebound. The original six independent trajectory slots,
RNG draw count/order and signed re-vectoring are untouched.

Actual original compiler experiments:

- `af852a`: natural **unsigned 16-bit `%2`** passed two actual native
  original TC4/full normal MAIN TLINK rounds.
- `af852b`: dropping the explicit unsigned conversion and using signed
  `%2` failed full CODE equality (**725** initialized bytes vs original
  **727**), so this source form was rejected.
- `af852c`: named target/speed/hitbox/recoil parameters without changing
  the native CODE in either round.
- `af852d`: replacing the original signed unary `-p->velocity_x` with
  `0 - p->velocity_x` also changed original CODE (same 727-byte length).
  Retain original unary negation, not an equivalent-looking rewrite.
- Final `af852e`: restored unary negation, retained real unsigned
  `%2` and added a TC4-compatible compile-time entity-width check;
  two independent full original compiler/linker rounds exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af852e --units ex_mima
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af852e
```

Both original compiler/normal MAIN linker rounds reproduce **all 727
initialized CODE bytes, 44 literal ordered native OMF FIXUPP fields,
4 PUBLIC offsets**, source/segment/ABI, complete original normal MAIN
EXE/MAP, **124,642 loaded Japanese program bytes and all 1,553 ordered
original MZ relocations**. Independent standard MZ serialization also
recreates the original 130,882-byte Japanese MAIN.EXE. The **98 other
project objects and CRT are reused** unchanged; no full cold replay,
patched target bytes or object padding.

Protected original-source-bound report:
`.analysis/work/exatt-layout-af852e/report.json`, SHA-256
`e2b56c67fec5e4a30d7ad2cdb2d660c818d8945c0227636e9dbcb196218a4e0e`.
This is a **new exact current-source native proof for a previously
covered CODE owner**, not new distinct ownership, historical vendor raw
OMF packet identity or canonical packed-game Factory acceptance.

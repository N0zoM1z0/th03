# TH03 MAIN after875 — Chiyuri complete Chargeshot, Gauge and original reset quirk

The complete original **nine-function** `cs_chiyu` Turbo C++ 4.02
physical owner implements eight 6-byte staggered projectiles per player,
original reset/creation, reverse-order staggered motion, sparse sprite
render and multi-continue collision tests, plus the two Gauge bullet/
pellet pattern entrypoints. Its 16 physical projectiles are in the
unchanged original DATA carrier, not newly allocated here.

All five principal loops are now natural typed C++ **`while`**: the
16-iteration original reset, eight-projectile creation, descending
update with a clipped `continue`, descending render and the substantial
hit tester with **five separate `continue` exits**. Each path advances
the original signed index and descending near pointer in the same
order as the original compiler; a hit/early return skips that update.
The exact original age stagger `(i*4)+2`, 0xE0 subpixel flight speed,
-48-pixel clipping threshold, distinct 14/32/-16-pixel hit margins,
32×48 sprite and the original 16-frame Gauge warning clock now have
meaningful C++ constants. The Gauge can use natural `if(!(byte_frame
%16))`, but the different *byte-valued* sprite animation parity must
retain its original `&1`.

## Actual native compiler-positive and negative experiments

- `af875a`: reset, creation and rendering loops converted to `while`;
  the full original object and normal MAIN linked exact twice.
- `af875b`: the staggered eight-projectile update changed to `while`,
  preserving the clipped-entity `continue` index/pointer update;
  native whole-source CODE remains exact twice.
- `af875c`: the collision tester's **five separate early-continue
  paths** now each advance the same original signed index and near
  pointer in a natural `while`; still all original CODE exact in
  two genuine TC4/normal MAIN TLINK rounds.
- `af875d`: tried replacing sprite `anim &1` with natural byte `%2`;
  actual TC4 produced **1,020 CODE bytes**, not original **1,011**.
  The original byte mask remains.
- `af875e`: the separate Gauge `%16==0` condition can use natural
  `if(!(frame %16))` and remains native-exact in both rounds.
- `af875f`: named the actual projectile age, signed flight/clip/hitbox
  and sprite dimensions; full native CODE/FIXUPPs/MAIN remain exact.
- `af875g`: independently challenged the apparently broken reset that
  clears the **first physical projectile's `age` 16 times** rather than
  clearing all sixteen records. Adding `p++` would be a behavioral fix,
  but genuine original TC4 produced **1,014** instead of **1,011**
  CODE bytes (first mismatch CODE segment 4 offset 10). Rejected.
- Final `af875h`: restored exact original reset pointer lifetime and
  tested the complete current maintained C++ in **two genuine original
  TC4 4.02/complete normal MAIN TLINK rounds**.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af875h --units cs_chiyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af875h
```

Both real original compiler/linker rounds reproduce **all 1,011
original CODE bytes, 96 literal ordered native OMF FIXUPP fields and
9 PUBLIC offsets**, original source/segment/data ABI, the complete
normal MAIN EXE and normalized MAP, **all 124,642 Japanese loaded
program bytes and all 1,553 original MZ relocation entries**.
Independent checked standard DOS MZ serialization reproduces the
original 130,882-byte Japanese MAIN.EXE; it does not claim original
vendor TLINK header byte identity. The **other 98 original project
objects and CRT were reused**, no full cold replay, patched target or
OBJ bytes, source substitution or fake NOP padding.

Retained genuine two-round native compiler/source/OBJ/EXE/MAP proof:
`.analysis/work/exatt-layout-af875h/report.json`, SHA-256
`a4f129541e7c08edc2392080fc841000d7cb3ed3a8258bab132caf6578a90481`.
This remains originally source-covered CODE. Native maintained C++ and
fresh semantic negative controls are **not new distinct original game
byte ownership, vendor raw OMF packet identity or canonical Factory
packed-file accepted credit**.

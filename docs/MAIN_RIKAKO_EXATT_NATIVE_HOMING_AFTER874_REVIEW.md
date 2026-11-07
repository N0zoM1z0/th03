# TH03 MAIN after874 — complete Rikako Extra Attack homing and state traversal

The complete original **five-function** `ex_rika` Turbo C++ 4.02
physical source controls eight normal launch slots, fourteen special
Extra Attack slots, its original 48×48 sprite renderer, 14-slot
collision/update/homing state machine and fourteen-slot render traversal.
This is one complete original object, not a fake modern per-function leaf.

All four original entity-loop sites are now **natural C++ `while`**:
normal eight-slot allocation, special fourteen-slot allocation, the
full fourteen-slot sprite dispatcher and the substantial homing/collision
update. The update loop retains **two different early `continue` exits**
for inactive and clipped entities. Each explicitly advances the original
signed 16-bit index and near 32-byte entity pointer before continuing.
The full update's normal path also advances index/pointer *after* the
mutable byte `p->frame++`. This preserves all original register and
side-effect ordering, confirmed by actual original compiler output.

Source names now capture the original 0x1200 random target range,
0x100 initial target Y, 0x64 launch speed, initial angle 0x40,
0x20 speed base, 32-pixel negative clip, 16-pixel hit margin, and the
48×48 sprite with its original 0x780 animation step. The original
character-specific +0x17 **homing-disable byte** remains a per-character
state: only frame values 0x40..0x50 can steer. The homing correction
is the original **signed char** `(target_angle - p->angle) / 8` with
truncation toward zero; it is *not* a signed arithmetic `>>3` on a
negative difference. The original mutable byte speed postincrement
also remains unchanged.

## Original TC4 compiler experiments and actual negative controls

- `af874a`: both eight-/fourteen-slot allocators changed to natural
  `while`, two original TC4/full normal MAIN TLINK rounds passed.
- `af874b`: full fourteen-slot rendering dispatcher also converted
  to `while`, still original CODE/FIXUPP/PUBLIC exact twice.
- `af874c`: large homing/collision updater converted to natural
  `while` **with both original early-continue index/pointer paths**;
  entire original object and normal MAIN linker passed twice.
- `af874d`: independently tested arithmetic `angle_delta >>= 3` in
  place of original signed byte `angle_delta /= 8`. This changed the
  original machine instructions (**699** candidate initialized CODE
  bytes versus **702** original), as well as rounding for negative
  values. Original signed division restored.
- `af874e`: named real target, radius, sprite and speed geometry,
  retaining the original complete native CODE in both rounds.
- `af874f`: changed mutable byte `p->speed++` to prefix. Original
  TC4 emitted **710** instead of **702** initialized CODE bytes;
  original postfix restored without instruction padding.
- Final `af874g`: entire current maintained source and explanatory
  codegen comments compiled twice with original TC4 4.02 and complete
  normal MAIN TLINK, including all source/segment/dependency checks.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af874g --units ex_rika
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af874g
```

Both actual original compiler/full normal TLINK rounds reproduce
**all 702 CODE bytes, 46 literal ordered original OMF FIXUPP fields
and 5 PUBLIC offsets**, original segment/DGROUP/ABI, both complete
normal MAIN EXEs and normalized MAPs, **124,642 Japanese loaded
program bytes and all 1,553 original MZ relocation entries**.
Independent standard DOS MZ serialization matches the pinned 130,882-
byte original Japanese MAIN.EXE. **98 other original game objects and
CRT reused**, without whole cold replay, patched object or target bytes,
source substitution, or fake NOPs.

Protected real native original compiler/OBJ/EXE/MAP evidence:
`.analysis/work/exatt-layout-af874g/report.json` SHA-256
`6a6ead73ae1112c3ed77df724ce491cff319a4469bb57162bb3233b153f08908`.
This is **improved current source** for original CODE already historically
covered, **not new unique target CODE byte credit, raw historical vendor
OMF packet identity or canonical Factory packed-file acceptance**.

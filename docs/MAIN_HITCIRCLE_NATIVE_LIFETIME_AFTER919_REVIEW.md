# TH03 MAIN after919 — complete original HitCircle age, collision and rendering leaf

The complete original four-function physical `hitcirc` Turbo C++ 4.02
source owns the twelve-enemy plus one-player HitCircle visualization,
enemy/player spawn coordinate transformation and original byte animation
cel, along with the real PC-98 monochrome sprite renderer. The original
shared HitCircle DATA/BSS and eight-pixel-byte VRAM address ABI remain
externally owned, not reallocated.

The complete **thirteen-slot HitCircle lifetime updater** and separate
**twelve-enemy HitCircle renderer** now use natural signed-index C++
`while`. Both advance their real near record pointer and signed index
after each original state or sprite operation; the thirteenth *player*
HitCircle continues to draw separately with white coloring. All three
original byte `age` activation predicates are now explicit `age !=0`.
The byte expiry threshold can naturally be written
`HITCIRCLE_FRAMES < p->age` without changing the historical TC4 CODE.
Original byte age and enemy-ring index postincrements remain in their
original forms, and so does the four-byte `AND DX,imm16` GRCG palette
bit test: C++ `_DX &= 1` produces a different shorter immediate.

Actual independent original compiler trials:

- `af919a`: whole 13-record lifetime `for` and 12-enemy renderer `for`
  changed to natural `while`, source and normal MAIN exact twice.
- `af919b`: all three separate byte age activity checks explicitly
  became `p->age != 0`, whole original object exact twice.
- `af919c`: original byte `last_id++` to prefix generated **449** vs
  original **445 CODE bytes**, first mismatch segment 1 offset 8;
  restored byte postfix.
- `af919d`: byte `p->age++` to prefix generated **449** vs original
  **445 CODE**, first mismatch segment 1 offset 179; restored postfix.
- `af919e`: reversed original age `age > LIMIT` into natural
  `LIMIT < age` *did* preserve original CODE and full normal MAIN.
- `af919f`: challenged original explicit `asm { and dx, 1 }` with
  C++ `_DX &=1`; TC4 emitted **444** vs original **445 CODE**
  (first mismatch at segment 1 offset 229). Restored authentic
  four-byte immediate hardware instruction; no manual NOP padding.
- Final `af919g`: complete maintained source and PC-98 register-aware
  comments recompiled in two independent original TC4 4.02/full
  normal MAIN TLINK rounds, exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af919g --units hitcirc
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af919g
```

Both independent original compiler/normal full linker rounds reproduce
**445 original CODE bytes, 30 literal ordered native OMF FIXUPP fields,
four PUBLIC offsets**, original segment/source/16-bit ABI, zero new
private DATA/BSS, normal MAIN EXE and MAP, **124,642 Japanese loaded
program bytes and all 1,553 MZ relocations**. Independent standard
DOS MZ serialization reproduces all **130,882 original Japanese
MAIN.EXE bytes**, not historical vendor header-writer identity.
**98 other original game project objects and CRT reused**, no full
cold replay, target/OBJ patches, NOPs or fabricated machine-code arrays.

Protected current-source-bound genuine compiler/TLINK receipt:
`.analysis/work/exatt-layout-af919g/report.json`, SHA-256
`f8f48e7f09fc35c2d41fda405193ab3e73ed965b6176309139b30ca74b39474b`.
This already had historical source coverage; improved native C++ is
**not new distinct original game CODE, raw vendor packet identity or
canonical Factory packed-game acceptance**.

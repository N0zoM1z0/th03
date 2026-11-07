# MAIN bullet update and GRCG renderer: compiler-owned register C++, after607

The maintained original `src/main/bullet/bullet.cpp` contains the large bullet
simulation/update, trails and the real 386 GRCG renderer. This is a **full
physical compiler producer**, not a source fragment. Three explicit inline
assembly instructions are now naturally written through Turbo C++'s existing
16-bit register interface:

- `grcg_pellet_put()` computes the doubled VRAM word displacement with
  `_AX <<= 1` rather than hand-authoring `shl ax, 1`. The signed destination
  check and 386 `MOVSD`/narrow `MOVSW` register requirements are untouched.
- `bullets_update()` initializes the trail-coordinate pointer register with
  `_BX = 0`, rather than a manual `xor bx, bx`. The original trail
  clipping, carry-flag and transfer branches are unchanged.
- `bullets_render()` initializes the GRCG pellet color register using
  `_DX = 0`, rather than a manual `xor dx, dx`. The high byte still
  distinguishes a transfer pellet. The hardware `out` instructions and
  register/flag-specific assembly remain where they are actually required.

All changes were tested using **real native Turbo C++ 4.02 and original TLINK**
against the immutable Japanese target, one affected physical object at a
time. The independent `af607b` (DX), `af607c` (BX) and `af607d`
(AX shift) experiments each yielded complete original CODE/FIXUPP/public
equality, not just successful compilation. A final `af607g` proof
recompiled the entire current Bullet TU in two independent rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af607g --units bullet
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af607g

**Full original result:** 2,685 CODE bytes (2,602 in BULLET_TEXT,
83 in PELLET_PUT), 196 ordered native fields, 20 PUBLIC offsets,
all original segment metadata, and the existing 9,500-byte Bullet BSS
layout. Both rounds reproduce the selected normal MAIN EXE and the
complete normalized MAP, the original 124,642-byte Japanese program
image and all 1,553 ordered MZ relocations; the separately reviewed
standard MZ format produces the exact 130,882-byte Japanese MAIN.EXE.

Evidence: `.analysis/work/exatt-layout-af607g/report.json`,
SHA-256 `3ba1f51565200bc64b47a9abbc4d629ac25b3dd7f9389bbd58878746fba577e5`.
The overlay retains the real two-round compiler/linker logs, source/header
snapshots and all raw OBJ, EXE and MAP outputs. Original objects and
historical after596 source-bound receipts were not rewritten.

The overlay/reviewer now also understand actual Fireball, Explosion and
four Enemy physical slots. Segment-aware accounting separates initialized
CODE and DATA bytes (the Fireball source owns one DATA byte) and BSS instead
of erroneously calling all initialized bytes CODE. Their source-control
experiments are independent of the accepted Bullet checkpoint.

These 2,685 bytes were already source-owned. This advances **natural
maintainable C/C++ and original native reproducibility**, not canonical
packed-file Factory acceptance or historical raw vendor OMF packet identity.

# TH03 MAIN Chiyuri: complete BOSS update, attack cadence and sprite geometry after742

This pass actually changes the complete maintained `src/main/boss/chiyuri.cpp`
original physical 16-bit Turbo C++ owner `ba_chiyu`. The object contains
eleven original PUBLIC functions and 2,654 initialized CODE bytes:
cardinal/ring/trailing/fan projectile controllers, the whole BOSS
update/collision dispatcher, ring/intro/palette render paths and template
initialization. It was never tested as a cherry-picked leaf.

## Accepted natural C++ source reconstruction

The eight-frame trailing-ring bomb warning, four-frame BOSS render tick
and its mutable 0..3 render-frame ring now use explicit named power-of-two
periods and the exact integer bit-mask operations. The original inclusive
frame gates, palette calls, random draw order, original mutable byte
postdecrements and the full boss hitbox updates were preserved.

The sixteen-sprite orbit renderer's `boss_effect_radius * 16` is now an
explicit signed 16-bit `<< 4` operation, and the sprite-sheet offset's
render-frame `* 4` is `<< 2`. All **three different signed entrance
radius** phases now use a natural signed `frame << 3`, with their separate
0x100/0x200/0x300 bases and original AL-mediated byte direction writes
intact. The sprite ring loop uses a named original sixteen-sprite bound.

## Tested codegen boundaries, not assumptions

- `af742a`: a first broad trial included replacing the unsigned byte
  `chiyuri_ring_speed / 4` with `>> 2`. It *failed* CODE equality (a
  four-byte overall size difference, including other edits), so the
  entire batch was not accepted.
- `af742b`: restored sensitive speed division and entrance radius scale;
  the unchanged-impact render mask and sprite offset shift passed both
  genuine TC4 compiler rounds.
- `af742c`: isolated `chiyuri_ring_speed >> 2` again. It **failed**,
  proving that apparently equivalent unsigned-byte shift changes the
  historical compiler codegen. The original integer division remains.
- `af742d`: one entrance signed `frame * 8` changed to `frame << 3` and
  passed. `af742e`: *all three* entrance shifts and the 16-bit orbit
  radius shift also passed independently.
- `af742f`: final maintained product source with cleaned constants,
  comments and original unsigned-byte speed division passed both
  independent TC4/TLINK rounds. Failed trials remain in protected ignored
  native writer trees and are **not** counted as source-exact.

Reproduce the affected-only genuine original Turbo C++ 4.02/TLINK proof
using a new unused DOS-safe stage name, never overwrite `af742f`:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af742f --units ba_chiyu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af742f

Both rounds exactly reproduce **2,654 original CODE bytes**, all **381
literal ordered OMF FIXUPP fields**, **11 PUBLIC offsets**, original
segments/DATA/BSS declarations and compiler-emitted source dependencies.
The full 99-object original normal MAIN EXE/normalized MAP, 124,642-byte
Japanese loaded program, all 1,553 ordered MZ relocations, and independently
serialized complete 130,882-byte Japanese MAIN.EXE matched. Other 98
original project objects and CRT were **reused**, not cold-rebuilt.

Primary original-source proof:
`.analysis/work/exatt-layout-af742f/report.json` SHA-256
`44b339f2efe27539e7a600534c163a279de5034476cc71661efc9b55f4ef1837`.
This records current-source natural C++ recovery for **already existing
owned bytes**, not new canonical Factory packed-game acceptance or
historic vendor raw-OMF packet identity. Whole-project source ownership
remains open.

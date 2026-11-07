# TH03 MAIN Yumemi major BOSS: native two-stage intro geometry and hardware overlap after780

The complete original 16-bit Turbo C++ `ba_yumem` source has **ten
original functions** and its full physical OMF owns **2,358 initialized
CODE bytes, 343 literal ordered native FIXUPP fields and 10 PUBLICs**.
It includes the long ring/aimed/cross/chase/rain attack patterns,
whole BOSS update/collision, main GRCG rendering, the extensive four-
phase 112-pixel entrance sprite rasterizer and the render dispatcher.
This source was rebuilt as one whole physical owner, not a tiny leaf.

## Actual natural C++ rendering recovery

The original four independent entrance-phase x-coordinate formulas
performed two separate 16-bit multiplications `(frame * 8) * 16`, with
the frame base reset at 0x18/0x30/0x48 and the final gate at 0x60.
We now express the original two-stage arithmetic as **two natural C++
shifts**, `((frame << 3) << 4)` (or `phase` for the three later phases).
The four phase boundaries, signed frame shift magnitudes and the two
separate per-stage multiplications are now named compile-time enums.
The original four horizontal sprite loops with 8-pixel movement, near
`register` left/right coordinate lifetimes, their separate sprite
ranges and overlap start/clear interrupts remain intact. Original
BOSS attack selection, bullet RNG, collision, `boss_frame`, state/clip
and draw ordering remain unchanged.

## Native experiments: two shifts are essential; hardware XOR remains

- `af780a` proved **all four separate two-level C++ shifts** exact in
  original Turbo C++ 4.02 as the complete BOSS object, both full normal
  MAIN links and all OMF fields.
- `af780b` combined the two shifts into one mathematically equivalent
  `<< 7`; actual original CODE changed. The historical two-stage
  calculation is a compiler-visible property, not merely final pixels.
- `af780c` attempted to replace the original overlap setup
  `asm { xor dx, dx }` with C++ `_DX ^= _DX`. This generated different
  historical DX operand encoding, so the original explicit hardware
  instruction remains. No fake instruction bytes were added.
- `af780d` restored both native-exact two-stage shifts and original
  hardware XOR, named all four intro phases, and matched the complete
  original BOSS/full MAIN link in both genuine TC4 rounds.
- `af780e` recompiled the final maintained source after clarifying the
  codegen-sensitive comment. Both original native rounds remained exact.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af780e --units ba_yumem
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af780e

Both rounds reproduce **all 2,358 original CODE bytes, all 343 ordered
literal OMF FIXUPPs, all 10 PUBLIC offsets**, original segment and
native source COMENT dependencies, complete normal MAIN EXE/normalized
MAP, Japanese **124,642-byte loaded program and all 1,553 ordered
MZ relocations**. Independent standard MZ serialization reproduces
all **130,882 bytes of original Japanese MAIN.EXE**. The remaining
98 original game objects and Borland CRT were reused; no full cold
replay, artificial padding or binary-byte patches were used.

Proof: `.analysis/work/exatt-layout-af780e/report.json`, SHA-256
`0fd64326d4aba8b8c0f5a39da1b74b0e89c8d90bb80c675562bd4f7696cebc7c`.
The failed original compiler stages remain separate protected negative
evidence. This is improved natural C++ for **already source-owned
original bytes**, not new canonical Factory packed-unit acceptance,
historical vendor raw OMF identity or complete game source ownership.

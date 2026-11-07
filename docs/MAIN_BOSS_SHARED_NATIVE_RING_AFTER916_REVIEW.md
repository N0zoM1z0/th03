# TH03 MAIN after916 — complete shared BOSS ring and central lifecycle owners

The current `src/main/boss/shared.cpp` is compiled as **two distinct
historical original physical Turbo C++ 4.02 project objects**:
`ba_sring` contains the complete ring and score-reward provider;
`ba_srest` contains the other seven central near/far BOSS providers,
including sine movement, descent, 32-byte state transfer, hit/death,
target updates, and random attack-pattern selection. Both objects keep
their original OMF source/header dependencies, near-pascal calling
conventions, DS:SI/ES:DI `rep movsw` state-copy effects and external
storage. This is not a standalone ring-only reimplementation.

The entire **sixteen-sprite primary explosion ring** and the separate
**eight-sprite secondary ring** now use natural typed `while`, with the
same original polar/sprite calls, original signed index and byte-angle
increments **after** each draw. The central BOSS controller's
RNG-rejection loop now uses natural `while(1)`, preserving exactly one
random word for every rejected recent pattern and its two-sided
window. Both angle steps (+0x10 and +0x20), 48×48 sprite dimensions
and 24-pixel placement margin are now named physical constants.

## Real original native compiler experiments, including negatives

- `af916a`: both full real ring loops naturally changed to `while`,
  while compiling **both physical project owners together** and
  linking the complete original MAIN twice: byte-exact.
- `af916b`: original BOSS random-pattern `for(;;)` became natural
  `while(1)` with genuine original TC4/TLINK byte equality twice.
- `af916c`: both original sprite angle steps and sprite dimensions
  became named source enum values, preserving all original bytes.
- `af916d`: original signed byte secondary angle `0 - (unsigned char)
  length` could **not** become unary `-static_cast<unsigned char>(length)`;
  original `ba_sring` CODE changed at segment 5 offset 206. Reverted.
- `af916e`: changing original mutable byte `boss_angle++` to prefix
  generated **602** CODE bytes for `ba_srest` vs original **601**.
  Postfix retained.
- `af916f`: changing `boss_pattern_i++` to prefix also generated
  **602** vs **601** `ba_srest` CODE bytes. Postfix retained.
- `af916g`: replacing signed word `length *= 8` with explicit
  `length = length * 8` changed `ba_sring` CODE at segment 5 offset
  53 despite identical initialized length. Original compound multiplication
  and old 16-bit register selection retained.
- Final `af916h`: both complete original physical owners, current
  source comments and original codegen forms recompiled in **two
  independent genuine TC4 4.02 and complete normal MAIN TLINK rounds**.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af916h --units ba_sring,ba_srest
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af916h
```

| Original physical TU | CODE bytes | Ordered native OMF FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_sring` | 348 | 22 | 1 |
| `ba_srest` | 601 | 84 | 7 |
| **Both current physical owners in each original native round** | **949** | **106** | **8** |

Both genuine original compiler/full normal linker rounds reproduce
all original CODE/FIXUPPs/PUBLICs and segment/source ABI, the complete
normal MAIN EXE and normalized MAP, **124,642 Japanese loaded program
bytes and all 1,553 ordered original MZ relocations**. Independent
standard DOS MZ serialization reproduces **130,882 original Japanese
MAIN.EXE bytes**, without establishing historical vendor direct header
byte serialization. **97 other original game objects and CRT reused**,
no full cold replay, original object/target byte patches, synthetic
machine-code arrays or NOP padding.

Protected current-source-bound native TC4/TLINK receipt:
`.analysis/work/exatt-layout-af916h/report.json`, SHA-256
`a6f04c070e9469c09dcc8b2b652db26d745fa049a161bdae3bcae353238e279d`.
This was historically source-backed original CODE. This improvement is
**not newly distinct original CODE ownership, vendor packet-identical
raw OMF or canonical Factory packed-game accepted credit**.

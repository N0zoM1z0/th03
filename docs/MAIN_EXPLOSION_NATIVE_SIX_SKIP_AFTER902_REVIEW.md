# TH03 MAIN after902 — complete explosion-chain hit testing with six native skip paths

The complete original physical `e_expl` Turbo C++ 4.02 project unit
owns the real **630-CODE-byte far-`__cdecl`**
`explosions_hittest()` engine, not a standalone modern collision mock.
It iterates the original combined Enemy/Fireball EFE carrier, accumulates
hits for enemy, pellet and red/blue fireball variants, drives explosion
chains, score, Gauge charge, charged fireballs, Extra Attacks and BOSS
panic side effects. The original shared state and collision coordinates
remain in separate historical physical owners.

## Natural C++ and real historical collision semantics

The entire original **EFE_COUNT entry** collision/chain scan now uses a
natural typed C++ `while`. All **six independent `continue` paths**
originally controlled by the `for` iterator now explicitly advance the
signed 16-bit index and original near entity pointer before continuing:
non-exploding entry, exhausted enemy explosion, wrong player,
byte-animation off-frame, separated top-left bound and separated
bottom-right bound. The successful-hit path also advances both registers
after the original score/Gauge/BOSS/fireball side effects. This is
verified by real machine-code equality of the *complete original 630
CODE bytes*, not solely by behavioral plausibility.

The original byte `frame &3` remains a real bit test, **not** a byte
`frame %4`, and the chain-hit counter retains the strict **`hits <255`
uint8 saturation** rather than `hits !=255`. The exploding enemy's
`expl_p->flag++` and chain scores remain original byte/memory updates,
not compiler-unequal prefix or pure abstract C++ refactors. The
original signed `bonus += bonus` is intentionally not converted to
`bonus <<=1`; old compiler evidence for that difference remains relevant.

## Genuine original TC4 compiler experiments

- `af902a`: changed the *entire large original collision-and-chain*
  loop with all six early-continue paths to natural `while`;
  both original Turbo C++ 4.02 and complete normal MAIN TLINK
  rounds matched original CODE/FIXUPPs/PUBLIC/EXE and MZ.
- `af902b`: re-challenged original strict uint8 saturation `hits <255`
  using logical `hits !=255`. Original TC4 produced **different CODE
  at segment 1 offset 239** despite still generating 630 initialized
  bytes; restored `<` to preserve target.
- `af902c`: re-challenged byte `frame &3` as natural `%4`. Native TC4
  generated **639** candidate CODE bytes versus **630** original,
  first difference at CODE segment 1 offset 49; restored the original
  bit mask.
- `af902d`: changed byte entity explosion flag postincrement to prefix.
  Native original CODE became **634** rather than **630** bytes,
  first difference at segment 1 offset 49; postfix restored.
- Final `af902e`: current entire original collision engine with
  explicit original pointer/index skipping and explanatory comments
  reproduced exact original machine code in two independent genuine
  TC4 4.02/complete normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af902e --units e_expl
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af902e
```

Both real original native compiler/full normal linker rounds reproduce
**all 630 CODE bytes, 49 literal ordered native OMF FIXUPP fields and
one PUBLIC offset**, source/segment/16-bit near/far ABI, complete
normal original MAIN EXE and normalized MAP, **124,642 Japanese loaded
program bytes and all 1,553 original MZ relocations**. Independent
standard DOS MZ serialization matches all **130,882 original Japanese
MAIN.EXE bytes**, not historical vendor header-byte serialization.
**98 other original game project objects and CRT reused**, without
full-project cold replay, synthetic machine-code buffers, target/OBJ
patches or fake NOP padding.

Protected actual source-bound two-round original TC4/TLINK receipt:
`.analysis/work/exatt-layout-af902e/report.json`, SHA-256
`eb467b182177ec06e44b332d9c5bfe68f4f010dae02a9a4ece0f330bdc791364`.
These original game bytes were already historically source-owned.
This improves exact maintainable C++ and native collision fidelity,
**not additional distinct CODE or canonical Factory packed-file credit**.

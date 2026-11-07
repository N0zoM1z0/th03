# TH03 MAIN after879 — complete Chain 2 particle initialization and state cutover

The original three-function `chain2` physical Turbo C++ 4.02 source
owns the 50-particle initializer and the complete hardware-specific
accelerate and periodic background controllers in `PLAYER_M_TEXT`.
Its first 40 of 50 physical 16-byte particles get different sprite
and RNG behavior from the final ten. No DATA/BSS pool is reallocated;
all native ES:DI graphics loops and shared `phase.inl` are retained
with the original register-interface constraints.

The full 50-slot initializer now uses a natural C++ typed `while` with
the original signed index/near-pointer order, exact two RNG coordinate
draws per particle and the original 40/10 conditional sprite stores.
Named original values distinguish the 0x233E randomized sprites from
the 0x20BE final sprites, and the 32-bit acceleration transition now
uses `round_frame > static_cast<unsigned long>(ACCELERATION_LAST_FRAME)`
with the original 144-frame value. This maintains the original PC-98
render/acceleration clock width and complete source-native CODE.

Actual original compiler experiments:
- `af879a`: 50-slot `for` -> `while` passed genuine original TC4 4.02
  and complete normal MAIN TLINK in both independent rounds.
- `af879b`: named sprite family values and explicitly unsigned long
  144-frame threshold; the entire original owner remained exact twice.
- `af879c`: replacing the original two separate sprite-store branches
  by a C++ ternary emitted **549** CODE bytes, not the original **550**
  (first difference CODE segment 4, offset 16). Rejected.
- `af879d`: changing original 32-bit `>144UL` to numerical-equivalent
  `>=145UL` changed original CODE at segment 4 offset 246 even though
  initialized length stayed 550. Original comparison restored.
- Final `af879e`: current maintained C++ and source explanations
  recompiled in both genuine original TC4/full normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af879e --units chain2
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af879e
```

Both genuine original native rounds match **550 original CODE bytes,
43 literal ordered native OMF FIXUPP fields and 3 PUBLIC offsets**,
original segment/ABI and source-header dependencies, complete normal
MAIN EXE/MAP, **124,642 Japanese loaded program bytes and 1,553
original ordered MZ relocations**. Independent standard DOS MZ
serialization reproduces the **130,882-byte original Japanese MAIN.EXE**.
The other **98 original project objects and CRT are reused**, no cold
replay, object/target byte patch, NOP padding or false ASM replacement.
Protected source-bound two-round original compiler/TLINK evidence:
`.analysis/work/exatt-layout-af879e/report.json`, SHA-256
`c26edc025b892aab2d4d85c84adbf80c4e91fd7de9774ad34de6c3df3a82b340`.
All original CODE bytes were historically source-backed. This is
maintained exact C++ improvement, not new distinct original CODE,
vendor raw packet-identical OMF or canonical Factory packed-file credit.

# TH03 MAIN after917 — complete CPU dodge, collision search and retry AI

The complete original physical `p_cpu` Turbo C++ 4.02 source owns four
near-pascal CPU controller functions: the original 3×3 dodge direction
lookup, player-target steering and RNG consumption, the complete
collision-avoidance/aim AI and the central frame-threshold dispatcher.
This is not a small stand-alone math helper: it retains original
player/hitbox/target state, 16-bit signed coordinates, byte dodge strategy,
unbounded retry logic and all observable original RNG draws.

The substantial nine-direction collision retry now uses ordinary C++
`while(1)` instead of `for(;;)`, preserving the exact player-movement,
near collision call, RNG fallback and BOMB-vs-hit branch order. The
original signed-byte collision-radius sweep (four radii, stopping at the
first hit) now naturally uses `while`, moving the +16 radius step
*after* its `player_hittest()` and before the next iteration. Thus a
successful early `break` does not advance the mutable local. The
unsigned-word four-frame collision scan can naturally use
`if(!(round_or_result_frame % CPU_COLLISION_SCAN_PERIOD))`. The retry
exit predicate accepts readable `if(player->is_hit == false)` with exact
original instructions. No CPU input flag, collision call or RNG draw
has been removed or reordered.

Genuine original Turbo C++ 4.02 experiments:

- `af917a`: full unbounded BOSS-independent CPU dodge/retry `for(;;)`
  -> natural `while(1)`, entire original `p_cpu` and complete normal
  MAIN exact in both independent compiler/linker rounds.
- `af917b`: signed-byte 32/48/64/80 collision-radius test loop to
  natural `while`, original machine code and complete normal MAIN exact.
- `af917c`: tested both a natural 16-bit zero remainder and reversing
  `cpu_frame <= cpu_safety_frames`. Combined changed original CODE at
  segment 4 offset 483 despite the same initialized byte length.
- `af917d`: restored original CPU-safety-frame comparison, leaving
  natural `if(!remainder)` alone. The full object then matched original
  CODE twice. Therefore the reversed safety comparison, not the
  remainder spelling, caused the prior difference.
- `af917e`: natural explicit `player->is_hit == false` retry exit
  matched all original TC4 CODE and normal MAIN in both rounds.
- `af917f`: changing both mutable byte `attempt++` operations to prefix
  generated **1,087** CODE bytes vs original **1,077**, first
  difference at segment 4 offset 336. Original postfix restored.
- Final `af917g`: all maintained source and compiler-specific comments
  passed two genuine independent original TC4/full normal MAIN TLINK
  rounds, exact source/physical object/whole program.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af917g --units p_cpu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af917g
```

Both real original compiler/full normal linker rounds reproduce
**all 1,077 original CODE bytes, 64 literal ordered OMF FIXUPP fields,
four PUBLIC offsets**, original source/segment/16-bit ABI, complete
normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes and all
1,553 ordered MZ relocations**. Independently checked standard DOS MZ
serialization reproduces all **130,882 bytes** of pinned Japanese
MAIN.EXE, without proving vendor header-byte serialization identity.
The **98 other original game project objects and CRT reused**, no
full cold replay, patched target/OBJ, artificial machine-code arrays
or NOP padding.

Protected current-source-bound original TC4/normal TLINK receipt:
`.analysis/work/exatt-layout-af917g/report.json`, SHA-256
`1c5e36a211373af63b3fbfededa27a6300ab6a8e846129b890dc5761aa78753e`.
These original CODE bytes were historically source-backed; this is
native C++ maintenance progress, not new distinct original byte
ownership or canonical Factory packed-game acceptance.

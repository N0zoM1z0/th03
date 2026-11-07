# TH03 MAIN: original-native complete Fireball creation, transfer and render — after743

This is an actual natural C++ change to `src/main/enemy/fireball.cpp`, not
an isolated invented leaf. The one physical original `e_fireb` Turbo C++
source owns 10 PUBLICs and its complete `E_FIREB_TEXT` CODE segment:
fireball spawning, sprite drawing, explosion phase updates, transfer to
the opposite playfield, collision/chain testing and the combined render
pass. The original also owns **one initialized DATA byte and one BSS byte**;
these initialized and uninitialized segment declarations are checked
alongside all **1,555 CODE bytes and 115 ordered OMF fixup fields**.

The newly recovered natural C++ explicitly expresses the original global
512-frame target selection in two 256-frame halves using unsigned 16-bit
bit-mask arithmetic, and the 8-frame sprite cycle as an unsigned-byte
mask. The four spawn/update/hittest/render **signed loop index** counters
use natural prefix `++i` or `--i`. Their pointer mutations intentionally
remain postfix, preserving the original OMF CODE and ZUN's original pool
traversal order. The transfer branch now uses natural `if(!p->pid)` for
the original two-player direction decision, with its precise opposite-X
comparison and shared `switch_to_fall` label kept intact. No original
uninitialized chain-slot bug or fireball/transfer behavior was fixed.

## Actual TC4 negative/positive source experiments

- `af743a` tried both natural masks and loop changes **plus** converting
  the explosion frame's `p->frame / 4` to `>> 2`. The initial native
  candidate was 3 bytes smaller (original CODE 1,555; candidate 1,552),
  so it did **not** match.
- `af743b` restored only the frame division, keeping the 512/8-frame
  masks and natural loops; both native compiler/linker rounds matched
  the complete object including its original initialized DATA.
- `af743c` additionally replaced the transfer PID `== 0` with `!pid`,
  which also reproduced the exact original code.
- `af743d` removed unused exploratory constants, clarified the source
  formatting and recorded the reason for preserving signed-byte
  `frame / 4`. Both fresh, genuinely compiled original TC4 rounds passed.
  Rejected trials were retained in their own ignored native proof trees.

Original native compiler source-bound scope (use a **new** stage if
recompiling; don't overwrite the retained writer receipt):

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af743d --units e_fireb
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af743d

Both rounds match all original **1,555 initialized CODE bytes, 1
initialized DATA byte, BSS, 115 ordered literal OMF relocation fields,
10 PUBLIC offsets and all segment metadata**, original normal full
MAIN EXE/normalized MAP, Japanese 124,642-byte loaded program and all
1,553 ordered MZ relocations. Independent standard MZ serialization
reproduces the original Japanese 130,882-byte MAIN.EXE. The 98 other
original project objects and original CRT were **reused, not cold
replayed**. No binary patch, target substitution or synthetic CODE.

Current-source proof `.analysis/work/exatt-layout-af743d/report.json`,
SHA-256 `28f83e24079720ef5ff9e7d1bd4246812e9461057d675ce443d5ba5853af9713`.
All original and compiled source dependencies, two real compiler/linker
OBJ/EXE/MAP rounds and writer logs are retained. This is recoverable
current-source codegen progress for already owned game bytes, not new
canonical Factory packed-file accepted credit, historic vendor raw OMF
packet identity or completed full-game source ownership.

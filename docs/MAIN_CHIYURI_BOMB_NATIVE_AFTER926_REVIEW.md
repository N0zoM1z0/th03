# TH03 MAIN after926 — complete Chiyuri Bomb original palette and axis effect

The real original physical `b_chiyu` Turbo C++ 4.02 project unit owns
one complete 490-CODE-byte Bomb state machine. The first 64 byte frames
handle palette and center warning, frames 64..143 handle GRCG shake,
16-frame four-axis explosion rings, and 8-bit sprite/resource calls;
the final branch fades color. Original `BX`/`AX` hardware carriers,
real palettes, MRS sprite call and four original far-Pascal effect
calls remain, not isolated or rewritten as a modern effect stub.

Both natural zero-remainder cadence guards `if(!(frame % 8))` and
`if(!(frame % 16))` are original-code exact. The original player index
branches can read naturally `if(pid_current)`. Phase cutoffs (64/144),
8/16 frame periods and original subpixel (144,184) center are now
source-named constants allocating no additional data. The original
signed intermediate geometry stays a **two-stage multiplication by 2
then 16** before emitting the four original signed-axis warning centers.

Genuine original TC4 compiler trials:

- `af926a`: both byte-frame `%8==0` / `%16==0` tests became natural
  `if(!remainder)`, whole original CODE and normal MAIN exact twice.
- `af926b`: both player byte `pid_current !=0` checks became
  `if(pid_current)` without changing any native instruction.
- `af926c`: byte shake `(frame &3)<2` changed to `%4`, producing
  **493 CODE bytes** vs original **490** (first mismatch CODE segment
  4 offset 19). Original `&3` restored, without padding.
- `af926d`: named original effect centers and phase cutoffs,
  complete TC4/TLINK native original exact twice.
- `af926e`: condensed original `((frame-64)*2)*16` to a single `*32`;
  genuine TC4 emitted **488 CODE bytes** vs **490**. The original
  two-stage signed arithmetic was restored.
- `af926f`: source-named `frame - CHIYURI_BOMB_PALETTE_END` within the
  original two multiplications remained byte-exact.
- `af926g`: natural inactive Bomb test `if(!bomb_flag[pid])` remained
  original native exact.
- Final `af926h`: all current source and codegen notes passed two
  independent original TC4 4.02 and complete normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af926h --units b_chiyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af926h
```

Both independent original native compiler/linker rounds match **490
CODE bytes, 48 literal ordered OMF FIXUPP entries, one PUBLIC offset**,
source/segment/16-bit ABI, complete normal MAIN EXE/MAP, **124,642
Japanese loaded bytes and 1,553 ordered MZ relocations**. Independent
standard DOS MZ serialization reconstructs all 130,882 pinned Japanese
MAIN.EXE bytes, not historical vendor header-writing identity.
**98 other original game objects and CRT reused**, no cold replay,
object patch, fabricated machine-code bytes or NOP padding.

Protected genuine current-source-bound original writer receipt:
`.analysis/work/exatt-layout-af926h/report.json` SHA-256
`006731a6ced83bbd6f0636f1161283b86ee44852df04ab6bdad85c9d85c9de5f`.
Already source-covered CODE; no new distinct game bytes or canonical
Factory packed-game acceptance credit.

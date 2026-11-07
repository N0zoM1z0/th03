# TH03 MAIN after890 — four complete original Enemy physical sources, natural control loops

This session changed the **actual 1,056-line maintained original Enemy C++
engine**. Its shared source is compiled into **four separate real historical
Turbo C++ 4.02 physical objects**, not a fictitious merged TU:

| Original owner | Entire compiled scope | CODE | Ordered OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `eforna` | All formation/script loaders, RNG and near spawn/move providers | 729 | 58 | 8 |
| `efornb` | Full ~867-byte ENEDAT script VM, velocity/angle and chain helpers | 1,064 | 37 | 4 |
| `eupda` | Original enemy sprite/explosion/update providers | 372 | 24 | 3 |
| `eupdb` | Full explosion-chain hit/scoring, forty-entity render and update | 1,160 | 103 | 4 |
| **Four complete original objects compiled simultaneously** | | **3,325** | **222** | **19** |

The 40-entity **reverse collision scanner**, whole enemy **renderer**
with early queued/free-entity skip, and large **update/script dispatch**
with two independent early-`continue` paths now use natural C++ `while`.
Each loop reproduces the original order of signed index, original near
pointer, compiler-sensitive near-script/hitbox/collmap calls and the
collision system’s last-frame chain side effects.

The **formation spawning** loop now uses `while` with both the original
mutable byte formation index and signed script index updated *after*
`enemies_add`. The ENEDAT loader’s inner enemy script-size loop and the
entire **256-formation randomization** also use `while`, without changing
script stream offsets, the original unbounded sentinel parsing or any RNG
draw. The original **uninitialized `prev` byte** remains uninitialized:
its stack value materially affects the first formation roll in the target.
The substantial ENEDAT VM interpreter's existing `for(;;)` is now natural
`while(true)`, without repairing the original broken loop opcodes or
altering its segmented ES script cursor.

## Genuine native compiler trial sequence

- `af890a`: 40-slot reverse hit test and complete enemy sprite dispatcher
  converted to `while`, including original `continue`; all four original
  project objects and full normal MAIN exact in two native rounds.
- `af890b`: complete 40-slot update with both original `continue` paths
  converted to `while`; both original compiler/linker rounds byte-exact.
- `af890c`: tried applying the same natural `while` to first-free-slot
  `enemies_add`. The genuine original compiler **rejected** it: original
  `eforna` 729 CODE bytes became 731 (first difference CODE segment 7,
  offset 10). Its original `for/continue/break` shape is retained.
- `af890d`: formation-spawning index and signed script cursor updated
  through natural `while` and the real same-segment `enemies_add` call;
  all four physical owners matched in both genuine rounds.
- `af890e`: ENEDAT loader’s full per-formation script-size/offset loop
  changed to natural `while`, still all four owners original-exact.
- `af890f`: complete 256-RNG-draw-formation loop changed to `while`,
  while preserving its original `do/while` retry and uninitialized `prev`.
- `af890g`: large segmented-ES original ENEDAT opcode interpreter now
  naturally uses `while(true)`, all four objects exact in both rounds.
- Final `af890h`: full current maintained source plus comments recompiled
  together as four actual physical objects, original TC4/normal TLINK
  **two independent rounds** again byte-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af890h --units eforna,efornb,eupda,eupdb
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af890h
```

Both independent real original TC4 4.02 and normal full MAIN TLINK
rounds reproduced all **3,325 original CODE bytes, 222 literal ordered
native FIXUPP fields and 19 PUBLICs**, original source/segments/
segmented ABI, complete normal original MAIN EXE/MAP, **all 124,642
Japanese loaded program bytes and 1,553 original MZ relocations**.
Independent checked standard DOS MZ serialization reproduced the
original **130,882-byte Japanese MAIN.EXE**. The **other 95 original
game project objects and CRT were reused**, no full cold replay,
synthetic machine-code buffer, NOP padding or modified target bytes.

Protected actual original compiler/TLINK source-bound proof:
`.analysis/work/exatt-layout-af890h/report.json`, SHA-256
`928bd9612b73a5a646807b6e7c9a192e55fc44bcaefb0ad0e2a7ff251025544b`.
These original physical owners already had historical source coverage.
This is improved current maintainable C++/compiler provenance, **not
3,325 new unique original CODE bytes, raw vendor packet-identical OMF
or canonical Factory packed-game accepted credit**.

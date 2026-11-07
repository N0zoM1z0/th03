# TH03 MAIN after906 — nine complete character selectors and resource loader

The real **3,888-CODE-byte original physical `ch_setup`** owner contains
all nine complete character callback/resource selectors and the resource
filename, sprite pair loading and final palette helpers. It binds the
nine original Extra Attack, Chargeshot, Gauge and BOSS callback families
through actual 16-bit *far function pointers*, not a reimplemented
callback table. The 128-byte player records and 12-byte Extra Attack
function tables keep their original external ownership and layout.

The full 12-byte filename template copy now uses natural C++ `while`,
with original per-byte memory writes, stack scratch and final terminator.
Both the template length and decimal filename radix are source-named.
The tens and ones filename digits now use natural explicit C++
assignments, preserving signed 16-bit division/remainder and the
original palette-mode low-bit mask. The nine character callback macros
use natural `if(pid == 0)` for player one, preserving all far/near
callbacks and the side-specific sprite/palette finalization order.

Actual original Turbo C++ 4.02 experiments:

- `af906a`: 12-byte filename `for` to natural `while`, entire original
  3,888-CODE-byte physical owner and full normal MAIN exact twice.
- `af906b`: named true file length for both stack buffer and source
  table, two independent original compiler/linker rounds exact.
- `af906c`: all nine callback `if(!pid)` checks became explicit
  `if(pid==0)` with exactly original native instructions.
- `af906d`: changed `resource >= 10` to mathematically equivalent
  `resource > 9`. **Different CODE at segment 4 offset 165** despite
  equal 3,888-byte initialized CODE length; restored >=.
- `af906e`: named the decimal radix for threshold/division/remainder,
  original native CODE/FIXUPPs and whole normal MAIN still exact.
- `af906f/g`: tens- and ones-digit compound `+=` became natural
  `fn[i] = fn[i] + value`, both independently accepted by original TC4.
- Final `af906h`: complete current source, resource-loader comments
  and nine character macro branches all recompiled in **two actual
  original TC4 4.02/full normal MAIN TLINK rounds**, exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af906h --units ch_setup
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af906h
```

Both original compiler/linker rounds match **all 3,888 CODE bytes,
1,135 literal ordered native OMF FIXUPP fields, and 12 PUBLIC offsets**,
original source/segment/callback ABI, the complete normal MAIN EXE and
normalized MAP, **124,642 Japanese loaded program bytes and 1,553
ordered MZ relocations**. Independent checked standard DOS MZ
serialization matches all **130,882 original Japanese MAIN.EXE bytes**;
original vendor linker header identity is separate. **98 other original
game objects and CRT reused**, no full cold replay, patched original
binaries, synthetic stubs or NOP padding.

Protected current-source-bound two-round native receipt:
`.analysis/work/exatt-layout-af906h/report.json`, SHA-256
`c2d7afd26f620140468d81bbc97edcbac8ab4830645c45d7bd3dbd67b5908413`.
Already source-owned game CODE: improved native maintainability is
**not new distinct original CODE, raw vendor packet identity or
canonical Factory packed-file acceptance**.

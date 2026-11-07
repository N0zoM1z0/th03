# TH03 MAIN after855: complete Mima BOSS native angles and renderer phases

The complete original **nine-function 1,922-CODE-byte `ba_mima` major
BOSS** is compiled in each experiment, not an isolated leaf. Its
physical scope includes the original BOSS template, spread and pellet
volleys, random-bomb warnings, aimed trail bullets, orbit phase,
full collision/update scheduler, the mode-2/5 sprite renderer and the
mask-based two-half introduction.

## Real C++ recovery

Three original **unsigned 16-bit** attack clocks now express their
even-frame condition naturally as `if(!(boss_frame % MIMA_FIRE_EVEN_PERIOD))`.
Two signed original BOSS bomb/volley position offsets and orbit radius
are explicit C++ semantic constants, as is the orbit shot's 0x40 angle
offset. The sprite transition keyframes 0x10/0x20, alternating intro
VRAM masks 0xAAAA/0x5555/0xFFFF and 0xC8 original intro separation with
one-frame-bit shift are now meaningfully named without changing the
exact 16-bit register/PC-98 hardware call order.

In particular, **two byte-valued global spread angle updates**, +9 and
+3, *do* compile identically to the target when their original values
are named as C++ constants here. This was not assumed from other
characters' different byte register allocation. Similarly the intro's
byte local opposite half-turn `angle += 0x80` remains native exact when
named. The target's original mode-5 `goto render_mode_2` and *byte*
trail remainder must remain distinct, however.

## Independent real Turbo C++ 4.02 experiments

- `af855a`: all three original even-frame attack clocks accept natural
  unsigned `%2` truth checks; both original native compiler/full normal
  MAIN TLINK rounds passed.
- `af855b`: replacing the mode-5 `goto render_mode_2` with a natural
  combined mode-2/5 C++ branch **failed** original CODE (candidate
  **1,924** vs **1,922** bytes). Restored the original path.
- `af855c`: named attack cadence, bomb origins, orbit radius and shot
  angle; original physical owner and complete MAIN remained exact.
- `af855d`: changing the original `unsigned char remainder` for the
  trail modulo to an `unsigned int` **failed** the source-native CODE
  comparison (**1,900** vs original **1,922**). Retained the byte carrier.
- `af855e`: named render sprite keyframes/masks and intro scale while
  restoring exact byte remainder; all 1,922 native CODE bytes matched.
- `af855f` and `af855g`: independently proved named **byte** spread +9
  and pellet +3 angle updates preserve real original TC4 instructions.
- `af855h`: separately proved the named intro byte half-turn +0x80.
- Final `af855i` recompiled *all current source* with precise codegen
  comments in two independent original TC4/TLINK rounds, full object exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af855i --units ba_mima
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af855i
```

Both genuine original native compiler/linker rounds match **all 1,922
CODE bytes, 277 literal ordered native OMF FIXUPP fields and 9 PUBLIC
offsets**, original source/segment ABI and full normal MAIN EXE/MAP,
**124,642 loaded Japanese MAIN bytes** and **all 1,553 ordered original
MZ relocations**. Independently reviewed standard DOS MZ serialization
recreates all **130,882 original Japanese MAIN.EXE bytes**. The
**98 unchanged original game objects and Borland CRT were reused**:
no all-project cold replay, patched object/target, fake NOP or code array.

Protected current-source-bound report with actual native compiler/TLINK
receipts: `.analysis/work/exatt-layout-af855i/report.json`, SHA-256
`9777cc25e2b092ffe072a014f31c953120c2a7b06515e7523dc19dd021fa2604`.
This is improved exact **current C++ source** for an already historically
source-covered original physical owner. The 1,922 bytes are **not newly
distinct original CODE**, vendor raw OMF packet identity or canonical
packed-game Factory accepted units.

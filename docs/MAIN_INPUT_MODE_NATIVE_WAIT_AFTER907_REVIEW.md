# TH03 MAIN after907 — all input modes and original two-phase wait controller

The original physical `inp_m_w` Turbo C++ 4.02 project object contains
nine far-Pascal interface modes (keyboard, joystick, player/CPU,
CPU/CPU, attract) and the complete **two-phase release-then-press
input_wait_for_change(int)** loop. Its 16-bit signed caller timeout and
PC-98 joystick register/interrupt ABI must remain exact.

Both original `for` loops in the wait controller now use natural C++
`while`: a **non-timeout release phase**, followed by a press phase
that obeys the original signed frame limit. Zero selects the historical
9,999-frame unlimited sentinel and negative values skip only the press
phase, *never* release polling. Release and press checks naturally spell
`input_sp == INPUT_NONE` and `!= INPUT_NONE`, preserving all real
interrupt calls and source order. The unusual original five-mode
joystick merge macro remains an in-place source expansion; a generic
inline reference helper previously changed original TC4 CODE.

Independent genuine compiler experiments:

- `af907a`: changed both loops, initially spelling the infinite loop
  `while(true)`. Original TC4 4.02 rejected the undeclared `true` in
  this historical source include environment; this failed trial was
  not disguised as an executable C++ rewrite.
- `af907b`: `while(1)` and `while(frames_waited < frames_to_wait)` both
  passed two original TC4/full normal MAIN TLINK rounds byte-exact.
- `af907c`: explicit `INPUT_NONE` instead of zero/nonzero input reads
  preserved all original machine-code instructions in both rounds.
- `af907d`: replacing independent CPU-vs-CPU `input_sp & CANCEL ||
  input_sp & OK` tests with one combined mask changed original native
  CODE to **360** vs **367** bytes, first difference CODE segment 1
  offset 213. Restored two original short-circuit tests.
- `af907e`: explicit `frames_to_wait == 0` sentinel predicate also
  matched original compiler output and signed two-phase behavior.
- Final `af907f`: complete current maintained C++ comments and all
  nine physical input entrypoints compiled in two independent genuine
  TC4 4.02/full normal MAIN TLINK rounds, exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af907f --units inp_m_w
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af907f
```

Both original compiler/normal linker rounds reproduced all **367
original CODE bytes, 58 literal ordered native OMF FIXUPP fields,
nine PUBLIC offsets**, original source/segment/input-mode ABI, complete
normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes and all
1,553 ordered MZ relocations**. Independent verified standard DOS
MZ serialization matches the pinned **130,882-byte original Japanese
MAIN.EXE**. **98 other original game objects and CRT reused**, without
whole cold replay, patched original code, synthetic OBJ or NOP padding.

Protected source-bound two-round native proof:
`.analysis/work/exatt-layout-af907f/report.json`, SHA-256
`02c98196c3609742cc24ea73310a0d0f90fb5c1afd8788e679b9e14d0bb2bb70`.
Previously source-owned original CODE, **not new unique CODE credit,
raw vendor packet identity or canonical Factory packed acceptance**.

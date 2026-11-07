# TH03 MAIN after839: complete input modes and original press-release wait

This stage recompiles the complete original `inp_m_w` physical Turbo C++
source. Its nine far-Pascal PUBLICs include keyboard-vs-joystick routing,
CPU-vs-CPU cancel handling, attract mode, joystick sensing and the
full `input_wait_for_change(int)` release/press polling routine.

The press-phase bounded polling is now an ordinary signed-frame
`for(; frames_waited < frames_to_wait; )`, while the release phase remains
an unbounded loop. The original sentinel 9999 semantics, negative frame
limit, unconditional 1-frame VSYNC delays, and actual hardware input
polling are unchanged. It is important **not** to simplify the two
independent cancel/OK flag tests or change the order of joystick reads.

Original compiler experiments and negative controls:

- `af839a`: the natural `for` press-phase passed genuine original
  TC4 4.02 and whole normal MAIN TLINK in both independent rounds.
- `af839b`: replacing separate `INPUT_CANCEL` and `INPUT_OK` short-
  circuit checks with one combined mask **failed** native CODE equality:
  candidate **360** vs original **367** bytes. The separate checks remain.
- `af839c`: replacing the caller-expanded joystick sensing macro with
  a natural `inline void merge_joystick(input_t&)` likewise **failed**:
  candidate **375** bytes. The original expanded per-caller source is
  retained to preserve TC4 register ownership and call layout.
- `af839d`: final current source with the exact original flag/joystick
  behavior and natural press-phase loop; two independent real original
  compiler/complete linker rounds passed.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af839d --units inp_m_w
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af839d
```

Both final rounds reproduce **all 367 original CODE bytes, 58 literal
ordered native OMF FIXUPP fields and 9 PUBLICs**, original source/segment
ABI, complete normal MAIN EXE/MAP, all **124,642 Japanese loaded program
bytes** and **1,553 ordered MZ relocation entries**. Independent standard
MZ serialization matches all **130,882 original Japanese MAIN.EXE bytes**.
The other **98 game objects and original CRT** were reused; no full cold
replay or object/target-byte patching. Protected source-bound receipt:
`.analysis/work/exatt-layout-af839d/report.json`, SHA-256
`00acf88ac610ebbc69da450b01108d8a22bda885667a87e869835024b22c1e2e`.

This is exact native source improvement for an already historically
covered original physical owner, not incremental unique CODE coverage,
raw historical vendor OMF identity or Factory packed-file acceptance.

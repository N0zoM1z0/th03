# TH03 MAIN after920 — full Marisa Chargeshot/Gauge native byte phases and GRCG

The complete nine-function original physical `cs_mari` Turbo C++ 4.02
translation unit contains one **50-byte, 12-history-sample beam per
player**, both ordinary and Hyper construction, full 12-sample
update/decay, three-sample hit test, all three independent GRCG beam
pattern bands and the mirrored two-phase five-shot Gauge scheduler.
The original physically external projectile and Gauge timing arrays,
player state, CPU registers and far/near callbacks remain untouched.

The original byte activity conditions in the construction, update,
hit and render entrypoints now naturally spell `active == 0` instead
of `!active`, and both public Gauge guards spell `active != GBAF_NONE`.
The four independent modulo-24 Gauge phases retain their exact
left-warn, right-warn, left-fire and right-fire side-effect order;
the zero remainder naturally uses `if(!remainder)` and the other
three constant equality predicates can have their operands reversed
without changing original TC4 CODE. The mutable byte 24-frame initial
beam cutoff can also read naturally `INITIAL_END > frame`, with
original instructions unchanged. No GRCG calls, RNG or bullet draws
are merged, nor is the real separate 12-point subpixel history flattened.

Genuine original TC4 4.02 compiler-positive and negative experiments:

- `af920a`: four real byte active guards and both public Gauge guards
  became explicit enum/zero comparisons, whole object and complete
  normal MAIN byte exact in both original rounds.
- `af920b`: one zero-remainder event and one warning-phase equality
  gained natural zero/constant-first syntax, full object original-exact.
- `af920c`: changing mutable byte `marisa_chargeshot_p->frame++` to
  prefix produced **1,514** original candidate CODE bytes vs target
  **1,509** (first mismatch CODE segment 4 offset 264). Reverted.
- `af920d`: replacing all four signed GRCG `y >> 5` conversions with
  signed `/32` changed native CODE to **1,521** vs **1,509** bytes
  (first mismatch CODE segment 4 offset 606). Negative-coordinate
  rounding also differs; restored original signed arithmetic shift.
- `af920e`: changing byte `marisa_gauge_frame[pid_current]++` to
  prefix produced **1,523** vs **1,509** CODE bytes (first mismatch
  CODE segment 4 offset 1105); restored postfix.
- `af920f`: both remaining Gauge warning/fire phase equality
  comparisons can reverse operands, original native CODE exact twice.
- `af920g`: reversed the original initial beam byte-frame `<24`
  comparison and preserved every native original CODE byte.
- Final `af920h`: current full nine-function physical source, original
  CODE/OMF ABI and explanations passed two genuine independent original
  TC4 4.02 and complete normal MAIN TLINK rounds exactly.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af920h --units cs_mari
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af920h
```

Both actual independent native compiler/full normal linker rounds
match **all 1,509 original CODE bytes, 152 literal ordered native
OMF FIXUPP fields and nine PUBLIC offsets**, original source/segment/
16-bit ABI, complete original normal MAIN EXE and normalized MAP,
**124,642 Japanese loaded program bytes and all 1,553 original
MZ relocations**. Independent standard DOS MZ serialization reproduces
all **130,882 pinned Japanese MAIN.EXE bytes**, not historical vendor
header-byte serialization. **98 other game project objects and CRT
reused**, no cold replay, altered original objects/target, fake CODE
buffers or NOP padding.

Protected current-source-bound original TC4/TLINK proof:
`.analysis/work/exatt-layout-af920h/report.json`, SHA-256
`201928f5b0f55be4cfc8640d0494dd2520aab10b3c67f5b18d13fb22ffa39b2f`.
Previously source-owned game CODE; no new distinct original game bytes,
vendor raw OMF packet identity or canonical Factory packed-game credit.

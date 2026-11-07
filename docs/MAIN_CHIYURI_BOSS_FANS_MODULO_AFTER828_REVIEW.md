# TH03 MAIN after828: complete Chiyuri major BOSS native C++ timing and four-fan geometry

`ba_chiyu` is the **entire original 746-line Chiyuri major BOSS physical
Turbo C++ 4.02 source**, with eleven original functions and 2,654 CODE
bytes: BOSS template, cardinal/ring/trail/fan attacks, full state and
collision update, sprite-ring drawing, main/intro/monochrome render and
the complete render dispatcher. This is not isolated small-leaf evidence.

## Actual changed natural C++ expressions

- The trail warning's unsigned 16-bit `boss_frame & 7` check now uses
  **natural `% CHIYURI_TRAIL_BOMB_PERIOD`**. This preserves the eight-tick
  sound/axis warning and the separate 0x30-frame final 48-bullet ring.
- The full BOSS update's **unsigned 16-bit `round_or_result_frame & 3`**
  animation cadence likewise now uses natural `%4`. The **different
  mutable byte `boss_render_frame &=3` remains**, because TC4's byte
  `%4` substitution is known to generate different instructions.
- All **four genuinely separate horizontal/vertical fan loops** now use
  named 112-pixel fan span, 64 angle units, signed center/vertical
  angular offsets and 16-subpixel scale. The original **16-bit integer
  division occurs before scaling**; restoring these semantics does not
  fold loops, alter per-pellet speed increments, or change RNG ordering.

`af828a` and `af828b` each compiled the full BOSS twice with one then
both natural modulo clocks. `af828c` additionally proved all four
fan phases with the named signed arithmetic. **The fresh `af828d`
experiment challenged a handwritten AL-specific intro phase update**
with a normal `register unsigned char` temporary, but emitted **2,674
CODE bytes** versus the real original **2,654**. That is a genuine
negative native compiler trial; the attempted register-local C++ form
was rejected, and the original 8-bit `_AL` read/add/store preserved.
Final **`af828e`** force-compiles the entire current maintained source
again (including corrected comments) in two independent original
TC4/TLINK rounds, not by repinning an older source hash.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af828e --units ba_chiyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af828e
```

Both genuine original compiler and complete normal MAIN TLINK rounds
reproduced **all 2,654 initialized CODE bytes, 381 literal ordered OMF
FIXUPP fields and 11 PUBLIC offsets**, original source/segment/ABI,
complete native original MAIN EXE and path-normalized MAP, all **124,642
Japanese loaded bytes and 1,553 ordered original MZ relocations**. An
independently checked standard MZ serializer reproduces all **130,882
Japanese MAIN.EXE bytes**. The original **98 other project objects and
Borland CRT were reused**; no whole cold replay, object post-processing,
byte padding, or target substitution occurred.

The full source-bound two-round report and protected private native
inputs/outputs are retained at
`.analysis/work/exatt-layout-af828e/report.json`, SHA-256
`814754759b65ff864ac1545a279934bea724a1deb12575d7a1ac33a267dddade`.
All these physical CODE bytes have historical source ownership: this is
native-confirmed source recovery **without new distinct byte credit**.
Raw vendor OMF identity and canonical packed-file Factory acceptance
are separate and remain open.

# TH03 MAIN after850: complete warning, Gauge and palette control

The original physical `warning` owner is one seven-function 1,560-CODE-byte
Turbo C++ 4.02 TU. Its scope includes two-player pause/quit, Gauge
highlight bars, portrait, 27-frame alternating flash, warning text,
red/fade transition and the sustained active Gauge brightness wave.
The original PC-98 near/far hardware calls, panel rows, byte state and
fall-through to active brightness on the warning-completion tick remain.

The current natural C++ recovery removes **four redundant unsigned casts
on the already unsigned 16-bit global frame** from the hyper/Gauge
highlight parity checks. Both key-release polling loops in
`round_pause_or_quit` are now typed natural `for` loops; the frame-zero
Gauge brightness state uses `if(!warning_fading_out[player])`. The 27
flash frames, two palette tones 100/50, six warning text-clear rows,
fade half-period and pulse peak now have named compile-time semantics.
These are native-tested source rewrites, not behavior-only guesses.

## Genuine original compiler trials, including byte-clock counterexamples

- `af850a`: four word-clock C++ `%2` expressions without redundant casts
  pass both original compiler/normal MAIN TLINK rounds.
- `af850b`: both key-release `while` loops converted to `for`; entire
  original object still byte-exact, including repeated BIOS reads.
- `af850c`: natural Gauge pulse zero truth check remains exact.
- `af850d`: removing the **explicit unsigned promotion** from the
  *one-byte* `warning_flag_bytes[player] % 2` changed TC4 instructions:
  the candidate grew to **1,569 CODE bytes** vs original **1,560**.
  The explicit promotion was restored; it is not equivalent to the
  already-unsigned 16-bit global frame case.
- `af850e`: named flash and palette-tone/text-row constants passed.
- `af850f`: replacing the original **byte-memory `+=13`, `-=13`,
  `+=4`, `-=4`** with corresponding enum-valued constants selected
  different TC4 codegen (candidate **1,521 CODE bytes**). Those four
  byte updates remain literal, while named phase bounds survive.
- `af850g/h`: restored original byte arithmetic and compiled the
  final maintained source twice through the authentic TC4/normal TLINK.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af850h --units warning
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af850h
```

Both independent original native rounds match **all 1,560 initialized
CODE bytes, 125 literal ordered OMF FIXUPP fields and seven PUBLICs**,
original segment/source ABI, complete normal MAIN EXE/MAP, all
**124,642 Japanese loaded program bytes and 1,553 ordered MZ
relocations**. Independently checked standard MZ serialization matches
all **130,882 bytes** of original Japanese MAIN.EXE. The other **98
original game objects and Borland CRT were reused**, no cold replay,
object patch, NOP padding or target substitution. Protected actual
source/OBJ/EXE/MAP/compiler evidence:
`.analysis/work/exatt-layout-af850h/report.json`, SHA-256
`c326ff02354d0d7c81eb0c11605de38d92cbc3e8a53378822f8b50f9a6966870`.

The physical original `warning` CODE was previously source covered;
this is more natural maintained C++ and current compiler provenance,
**not new distinct game CODE ownership, raw historical vendor OMF
packet identity or canonical packed-file Factory acceptance**.

# TH03 MAIN after894 — native Rikako Bomb explosion row and timed palette control

The complete original `b_rika` Turbo C++ 4.02 physical unit contains
one **546-CODE-byte Rikako Bomb** update/render controller, including
64-frame initial palette, 128-frame quake, four vertical GRCG beams,
original mutable signed `rikako_bomb_line_offset` in its separate DATA
carrier, random explosion row and final fade.

The original randomized first X and **96-pixel-spaced explosion row** now
uses ordinary C++ `while(x <= RIKAKO_BOMB_ROW_END_X)`, preserving all
far-Pascal explosion calls, original signed coordinate and RNG draw.
The 8-frame explosion trigger and independent 4-frame sound trigger
now use natural `if(!(frame % PERIOD))` while the **different byte
shake clock** retains `if((frame &3)<2)`. All physical phase cutoffs,
0x41 line offset growth, 0x480 reset, explosion Y=0x1700 and row
span/stride now have named original source constants. The near/far MRS
bool-stack ABI and live original hardware register writes stay intact.

## Real native compiler experiments

- `af894a`: explosion row converted to `while`; all original CODE,
  ordered fixups and whole normal MAIN exact in two genuine TC4 rounds.
- `af894b`: both byte `%8==0` and `%4==0` event conditions converted to
  natural `if(!remainder)`; still entirely native exact twice.
- `af894c`: replacing the different byte shake `(frame &3)<2` by
  mathematically equivalent `(frame %4)<2` generated **549** instead of
  original **546** CODE bytes (first difference segment 4 offset 19).
  The original bit mask was restored, not replaced by padding.
- `af894d`: original phase, row and mutable line-offset semantics named,
  full original native object and MAIN exact twice.
- Final `af894e`: current maintained source and comments recompiled
  exactly in two independent original TC4 4.02/normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af894e --units b_rika
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af894e
```

Both genuine original compiler/complete normal TLINK rounds match **all
546 CODE bytes, 56 literal ordered native OMF FIXUPP fields and one
PUBLIC offset**, original source/segment/external state ABI, complete
normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes and all
1,553 ordered MZ relocations**. Independent checked standard DOS MZ
serialization recreates the **130,882-byte original Japanese MAIN.EXE**.
The **98 other original project objects and Borland CRT were reused**,
no full-project cold replay, target/object patch or fake padding.

Protected actual original compiler/OBJ/EXE/MAP report:
`.analysis/work/exatt-layout-af894e/report.json` SHA-256
`862ead46783ae5b1810853657bc83f4d530a2ced0546ff2652420ba0c8d2337d`.
Previously source-owned original bytes; no additional distinct CODE,
raw historical vendor OMF identity or canonical Factory packed credit.

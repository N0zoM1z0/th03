# TH03 MAIN after923 — complete original entry and round scheduler

The physical `entry` Turbo C++ 4.02 owner is the full 3,050-CODE-byte
MAIN entry, 200-line frame scheduler, stage setup, round reset and
register-bound score commitment. The maintained `entry.cpp` includes
four real edited `.inl` bodies. No new DATA/BSS or alternative entry is
introduced.

Native exact natural C++ work: `main()` unbounded round loop is `while(1)`;
story BCD digit copy, two-player character/speed/callback binding and
initial gauge/combo reset use `while`; all EFE, both-player Extra Attack,
Shotpair and two-player state reset loops also use `while`, preserving
duplicate hit flag stores and the entire RNG charge-threshold order.
`round_score_commit` uses natural `while` but retains the actual `_CX`
register for all score digits and each opposing-score clear. The two
global 16-bit frame counters accept prefix increments; two unsigned-word
render-frame parity checks accept natural `%2` and retain all original
PC-98 page flips, distinct return paths and goto labels.

Actual original compiler trials: `af923a-g` each passed both complete
original TC4/full normal MAIN TLINK rounds after successive natural
loop, player reset, CX writer, word-clock and parity changes. `af923h`
changed original byte `frame_mod16 &15` to `%16` and generated **3,060
vs 3,050 CODE bytes**; `af923i` prefixed byte `round_speed` and
produced **3,054**. `af923j` was a combined unisolated negative;
`af923k` restored both candidates, and isolated `af923l` showed that
prefixed `round_id` alone also generates **3,054**. All original
byte masks and postfix spellings are retained in final `af923m`.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af923m --units entry
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af923m
```

Both genuine original compiler and complete normal MAIN linker rounds
match **3,050 CODE bytes, 433 literal ordered original OMF FIXUPPs,
eight PUBLICs**, original source/include/16-bit ABI, full normal MAIN
EXE/MAP, **124,642 Japanese loaded bytes and 1,553 ordered MZ
relocations**. Independently reviewed standard MZ serialization
reproduces the 130,882-byte Japanese MAIN.EXE, not historical vendor
header writer identity. 98 other original game objects and CRT reused;
no full cold replay, object patching, synthetic bytecode or NOP padding.

Native source-bound receipt `.analysis/work/exatt-layout-af923m/report.json`
SHA-256 `8e3b621f010b3217119e14c696aa10a541d62c753697dc17bdd1d5f191f533f2`.
Historically covered CODE; no new unique original CODE/canonical Factory
packed-game credit.

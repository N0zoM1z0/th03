# TH03 MAIN after870: exact Kotohime Bomb row, phase and dead-index source

The full original `b_koto` physical Turbo C++ 4.02 project source owns
the single **528-CODE-byte Kotohime Bomb controller**, including
palette interpolation, explosion timing, screen quake, MRS display,
96-pixel-spaced bomb explosion row and the last byte-fade phase.
The original **two-byte explosion-Y state** remains in the separate
frozen Bomb DATA carrier: this compilation does not duplicate private
BSS, fabricate state ownership or create a new Bomb implementation.

## Natural recovered C++ and target-specific original behavior

The four-pellet explosion row now uses a typed natural
`while(x <= KOTO_BOMB_ROW_END_X)` loop; the 96-pixel subpixel stride,
original physical start/end screen coordinates, original explosion-Y
state mutation and the signed 16-bit **`i` update** retain their exact
per-call ordering. The first palette phase ends at frame 64, the
second screen-shake phase at frame 128, and both original eight-frame
explosion triggers can now use the readable C++ `if(!(frame % 8))`.
The actual first explosion's signed starting X/X progression and Y
progression/offset, 16-frame row phase and 0x2E0 vertical decay are
now meaningfully named without changing 16-bit intermediate math or
PC-98 GRCG/Pascal hardware calls.

The Bomb also intentionally retains two **real historical irregularities**:
its byte-valued screen shake **`(frame &3)<2` is *not* native-equivalent
in TC4 to a `%4` test**, and the final fade uses the previous **stack
contents of the uninitialized local `color`**. The latter is undefined
portable C++ but it is truly original source/target behavior. Neither
initialization, zero fill nor an invented product bug fix is introduced.

## Original compiler experiments, including independent rejected forms

- `af870a`: replaced the full original explosion-row `for` with a
  natural `while`, preserving the **otherwise unused `i`** advancement;
  all 528 original CODE bytes and full normal MAIN linked twice.
- `af870b`: challenged the byte shake mask with `frame % 4 <2`;
  the original TC4 produced **531** candidate initialized bytes vs
  the real original **528**, first mismatch CODE segment 4 offset 20.
  The original byte mask was restored.
- `af870c`: two separate byte frame `%8 ==0` tests became natural
  `if(!(frame %8))`; both full original compiler/normal TLINK rounds
  remained exact with the original shake mask.
- `af870d`: named the original exact frame phases, two clock periods,
  start/stride/finish X coordinates and signed Y decay; all original
  CODE, FIXUPPs and whole Japanese MAIN remained exact twice.
- `af870e`: challenged the **apparently dead** local `int i`, its
  frame-based initial value `(frame % 16)/2`, and its loop increment.
  Removing them emitted only **505 CODE bytes** vs original **528**,
  with first byte difference at CODE segment 4 offset 5. Therefore the
  original signed index and apparently unused computation stay in
  source: this is measured compiler codegen, not speculative cleanup.
- Final `af870f`: restored the exact original `i` lifetime and explicitly
  documented the original uninitialized stack color, with two genuine
  original TC4 4.02/full normal MAIN TLINK rounds again fully exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af870f --units b_koto
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af870f
```

Both original compiler/normal linker rounds matched **all 528 original
CODE bytes, 50 literal ordered native OMF FIXUPP fields, 1 PUBLIC**,
original segment/source ABI, normal MAIN EXE/MAP, entire **124,642-byte
Japanese loaded program and all 1,553 original MZ relocations**.
Independently reviewed standard DOS MZ serialization reproduces all
**130,882 original Japanese MAIN.EXE bytes**, not claiming the historic
TLINK wrote an identical header. The other **98 unchanged original game
objects and CRT were reused**; no whole cold replay, object/target
patching, fake NOP padding or new external storage.

Protected actual original compiler/source/OBJ/EXE/MAP native proof:
`.analysis/work/exatt-layout-af870f/report.json`, SHA-256
`588e107824783e7714bf6de6902e892142425153de5f2bab0f6a36acd40e72c0`.
This original physical Bomb source was already historically covered.
Current native C++ fidelity and new dead-index evidence are **not
additional distinct original CODE ownership, vendor raw packet identity
or canonical Factory packed-file accepted byte credit**.

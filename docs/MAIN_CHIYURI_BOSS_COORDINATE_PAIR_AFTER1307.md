# Chiyuri BOSS position-pair indexing and TC4 code generation

The BOSS mode-selection controller chooses one of five `(x, y)` destinations
from a single interleaved DATA table. The original labels
`_chiyuri_boss_x_words` (1D56:08D6) and `_chiyuri_boss_y_words`
(1D56:08D8) are **two word-indexed views**, two bytes apart. The original
8-bit local holds **twice** the selected random pair index, so both `int[]`
accesses advance four bytes per pair. The maintained
`src/main/boss/chiyuri.cpp` now uses bracket indexing and a descriptive
`position_word_i` without changing the physical DATA symbols.

A tempting true `struct { int x, y; }[]` representation was compiled in the
negative trial `af1307a`: its complete 2,654-byte original BOSS object failed
CODE comparison. In the selection path around original CODE offset 0x647,
TC4 compiled a four-byte struct stride with `SHL AX,2`, rather than the
original byte `ADD AL,AL` **before** the local store and later `ADD AX,AX`
word-indexing operations. The struct form also turned the Y-member read into
`[BX+2]` based on the X symbol, instead of the original independently
relocated Y symbol. This matters even though the C++ values are equivalent.

The corrected natural array-index version (`af1307b`) compiled in two
original TC4 rounds. Both rounds reproduced the **full physical `ba_chiyu`
object**: all 2,654 initialized CODE bytes, 381 ordered native fields,
PUBLIC offsets, segment definitions, and the complete normal Japanese MAIN
image and ordered MZ relocations. The scoped record is
`.analysis/work/exatt-layout-af1307b/report.json`; reproduce with:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage NEW_STAGE --units ba_chiyu
```

Use an unused DOS-safe `af` stage for `NEW_STAGE`. This establishes the
source-bound MAIN BOSS scope, not whole-product or Factory packed-file acceptance.

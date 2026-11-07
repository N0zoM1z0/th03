# Chiyuri BOSS full source: original-native attack modes and timing (after635)

The maintained full Chiyuri BOSS translation unit includes 11 native
functions, with the substantial `gba_boss_update_chiyuri` mode
dispatcher, cardinal and ring barrages, trailing ring, fan attacks
and multiple complete renderers. This recovery is not a leaf-only
source edit.

Two independently tested *natural C++* cadence substitutions preserve
the original code:

- In `chiyuri_pattern_trail_ring`, the warning-bomb periodic test is
  now `boss_frame % 8 == 0` instead of `boss_frame & 7 == 0`.
- In the large `gba_boss_update_chiyuri` state machine, the rendering
  subframe tick condition is now `round_or_result_frame % 4 == 0`
  rather than masking with 3. The existing 0..3 counter wrap remains.

Both tests compiled the changed source with original Turbo C++ 4.02,
yielding exact full object byte/fixup equality in source-OMF-attested
`af635a` and `af635b` negative/positive control isolation.

The attack scheduler now uses 18 named Chiyuri-specific original
mode values: four cardinal, four ring, four trailing-ring, four fan
modes, plus intro, selector, descending and exploding states.
The trail warning and 0x30 ring-release frame, plus horizontal/vertical
fan emission at 0x20/0x40, are represented as compile-time enums.
No mode table, extra DATA or runtime state is added. The four
separate fan passes preserve their original loop order, signed
register arithmetic and emitted bullet properties.

Final two independent original native compiler and complete MAIN
TLINK rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af635c --units ba_chiyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af635c

All **2,654 original CODE bytes**, **381 literal ordered FIXUPP fields**,
**11 PUBLICs**, segment definitions, both complete original normal
MAIN EXEs and normalized MAPs match the source-native ancestor.
The complete Japanese loaded program and all **1,553 ordered MZ
relocations** remain equal; independent standard MZ serialization
matches the exact 130,882-byte Japanese MAIN.EXE.

The emitted OMF COMENT dependencies prove Turbo C++ consumed the actual
staged changed source, avoiding the historical v1 include bug. Complete
two-round native proof, source inputs and writer logs:
`.analysis/work/exatt-layout-af635c/report.json`, SHA-256
`e5bc0132a0401d162a3cefd89f8f14a814a9ee0ce60c69091974a81219cf2ad5`.
Only the affected Chiyuri BOSS object was recompiled; all other game
objects/libraries were reused without full cold replay.

This is a verified natural-source recovery of already tracked bytes,
not new canonical Factory packed-file credit, historical vendor raw
OMF packet identity or physical gameplay execution.

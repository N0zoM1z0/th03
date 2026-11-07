# Ellen original charged-shot and Gauge controller: source-rooted after652

The real `cs_ellen` compiler TU (ten original native functions,
**1,530 complete CODE bytes**) contains a 64-slot projectile pool,
the large active-batch update with homing and boundary clipping,
private sprite rendering, collision, and two-region Gauge attack.
It was not included in the earlier after650 30-object selected scope.

The v2 native scoped compiler driver now recognizes the original
`src/main/player/chargeshot_ellen.cpp` physical source and
`obj/th03/cs_ellen.obj` TLINK slot. Its `af651b` unchanged-source
control passed two original TC4.02 rounds, with the actual emitted
OMF COMENT dependencies proving the compiler read the forced source.

The maintained C++ changes are concrete, not only renamed constants:

- The large `chargeshot_update_ellen` now decrements an occupied
  projectile's countdown via `--ellen_chargeshot_p->state` instead
  of a nested assignment/subtraction expression. Both formulations
  produce precisely original code (`af652a`).
- The small private sprite render helper no longer introduces a
  temporary `#define _AX` macro. Explicit
  `static_cast<int16_t>(_AX) >>= 4`, `+= 8` and signed register
  argument values reproduce the original pixel conversion and ABI
  (`af652e`).
- The original 12-byte projectile struct has compiler-time size,
  +04 center and +08 velocity assertions, and the four-byte
  Gauge timing record also has a size check. The first 32 slots
  belong to one player, 64 slots to two. The original staged
  even-numbered `state` initialization 0..62 is **not**
  falsely described as 64 immediately active shots.
- The large update now names its decelerating and aimed stages,
  initial length 0x50, per-frame length reduction 2 and
  aimed velocity 160; the Gauge routine identifies the genuine
  eight-frame volley cadence, initial horizontal position,
  mirrored Y boundary and 24-pixel-step side volleys.
  Those limits are compile-time enums, not newly generated DATA.

A more radical negative test attempted to replace the large
update's `goto active` with loop `break` plus a final index
check (`af652b`). Turbo C++ changed the complete CODE payload;
the real original cross-loop jump is deliberately preserved,
not claimed to be recovered from natural source.

Final **actual-current-source, OMF-dependency-attested** original
Turbo C++ 4.02/TLINK two-round native evidence:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af652g --units cs_ellen
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af652g

Both newly compiled original objects have **all 1,530 original CODE
bytes, 169 literal ordered OMF FIXUPPs, ten PUBLIC offsets and
original segment metadata**. Both whole normal MAIN links and
path-normalized complete MAPs match the frozen after596
source-native baseline. The original Japanese program image,
1,553 literal ordered MZ relocations and independently serialized
130,882-byte Japanese MAIN.EXE also match.

Retained evidence: `.analysis/work/exatt-layout-af652g/report.json`,
SHA-256 `63760a6e08ac4be030a9896f77ab7d196c470dc0e45d7976da32a2ae4a3b6e71`.
Only this one physical native producer was recompiled in both
rounds. Original targets, historical receipts, 98 other project
objects and CRT/library inputs were not rebuilt or overwritten.

This proves maintained C++ is original-byte-exact over an already
tracked native owner, not new canonical packed-game Factory credit,
historical raw vendor OMF packet identity or hardware runtime proof.

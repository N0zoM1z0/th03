# TH03 warning/Gauge/portrait status controllers: original native C++ after669

This source-rooted compiler proof covers the *complete original*
seven-function player warning source producer (`warning`) in
PLAYER_M_TEXT. The large `round_CB81` warning transition
and ongoing Gauge brightness state machine, portrait/flash
controller, two resource-intensive Gauge highlight renderers,
and pause/quit loop are all compiled together. The original
source contributes 1,560 CODE bytes with 125 native fixups.

The v2 scoped Turbo C++ source driver now binds the exact
`src/main/player/warning.cpp` physical original object and
historical full-MAIN MAP path (not an invented `th03/warning.cpp`).
Both rounds of `af669a` independently established the real
unchanged-source baseline before any modifications.

Six substantive natural C++ rewrites pass source/native comparison:
- Four `round_or_result_frame & 1` uses across the large
  hyper highlight and two Gauge bar coloring functions now use
  explicit `static_cast<unsigned int>(round_or_result_frame) % 2`.
  These preserve the same original sprite timing, palette/color
  selection and masked-bit machine instructions (`af669b`).
- The long warning transition function's one-byte
  `warning_flag_bytes[player] & 1` tests the same low bit
  using an explicitly unsigned C++ remainder (`af669c`).
- The 27-frame warning flash's alternating palette tone
  uses `static_cast<unsigned int>(frame) % 2` instead of a
  signed-int mask, with original CODE unchanged (`af669e`).

The same large warning-state updater now clears its six text
rows with a natural `for(i=0, y=11; i<6; i++, y++)` rather
than a separated initialization and while loop. The genuine
TC4 compiler emits the same original native bytes (`af669d`).
The intentional **fallthrough into active Gauge brightness
updates on the completion tick** remains unchanged. All
original PC-98 hardware and intra-segment far-return
assembly calls are retained where native opcode identity
requires them; no logic fixes or external DATA were introduced.

Final two-round current-source/OMF-COMENT-attested native proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af669f --units warning
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af669f

Both original Turbo C++ 4.02/TLINK rounds match **all 1,560
CODE bytes, 125 literal ordered OMF FIXUPP fields, seven
PUBLIC offsets and original OMF segment definitions**.
Both complete normal MAIN EXEs, path-normalized MAPs,
Japanese loaded program and all 1,553 ordered MZ
relocations match. Independently serialized complete
130,882-byte Japanese MAIN.EXE also agrees byte-for-byte.

Preserved native source and output evidence:
`.analysis/work/exatt-layout-af669f/report.json`,
SHA-256 `84620e2c3a73290acb9009d21e381aae7540aa19eb05d174a05870a45d23aa57`.
Both compiler/linker rounds, original response files, emitted
OBJ/EXE/MAP and actual consumed-source dependency records
are retained. Only this one original project object was
recompiled, with the other 98 originals and CRT reused.
This was not a full cold replay.

These previously tracked original CODE bytes are not new
Factory packed-file credit, evidence of historic vendor raw
OMF packet identity or PC-98 hardware runtime certification.

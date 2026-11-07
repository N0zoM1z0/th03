# Ellen BOSS large spread and Extra Attack timing, original native C++ (after630)

The full Ellen physical BOSS source consists of nine functions / **1,675
original CODE bytes** including three large attack routines, the mode
dispatcher and render loops. Its scheduler uses 18 byte-mode IDs with
three distinct attack groups. Their meaning is now explicit as a
character-specific C++ enum, preserving the shared pattern selector's
2..17 numerical values and the 0x80/0xFF exit states.

The spread attack's 0x10/0x14 collision-warning pulses, 0x18 direction
setup, 0x1C warmup end, 0x24 multi-volley transition and 0x2C finish
are named as compile-time phases. The Extra Attack distinguishes
0x20/0x24/0x28 warning pulses from first (0x30) and final (0x60)
radial burst frames, with the original +2 vs 0xFE mode arguments and
unchanged sequential RNG calls. Both use ordinary C++ enum constants,
not extra DATA or new runtime state.

This work did not silently simplify original control flow: an attempted
branch inversion in the spread attack (`af630a`) changed original
CODE. Replacing the nine-strip renderer's decrement-and-negative
wraparound with the intuitive `i == 0 ? 8 : i - 1` also changed
compiler output (`af630d`); the original signed increment/decrement
sequence is retained. With this rejected candidate removed, the
source-bound original TC4.02 compiler and normal TLINK generated the
complete original output:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af630f --units ba_ellen
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af630f

**Both independent rounds:** entire 1,675 CODE bytes, **213 literal ordered
native fields**, nine PUBLIC symbols and all segment metadata identical.
Both full normal MAIN EXEs and complete path-normalized MAPs match the
retained after596 source-native original. The Japanese loaded program,
all 1,553 ordered MZ relocations and separate full 130,882-byte original
Japanese MAIN.EXE serialization remain exact.

Native proof:
`.analysis/work/exatt-layout-af630f/report.json`
SHA-256 `498a29eba38fb9bd4ea6bf0305cdede427c281a97fe850d3ba9e71e712389817`.
The compiler actually consumed the staged modified source: the emitted
OMF COMENT dependency paths are verified, unlike historical v1 false
positives. Only this complete physical unit was rebuilt, with other
original project objects and libraries reused.

The recovered mode/phase meaning strengthens maintained large-function
C++ without adding newly accepted canonical packed-file bytes,
historical vendor OMF packet identity or runtime device coverage.

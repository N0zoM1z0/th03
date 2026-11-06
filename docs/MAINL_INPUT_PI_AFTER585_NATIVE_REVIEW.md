# MAINL nine input modes and natural PI raster loops — after585

Four true first-use Turbo C++ translation units now compile together from
the **maintained original natural C++ source**, rather than copying
opcodes from the Japanese target.

| Native module | Original source | Original first-use binary | CODE | PUBLICs | OMF fixups |
| --- | --- | --- | ---: | ---: | ---: |
| inp_m_w | shared/hardware/input_modes.cpp | O (OP) | 367 | 9 | 58 |
| pi_put | shared/formats/pi_put.cpp | O (OP) | 173 | 2 | 10 |
| pi_put_i | mainl/formats/pi_put_interlace.cpp | L (MAINL) | 135 | 1 | 6 |
| pi_put_q | mainl/formats/pi_put_quarter.cpp | L (MAINL) | 177 | 1 | 3 |
| Total | four real C++ bodies | | **852** | **13** | **77** |

This captures the complete input-mode function family, including keyboard
vs keyboard, keyboard vs joystick, joystick vs keyboard, human/CPU control,
attract-mode input, and the waiting-for-release/press logic. The three
PI blitters include the complete color palette, row pointer/segment carry,
interlaced line stride and quarter-image fixed-height loops. Small
functions and nontrivial loops are both included, not only leaf functions.

The independent native experiment first compiled each with its genuine
OP or MAINL initial compiler conditions and simultaneously substituted
all four objects into the most recent natural-source MAINL build.
This complete 67,372-byte Japanese decoded EXE and all 677 ordered
relocations were byte-exact. The two separately staged and freshly compiled
after585 native rounds repeated the result and verify the entire
initialized CODE/OMF FIXUPP/PUBLIC/segment ABI of each object.
Only compiler diagnostic paths change in MAP text.

The recent natural-source chain contains the corrected CUTSCENE_TEXT
continue menu, full root CFG/win/story and stage control, Staff Roll,
cutscene, score editor, CDG image and text routines, keyboard scan,
sound, registration data, vector and original linked CRT.
No full cold replay, target-byte patch or historical receipt repinning
was used. These 13 functions are historical owners; no new Factory
or whole-project authored-function credit is inferred. Original vendor
OMF THEADR/LNAMES/COMENT record chronology also remains unproven.

Read-only affected verification:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_input_pi_after585_work.py

Native driver: scripts/build_th03_mainl_input_pi_after585_work.py
Report: .analysis/work/mainl-input-pi-after585-native-build.json
Review: .analysis/work/mainl-input-pi-after585-native-review.json
All four source wrappers, eight original OMF objects, two EXE/MAP pairs,
ten native writer logs and exact normal response files are retained.

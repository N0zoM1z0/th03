# MAINL score recovery, press/measure waits and PI loader: after587

Three additional original 16-bit C++ source producers were rebuilt
together with their actual original first-use compile conditions:

| Original module | Natural source | BINARY | CODE | PUBLIC functions | Ordered OMF fixups |
| --- | --- | --- | ---: | ---: | ---: |
| scoredat | mainl/scoredat.cpp | O | 229 | 3 | 15 |
| inp_wait | mainl/hardware/input_wait.cpp | L | 126 | 2 | 11 |
| pi_load | shared/formats/pi_load.cpp | O | 70 | 1 | 6 |
| Total | Three maintained sources | | **425** | **6** | **32** |

This includes more than trivial wrappers. Scoredat decodes score data,
recreates default rank entries and checks score checksums, retaining
the original unchecked state behavior. The input-wait code uses the
actual vsync counter, current input mode and playback-measure queries
to coordinate confirm/shot presses; PI loading performs the original
buffer-free and packed graphics-load calls with unmodified failure
handling.

All three 16-bit Turbo C++ 4.02 objects were separately compiled using
the genuine GAME=3/BINARY O/L/O conditions. Every original initialized
CODE byte, all 32 ordered OMF relocation fields, all six original PUBLIC
entries and all three original segment definitions match, including
the original decorated names and ABIs.

The first experiment substituted all three newly compiled objects into
the current after586 source-native 36-project-object MAINL link and
confirmed complete original output. Two independently staged full
compiler/linker rounds repeated the result: the entire **67,372-byte
Japanese original decoded MAINL EXE** matches byte-for-byte, including
all **677 ordered MZ relocations** and original MAP contribution geometry.
Only the new compiler source diagnostic paths differ in MAP text.

The existing chain already includes nine input modes, four PI drawing
loops, sound priority/music/file loading, the corrected continue-menu
segment, root story/stage control, Staff, cutscene, CDG, keyboard with
natural EVEN, registration DATA, and original C0/CRT. Other 33 project
objects and the library were reused, not rebuilt. No full cold replay,
code/data patch, or tampering with old source receipts occurred.

Focused read-only verification:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_score_input_pi_after587_work.py

Builder: scripts/build_th03_mainl_score_input_pi_after587_work.py
Native report: .analysis/work/mainl-score-input-pi-after587-native-build.json
Review: .analysis/work/mainl-score-input-pi-after587-native-review.json

These six functions already appear in the original source/ownership
evidence. No new function denominator, raw vendor OMF packet identity,
whole-project source acceptance or canonical Factory credit is asserted.

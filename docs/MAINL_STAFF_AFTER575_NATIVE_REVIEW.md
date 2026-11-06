# MAINL large Staff Roll and ending control: native C++ source integration

The 797-line maintained natural C++ file src/mainl/staff/data.cpp owns
MAINL's final ending/Staff Roll gameplay, snow effects, scrolling staff,
gallery transitions, verdict, score text, mutable state and typed initialized
art. It compiles into the original staffdat.obj producer in Borland's
STAFFP_TEXT group. The 3,695-byte CODE contribution contains 19 original
public procedures; its separate 224 initialized DATA bytes contain flake
sprites, dissolve masks, filename pointers and character/rank tables,
including six exported DATA names. The object uses 342 original ordered
native OMF FIXUPP fields, none synthesized or patched.

The new tiny source TU src/mainl/staff/producer.cpp includes the complete
maintained C++ code. Native first-use compilation with Turbo C++ 4.02,
original GAME=3/BINARY='L' flags and context headers yields exact original
initialized CODE/DATA bytes, ordered FIXUPP fields, all 25 PUBLIC names/
offsets and segment geometry. Its OMF THEADR/LNAMES/COMENT dependency
source path differs, so original raw OMF packet identity is not asserted.

Both independent TCC/TLINK rounds include the after573 natural cutscene
C++, four TASM-sourced sound functions, keyboard with native EVEN,
registration DATA EVEN, vector math and the entire retained C0/CRT library.
Each links the complete 67,372-byte original Japanese decoded MAINL EXE
exactly, including all 677 ordered MZ relocations. MAP geometry remains
identical; diagnostic filenames are normalized only for text comparisons.

The initial after574 trial passed both compiles and links but failed a
cross-round MAP text equality check because the upstream cutscene object
had independently named r1/r2 source files. Its native receipts, logs,
source and objects are retained as a failed experiment; they were not
promoted to a completed build. The new after575 script repeats the complete
native build with an explicit bounded diagnostic-path check; no target/code
bytes or old objects are edited.

Source/command/proof artifacts:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_staff_after575_work.py

Producer: scripts/build_th03_mainl_staff_after575_work.py
Native report: .analysis/work/mainl-staff-after575-native-build.json
Review: .analysis/work/mainl-staff-after575-native-review.json

The 19 procedures are historical existing source owners, not newly
discovered functions. Neither original historical source compiler identity,
whole-project source acceptance nor canonical Factory credit is claimed.
No full cold replay or historical receipt repinning occurred.

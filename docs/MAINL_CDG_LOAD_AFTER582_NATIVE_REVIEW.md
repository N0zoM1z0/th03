# MAINL CDG file loader: independently source-compiled five original routines

The maintained src/shared/formats/cdg_load.cpp provides five original
16-bit C++ image-load/free routines: single-slot CDG load, single-slot
no-alpha, all frames, all frames without alpha, and memory release. It
parses CDG headers, selects image frames, allocates 4-plane buffers,
reads colors/alpha, and respects the original unchecked file-I/O logic.

This producer was *first compiled for TH03 OP*, not MAINL. The source-native
verification therefore uses the actual Turbo C++ 4.02 first-use
GAME=3/BINARY='O' flags (-O -b- -3 -Z -d -ml). The new maintained
src/mainl/formats/cdg_load_producer.cpp forwards to the exact same
shared natural C++ source without code-string, byte arrays or patches.

Two fresh TC4 builds reproduce the original entire 593-byte CODE
initializer, all five original PUBLIC entries, all 35 ordered native
OMF FIXUPP fields and original CODE/DATA/BSS segment definitions.
Both objects were substituted into the newest after580 source-native
MAINL normal link containing the large root/story controller, scoreboard,
Staff Roll, cutscene, natural CDG blitters/sound, keyboard, registration
DATA and original source-backed CRT library.

Both complete 67,372-byte Japanese decoded MAINL EXEs matched the
original file byte-for-byte with all 677 ordered MZ relocations and
all original MAP addresses. The new diagnostic source module name is
normalized only for MAP comparisons. The original full Borland OMF packet
chronology and vendor source filenames are not asserted equal.

This is a new independently reproducible first-use C++ source and
cross-module link proof, not five newly discovered procedures or an
increase to the historic accepted-function denominator. Factory packed
unit acceptance and original compiler identity remain separate.

Read-only affected evidence:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_cdg_load_after582_work.py

Native build: scripts/build_th03_mainl_cdg_load_after582_work.py
Report: .analysis/work/mainl-cdg-load-after582-native-build.json
Review: .analysis/work/mainl-cdg-load-after582-native-review.json
The reusable, SHA-locked focused compiler/reviewer is
scripts/lib/native_cpp_forward.py; all actual source inputs,
native OBJ/EXE/MAP vectors and four writer logs are retained.
No full cold replay was run.

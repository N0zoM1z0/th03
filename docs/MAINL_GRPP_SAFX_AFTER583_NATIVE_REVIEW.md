# MAINL original CG-ROM text renderer: full natural C++ source native link

The complete original Turbo C++ grppsafx.obj translates the natural
src/shared/graphics/text.cpp implementation of GRAPH_PUTSA_FX, a
613-byte non-leaf graphics/text procedure. Its 16-bit code programs
PC-98 GRCG/CG-ROM, decodes multibyte Shift-JIS glyphs, applies font
weight, advances the pixel cursor and OR-renders full glyph rows to VRAM.

This source was first compiled for OP rather than MAINL. The new bounded
src/mainl/display_hardware/grppsafx_producer.cpp simply includes the
unmodified maintained natural shared implementation. Two independent
original Turbo C++ 4.02 GAME=3/BINARY='O' native compiles produce exactly
all 613 original CODE bytes, all six original ordered OMF fixups,
the original decorated PUBLIC procedure entry and exact segment geometry.

The source objects were substituted into the latest after582 native
MAINL link containing the full original root/stage/story controller,
CDG image loader and TASM blitters, Staff Roll/ending, cutscene,
high-score name editor, natural sound, input and root-data alignment,
and all unchanged source-backed C0/CRT providers. Both complete
67,372-byte Japanese decoded MAINL EXE outputs match the original,
including every one of 677 ordered MZ relocations and all original MAP
geometry. Only the compiler module's diagnostic source filename differs.

Native reports, source snapshots and four writer logs are retained.
Run the read-only focused verification without rebuilding the cold chain:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_grppsafx_after583_work.py

Builder: scripts/build_th03_mainl_grppsafx_after583_work.py
Report: .analysis/work/mainl-grppsafx-after583-native-build.json
Review: .analysis/work/mainl-grppsafx-after583-native-review.json

The single original text procedure was already a maintained source owner.
This stage does not increase the historic function denominator, claim raw
OMF vendor packet identity, or grant whole-game/canonical Factory acceptance.
The same frozen first-use OP source and original Japanese targets are
unchanged.

# MAINL natural high-score editor and registration menu: after578 native

This stage source-compiles the complete 584-line maintained natural C++
registration implementation in src/mainl/regist.cpp, reached through the
already-maintained src/mainl/hiscore/regdata.cpp first-use translation unit
and the new minimal src/mainl/hiscore/producer.cpp wrapper. Neither original
maintained file was edited or flattened into a copied dependency bundle.

The original 16-bit Turbo C++ module regdata.obj owns **2,788 CODE bytes**,
**40 initialized DATA bytes** (ten original FAR pointers), and **15 original
CODE PUBLIC functions plus one DATA symbol**. Two especially large
complete procedures are the 739-byte name-entry editor (CODE+1501..2239)
and 348-byte registration menu (CODE+2372..2719). Related functions handle
score decoding and saving, drawing/rerendering score tables and alphabet,
music changes, cursor movement and preserved unchecked user input indices.

Two independent TC4.02 GAME=3/BINARY='L' builds emit the complete original
CODE/DATA initialized bytes, all **188 original OMF FIXUPP fields in their
original order**, all PUBLIC locations and original segments. Historical
OMF dependency path headers/COMENT packets are not claimed byte-identical.

Both source objects were actually linked into the latest after577 MAINL
chain containing natural CDG, large Staff Roll/Cutscene, natural sound
hardware functions, keyboard with native EVEN, registration text DATA
alignment, vector calculations and the original source-backed C0/CRT.
The complete **67,372-byte original Japanese decoded MAINL EXE** matched
both rounds, including every one of **677 ordered MZ relocations**. MAP
geometry and all contribution positions matched; only the C++ source
wrapper diagnostic path changed. Cross-round comparisons explicitly
normalize the independently source-staged Staff/Cutscene r1/r2 filenames.

Builder: scripts/build_th03_mainl_hiscore_after578_work.py
Native report: .analysis/work/mainl-hiscore-after578-native-build.json
Read-only verifier: scripts/review_th03_mainl_hiscore_after578_work.py

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_hiscore_after578_work.py

The original 15 functions already appear in the historic decoded ownership
review, so none are newly counted. No all-project cold replay, score behavior
rewrite, original OMF tool/provenance claim or canonical Factory credit.
Both original native writer rounds, their complete OBJ/EXE/MAP vectors, input
file snapshots, source hashes and compiler/linker logs remain preserved.

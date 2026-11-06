# MAINL large root controller: source-native C++ integrated into latest link

Original rootdata.obj contains 2,458 initialized CODE bytes, 112 initialized
DATA bytes and 186 BSS bytes. This is the full original 11-function root
control TU, **not a small data-only shim**. Natural maintained C++ implements
the game configuration/resident pointer, win screen drawing/animation,
story opponent dispatch, stage-background loading, the full stage-intro
switch, paired CDG sprites, shot loading and the original main entry.

The complete maintained source lives in src/mainl/root/complete_data.cpp.
Its new tiny independent first-use producer src/mainl/root/producer.cpp is
source-only, without opcode arrays or patches. Each of two original Turbo
C++ 4.02 GAME=3/BINARY=L native compiler rounds used a separately staged
copy of this maintained natural source. The emitted rootdata.obj matches
the original complete initialized CODE+DATA, all **278 ordered native
OMF FIXUPP fields**, 11 original CODE PUBLICs, 3 DATA PUBLICs, 3 BSS
PUBLICs and the exact original segment allocation and ABI.

Each new source object was really substituted in place of the existing
source-native root slot of the after578 MAINL normal link. The parent already
contains source-native staff/ending, cutscene, CDG, high-score editor,
input scanner, natural sound, registration DATA and C0/CRT. Both entire
**67,372-byte original Japanese decoded MAINL EXEs** remain byte-identical
with all **677 ordered MZ relocations** and original MAP coordinates.
The root's new wrapper diagnostic module name is normalized only for
MAP text comparisons; original historical OMF THEADR/COMENT identity and
the whole packed original game are not asserted.

Run the retained, read-only affected review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_root_controller_after580_work.py

Native driver: scripts/build_th03_mainl_root_controller_after580_work.py
Build: .analysis/work/mainl-root-controller-after580-native-build.json
Review: .analysis/work/mainl-root-controller-after580-native-review.json

All full input scripts, source snapshots, both original compiler/linker
logs and raw OBJ/EXE/MAP vectors remain retained. The 11 functions were
already historical source owners: no double-counted authored function
credit, new canonical Factory receipt or whole-game source closure.
No full cold replay was executed.

# Original MAIN bullet engine: full natural C++, GRCG and 9.5 KB BSS

Maintained natural C++ source src/main/bullet/bullet.cpp implements the
complete original non-leaf bullet subsystem: bullet template/group spawning,
inter-playfield transfer, per-frame acceleration and motion, trail storage,
hit processing, 16x16 cel rendering and a separate 386 fast GRCG pellet renderer.

The original bullet.obj has 2,602 initialized CODE bytes in BULLET_TEXT,
83 CODE bytes in PELLET_PUT, 9,500 BSS bytes for bullet/trail state,
20 original PUBLIC symbols and 196 ordered OMF fixups. The actual source
contains local -a2 packing; globalizing or removing it is not assumed safe.

The new src/main/bullet/producers/bullet_native.cpp compiles the complete
unchanged maintained C++ with original first-use Turbo C++ 4.02
GAME=3/BINARY='M' flags. Two independent native compiler rounds reproduce
the entire original initialized CODE, 196 ordered OMF literal references,
all original PUBLIC locations and segment allocations. Raw OMF
THEADR/COMENT/LNAMES packet identity is not claimed when the source
wrapper changes module diagnostic dependencies.

Both objects were substituted into the after572 source-backed native MAIN
link, already containing nine major BOSSes, four large enemy script/
collision controllers, natural keyboard and original C0/CRT. Both links
reproduce the entire retained 132,322-byte source-native EXE and original
MAP geometry. All 124,642 original Japanese program bytes and 1,553 ordered
MZ relocations are exact. The separately proven standard MZ format stage
produces the entire 130,882-byte Japanese original MAIN.EXE, byte for byte,
in both native rounds. Direct TLINK output is distinct from the compact file.

This is significant native source integration of existing authored functions,
not a newly credited Factory function set or new original vendor provenance.
No target-byte code patches, cold full replay or historical receipt edits.

Read-only review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_bullet_after588_work.py

Builder: scripts/build_th03_main_bullet_after588_work.py
Build: .analysis/work/main-bullet-after588-native-build.json
Review: .analysis/work/main-bullet-after588-native-review.json
Both genuine code/OBJ, native link/compact MZ rounds and writer logs are retained.

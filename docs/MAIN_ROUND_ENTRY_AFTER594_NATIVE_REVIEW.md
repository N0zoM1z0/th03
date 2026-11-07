# MAIN original top-level round loop and stage/score scheduler: after594

The large complete maintained natural source
src/main/core/entry.cpp includes four original 16-bit C++ implementation
fragments: the top-level MAIN entry point, round loop and dispatch,
stage setup/restart, and end-of-round score commit. It is not a tiny
leaf wrapper. The original source-local Borland PLAYFLD_TEXT segment
and near/far calling conventions are preserved.

The fresh first-use translation unit
src/main/core/producers/entry_native.cpp includes this one maintained
original C++ source. Two independently staged Turbo C++ 4.02
GAME=3/BINARY='M' compilations reconstruct the entire original
3,050-byte PLAYFLD_TEXT CODE initializer, all eight original PUBLIC
locations, all 433 ordered native OMF FIXUPP fields, and the exact
four-segment OMF declarations including the empty ENTRY_TEXT segment.
The original vendor compiler module dependency metadata is not
asserted byte-identical to the new wrapper's metadata.

Each original-source compiled entry object was truly linked in place
of the original in the after593 source-native 99-project-object MAIN,
which already contains the full original character callback resource
setup, large player movement/hit/damage control, all nine large boss
functions, bullet/trail engine, fireball/explosion, enemy scripts,
natural collision modules and keyboard. Both native TLINK results
match the retained complete source-native MAIN EXE and all original
MAP geometry. The original Japanese load-image length of 124,642
bytes and all 1,553 ordered MZ relocations remain exact.

After a separately identified standard MZ file-format serialization,
both independently produced full MAIN output files match the entire
original Japanese 130,882-byte MAIN.EXE exactly. This does not establish
historical TLINK direct compact-file identity, whole-project source
ownership or canonical Factory publication acceptance.

Read-only targeted proof:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_entry_after594_work.py

Producer: scripts/build_th03_main_entry_after594_work.py
Native source receipt: .analysis/work/main-entry-after594-native-build.json
Review receipt: .analysis/work/main-entry-after594-native-review.json

Both actual source/response inputs, native OBJ/EXE/MAP vectors, complete
Japanese compact MZ products and four compiler/linker logs are retained.
The eight functions already belonged to the historical authored ledger,
so no duplicate source or Factory credit is claimed.

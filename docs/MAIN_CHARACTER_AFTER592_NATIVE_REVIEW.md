# MAIN character resource and BOSS-callback setup — after592

Nine playable character variants share one complete natural C++ first-use
producer, src/main/player/character_setup.cpp. It loads character resources,
selects sprites and installs the original charged-shot, bomb, boss update,
stage palette and round-background callbacks. The source retains original
character-specific function references and Borland local -a1/-a2 struct
packing rather than replacing callbacks with target-byte address tables.

A new tiny first-use translation unit
src/main/player/producers/character_setup_native.cpp includes that
unchanged implementation. Both independent original Turbo C++ 4.02
GAME=3/BINARY='M' compilation rounds produce exactly 3,888 original
HITCIRC_TEXT CODE bytes, 12 original PUBLIC function names/offsets,
1,135 literal ordered OMF FIXUPP fields, and the precise original
segment declarations, including the empty CH_SETUP_TEXT placeholder.
The historical original Borland OMF THEADR/COMENT dependency packaging
is different with the new source filename and is not claimed identical.

Each new original-source compiled ch_setup.obj was substituted in the
source-native after591 99-object MAIN link containing nine major BOSS
modules, the complete bullet/fireball/large enemy control and natural
collision code. Both normal TLINK outputs reproduce the exact entire
previous 132,322-byte native MAIN EXE and original MAP coordinates.
All 124,642 Japanese program bytes and 1,553 ordered original MZ
relocations are identical. A separate, explicitly identified standard
DOS MZ header serialization emits the complete 130,882-byte original
Japanese MAIN.EXE in both rounds.

The entire original character/BOSS callback group was already maintained
and represented in the function ledger. This is a reproducible full-source
cross-module integration proof, not a claim of newly discovered functions,
raw vendor OMF packet identity or canonical Factory acceptance.

Affected-only read-only verification:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_character_after592_work.py

Driver: scripts/build_th03_main_character_after592_work.py
Receipt: .analysis/work/main-character-after592-native-build.json
Review: .analysis/work/main-character-after592-native-review.json
The maintained common source, two actual compiler source materializations,
two native OBJ/EXE/MAP and compact EXE sets and four writer logs are retained.
No full cold replay was run.

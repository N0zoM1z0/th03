# MAIN original player movement, damage and shot control: after593

The maintained natural 16-bit source src/main/player/core.cpp owns the
original complete MAIN_010_TEXT player controller. It includes the
player movement and clamp, active/hyper state, damage processing and
hit testing, shooting setup, bomb activation and per-round player
state. Original segmented source-local Borland packing, optimization
flags and the 16-bit near/far calling conventions remain unchanged.

The new small first-use source unit
src/main/player/producers/core_native.cpp includes this complete
maintained C++ implementation. Two independent source materializations
under genuine Turbo C++ 4.02 GAME=3/BINARY='M' flags exactly reproduce
the original **3,135 CODE bytes**, **21 original PUBLIC functions**,
**260 ordered literal OMF FIXUPP fields** and complete four-segment
layouts, including the uninitialized CORE_TEXT placeholder.
The original vendor module source diagnostic records/COMENT packaging
do not need to be byte-identical to establish the verified native
linking scope.

Each newly compiled object actually replaces the source-native core
slot in the after592 normal MAIN linker response. That response
already includes nine original large BOSSes, the entire bullet/trail
engine, fireball/explosion, collision modules, natural keyboard,
four large enemy control objects and all nine character callback
sets. Both full native TLINK EXEs and original MAP coordinates match
the source-native parent. All **124,642 original Japanese loaded
program bytes** and **1,553 ordered MZ relocation entries** agree.

Using the separately verified ordinary DOS MZ container serializer,
both output files reproduce the **entire 130,882-byte original Japanese
MAIN.EXE** byte-for-byte. This does not claim that historical TLINK
directly wrote that compact MZ header.

Read-only affected review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_core_after593_work.py

Native driver: scripts/build_th03_main_core_after593_work.py
Source report: .analysis/work/main-core-after593-native-build.json
Read-only result: .analysis/work/main-core-after593-native-review.json

The 21 functions are historical original source owners: no duplicated
authored-function credit, whole-project source completion or canonical
Factory acceptance is inferred. No full cold replay was executed.

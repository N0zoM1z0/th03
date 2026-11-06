# MAIN native hitbox, animated hitcircles and 386 collision map

This stage combines complete original collision semantics from three
independently maintained real-mode C++/assembler sources:

| Original source producer | Native source | CODE | PUBLIC | Ordered OMF FIXUPP |
| --- | --- | ---: | ---: | ---: |
| hitbox.obj | src/main/collision/hitbox.cpp | 266 | 1 | 33 |
| hitcirc.obj | src/main/collision/hitcircle.cpp | 445 | 4 | 30 |
| collmap.obj | src/main/collision/map.asm | 432 | 3 | 27 |
| Total | Three original complete modules | 1,143 | 8 | 90 |

The 16-bit hitbox code performs shot-pair, explosion and charged-shot
damage, preserving the original 16-bit stack and near/far calling rules.
The HitCircle C++ source handles enemy/player hit indicators, sprite
cels, clipping, animation and rendering. The 386 collision-map TASM
source performs the bit-striped rectangle/vertical/slope map writes.
It includes natural loops and mutable source variables, not opcode
arrays or a patched object image.

## Failed natural C++ hypotheses retained

A previous source note suggested replacing an original inline call with
ordinary natural C++ damage addition. Three real Turbo C++ variants
were compiled: direct C++ call, AL-return assignment and casted near
function pointer. All compile and produce 266-byte objects, but at
hitbox CODE+207 they emit 9Ah direct FAR CALL instead of the original
90h 0Eh E8h sequence (NOP, PUSH CS, near CALL). Their OMF FIXUPP
fields also differ. These are **negative compilation evidence**, not
a basis for replacing the original working source.

The original maintained 16-bit inline-call convention was preserved;
the three failed source variants and their compiled objects/logs are
retained under TH03WORK/probe/af590h. A separate original long
DOS-path experiment failing at filename conversion was also preserved
under TH03WORK/probe/af590hittest-natural-try.

## Complete normal source-native MAIN link

The three original source files were freshly compiled/assembled in
two independent rounds with original GAME=3/BINARY='M' TC4/TASM flags.
Both rounds reproduce all 1,143 initialized original CODE bytes,
all 90 ordered literal OMF fixups, all eight PUBLIC names/positions
and exact original segment geometry. Raw Borland OMF source module
packet identity is not asserted.

These three objects were substituted simultaneously into the after589
source-native MAIN link, already containing nine BOSSes, bullet/trail
and GRCG code, fireball/explosion generation, enemy scripts and
keyboard. Both TLINK runs reproduce the entire retained source-native
MAIN EXE and exact original MAP allocations. All 124,642 original
Japanese loaded program bytes and 1,553 ordered MZ relocations match.
The independently source-derived standard MZ container step reproduces
the **entire original 130,882-byte Japanese MAIN.EXE** in both rounds.

Run the read-only affected proof (no cold replay):

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_collision_after591_work.py

Producer: scripts/build_th03_main_collision_after591_work.py
Report: .analysis/work/main-collision-after591-native-build.json
Review: .analysis/work/main-collision-after591-native-review.json

No original machine code, old C++ input, vendor OMF, binary target or
source-ownership ledger was patched. These eight functions were already
represented in historic authored-function evidence; no duplicate credit
or canonical Factory acceptance is claimed.

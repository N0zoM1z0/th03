# MAIN fireball generator and large explosion collision controller: after589

Two complete natural C++ producers, not omitted large functions, are now
recompiled from their original maintained source on real Turbo C++ 4.02
GAME=3/BINARY='M' first-use flags:

- src/main/enemy/fireball.cpp: the complete original E_FIREB_TEXT
  1,555-byte CODE body, one initialized DATA byte, one BSS byte,
  10 original PUBLIC declarations and 115 ordered OMF fixups.
  This contains inter-playfield fireball transfer, red/blue generation,
  velocity transitions, animation, rendering, explosions and collision
  dispatch. Original generation_prev and charged-chain behavior remains.
- src/main/enemy/expl.cpp: the complete 630-byte E_EXPL_TEXT
  explosion_hittest non-leaf collision controller with 49 ordered
  original OMF fixups and a true original PUBLIC entry. It handles
  chained explosion and projectile/enemy hit processing.

The two fresh source forwarding TUs are under
src/main/enemy/producers. They include the original maintained C++ code
unchanged, rather than copying a flattened source or machine-byte body.

Two fully independent source-native compiler rounds verified every original
initialized CODE/DATA byte, original literal OMF FIXUPP site and its order,
all original PUBLIC locations, BSS allocation and segment ABI.
Raw vendor OMF source dependency/COMENT/LNAMES packet equality is not
asserted when module diagnostic paths differ.

Both new source objects were simultaneously substituted into the after588
MAIN normal TLINK response, which already contains the complete source-
native bullet engine, 386 GRCG pellet renderer, nine major BOSS modules,
four natural enemy script/hittest producers and original keyboard source.
The entire source-native MAIN EXE and original MAP coordinates remain
unchanged. The complete 124,642 Japanese original load-image bytes and
all 1,553 ordered MZ relocation entries agree in both rounds.

The separate source-derived standard DOS MZ container step also emits
the entire 130,882-byte Japanese original MAIN EXE exactly. This is
**not** a claim that native TLINK directly emitted the compact historic
MZ header, nor that every game source has gained canonical acceptance.

Read-only affected evidence review, without a full cold replay:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_fireball_after589_work.py

Producer: scripts/build_th03_main_fireball_after589_work.py
Native report: .analysis/work/main-fireball-after589-native-build.json
Reviewer: .analysis/work/main-fireball-after589-native-review.json

Both actual compiler source wrappers, OBJ/EXE/MAP outputs, two compact MZ
files and all six original native writer logs remain retained. These
functions were historical source owners, not new ledger denominator credit.

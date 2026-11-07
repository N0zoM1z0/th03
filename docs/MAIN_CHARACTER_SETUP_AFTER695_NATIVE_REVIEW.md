# TH03 character resource loader and nine callback selectors: original-native after695

The full original `ch_setup` physical Turbo C++ 4.02 translation unit is
a substantial **3,888-CODE-byte** owner in HITCIRC_TEXT. It contains
the resource filename/sprite-pair loader, sprite postprocessing and
nine separate, fully linked character callback selectors (not
a small isolated helper). The selectors own character chargeshot,
Extra Attack, BOSS, Bomb, hyper and background chain dispatch,
including distinct player-0/player-1 paths.

## Original physical compiler and linker slot

The historical source-native full MAIN TLINK response uses
`probe/af592p/r1/ch_setup.obj` (and r2), **not**
`obj/th03/ch_setup.obj` as a linker input. The independent
source-native driver now selects that exact historical slot
without modifying the original response, while comparing
the emitted object with the original physical owner.
The smaller `p_gauge` object was also discovered in the
same original-baseline probe to have only **three**
MAP ownership rows, instead of an assumed generic four.
The joint unchanged-source source-OMF-attested control
`af694c` proved 3,943 CODE bytes across both owners.

## Actual C++ reconstruction and negative evidence

- In the shared 12-byte resource filename copy helper,
  `for(int i=0; i<12; ++i)` naturally replaces the old
  postincrement, with exact native codegen (af694d).
- The character callback macro now uses ordinary C++
  `if(!pid)` for the first player's callback branch,
  and emits exact original CODE for **all nine**
  character-specific selector instantiations (af694f).
- All nine original odd MRS resource pair IDs 1,3,...,17
  are now named by character in a compiler-time enum.
  Their original resource pairing and second-player
  sprite mirroring/hardware hooks remain intact
  without new DATA or runtime state (af695a).
- The file loader's decimal ones-place update is written
  as `resource = resource % 10` instead of an
  assignment remainder operator. The real original
  TC4 emitted identical 16-bit CODE (af695b).
- Crucial negative test: replacing the resource
  palette bit `players[pid].playchar_paletted.v & 1`
  with explicit unsigned `% 2` **changed original
  native instructions** (af694e). The real mask
  remains; numerical equivalence is not enough
  to prove original compiler output.

Final genuine modified-source/OMF-COMENT-attested
two-round original TC4.02 compiler/full normal MAIN
TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af695c --units ch_setup
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af695c

Both compiler rounds reproduce **all 3,888 original
CODE bytes, 1,135 literal ordered native FIXUPP
fields and twelve PUBLIC offsets**, all OMF
segment/data/BSS metadata, complete normal MAIN
EXE, full path-normalized MAP, the original
Japanese loaded image, all 1,553 ordered MZ
relocations and the independently serialized
original 130,882-byte Japanese MAIN.EXE.

Retained actual native/source writer evidence:
`.analysis/work/exatt-layout-af695c/report.json`;
SHA-256 `f82ad48826472c2a555f8a4f3c57a3dc4095ecfc81336fc2f096b01c32f1dc2b`.
Only this one affected complete original physical
translation unit was rebuilt twice, reusing 98
other project objects and startup/CRT libraries.
No whole cold replay or original object patching.

The original CODE was previously source-owned.
This proof does not imply new canonical Factory
packed-game byte credit, historical vendor raw
OMF packet-byte identity or actual PC-98 runtime.

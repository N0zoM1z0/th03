# Two previously unselected MAIN physical owners: transition and round RNG

The maintained natural C++ stage-demo wipe in
`src/main/round/demo_transition.cpp` is now source-bound to the genuine
`tr_ctx.obj` (663 initialized CODE bytes, 74 native ordered fields, three
PUBLICs). The three near callbacks own both opposing triangular wipes,
clip-window updates, mask phases and frame state transitions. Original
TC4 4.02 stage `af1333a` reproduced the entire physical object and both
normal Japanese MAIN links without modifying any other project OBJ.

The other new physical owner is the original `roundpr.obj` (82 CODE
bytes, nine literal native fixup fields, four PUBLICs). Its maintained
symbolic `src/main/round/roundpr.asm` composes the actual project
`randring_getters.inl`, `randring_fill.inl` and `collision/reset.inl`.
These supply the far IRAND seeded fill, near Pascal RNG getter/AND
functions and collision-map zeroing. The source carrier preserves the
six original _TEXT/PLAYFLD/CFG_LRES/HITCIRC/DATA/BSS MAP rows and the
original 16-bit public layout. Source-bound TASM/TLINK stage `af1333c`
reassembled the complete owner twice and reproduced both original normal
MAIN executables byte-for-byte with normalized MAP and ordered MZ
relocations equal. The three included source files were checked against
the versions consumed by TASM, not inferred from a filename alone.

These add two genuinely distinct original physical source-bound objects
to the active inventory; the corresponding authored function regions were
already present in the ledger. Other project objects and CRT remained
unchanged, and no full cold build ran.

Read-only current source checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1333a
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_roundpr_asm.py --stage af1333c --check
```

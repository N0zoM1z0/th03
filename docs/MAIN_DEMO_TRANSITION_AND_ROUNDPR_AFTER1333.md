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

## Pre-tested stage wipes and TC4 enum signedness (2026-11-11)

Both closing checkerboard passes and the uncovering four-triangle pass
now use pre-tested `while` traversals with a signed 320-pixel second-
playfield offset. Each iteration draws before advancing the original
signed index; the original clip windows, alternating masks, GRCG calls,
16-frame callback changes and 16-bit assembly arguments are unchanged.

An independent original TC4 compiler experiment established a subtle
constraint: naming `320` in the **same enum** as high-bit `0xAAAA` and
`0xFFFF` masks (`af1367m`) changes the entire physical CODE. Its
unsigned enum type affects the signed loop-bound comparison. Separating
the small signed offset/frame constants from the hardware mask enum
(`af1367n`) restored native equality. This avoids any ad hoc byte patch.

Stages `af1367h`–`af1367j` proved all three loop rewrites. Stage
`af1367l` proved named masks, `af1367n` the separated enum types and
`af1367o` the named 16-frame phase deadline. Current source-bound
`af1367p` reproduces all **663 CODE bytes, 74 ordered native fields,
3 PUBLICs**, with two original TC4 rounds and exact normal MAIN links.
Joint `af1367q` recompiles Stage Demo Transition, MAIN entry, HitCircle
and Hitbox: **4,424 CODE bytes, 570 fields, 16 PUBLICs**, complete
original Japanese MAIN images and ordered relocations in both rounds.

Current proof: `.analysis/work/exatt-layout-af1367p/report.json`, SHA-256
`e1084a402afd1834456f0ae54f878424491e48a502381ec698b00f724e36f828`.
Joint proof: `.analysis/work/exatt-layout-af1367q/report.json`, SHA-256
`4fa89068a2e31391e78407b4fe8dffd373df7610e6a45e78f20a3d124e336af9`.

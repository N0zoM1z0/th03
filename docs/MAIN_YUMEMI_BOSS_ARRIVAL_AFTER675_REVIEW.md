# Yumemi major BOSS arrival: four original-native natural C++ geometry phases (after675)

This verifies source recovery in the *complete original*
2,358-CODE-byte nine-function Yumemi major BOSS owner,
not merely isolated leaf machine instructions. The long
arrival renderer draws four stages of moving, repeated
112x112 sprites with deliberately ordered pixel positions
and corresponding collision/intro state transitions.

The historical original code advances sprite origin by
two consecutive 16-bit left shifts:
    ((boss_frame << 3) << 4)
and, in the other three phases:
    ((phase << 3) << 4)

These are now **natural C++ expressions with the same two
ordered scaling stages**:
    ((boss_frame * 8) * 16)
    ((phase * 8) * 16)

The original Borland Turbo C++ 4.02 compiler generates
the same exact instructions for the changed source.
Genuine current-source independent two-round native checks
`af675a` (unsigned boss frame) and `af675b`
(all three eight-bit phase paths) reproduce the original
whole 2,358-byte object.

A tempting simplification of one phase to just
`phase * 128` changed original TC4 CODE (`af675c`).
The actual first-then-second operation sequence matters
to old compiler scheduling. That original-unequal variant
is rejected and the four native-equal two-stage natural
C++ expressions are retained.

The source leaves the original PC-98 sprite overlap
XOR DX,DX instruction, hardware INT service calls,
screen clipping, forward/reverse draw order and
original frame boundaries unchanged. It does not
introduce new initialized DATA/BSS or target-derived bytes.

Final two-round original TC4/TLINK source-OMF-proven result:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af675d --units ba_yumem
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af675d

Both native object rounds match **all 2,358 original CODE bytes,
343 literal ordered FIXUPP fields, ten PUBLIC offsets** and
all original OMF segment metadata. Both full normal MAIN
EXEs and path-normalized MAPs agree with the retained
source-native original, as do the loaded Japanese game
image, all 1,553 literal ordered MZ relocations, and
the separately serialized exact 130,882-byte original
Japanese MAIN.EXE.

Retained actual-source, original writer and linked proof:
`.analysis/work/exatt-layout-af675d/report.json`,
SHA-256 `71193cc240c75b785c625efa22f11c3c102f072116f70e6bef04da611100208f`.
Only this one complete physical BOSS object was rebuilt
in two genuine rounds. Other 98 original project
objects and startup/CRT inputs were reused, without
a full cold replay or object byte patch.

This improves maintainable C++ over already accepted
source-owned CODE bytes; it is not new Factory packed-game
canonical byte credit, historical raw vendor OMF packet
byte identity or actual PC-98 runtime proof.

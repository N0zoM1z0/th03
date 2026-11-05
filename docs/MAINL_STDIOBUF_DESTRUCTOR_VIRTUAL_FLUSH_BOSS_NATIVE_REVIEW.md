# Original stdiobuf virtual destructor, RTTI and overflow flush — after451

Original Japanese Borland `CL.LIB` member `sdbdtr` (index **826**) is
now recovered as actual native [8086 source](../src/mainl/crt/sdbdtr.asm).
The full FAR C++ destructor decrements the 32-bit destructor reference
counter, conditionally resets the dynamic vtable, makes the actual
**virtual overflow(-1) call** through slot DATA+24, destroys its
`streambuf` base with the original destructor-flag argument and
optionally deletes the outer far object. The virtual call is not
mistaken for a direct external `overflow` call: its full `this`/argument
layout and indirect dispatch through the object vptr are preserved.

All **224 original CODE + 52 initialized DATA** bytes are source-equal,
including the complete Borland typed `stdiobuf` RTTI at CODE+96 and its
`streambuf` ancestor RTTI at CODE+164. The DATA-backed RTTI and all
**11 original far virtual-function symbols** are genuine typed external
references, not zero placeholders. The **19 logical original OMF
FIXUPPs** match at all sites, widths, addends, frame methods and
actual targets, including CODE+37 -> DATA+8, the far base destructor
at CODE+66 and DATA+0 -> CODE+96. Borland's literal FIXUPP record
chronology still differs from the TASM object; raw original record
serialization is *not* claimed.

The after451 producer independently validates the inherited after450
native source-bound carrier, then performs **two fresh TASM/TLIB/TLINK
rounds** retaining both raw OBJ/LIB/EXE/MAP vectors, logs and source
hashes. Both complete decoded Japanese MAINL EXE/MAP equal the target,
with a 67,372-byte EXE and 677 ordered DOS MZ relocations. Working
CRT: **659/893** original source-linked members, **177,307** source
CODE bytes and 234 contextual vendor members. This is bounded working
source evidence, not Factory formal accepted-source credit or a full
cold replay.

Focused reviewer: scripts/review_th03_mainl_after451_work.py
(mode stdiobuf-virtual-destructor-boss); tests: tests.test_mainl_after451_work.

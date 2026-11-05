# Complete original filebuf::close, virtual flush and DOS descriptor — after453

The live Japanese Borland `CL.LIB` `fsbclose` member (slot **707**) is
now recovered as maintained [8086 source](../src/mainl/crt/fsbclose.asm).
The complete C++ FAR `filebuf::close` checks the original -1 descriptor
and open flag, returns null for an unopened buffer, calculates the
pending put area, and conditionally invokes the **genuine virtual
`overflow(-1)`** method using the object's DATA-backed vtable at
slot +24. It also calls the original far DOS `_close`, clears the
filebuf descriptor and attached state, then returns the actual far
`this` only if both flushing and closing succeeded. Both native
failure paths and the original 16-bit ABI are retained; no extra
safety/cleanup behavior was inserted.

The complete **174 CODE bytes**, original `_TEXTA`/`_DATA`/`_BSS`
segments, DATA-first GROUP, public and sole `_close` import match
original. The original `_close` call's **literal ordered OMF FIXUPP**
at CODE+125 agrees exactly with TASM, including segment, site,
frame/target method, width, and addend. There are no initialized
DATA bytes or patched target machine-code arrays. This member's
literal FIXUPP equality does not imply that every OMF record in the
entire vendor program is identical.

The after453 producer checks the retained after452 660-source CRT
and performs two independent native TASM/TLIB/TLINK rounds, keeping
all logs/source hashes and raw OBJ/LIB/EXE/MAP round outputs. Both
complete Japanese decoded MAINL EXE/MAP equal their targets, with
67,372 bytes and 677 ordered MZ relocations. The working CRT now
contains **661/893** source members, **177,672 original-equal CODE
bytes**, with **232 original library members still contextual**.
No Factory canonical source acceptance or full cold replay is claimed.

Reviewer: scripts/review_th03_mainl_after453_work.py (mode
filebuf-close-flush-and-descriptor). Tests: tests.test_mainl_after453_work.

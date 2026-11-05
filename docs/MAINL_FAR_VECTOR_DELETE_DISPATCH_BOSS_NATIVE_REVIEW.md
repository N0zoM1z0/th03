# Original far vector deletion and destructor-count dispatch — after462

The original Borland Japanese CL.LIB member vdelxf (slot **142**)
has been recovered in maintainable [8086 source](../src/mainl/crt/vdelxf.asm).
This is the complete far C++ array destruction routine, rather than
only its small leaf dispatcher. The real control flow processes hidden
element-count and ownership flags, selectively obtains vector metadata
from the caller stack or before the allocated pointer, invokes the
native near 32-bit N_LXMUL@ to adjust the global destructor reference
counter, and calls the full far vector-deletion helper with either
the 14- or 16-byte ABI argument list.

All **215 original CODE bytes**, all original group/segment definitions,
the real FAR exported symbol and three ordered externs match the
original. The four OMF fixup sites, target names, types and addends
match: CODE+118 N_LXMUL@, CODE+123 the global destructor count,
and CODE+171/+202 the correct far deletion helper. Of these,
**three logical OMF fixups** match completely. The sole difference
is Borland's TARGET frame method 5 versus TASM's CODE segment frame
method 0 on the actual near N_LXMUL@ call at CODE+118. The
builder permits only this exact site/target/frame alternative,
and the focused test checks the other fields individually.
Literal ordered original FIXUPPs and whole OBJ serialization therefore
are **not** claimed identical; no code-byte fixtures or patches were used.

After462 validates the complete retained after461 669-member carrier
and performs two fresh TASM/TLIB/TLINK native rounds, preserving
OBJ/LIB/EXE/MAP pairs, source hashes and the writer logs. Both
67,372-byte Japanese decoded MAINL EXEs and their MAPs are
byte-for-byte identical to the target; all 677 ordered MZ
relocations survive. Working CRT: **670/893 source-linked members**,
**179,995 source CODE bytes**, 223 contextual vendor members.
This is *not* a full cold replay or formal Factory acceptance.

Focused reviewer: scripts/review_th03_mainl_after462_work.py,
mode far-vector-delete-dispatch-boss;
tests: tests.test_mainl_after462_work.

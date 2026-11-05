# Original FAR heap linear search / find+insert boss — after469

Japanese Borland CL.LIB member hlsearch (original slot **466**) is
now maintained in [8086 source](../src/mainl/crt/hlsearch.asm).
This is the complete original private near search core at CODE+0,
plus public FAR __hlsearch at CODE+124 and __hlfind at +167.
It traverses a FAR array using the actual caller-provided FAR
comparison callback and Borland near N_PADA@ stride arithmetic.
The insert-enabled entry increments the actual array count and
uses the genuine FAR __fmovmem to insert; find-only returns
null without mutating the count. The exact 16-bit parameter order,
FAR pointer result and near callee-pop-20 ABI are preserved.

The complete **209 original CODE bytes**, zero DATA/BSS, three
real entrypoint offsets, two ordered imports and all original
segment/group metadata match the original Japanese CL.LIB member.
All original OMF relocation sites, targets, types and addends
match. The FAR __fmovmem fixup at CODE+91 is fully identical;
the NEAR imported N_PADA@ call at CODE+52 uses Borland
TARGET-frame method 5, whereas TASM selects CODE-frame method 0.
The scoped builder permits only that exact site/target/frame
alternative and its test asserts every other field unchanged.
Literal original FIXUPP record equality and raw complete Borland
OBJ program equality are not claimed; no target-byte fixtures,
padding or post-assembly patches are used.

After469 verifies the retained after468 676-source original CRT
carrier and builds two fresh TASM/TLIB/TLINK rounds with entire
OBJ/LIB/EXE/MAP vector, writer logs, and source hashes retained.
Both Japanese decoded MAINL EXE/MAP are byte-for-byte target-equal,
including the 67,372-byte EXE and 677 ordered MZ relocations.
Working CRT: **677/893** original source-linked members,
**181,413 original-equal CODE bytes**, 216 contextual vendor members.
This is not full cold replay or Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after469_work.py,
mode far-heap-linear-search-boss.
Tests: tests.test_mainl_after469_work.

# Giant cplx2: all 22 original FAR bodies and CRT initializer recovered

Japanese Borland CL.LIB original member cplx2 (slot 209) has **5,598 CODE
bytes, 63 DATA bytes, an empty BSS segment, six INITDATA bytes, and
22 original public FAR complex math and stream functions**. The
[maintained natural 8086/x87 source](../src/mainl/crt/cplx2_all_bodies_partial_omf.asm)
now implements **all 22 FAR public bodies** plus the private original
CODE+5575 CRT initializer. This is no longer a function-body coverage
gap: the remaining obstacles are exact assembler encoding/OMF and
complete target-link identity, not omitted complex algorithms.

Two important native functions have been added after the twenty-function
checkpoint. The 178-byte original ostream insertion at CODE+5091..5268
prints the original typed strings "(" (DATA+56), ", " (+58), and ")"
(+61) with native ostream::outstr and two true 80-bit long-double insertions.
The 306-byte istream extraction at CODE+5269..5574 parses one or two
double components, handles opening/closing delimiters, putback, failbit
clear, stream-state checks and the genuine near N_SCOPY@ 16-byte result
transfer. It is followed by a private 23-byte FAR CRT initializer at
original CODE+5575..5597, which uses real fldz/fstp x87 instructions
to initialize the two deliberately unmaterialized DATA+0/+8 qwords.
The six original INITDATA bytes contain priority 2001h and a symbolic
FAR pointer to that private initializer. All **47 initialized DATA
bytes at +16..62**, including typed math constants and three stream
strings, agree with original CL.LIB.

**CODE exactness with explicitly bounded gaps.** Borland's 5,598 CODE
bytes correspond to 5,596 natural TASM output bytes: two direct
same-segment FAR CALLs at original CODE+799/+984 are emitted by
TASM as four-byte PUSH CS plus near CALL, each one byte shorter.
After aligning at those two known instructions, all **5,588 remaining
native CODE bytes** are original-equal, including both new stream bodies
and the complete native zero initializer. All 22 public names/offsets
agree after the two one-byte shifts. INITDATA's symbolic initializer
pointer consequently has original addend 5575 and native addend 5573,
which correspond to the same function identity.

**OMF exactness limits.** Original cplx2 contains **860** OMF relocations
(859 CODE and one INITDATA); TASM emits **858** (857 CODE and one
INITDATA). All 857 emitted CODE relocation fields match original
sites after the shifts, target symbol names, location widths and
addends. The INITDATA relocation is also checked, accounting for its
two-byte shifted CODE addend. The two missing originals are the
same-segment FAR calls. Of the original CODE relocations, **734
Borland FPU frame-method-4 references** compile with TASM method 5.
The final original imported near N_SCOPY@ call at CODE+5561 has
target-frame method 5 but TASM emits CODE-frame method 0.
This last distinction is explicitly site-locked and is *not*
normalized or described as original raw OMF identity.
These differences prevent any claim of exact original raw OBJ.

The [independent scoped verifier](../scripts/probe_th03_cplx2_full_body_partial_omf.py)
executes two real TASM rounds, verifies all aligned CODE,
all initialized/unmaterialized DATA semantics, all public
exports, complete segment layout, native INITDATA pointer,
all emitted relocations and nonvolatile OMF stability.
Targeted test: tests.test_cplx2_full_bodies_partial_omf.

**Credit and next steps:** This is a major natural source reconstruction
but not yet an accepted source-linked original CRT member. A
complete original-equal native MAINL EXE/MAP is *not* claimed,
and **zero** full CRT source members/Factory units are earned by
this artifact. Repair the two direct FAR-call encodings and the
original Borland OMF frame representation, then attempt a
source-bound full member link; preserve all current proofs and
never patch target executable or OBJ bytes. No full cold replay.

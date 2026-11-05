# Original cplx2: seventh complete FAR atan(complex) function (scoped source)

The giant Japanese Borland CL.LIB complex math member cplx2
(index 209) contains **5,598 original CODE bytes and 22 FAR
public entrypoints**. Maintained
[8086/x87 source](../src/mainl/crt/cplx2_seven_functions_partial.asm)
now includes seven complete FAR function bodies: three division
operators, acos, arg, asin, and the new **atan(complex)**.

The seventh atan body is original CODE+1608..1890, **283 completely
original-equal machine-code bytes**. The new source reproduces its
real/imaginary double-precision operations, FPU stack ordering,
x87 emulation references, 2.0f typed numeric constant, FAR
abs(complex) and log() calls, native near arg(complex) invocation,
and the hidden result object pointer or 16-byte FAR allocation
ABI. It is natural assembly, not a target opcode byte array.
Its complete function-body machine code is identical to Borland,
including original control flow and local stack offsets.

The original first seven complete functions cover CODE+0..1890,
**1,891 original CODE bytes**, of which TASM emits **1,889
CODE bytes**. The two missing bytes are exclusively the two
previously identified one-byte local FAR-call shortenings in
acos at original CODE+799 and +984 (direct FAR CALL versus
TASM PUSH CS + NEAR CALL). Outside those two precisely
disclosed encoding gaps, all **1,881** aligned source CODE
bytes are original-equal, including all new atan bytes.

The prefix has **297 original OMF FIXUPPs**, of which **295
native symbolic relocations** match original sites (after
aligning the two call shifts), target symbol names, location
kinds/widths and addends. The two original local FAR calls
retain original CODE-target fixups not emitted by TASM.
There are **261 original Borland location-frame method 4**
FPU fixups; native TASM EMUL expresses them with method 5.
This remains explicitly disclosed rather than silently
normalized into a false raw OMF identity claim.
The original DATA+0..15 remains unmaterialized, and all
12 initialized DATA+16..27 bytes match.

The [scoped native checker](../scripts/probe_th03_cplx2_atan_partial.py)
performs two complete native TASM assembler rounds under the
same writer lock, re-checks every aligned instruction byte
and every emitted symbolic relocation against the original
CL.LIB record, and checks all nonvolatile OMF records
between rounds (not hiding an optional COMENT build-time byte).
Focused test: tests.test_cplx2_atan_partial_native.

**Scope limit:** the remaining 3,707 CODE bytes, 15 later
FAR public bodies, complete original DATA/INITDATA and exact
original frame-4 fixup serialization still need recovery.
This is a real large-Boss source advance, but cplx2 is **not**
one complete source-linked CRT member and earns **zero**
new source-member or Factory acceptance credit. No full
cold replay, binary patch or complete MAINL link is
claimed for this partial artifact.

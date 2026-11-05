# Large complex-math cplx2: seventh complete FAR atan(complex) function

Original Japanese Borland CL.LIB cplx2 (slot 209) is a
**5,598-CODE-byte, 22-public** complex math/iostream boss.
The maintained
[partial 8086/x87 source](../src/mainl/crt/cplx2_seven_functions_partial.asm)
now has **seven entire natural FAR function bodies**, namely
three complex division overloads and acos, arg, asin and
the new **atan(complex)** at original CODE+1608..1890
(**283 original-equal instruction bytes**).

The new atan body uses genuine x87 register/stack instructions,
real-double squaring and normalization, FAR complex
real/imaginary division, the original constants at
DATA+16 and +24, genuine FAR abs(complex)/arg(complex)
and _log calls, and the original conditional FAR
16-byte result allocation. Its natural source maintains
the original Borland local-variable locations, return
ABI, signed operations and x87 wait semantics.
No target executable byte arrays or filler instructions.

The complete original prefix CODE+0..1890 now totals
**1,891 CODE bytes**. Native TASM produces **1,889**:
the sole persistent CODE differences are the two
previously discovered 1-byte shortened local FAR calls
inside acos at original CODE+799 and +984. With these
two exact gaps accounted for, **all other 1,881 CODE
bytes are original-equal**, including the entire 283-byte
new atan function.

Of **297 original OMF FIXUPPs** in this prefix,
**295 emitted native references** match the original
site (after those two call-length shifts), location
kind/width, symbolic imported target, segment
relation and addend. The two same-CODE FAR-call
FIXUPPs are absent in TASM's encoding. Exactly
**261 original Borland x87 location-frame method-4
references** emit as TASM method 5. We preserve
that discrepancy explicitly; raw original Borland
FIXUPP frames and total OBJ program identity
are **not** claimed equal.

The independent
[scoped seven-function checker](../scripts/probe_th03_cplx2_atan_partial.py)
compiles the source twice with real native TASM,
verifies all mapped CODE bytes and every original
target name and addend, and compares all nonvolatile
OMF records across rounds (permitting only an observed
TASM COMENT timestamp byte to vary).
The targeted test is tests.test_cplx2_atan_partial_native.

**This is partial large-Boss progress**, not a finished
library member. The remaining 3,707 original CODE
bytes, 15 later public functions, complete original
DATA/INITDATA and exact method-4 framing are not
yet recovered. No full native MAINL EXE/MAP
link is claimed for this partial source, and it
adds zero complete CRT members or Factory
accepted-source credit. No full cold replay
was run.

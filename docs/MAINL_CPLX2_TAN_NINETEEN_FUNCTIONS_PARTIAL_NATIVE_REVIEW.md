# Original cplx2: nineteenth complete FAR tan(complex) body

The Japanese Borland cplx2 CL.LIB member (slot 209) has
5,598 CODE bytes and 22 FAR complex math/stream public
interfaces. The maintained
[8086/x87 partial source](../src/mainl/crt/cplx2_nineteen_functions_partial.asm)
now reproduces **nineteen complete FAR function bodies**
through original CODE+4780. New tan(complex) at original
CODE+4429..4780 is **352 original-equal CODE bytes**.

The genuine tangent routine evaluates native FAR sine/cosine
of the real component and the exponential of the imaginary
component, preserving the original 80-bit exponential and
reciprocal temporaries. It builds the denominator from
two squared intermediate terms, divides the two original
signed numerators by that value, and uses the conditional
original 16-byte FAR result allocation ABI. The real
DATA+52..55 constant is **4.0f**, verified from the
Japanese original rather than guessed from a simplified
mathematical identity. All 40 initialized DATA+16..55
bytes are original-equal, while DATA+0..15 remains
genuinely unmaterialized.

Original CODE+0..4780 is **4,781 bytes**; TASM emits
**4,779**, owing only to the two established shorter
same-CODE FAR calls in acos at original CODE+799/+984.
All other **4,771 aligned source CODE bytes** match,
including the whole tan function. All nineteen public
names and original offsets match after the two shifts.
Of **750 original prefix OMF FIXUPPs**, all **748
emitted symbolic native references** agree by location,
target name, width, kind and addend. The two original
local FAR-call fixups remain absent, and **649 original
Borland frame-method-4 x87 references** are emitted
as method 5 by TASM EMUL. These unresolved differences
are explicitly recorded; complete raw Borland OBJ
identity is not claimed.

The [native scoped verifier](../scripts/probe_th03_cplx2_tan_partial.py)
runs two real TASM rounds, compares every aligned CODE,
typed DATA, all nineteen public offsets and 748 emitted
original-symbol fixups, and checks nonvolatile OMF stability.
Focused test: tests.test_cplx2_tan_partial_native.

**Incomplete remainder:** 817 original CODE bytes and
three FAR public functions, additional original DATA
and INITDATA, and full original frame-4 serialization.
This source is a real partial large-Boss advance but
does not claim a complete cplx2 CRT source member,
a full decoded MAINL EXE link or Factory acceptance.
No full cold replay was run.

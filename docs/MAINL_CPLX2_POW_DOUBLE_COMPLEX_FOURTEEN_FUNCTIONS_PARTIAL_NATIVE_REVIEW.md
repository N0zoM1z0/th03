# Giant cplx2: fourteenth complete FAR pow(double, complex) function

Original Japanese Borland CL.LIB cplx2 contains 5,598 CODE bytes
and 22 complex mathematics/stream FAR functions. The
[maintained original x87 source](../src/mainl/crt/cplx2_fourteen_functions_partial.asm)
now implements **fourteen complete original FAR function bodies**.
The new pow(double,complex) function occupies original
CODE+3226..3531: **306 machine-code bytes individually verified
byte-for-byte**, including actual floating-point comparisons and
the exceptional scalar-zero / negative-power path, _fabs / _log
on the scalar base, the negative-base branch with complex*pi
multiplication, and the same-CODE complex exponential call.
This is natural 8086/x87 source, not an opcode byte fixture.

The original CODE+0..3531 prefix is **3,532 bytes**; TASM emits
3,530, due only to the two known acos local direct-FAR-call
shortenings at original CODE+799 and CODE+984.
All remaining **3,522 aligned source CODE bytes** are original-equal.
Original DATA+0..15 is unmaterialized as genuine uninitialized
storage. All **28 original initialized DATA+16..43 bytes** now
match, including a naturally declared double-valued pi constant
at DATA+36..43. The original **546 prefix OMF FIXUPPs**
contain two same-CODE FAR calls absent from TASM's compressed
encoding; all **544 emitted native references** match the original
sites after the two shifts, import names, widths and addends.
**473 original Borland FPU location-frame method-4 references**
compile as method 5 with TASM EMUL. These remain explicitly
unresolved and are not counted as raw original OMF equality.

An earlier in-progress scratch OBJ contained a two-byte x87
WAIT/NOP discrepancy after a local FSTP, but inspection of the
actual retained working source showed that correction had already
been made. Reassembling the **current dirty source** produced the
original 306-byte function body exactly, rather than restoring the
stale scratch product. All symbol targets were then audited anew.

The [independent scoped verifier](../scripts/probe_th03_cplx2_pow_double_complex_partial.py)
compiles **two native TASM rounds** under the writer lock,
checks aligned CODE, initialized DATA, 544 complete symbolic
relocations and nonvolatile native OMF equality. Focused tests:
tests.test_cplx2_pow_double_complex_partial_native.

**Remaining work:** 2,066 CODE bytes and eight more original
FAR functions, full DATA/INITDATA and original method-4
framing. The two shortened FAR calls are still unresolved.
This source is **not a full linked cplx2 CRT member and earns
zero new complete-member or formal Factory accepted credit**.
No full cold replay was run.

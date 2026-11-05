# cplx2 ninth FAR cosh(complex) — original code and relocation audit

Japanese Borland CL.LIB member cplx2 is a **5,598-CODE-byte, 22-public**
complex-math boss. The maintained
[partial 8086/x87 source](../src/mainl/crt/cplx2_nine_functions_partial.asm)
now reconstructs **nine entire FAR function bodies**: three
division overloads, acos, arg, asin, atan, cos and cosh.

**New in this scope:** the complete original cosh(complex)
at CODE+2124..2357, **234 byte-identical original CODE bytes**.
The source implements the real exponential on the complex
real component, sine/cosine of the imaginary component,
the original 80-bit floating intermediates, x87 multiply
and division with typed 2.0f DATA, and the hidden 16-byte
FAR result allocation ABI. This is natural source, not copied
executable bytes, NOP padding or postprocessing.

The original prefix CODE+0..2357 totals **2,358 bytes**;
native TASM emits **2,356**. Only two historical local
acos FAR calls at original CODE+799/+984 are one byte
shorter as native PUSH CS + NEAR CALL rather than direct
five-byte FAR CALL. Apart from these two precisely known
calls, **2,348 aligned bytes of native source CODE match**,
including all 234 new cosh bytes.

Of **377 original OMF FIXUPPs** in this prefix, all **375
emitted native** sites, sizes, symbol target identities and
addends match after the two known shifts. The two original
same-CODE FAR-call fixups remain absent; **329 original
Borland frame-method-4 FPU fixups** are represented by
TASM EMUL method 5. Those are explicit unresolved OMF
differences, not silently normalized equality.

The [scoped checker](../scripts/probe_th03_cplx2_cosh_partial.py)
runs two independent native TASM rounds under the writer
lock, compares all aligned original bytes, verifies every
emitted relocation's symbolic original target, and checks
nonvolatile OMF records between rounds while separately
disclosing possible TASM COMENT clock-byte changes.
Focused test: tests.test_cplx2_cosh_partial_native.

**Remaining work:** 3,240 original CODE bytes, 13 further
public function bodies, full original DATA/INITDATA
and method-4 OMF serialization. This does not replace
the full original cplx2 CRT member, grant formal Factory
acceptance, or establish a full MAINL native link for cplx2.
No full cold replay was performed.

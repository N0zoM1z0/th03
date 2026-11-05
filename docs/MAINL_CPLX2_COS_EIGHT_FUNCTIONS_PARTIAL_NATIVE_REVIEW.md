# Large cplx2: eighth complete FAR cos(complex) body, original prefix +0..2123

The Japanese Borland complex math CL.LIB member cplx2 has 5,598
original CODE bytes and 22 FAR public functions. The maintained
[partial 8086/x87 source](../src/mainl/crt/cplx2_eight_functions_partial.asm)
now recovers **eight full FAR bodies**: three complex division
overloads, acos, arg, asin, atan and the new cos(complex).

The new **cos(complex) is 233 original-equal CODE bytes**, at
original CODE+1891..2123. It implements the actual Borland
double-precision complex cosine using FAR _exp, _sin and _cos,
original 80-bit floating-point exponential intermediates,
x87 FIERQQ/FIDRQQ/FIWRQQ references, the original typed 2.0f
constant at DATA+24, and the native conditional allocation
of the 16-byte FAR complex result. Every instruction and ABI
detail in the cos body matches the original, with no copied
target machine-code arrays or post-assembly binary patches.

The full first-eight-functions prefix comprises **2,124 original
CODE bytes** and **2,122 TASM CODE bytes**. Only the same two
acos local-call encodings at original CODE+799/+984 differ in
width: Borland direct FAR CALL is five bytes and TASM emits
PUSH CS plus a four-byte near call. All the other 2,114
aligned native source bytes equal their original counterparts,
including the new cos body.

The 2,124-byte original prefix has **337 FIXUPPs**. Of these,
335 emitted native fields match original location, width,
target symbol identity and addend after accounting for the
two established call shifts. The two original local FAR-call
fixups are not emitted by TASM. There are **295 original
Borland frame-method-4 FPU references** that TASM EMUL
represents as frame method 5. Those differences remain
explicit and are not normalized into false complete
original OMF identity. Original DATA+0..15 remains
unmaterialized while the 12 typed DATA+16..27 bytes agree.

The [strict partial verifier](../scripts/probe_th03_cplx2_cos_partial.py)
runs two independent TASM rounds with original source and
checks original aligned bytes, full imported symbol names,
every emitted OMF field, and nonvolatile OMF record stability
aside from the separately disclosed optional COMENT timestamp.
Focused test: tests.test_cplx2_cos_partial_native.

**Still incomplete:** 3,474 later original CODE bytes,
14 remaining FAR functions, original DATA/INITDATA and the
frame-4/source-FAR-call differences are unresolved. This
partial source adds **zero** complete CRT source-linked members
or Factory accepted-source credit and does not claim a
complete MAINL EXE link or a cold replay.

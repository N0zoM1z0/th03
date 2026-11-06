# Large cplx2: fifteenth original FAR pow(complex, complex) function

The Japanese Borland CL.LIB cplx2 member contains 5,598 CODE
bytes and 22 public FAR math/stream functions. The
[maintained 8086/x87 partial source](../src/mainl/crt/cplx2_fifteen_functions_partial.asm)
now implements fifteen full FAR function bodies: three complex
division operators, acos, arg, asin, atan, cos, cosh, exp,
log, log10, and three distinct pow overloads.

The latest pow(complex, complex) routine at original
CODE+3532..3740 is **209 original-equal machine-code bytes**.
Its source implements real/imaginary zero-base comparisons,
the native exceptional negative-exponent branch, local
complex log, FAR complex multiplication and local complex
exp with native Borland hidden 16-byte return object ABI.
This is meaningful FPU and 16-bit stack logic, not a copied
opcode array, filler, or post-assembly binary patch.

All **3,741 original CODE bytes** through the fifteenth
function are reconstructed in **3,739 TASM bytes**, with
only two existing intra-segment direct FAR call encodings
in acos at original CODE+799/+984 each one byte shorter
as PUSH CS plus near CALL. The other **3,731 aligned
native CODE bytes are original-equal**, including every
byte of the new pow body.

The prefix contains **574 original OMF FIXUPPs**, and
all **572 TASM-emitted references** match original
sites after the two known shifts, symbolic target names,
location widths/kinds and addends. Two original same-CODE
FAR calls remain absent, while **496 original Borland FPU
location-frame method-4 FIXUPPs** compile as method 5.
All 28 initialized original DATA+16..43 bytes match,
including typed pi; DATA+0..15 remains unmaterialized.
Full original Borland OMF framing is not claimed.

The [independent scoped verifier](../scripts/probe_th03_cplx2_pow_complex_complex_partial.py)
performs two real TASM rounds and checks all aligned CODE,
symbolic FIXUPPs and nonvolatile OMF records. Targeted
tests: tests.test_cplx2_pow_complex_complex_partial_native.

The remaining 1,857 CODE bytes, seven public functions
and full DATA/INITDATA/module-level frame fidelity remain.
**This is not a complete source-linked CRT member**,
does not earn any formal Factory accepted-source credit
and is not a full MAINL native link. No full cold replay.

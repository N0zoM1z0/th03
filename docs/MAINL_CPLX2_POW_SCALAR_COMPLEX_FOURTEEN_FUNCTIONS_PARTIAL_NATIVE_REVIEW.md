# cplx2 fourteenth complete FAR pow(double,complex) function

The Japanese Borland CL.LIB cplx2 member consists of
5,598 CODE bytes and 22 original FAR functions.
The [maintained native 8086/x87 partial source](../src/mainl/crt/cplx2_fourteen_functions_partial.asm)
now implements **fourteen entire original FAR math bodies**,
including all three complex-power overload families recovered so far.

**New in this stage:** the entire 306-byte original FAR
pow(double,complex) at CODE+3226..3531. It implements the
genuine zero-real-base and negative-exponent comparison,
writes original zero-complex output for that special case,
calls the real FAR fabs/log conversions, handles the negative
base with the typed pi argument, multiplies the complex exponent
using the Borland FAR complex multiplication helper, and invokes
the original local exp(complex) for the final FAR result.
All machine-code instructions and original 16-bit stack/FPU
ABI in this function are byte-identical to the Japanese
original; there are no copied executable bytes.

The first source candidate was **two bytes too long**, with
an unnecessary explicit FWAIT after a stored logarithm
temporary. TASM generated extra NOP/FWAIT bytes that
do not exist before the original next FLD. Removing this
source-level excess restored the entire original 306-byte
function body; the initial mismatch was not hidden with
an object or target patch. DATA+36..43 is the original
IEEE pi double, constructed using a typed full-precision
numeric literal. All 28 original initialized DATA bytes
at DATA+16..43 now match; DATA+0..15 remains genuinely
unmaterialized.

Across the fourteen complete bodies the original CODE
prefix spans **3,532 bytes**. Native TASM emits **3,530
CODE bytes**, two bytes shorter exclusively due to the
previously identified direct FAR-call encodings at
acos CODE+799 and +984. All other **3,522 aligned
native CODE bytes** match the original, including
the entire new pow(double,complex) body.

The first 3,532 original bytes contain **546 FIXUPPs**;
all **544 emitted native symbolic fields** match original
site (after those two shifts), kind/width, target symbol
and addend. The two original acos direct FAR-call fixups
remain absent. **473 original Borland frame-method-4 FPU
references** are expressed by TASM as method 5. Both
differences remain explicit, not normalized into false
claims of raw original OMF equality.

The [scoped verifier](../scripts/probe_th03_cplx2_pow_double_complex_partial.py)
performs two independent TASM rounds and reviews all
original CODE, typed DATA and emitted original-symbol
FIXUPPs, including stable nonvolatile OMF evidence.
Focused tests: tests.test_cplx2_pow_double_complex_partial_native.

The remaining **2,066 original CODE bytes and eight
later FAR public functions**, full original DATA/INITDATA
and exact Borland frame-4 serialization still need source.
This is genuine large-boss partial progress, **not** another
complete source-linked CRT member or Factory accepted unit.
No complete MAINL link or full cold replay is claimed.

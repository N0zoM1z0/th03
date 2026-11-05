# Large complex-math boss cplx2: sixth complete FAR asin(complex) function

Japanese Borland CL.LIB cplx2 (index **209**) has 5,598 original
CODE bytes and 22 complete FAR math/stream public entrypoints.
The maintained [source](../src/mainl/crt/cplx2_six_functions_partial.asm)
now reconstructs **six complete FAR function bodies**: three complex
division overloads, acos, arg, and the newly completed
**asin(complex), original CODE+1217..1607 (391 bytes)**.

The asin source contains actual native x87 operations. It uses the
original double -2.0 and single 2.0 constants, the genuine
arg(complex), abs(complex), _sqrt, _sin, _cos, _log
routines and the original C++ FAR result allocator. Its
real/imaginary composition differs correctly from acos:
one real-part FADD uses the base real component rather than
the imaginary component, while the imaginary contribution
uses FLD+FCHS+FADDP rather than FSUBR. The source retains
the exact Borland register, stack and FPU ABI.

**Important discovery during independent relocation comparison:**
the first natural asin draft happened to be byte-for-byte
CODE-equal, but retained acos's _cos then _sin import
ordering. The original asin requires _sin at CODE+1388
and _cos at CODE+1424; the 5-byte FAR calls themselves
have identical raw placeholder CODE. The strict original
symbol-target reviewer rejected this first draft.
We corrected the source calls based on actual Borland
EXTDEF/FIXUPP evidence, not a byte-only match. Both now
have the correct semantic target and exact original site.

The original six-function prefix CODE+0..1607 comprises
**1,608 original CODE bytes**; natural TASM emits **1,606**
because the two *previously documented* acos local direct
FAR calls at original CODE+799 and +984 compile as
4-byte PUSH CS+NEAR CALL rather than original 5-byte
direct FAR CALL. After aligning around those two
honestly disclosed gaps, **all remaining 1,598 native
source CODE bytes** are original-equal, including the
entire new 391-byte asin function.

Of **248 original prefix FIXUPPs**, all **246 emitted native
references** now match original symbolic target names,
location, widths and addends after accounting for the two
call-byte shifts. The two original local FAR-call
fixups are absent, and **218 original Borland frame-method-4
FPU references** compile with TASM frame method 5.
This is explicitly retained as original-vs-TASM frame
mismatch; we do not claim complete raw original OBJ or
literal original FIXUPP serialization equality.

The [scoped verifier](../scripts/probe_th03_cplx2_asin_partial.py)
independently builds two native TASM rounds under the
writer lock, confirms all aligned original CODE and
original EXTDEF-targeted fixups, and checks both OMF
outputs excluding only TASM's changing COMENT 40E9
timestamp byte. The focused test is
tests.test_cplx2_asin_partial_native.

**This remains partial large-boss source, not a full
library-member replacement.** The remaining 3,990
original CODE bytes, 16 other FAR public bodies,
complete DATA/INITDATA footprint and exact method-4
frame semantics are unfinished. No new source-linked
CRT member count, decoded MAINL native link or formal
Factory acceptance is claimed for this partial program.
No full cold replay was performed.

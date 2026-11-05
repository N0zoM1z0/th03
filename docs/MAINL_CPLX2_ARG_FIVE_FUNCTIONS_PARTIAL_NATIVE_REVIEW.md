# Large cplx2: fifth complete FAR arg(complex) function (scoped source)

Japanese Borland CL.LIB member cplx2 is **5,598 CODE bytes** with
22 original public C++ functions. The maintained
[partial source](../src/mainl/crt/cplx2_five_functions_partial.asm)
now includes five entire FAR function bodies:
the three previously recovered complex division overloads
(CODE+0..691), the complete acos(complex) (CODE+692..1078),
and newly recovered **arg(complex) at original CODE+1079..1216**.

The added arg operation is **138 original-equal bytes** with
actual x87 comparisons against original DATA+0/+8 (two
unmaterialized double-sized zero regions), the real floating
status/SAHF path, and a genuine FAR _atan2 call. No original
executable-byte arrays or artificial padding are present.

The two previously identified same-segment FAR call encoding
differences in acos remain unchanged: original CODE+799 and
+984 have five-byte direct FAR calls targeting the original
arg entry at CODE+1079; TASM emits four-byte PUSH CS + CALL NEAR
sequences, shifting native arg to CODE+1077. After accounting
for these **two explicitly disclosed one-byte shortenings**,
**all other original CODE bytes in the 1,217-byte prefix** match
native TASM, including every byte of arg.

The full five-body original prefix has **184 original OMF
fixups**; 182 compiled fixups match location, size, target
symbol identity, segment relation and addend after the two
known call-site shifts. The two original CODE-local FAR
call fixups are absent from TASM's output, and **163 original
Borland frame-method-4 x87 references** compile as method 5.
These are original-vs-TASM metadata discrepancies, not
silently normalized evidence of raw OBJ equality. Original
DATA+0..15 remains truly unmaterialized; the 12 initialized
bytes at DATA+16..27 are reproduced exactly.

The independent [scoped checker](../scripts/probe_th03_cplx2_arg_partial.py)
performs **two real TASM rounds** under the repository writer
lock, compares every aligned original byte and fixup, verifies
all nonvolatile OMF record bytes across rounds and separately
records the optional native COMENT timestamp byte. The test is
tests.test_cplx2_arg_partial_native.

**Important:** This is **not** a complete original CRT library
member: the remaining 4,381 CODE bytes, 17 subsequent public
functions, further DATA/INITDATA and original method-4 frame
semantics are not reconstructed. This scoped source therefore
adds **zero** complete CRT source members, performs no full
cold replay, and earns no new Factory accepted-source credit.
The current complete CRT carrier remains after484 (692/893).

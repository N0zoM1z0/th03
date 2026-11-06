# Original large cplx2: seventeenth complete FAR sinh(complex)

Japanese Borland CL.LIB member cplx2 has 5,598 original CODE
bytes and 22 complex FAR public interfaces. The maintained
[8086/x87 source](../src/mainl/crt/cplx2_seventeen_functions_partial.asm)
now reconstructs **seventeen complete FAR functions**, including
the new sinh(complex) at original CODE+3974..4207 (**234 bytes**).

The actual sinh body has the original exponential of the real
part, real-component 80-bit intermediate computation, FAR sine
and cosine of the imaginary part, original x87 arithmetic,
and conditional Borland 16-byte FAR result allocation.
It differs from cosh in the correct x87 addition/subtraction
order; the difference was determined by comparing original
instructions, not by renaming functions. All 234 new CODE
bytes and the new PUBLIC entry match original CL.LIB.
TASM requires an early and an in-place PUBLIC declaration
to emit this additional symbol without changing CODE.
No target byte arrays, NOP filler or post-assembly patches
are present.

The original first seventeen function bodies cover CODE+0..4207
(**4,208 original CODE bytes**). Native TASM emits 4,206
bytes because two previously established local direct FAR
calls in acos, original CODE+799 and +984, compile each one
byte shorter as PUSH CS plus near CALL. All other **4,198
aligned native CODE bytes** match their original counterparts.
The original prefix has **654 OMF FIXUPPs**, of which **652
emitted native symbolic fields** match source target names,
location widths/kinds, addends, and sites after the known
two shifts. The original same-CODE FAR-call fixups remain
unrepresented in the shorter TASM encoding. **564 original
FPU location-frame method-4 references** compile with method
5 and are explicitly excluded from claims of exact raw
original OMF identity. The 36 initialized DATA+16..51
bytes are exact, and DATA+0..15 remains unmaterialized.

The [scoped verifier](../scripts/probe_th03_cplx2_sinh_partial.py)
performs two native TASM rounds under the writer lock and
checks actual CODE, all 17 public offsets, typed DATA,
every emitted OMF reference and nonvolatile OMF stability.
Test: tests.test_cplx2_sinh_partial_native.

**Still incomplete:** 1,390 original CODE bytes, five further
FAR functions, full DATA/INITDATA and the original frame-4
serialization. This is only a scoped large-Boss reconstruction;
it does not earn a full source-linked CRT member, a complete
MAINL EXE link, or Factory accepted-source credit.
No full cold replay was performed.

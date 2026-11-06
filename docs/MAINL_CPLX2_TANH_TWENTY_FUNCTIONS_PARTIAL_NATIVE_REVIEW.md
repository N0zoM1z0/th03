# cplx2 twentieth complete FAR tanh(complex) original body

The original Japanese Borland CL.LIB cplx2 member (slot 209)
is a 5,598-byte CODE segment with 22 FAR complex math/stream
public entrypoints. The maintained
[8086/x87 partial source](../src/mainl/crt/cplx2_twenty_functions_partial.asm)
now implements **twenty complete FAR functions** through
original CODE+5090. The new tanh(complex) at CODE+4781..5090
contributes **310 byte-exact original CODE bytes**.

The source calculates real exponent and its 80-bit reciprocal,
actual sine/cosine of the imaginary component, two original
80-bit numerator/denominator intermediates, 4.0f and original
double component arithmetic, preserving the x87 stack ordering
and 16-bit stack frame. It returns the original hidden FAR
complex object pointer, allocating a 16-byte object only when
necessary. It is authentic natural 8086/x87 source, not a
copy of original executable bytes or a patched OMF/EXE.

Original CODE+0..5090 spans **5,091 bytes**; native TASM emits
**5,089** because two previously disclosed direct FAR calls in
acos at original CODE+799/+984 compile one byte shorter each.
All other **5,081 aligned CODE bytes** match original, including
the complete new tanh. All 20 public names/offsets agree after
the shifts. Of **809 original prefix OMF FIXUPPs**, all **807
native-emitted references** match original sites, target names,
location widths/kinds and addends. Two original same-CODE FAR
calls remain absent; **703 original Borland method-4 FPU
frame references** compile as TASM method 5. These metadata
gaps remain explicit and are not mislabeled raw original
OMF identity. All 40 initialized DATA+16..55 bytes match;
DATA+0..15 remains genuinely unmaterialized.

The [scoped verifier](../scripts/probe_th03_cplx2_tanh_partial.py)
runs two real native TASM rounds, checks original CODE and
typed DATA, public symbols, imported target identity and
all emitted OMF fields, and confirms nonvolatile OMF stability.
Test: tests.test_cplx2_tanh_partial_native.

**Still incomplete:** 507 original CODE bytes and two
stream public functions, the remainder of original DATA
and INITDATA and exact original method-4 frame serialization.
This is **partial large-Boss source**, not a complete
source-linked CRT member, complete linked MAINL EXE or
formal Factory accepted-source credit. No full cold replay.

# Original cplx2: sixteenth complete FAR sin(complex) source

The Japanese Borland CL.LIB cplx2 member contains 5,598 original
CODE bytes and 22 FAR exported math/stream operations. The
[maintained 8086/x87 partial source](../src/mainl/crt/cplx2_sixteen_functions_partial.asm)
now implements **sixteen complete FAR function bodies**.
The latest sin(complex) at original CODE+3741..3973 is
**233 machine-code bytes exactly matching the original**.
It performs the true complex sine with an exp of the imaginary
component, 80-bit intermediates, distinct cosine/sine calls
on the real component, and genuine hidden FAR result allocation.
The new original DATA+44..51 is a typed double **-0.5**
used to generate the correct imaginary sign, not a copied
target byte sequence. All **36 initialized original DATA bytes**
at +16..51 match the original, while DATA+0..15 remains
unmaterialized as in Borland CL.LIB.

A significant source-level trap was caught by checking original
public names, not just CODE. The first TASM compilation generated
every CODE byte correctly but failed to emit the **sixteenth
public export**, despite a PUBLIC directive beside the function.
Four different declaration experiments isolated the behavior.
Declaring the real sin symbol once earlier in _TEXT and again
beside its PROC causes TASM to emit the original sixteenth PUBLIC
at native CODE+3739, corresponding to original CODE+3741.
This is a genuine extra source-level declaration: no code,
OBJ or MAP bytes were patched.

Original CODE+0..3973 comprises **3,974 bytes**, of which TASM
emits **3,972** because two previously discovered direct FAR
calls inside acos at original CODE+799 and +984 assemble one
byte shorter each. All other **3,964 aligned native CODE bytes**
match their original source, including the new sin function.
Of **614 original prefix OMF FIXUPPs**, all **612 emitted
native references** match original sites after these two
shifts, import names, location widths/kinds and addends.
**530 original location-frame method-4 x87 references**
compile with TASM frame method 5. The two original local
FAR-call fixups remain absent. These differences are explicitly
unresolved, not misrepresented as complete vendor OMF identity.

The [scoped native verifier](../scripts/probe_th03_cplx2_sin_partial.py)
runs two real TASM rounds, independently checks aligned CODE,
all typed initialized DATA, public offsets and every emitted
symbolic fixup. Focused tests: tests.test_cplx2_sin_partial_native.

**Still partial:** 1,624 original CODE bytes, six later FAR
functions, complete original DATA/INITDATA and exact original
FPU frame-4 serialization remain to be reconstructed. This
does not link as a complete original cplx2 CRT member and earns
zero new full source-member or formal Factory accepted credit.
No cold replay was run.

# Original cplx2 thirteenth complete FAR pow(complex, double) body

Japanese Borland CL.LIB member cplx2 is a 5,598-CODE-byte,
22-function FAR complex math boss. The maintained
[partial natural 8086/x87 source](../src/mainl/crt/cplx2_thirteen_functions_partial.asm)
now includes **thirteen complete FAR bodies**, from three complex
division overloads through log10 and newly pow(complex,double).

The entire **358-byte pow(complex,double) at original CODE+2868..3225**
is byte-identical to the original. It implements the actual
zero-complex-base comparison using the original unmaterialized
DATA+0/+8 zero double constants, the genuine negative-exponent
branch, local arg(complex), far abs(complex), far _pow,
_sin/_cos with x87 magnitude/phase arithmetic, and the
original hidden 16-byte FAR result object allocator.
Importantly, original CODE comparison caught a first-draft
return branch aimed six bytes too early: the original
zero-base/negative-exponent jump skips two intermediate
pointer loads while the normal result path executes them.
Two genuine source labels were separated to reproduce the
original branch. No raw executable-byte arrays, arbitrary
NOP padding or object patches were introduced.

The original first thirteen function bodies span **3,226
CODE bytes**; TASM emits **3,224**, because the two
previously established acos local FAR calls at original
CODE+799/+984 compile as four-byte PUSH CS plus near CALL
instead of original five-byte direct FAR CALL. All other
**3,216 native aligned CODE bytes** equal original,
including the new entire 358-byte pow body.

Of **492 original prefix FIXUPPs**, all **490 emitted native
fields** match exact original site (accounting for shifts),
target symbol name, location type, width and addend.
The same two local direct FAR-call fixups remain unrepresented.
**425 original Borland FPU location-frame method-4 fields**
compile with TASM method 5. This discrepancy is retained as
a proof limitation, not falsely claimed original record equality.
The first 16 original DATA bytes remain unmaterialized and the
20 original initialized DATA+16..35 bytes match exactly.

The [scoped verifier](../scripts/probe_th03_cplx2_pow_complex_double_partial.py)
performs two native TASM rounds, independently checks every
aligned original CODE byte and every emitted symbolic OMF
target/addend, and checks all nonvolatile native OMF records.
Focused tests: tests.test_cplx2_pow_complex_double_partial_native.

**Still unfinished:** 2,372 original CODE bytes, nine later
FAR functions, remaining DATA/INITDATA source and exact Borland
method-4 FPU framing. This work is a large-boss partial source,
not a complete source-linked CRT member, not a complete linked
MAINL EXE/MAP pair and not formal Factory acceptance.
No full cold replay was run.

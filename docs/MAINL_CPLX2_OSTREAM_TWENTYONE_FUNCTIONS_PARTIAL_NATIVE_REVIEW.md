# Original cplx2: twenty-first complete FAR ostream insertion for complex

Japanese Borland CL.LIB cplx2 contains 5,598 CODE bytes and 22 public FAR
complex-math and stream interfaces. The maintained
[natural 8086/x87 source](../src/mainl/crt/cplx2_twentyone_functions_partial.asm)
now reconstructs **21 entire FAR function bodies**, with the newly
completed ostream << complex at original CODE+5091..5268 (**178 bytes**).

This is an actual stream formatting routine, not a copied executable
byte sequence. The source prints the original typed DATA strings:
DATA+56 "("; DATA+58 ", "; and DATA+61 ")", with NUL terminators.
It extracts both original 64-bit complex components, casts each to
the original native ten-byte 80-bit long-double stream argument,
calls the real ostream long-double inserter twice, and uses
the real FAR ostream::outstr three times. Intermediate DX:AX
ostream return pointers and original caller stack conventions match.

The original first 21 function bodies occupy **5,269 CODE bytes**;
TASM emits **5,267** because two previously disclosed acos
same-segment five-byte direct FAR CALLs at original CODE+799/+984
compile as four-byte PUSH CS + NEAR CALLs. Outside those two
specific sequences, **5,259 aligned native CODE bytes** match,
including all 178 output-function bytes. All 21 public names and
offsets also match after the two known shifts.

Of the **829 original prefix CODE FIXUPPs**, all **827 emitted
native symbolic references** match original code sites (aligned),
imported symbol names, kinds, widths and addends. The two
original local FAR-call fixups are still unrepresented, while
**715 Borland x87 frame-method-4 references** compile as TASM
method 5. These differences are disclosed instead of claiming
complete original raw OMF equality. All 47 initialized original
DATA bytes at +16..62 now match, with DATA+0..15 unmaterialized.

The [scoped verifier](../scripts/probe_th03_cplx2_ostream_partial.py)
performs two genuine native TASM rounds, reviews original CODE,
all 21 public offsets and full initialized DATA, and compares every
emitted symbolic FIXUPP and the nonvolatile native OMF records.
Test: tests.test_cplx2_ostream_partial_native.

**Still incomplete:** the final 329-byte istream input body,
34-byte private initialization routine within that tail,
original six-byte INITDATA startup registration and exact
Borland FPU frame-method-4 serialization. This remains partial
source, with **zero complete source-linked CRT/Factory credit**.
No full cold replay, target byte arrays or OBJ patching occurred.

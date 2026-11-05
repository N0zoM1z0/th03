# Original large cplx2: fourth full acos body and the exact FAR-call gap

Japanese original Borland CL.LIB cplx2 (slot 209) contains a large
**5,598-byte CODE segment and 22 public complex math procedures**.
This scoped continuation recovers the complete fourth
**acos(complex)** FAR procedure (original CODE+692..1078)
in maintained [natural 8086/x87 source](../src/mainl/crt/cplx2_four_functions_partial.asm),
along with the three previously recovered FAR complex-division
functions at CODE+0,+166,+405. This is actual additional large-Boss
source work, not a completion/acceptance claim for the whole CRT
library member.

The acos body preserves the true complex square and cross terms,
the original typed -2.0 double and 2.0 single-precision constant
at original DATA+16 and +24, real x87 FIERQQ/FIDRQQ/FIWRQQ
arithmetic, real abs/sqrt/sin/cos/log calls, and the hidden 16-byte
FAR return-object allocation path. Source-level branch, local
double temporaries, stack frame and result writes are all original-
byte-equal **except two explicitly identified call encodings**:

- Original CODE+799..803 invokes local FAR arg(complex) at CODE+1079
  using a five-byte direct FAR CALL. TASM compiles the corresponding
  symbolic local call as PUSH CS followed by a NEAR CALL (four bytes).
- Original CODE+984..988 repeats the same direct FAR CALL; TASM
  again emits a four-byte PUSH CS / NEAR CALL.

These are semantically equivalent for the 16-bit FAR-call stack
return ABI but they are **not byte-equal**. They also make the
compiled declaration-only arg symbol occur at CODE+1077 rather
than the original CODE+1079. The arg function body itself is NOT
implemented here. No NOP or copied opcode bytes are introduced
to make the product appear exact. Tests prove identical native/
original CODE in **all three other contiguous spans**, totalling
1,069 original CODE bytes; native assembled source is 1,077 bytes
against the 1,079-byte original four-function prefix.

The original four-function prefix has **161 FIXUPP references**.
159 emitted TASM references match original sites after the two
known one-byte call shortenings, including exact location kinds,
widths, symbolic original targets, addends, and segment relations.
Both original local FAR-call CODE relocations at CODE+800/+985
(target CODE+1079) are **missing from the compiled TASM OMF**.
Of the other original fixups, 143 are real Borland location-frame
method-4 FPU references emitted by TASM EMUL as method 5; this
difference remains explicit. The two original DATA-reference
locations frame correctly and the twelve initialized bytes
of original DATA+16..27 match; original DATA+0..15 is genuinely
unmaterialized rather than zeros copied as initialized bytes.
Consequently neither full FIXUPP equivalence nor complete
original raw OBJ identity is claimed.

The source-only [scoped checker](../scripts/probe_th03_cplx2_acos_partial.py)
assembles both native rounds under the Borland writer lock,
checks every semantic/code span and every non-omitted original
relocation by identity and site, confirms two native nonvolatile
OMF outputs agree, and detects (rather than hiding) any TASM
COMENT 40E9 clock-byte change. The focused test is
tests.test_cplx2_acos_partial_native.

**Still unowned:** cplx2 has another 4,519 original CODE bytes
after the acos range, including 18 later public procedures,
the complete original 63-byte DATA and six-byte INITDATA members,
and unresolved original method-4 framing / same-CODE FAR call
encoding. This partial scope never updates the full CRT count
(686/893 at after478) or Factory accepted-source ledger.
No full cold replay was run. Its main value is documenting
a complete semantic acos recovery, typed constants, and the
two exact remaining compiler discrepancies as actionable,
independently checked obstacles.

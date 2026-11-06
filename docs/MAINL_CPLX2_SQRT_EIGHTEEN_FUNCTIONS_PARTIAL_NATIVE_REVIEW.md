# Large original cplx2: eighteenth complete FAR sqrt(complex)

Japanese Borland CL.LIB member cplx2 (slot 209) is a 5,598
CODE-byte complex math Boss with 22 FAR public functions.
The [maintained native 8086/x87 source](../src/mainl/crt/cplx2_eighteen_functions_partial.asm)
now implements **eighteen complete FAR function bodies**.
The new sqrt(complex) occupies original CODE+4208..4428,
all **221 CODE bytes original-equal**. It calls the actual
local arg(complex), divides the phase by the real typed
2.0f, takes the native far abs(complex) then far scalar
sqrt, and combines sine/cosine of the half-phase with
the square-root magnitude. The original conditional
Borland 16-byte FAR complex return-object allocation,
register and x87 stack ABI are preserved. No target
opcode arrays, artificial padding or binary patching.

Original CODE+0..4428 totals **4,429 bytes**; TASM emits
**4,427**. Two already documented direct FAR calls in
acos (original CODE+799 and +984) compile one byte
shorter as PUSH CS plus near CALL. All other **4,419
aligned native CODE bytes** match original, including
every sqrt instruction. All eighteen symbolic public
names and entrypoint offsets agree after these shifts.

Of **683 original prefix OMF FIXUPPs**, all **681 TASM-
emitted symbolic references** match original locations,
target names, types/widths and addends after the two
call-site shifts. The two original same-CODE direct FAR
call fixups remain unrepresented. **587 original Borland
FPU location-frame method-4 fixups** compile as TASM
method 5. They remain explicitly unresolved, not
silently described as raw original OMF identity.
All 36 initialized DATA bytes at +16..51 are equal;
DATA+0..15 remains genuinely unmaterialized.

The [scoped native checker](../scripts/probe_th03_cplx2_sqrt_partial.py)
runs two fresh TASM rounds under the writer lock,
checks all aligned CODE, public offsets, typed DATA and
original-symbol OMF sites, then verifies nonvolatile
OMF stability. Focused tests:
tests.test_cplx2_sqrt_partial_native.

**Scope limit:** 1,169 original CODE bytes, four later
FAR functions and the remaining DATA/INITDATA and original
frame-4 OMF serialization are not yet reconstructed.
This remains a partial Boss source artifact, not a
complete source-linked CRT member, MAINL native link or
Factory accepted-source credit. No cold replay was run.

# cplx2 eleventh complete FAR log(complex) function

The original Japanese CL.LIB cplx2 member has 5,598 CODE bytes
and 22 FAR exported functions. The
[maintained 8086/x87 source](../src/mainl/crt/cplx2_eleven_functions_partial.asm)
now implements **eleven complete FAR math function bodies**,
from the three division operators through acos, arg, asin,
atan, cos, cosh, exp, and the new log(complex).

The new original CODE+2564..2707 log(complex) body is
**144 byte-identical CODE bytes**. It calls the actual
local FAR arg(complex) using original PUSH CS and NEAR CALL,
the native FAR abs(complex), FAR _log for the magnitude,
stores real/imaginary outputs in the correct order and
uses the original 16-byte FAR allocator when the hidden
return object pointer is zero. It preserves the Borland
FPU and stack ABI without copied target byte arrays.

Across the first **2,708 original CODE bytes**, TASM emits
**2,706**. Only two previously identified direct FAR
calls inside acos at original CODE+799/+984 are encoded
one byte shorter as PUSH CS plus NEAR CALL. All other
**2,698 aligned source bytes** match the original,
including the entire new log body.

The original prefix contains **419 OMF FIXUPPs**.
**417 emitted native fields** match the original symbolic
targets, location kinds, widths and addends after the
two disclosed call-site shifts. The two original local
direct FAR-call fixups remain absent. **364 original
Borland frame-method-4 FPU fixups** compile with TASM
method 5; this is disclosed rather than normalized away.
The original initialized 12 DATA bytes at +16..27
are reproduced; full original DATA/INITDATA and raw OMF
identity have not been established.

The [independent scoped verifier](../scripts/probe_th03_cplx2_log_partial.py)
assembles two real native TASM rounds, reviews every aligned
CODE byte and emitted original-symbol fixup, and checks
nonvolatile OMF across rounds. Test:
tests.test_cplx2_log_partial_native.

**Limit:** 2,890 original CODE bytes and eleven public
function bodies remain. This is a verified large-Boss
partial reconstruction, **not** a complete cplx2 source
member, not a full MAINL EXE rebuild, and not formal
Factory acceptance. No full cold replay was run.

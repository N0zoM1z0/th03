# Original DOS intdos/intdosx register bridge — after488

The original Japanese Borland CL.LIB member intdos (slot **176**)
is now [maintained 8086 source](../src/mainl/crt/intdos.asm).
It implements the complete original FAR _intdos at CODE+0,
and _intdosx at CODE+50. The first uses the genuine FAR
_segread helper and then the same-CODE PUSH CS + NEAR call
into the second FAR interface, preserving the 16-bit register
and segment input/output ABI.

The second function restores the actual caller's AX/BX/CX/DX/SI/DI,
DS and ES registers before the real DOS INT 21h, captures the
flags twice and returns the native register image, segment image
and carry bit to the caller. Error handling invokes the exact
near __IOERROR with original stack operands. This is not an
invented host syscall bridge or a high-level compatibility wrapper.

The complete **146 original CODE bytes**, both public offsets,
the two ordered imports, original BSS-before-DATA GROUP, empty
DATA/BSS and **both literal ordered OMF FIXUPPs** match.
The _segread FAR call has its original CODE+14 target/frame,
and the __IOERROR near call retains its exact original CODE+139
location, frame method 0 and target. No target CODE array,
object rewriting or arbitrary padding is used.

After488 verifies the inherited after487 695-source carrier,
then runs two fresh TASM/TLIB/TLINK rounds retaining all
raw OBJ/LIB/EXE/MAP pairs, logs and source hashes. Both
complete decoded Japanese MAINL EXE/MAP exactly equal
the pinned originals (67,372 EXE bytes; 677 ordered MZ
relocations). Working CRT: **696/893** source-linked
original members, **184,690 CODE bytes**, 197 unchanged
contextual vendor members. No full cold replay or formal
Factory accepted-source credit is claimed.

Focused reviewer: scripts/review_th03_mainl_after488_work.py
(mode dos-intdos-intdosx-register-boss);
tests: tests.test_mainl_after488_work.

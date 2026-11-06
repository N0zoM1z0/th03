# Original DOS creat with symbolic exitopen close callback — after506

Japanese Borland CL.LIB member creat (slot **210**) is now
reconstructed in [maintained 8086 source](../src/mainl/crt/creat.asm).
Its private near helper performs real DOS AH=3Ch file creation
using the caller's FAR DS:DX filename, and reports the original
DOS error through near __IOERROR. Public FAR _creat at
CODE+31 applies the real __notUmask file attributes, calls
the original near helper, installs a FAR __xclose callback
into the actual mutable __exitopen variable, calls the
real FAR _ioctl and computes the original __openfd
descriptor flags using __fmode and the file's attributes.
This preserves the exact native 16-bit stack and register ABI.

All **156 original CODE bytes**, one true public at CODE+31,
all seven imported symbols, empty DATA/BSS and original
BSS-before-DATA GROUP agree with the pinned Japanese CL.LIB.
All **nine literal ordered original OMF FIXUPPs** match,
including CODE+79/+81 and +85/+87, which emit actual
far segment and offset symbolic references to the live
__exitopen callback and its __xclose target.
There is no target-code array or post-assembly object rewrite.

After506 independently validates the unchanged after505
713-source CRT carrier and performs two real fresh
TASM/TLIB/TLINK rounds. Both full Japanese decoded MAINL
EXE and MAP are byte-identical to their targets, preserving
67,372 bytes and all 677 ordered DOS MZ relocations.
Raw OBJ/LIB/EXE/MAP pairs, writer logs, source/driver hashes
and original parent receipt are retained. The working CRT
is **714/893 complete source-linked members**, **187,199
source-built CODE bytes**, with 179 original vendor-context
members still present. This is scoped working-source proof,
not formal Factory acceptance or cold replay.

Reviewer: scripts/review_th03_mainl_after506_work.py
(mode dos-creat-exitopen-close-callback-boss).
Tests: tests.test_mainl_after506_work.

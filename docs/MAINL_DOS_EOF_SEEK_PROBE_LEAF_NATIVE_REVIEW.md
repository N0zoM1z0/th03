# Original DOS device/seek EOF probe — after474

The original Japanese Borland CL.LIB member eof (index **216**)
is recovered as natural [8086 source](../src/mainl/crt/eof.asm),
a complete FAR _eof(handle) function, not a read-only
descriptor-flag wrapper.

Its **125 CODE bytes** implement the genuine DOS INT 21h
AX=4400h device information call, and for seekable files
the actual AX=4201h current-offset, 4202h end-offset and
4200h restore-offset probes. It compares the 32-bit
DX:AX offset against the saved end location, preserves
the original DOS carry/AX error path and delegates to
the original near __IOERROR. It also retains the Borland
__nfile and __openfd descriptor-closed checks, device
handling, and the exact FAR return and 16-bit stack ABI.

Every original CODE byte, all public/import symbols, no DATA/BSS,
the native BSS-before-DATA group and all **three literal
ordered original OMF FIXUPPs** match. The original near
__IOERROR at CODE+117 retains the exact CODE frame, target,
width and addend; __nfile at CODE+13 and __openfd at
+30 match all their DGROUP-framed fields. There are no
target-byte fixtures, binary padding, or OBJ patches.

After474 validates the retained after473 681-member source
carrier and performs two independent TASM/TLIB/TLINK
native rounds, preserving all raw OBJ/LIB/EXE/MAP outputs,
logs and source/driver hashes. Both decoded Japanese
MAINL EXE/MAP match the pinned original (67,372-byte EXE,
677 ordered DOS MZ relocations). Working CRT:
**682/893** original source-built members,
**182,280 original-equal CODE bytes**, 211 unchanged
contextual vendor members. No full cold replay or formal
Factory source acceptance was claimed.

Focused reviewer: scripts/review_th03_mainl_after474_work.py
(mode dos-file-eof-seek-probe-leaf).
Tests: tests.test_mainl_after474_work.

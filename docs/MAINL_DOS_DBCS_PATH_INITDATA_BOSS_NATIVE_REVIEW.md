# Original DOS DBCS path initializer and path character predicates — after465

Original Japanese CL.LIB member _pathops (index **186**) is
maintained in [8086 source](../src/mainl/crt/_pathops.asm),
with the complete **208 CODE, 16 initialized DATA and 6 CRT INITDATA**
bytes, not just two exported leaf functions.

The private near initializer (CODE+0) saves all original registers,
tests the cached far DBCS range vector and invokes the genuine
DOS INT 21h AX=6300h service to locate the lead-byte range table.
The original failure path uses the maintained zero-terminated
default DBCS table instead. Both DATA publics are real original
symbols: ___path_dbcs_vector at DATA+0 and
___path_dbcs_default at +4. Its complete 16-bit return path,
register restoration and abnormal two-POP-BX epilogue are preserved.

The FAR ___path_isdbcsleadbyte (CODE+73) scans the original
range table and ___path_issbcs (CODE+110) detects dangling
DBCS lead-byte pairs within the caller's far path. The latter
retains the native PUSH CS plus NEAR call into the first FAR
entry, preserving the exact Borland 16-bit ABI and range tests.

Unlike ordinary three-segment CRT objects, this module has the
original _INIT_ segment of class INITDATA, with six real bytes:
the original initialization priority word 0F00h, a symbolic
CODE+0 initializer address, and a reserved zero word. The
literal INITDATA FIXUPP at segment 4, offset +2, targets the
original private near initializer. All **eight original
literal ordered OMF FIXUPPs match exactly**, including this
fourth-segment reference; the four original SEGDEFs, DATA
publics and special GRPDEF 0aff03ff02 also match. The complete
raw Borland OBJ record program is not separately asserted
equal, nor is the executable manufactured from byte fixtures.

After465 validates its unchanged after464 672-member native
carrier then runs two fresh TASM/TLIB/TLINK native rounds with
all OBJ/LIB/EXE/MAP output pairs, writer logs and source
hashes retained. Both complete decoded Japanese MAINL EXE/MAP
are original-equal (67,372 EXE bytes and 677 ordered MZ
relocations). The working CRT now has **673/893 source members**,
**180,648 original-equal CODE bytes**, and 220 contextual vendor
members. This is not Factory source acceptance or cold replay.

Focused reviewer: scripts/review_th03_mainl_after465_work.py
(mode dos-dbcs-path-initializer-boss);
tests: tests.test_mainl_after465_work.

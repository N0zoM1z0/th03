# Original DOS MKNAME / TMPNAM filename generation and BSS state — after492

Japanese Borland CL.LIB member mkname (index **89**) is now
maintained as [native 8086 source](../src/mainl/crt/mkname.asm).
It includes both complete original near entrypoints __MKNAME
(CODE+0) and __TMPNAM (CODE+97). The real __MKNAME chooses
the default 13-byte FAR BSS filename buffer when no destination
is supplied, selects either the actual TMP prefix or a caller-
supplied FAR prefix, copies with original FAR __stpcpy, appends
a decimal identifier through near __UTOA and concatenates
the true .$ $$ extension through far _strcat. The __TMPNAM
routine updates the caller's FAR counter, calls the native
near __MKNAME to generate the next candidate, checks actual
DOS file attributes through __dos_getfileattr, and retries
according to the original 16-bit caller-stack convention.

All **188 CODE and nine initialized DATA bytes**, and the
actual **13-byte uninitialized BSS buffer**, match original
Japanese CL.LIB. The initialized bytes are the two typed
strings TMP\0 and .$$$\0; they are not executable byte
fixtures or unexplained padding. Both original near publics,
all four ordered imports, and the true segment/group layout
match. All **seven logical OMF FIXUPP sites, targets, kinds,
widths and addends** agree with original. Six of the seven
OMF fixups match completely. The single imported near
__UTOA call at CODE+64 uses original Borland TARGET-frame
method 5 versus TASM CODE-frame method 0. This exact site
and import are the only permitted difference in the source-
bound producer and test. Literal ordered original FIXUPP
equality and whole Borland OBJ identity are not asserted.

After492 verifies the entire after491 699-source CRT carrier,
then executes two fresh native TASM/TLIB/TLINK rounds
retaining all raw OBJ/LIB/EXE/MAP output pairs, writer logs
and source/driver hashes. Both decoded Japanese MAINL EXE/MAP
are byte-for-byte original-equal (67,372 EXE bytes, 677
ordered DOS MZ relocations). The working CRT reaches
**700/893 source-linked original members**, **185,353
original-equal CODE bytes**, with 193 contextual vendor
members. This is not full cold replay or formal Factory
source acceptance.

Focused reviewer: scripts/review_th03_mainl_after492_work.py
(mode dos-temp-name-counter-boss).
Tests: tests.test_mainl_after492_work.

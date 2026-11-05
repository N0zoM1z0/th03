# Complete original DOS file-create family — after498

The Japanese Borland CL.LIB creata member (index 211) is now
recovered as [maintained 8086 source](../src/mainl/crt/creata.asm).
It contains the complete private near DOS 21h file-create
engine at CODE+0..54 and **four** actual FAR public entrypoints:
__rtl_creat at +55, __creat at +83, _creattemp at +108 and
_creatnew at +139. These are different entrypoints, not
aliases or generated duplicate wrappers. The native private
engine uses caller-provided AH and CX, a true FAR DS:DX
filename pointer, DOS INT 21h, the actual __openfd
descriptor flags on success, and near __IOERROR on failure.
The three public operation modes use DOS 3Ch, 5Ah and 5Bh
with the correct Borland __fmode state and stack ABI.

Every one of the **170 original CODE bytes**, four FAR public
offsets, three external imports, BSS-before-DATA group,
and **all four literal ordered original OMF FIXUPPs** match.
The four relocation sites are CODE+36 to __openfd,
+45 to near __IOERROR, and +126/+157 to __fmode.
The first source attempt incorrectly treated the private
CODE+0 helper as an export and omitted a distinct public
entrypoint. Comparing original publics and CODE immediately
exposed this and the true four-function layout was restored.
No target opcode arrays, padding or object patches are used.

After498 verifies the unchanged after497 **705-source** CRT
parent, then runs two fresh native TASM/TLIB/TLINK rounds.
Both full decoded Japanese MAINL EXE/MAP match the original
targets byte-for-byte, including 67,372 EXE bytes and
677 ordered MZ relocations. Raw OBJ/LIB/EXE/MAP pairs,
writer logs, source/driver hashes and the parent receipt
are preserved. The working CRT advances to **706/893**
source-linked original members, **186,165 CODE bytes** and
187 contextual vendor members. No full cold replay or
formal Factory source credit is implied.

Focused reviewer: scripts/review_th03_mainl_after498_work.py
(mode dos-create-family-four-far-boss).
Tests: tests.test_mainl_after498_work.

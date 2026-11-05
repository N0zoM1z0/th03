# Original DOS lock/unlock and near IOERROR — after496

Original Japanese Borland CL.LIB member lock (slot **245**)
is now maintained as [native 8086 source](../src/mainl/crt/lock.asm).
It comprises both complete FAR _lock (CODE+0) and _unlock
(CODE+39), invoking the original DOS INT 21h AX=5C00h / 5C01h
region lock/unlock services with the true BX, CX:DX and SI:DI
16-bit handle/range register ABI. The native carry/error path
passes the original DOS error code to near __IOERROR.

Every one of the **78 original CODE bytes**, both FAR publics,
the original empty DATA/BSS layout, BSS-before-DATA GROUP,
lone __IOERROR import, and **both literal ordered OMF FIXUPPs**
are original-equal. Fixups at CODE+33 and +72 use their true
CODE-frame method 0, import target and word-sized near call.
There is no target-byte fixture, filler or OBJ mutation.

After496 independently validates its after495 **703-source**
parent and runs two fresh TASM/TLIB/TLINK native rounds.
Both decoded Japanese MAINL EXE and MAP equal the original
files byte-for-byte (67,372 EXE bytes and 677 ordered MZ
relocations). The preserved receipt binds both raw
OBJ/LIB/EXE/MAP vectors, writer logs, source/driver hashes
and the original parent. Working CRT reaches **704/893**
original source-linked members, **185,827 CODE bytes**, with
189 contextual vendor members. These are scoped source
results, not full cold replay or Factory accepted-source credit.

Reviewer: scripts/review_th03_mainl_after496_work.py,
mode dos-file-region-lock-unlock-leaf.
Tests: tests.test_mainl_after496_work.

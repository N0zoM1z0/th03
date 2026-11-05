# Original ios::usersize FAR array resize boss — after499

The Japanese Borland CL.LIB member stusize (index **889**) is
recovered in [maintained 8086 source](../src/mainl/crt/stusize.asm).
This is the complete 156-byte FAR ios::usersize(int) member.
It allocates a new four-byte-per-entry FAR user-word array
through the genuine Borland FAR new[] helper, copies the old
array with the real _memcpy call when old entries exist,
releases the old FAR storage through the original array-delete
helper, updates the ios object FAR pointer at +22h/+24h,
and zero-initializes each additional 32-bit user slot while
updating its original size field at +26h. It retains native
unchecked allocation behavior and signed 16-bit count logic.

All **156 CODE bytes** and all three original logical OMF
references match: the native far allocator at CODE+17,
_memcpy at +67, and the original array-delete helper at +83.
The true _TEXTA/_DATA/_BSS, DATA-first GROUP, one FAR public
and three ordered imports match original Japanese CL.LIB.
Borland and TASM literal FIXUPP order differs; raw original
OBJ record identity is not claimed. The initial natural ASM
used the opposite TASM GROUP declaration; comparison to
the actual original GROUP corrected that before integration.
No executable byte fixtures or object patches were introduced.

After499 checks the unchanged after498 **706-source** parent
before two fresh native TASM/TLIB/TLINK rounds, retaining
both complete OBJ/LIB/EXE/MAP outputs, writer logs and
source/driver hashes. Both Japanese decoded MAINL EXE/MAP
are byte-identical to the targets (67,372 EXE bytes and
677 ordered MZ relocations). Working CRT now **707/893**
complete source-linked members, **186,321 original-equal
CODE bytes**, with 186 contextual vendor members.
No full cold replay or Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after499_work.py
(mode ios-usersize-far-array-boss);
tests: tests.test_mainl_after499_work.

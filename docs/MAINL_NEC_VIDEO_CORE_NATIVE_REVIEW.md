# Original Japanese NEC PC-98 CRT initialization and screen-line video core

Two actually selected original Borland CRT modules are fully reconstructed
as authored symbolic 8086 code: **542 `cnecinit` (209 CODE bytes)** and
**546 `cnecscrn` (333 CODE bytes)**. `cnecinit` owns all five original
PUBLIC entries, including `___nec_c0crtinit`, screen height/window queries,
and both native NEC BIOS video services at original CODE+195/+202.
`cnecscrn` owns `__NEC_ZAP_LINE` at CODE+64 and `__NEC_MOVELINE` at +179.

Both sources preserve original PC-98 real-mode video memory and BIOS
register semantics, full segment/ES ownership, row and attribute handling,
all original branches and the 8086 string operations. The two actual
original member slots have empty initialized DATA/BSS and original
`08ff03ff02` DGROUP with distinct ordered original external imports.
Neither source contains copied original executable CODE-byte arrays,
artificial padding or post-assembly OBJ edits.

Independent native TASM 5.0 `/m /mx /kh32768 /t` reproduces **all 542/542
original CODE bytes**, all seven exported public entries, every original
ordered EXTDEF, and **all 29/29 literal original OMF FIXUPP fields**,
**including the original record sequence, sites, targets, frame methods,
widths, kinds and addends**. This is an unusually strong OMF result;
complete literal identity of unrelated OMF record types is not asserted.

An original 8086 ModRM subtlety was resolved in `cnecscrn`: three genuine
`XCHG SI,DI` operations at CODE+150/+157/+311 encode `87 FE`. TASM
encoded an equivalent operand order as `87 F7`; writing the operands in
the orientation TASM uses for `87 FE` reproduces the original machine
instructions naturally without changing semantics or patching objects.

`scripts/build_th03_mainl_after261_work.py nec-video-core` inherits the
source-bound **261-source** Japanese CRT, replaces both actual selected
slots in **two independent normal TASM/TLIB/TLINK rounds**, and rebuilds
the **entire 67,372-byte decoded original Japanese MAINL EXE and MAP
byte-for-byte**, including all **677 ordered DOS MZ relocations** and
**630 unchanged original vendor CRT member programs**. Working-source CRT
reaches **263 members / 98,203 original-equal CODE bytes**. This is
working source evidence, not formal accepted-ledger credit, and no full
cold replay was performed.

Proofs: `review_th03_mainl_after261_work.py nec-video-core`,
`tests.test_mainl_after261_work`, raw native OBJ/LIB/EXE/MAP vectors,
source-bound receipts and real writer logs under `.analysis/work/after261-*`.

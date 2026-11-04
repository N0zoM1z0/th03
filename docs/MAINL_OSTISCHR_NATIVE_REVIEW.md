# Japanese MAINL original `ostream::operator<<(char)` (ostischr)

The genuine selected Borland large-model CRT member **814**, `ostischr`,
contains **597 original CODE bytes** for the complete far C++ character
insertion method `@ostream@$blsh$qc` at CODE+0. It preserves the original
`_TEXTA` segment, empty `_DATA` and `_BSS`, and `08ff02ff03` DGROUP.

`src/mainl/crt/ostischr.asm` is a full symbolic 8086 source recovery of
prefix/suffix handling, character insertion and padding, output flags,
error-state propagation, and three true far virtual streambuf calls at
CODE+157/+317/+484 (`call dword ptr [bx+18h]`, original `FF /3`).
The real five external fixups reference `ios::setstate` and the ostream
prefix/suffix routines in their original near/far ABI and EXTDEF order.
No copied executable CODE arrays, object patches or fabricated padding.

TASM 5.0 `/m /mx /kh32768 /t` reconstructs **597/597 original CODE bytes**,
all original PUBLIC/EXTDEFs and segment layout, and **5/5 original native
FIXUPP sites, targets, addends and frame methods**. The Borland compiler and
TASM serialize these same fixups in different record order; literal complete
OMF record identity is **not** claimed.

`scripts/build_th03_mainl_after136_work.py ostischr` uses the selected
**136-source original Japanese CRT** and performs two independent normal
TASM/TLIB/TLINK rounds, both reproducing the **whole 67,372-byte original
decoded Japanese MAINL EXE and MAP byte-for-byte**, including **677 ordered
MZ relocations** and **756 untouched contextual vendor member programs**.
Working-source CRT grows to **137 members / 65,165 original-equal CODE bytes**.
These are working-source proofs, not formal accepted-ledger credit; no full
cold replay was run.

Review: `review_th03_mainl_after136_work.py ostischr`,
`tests.test_mainl_after136_work`. Retained raw OBJ/LIB/EXE/MAP pairs, native
writer logs and hash-bound receipts are under `.analysis/work/after136-*`
and `.analysis/work/mainl-after136-*`.

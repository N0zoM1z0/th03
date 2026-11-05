# Original setenvp: sparse INITDATA and a genuine absolute PUBDEF

The Japanese original Borland CRT member **364** (`setenvp`) now has a
complete native 8086 source implementation in `src/mainl/crt/setenvp.asm`.
It owns **88 bytes of CODE**, **4 initialized DATA bytes** (the far
`__environ` global), and one original **6-byte `_INIT_` startup segment**.
Only the first **four** bytes of `_INIT_` are materialized: priority `1000h`
and a relocation-backed offset to `setenvp_init`. The trailing **two bytes
are originally uninitialized**, faithfully declared with `dw ?`; no
synthetic zeros or file-byte credit is invented. Original DOS environment
block parsing, far memory allocation, abort on allocation failure, far
pointer traversal, and the `__C0environ` export copying direction are
retained without defensive changes.

The original member has a normal DATA public `__environ`, **six original
imports**, 11 OMF fields and a nonstandard absolute **PUBDEF
`__setenvp__` at frame:0, offset:0**. This last symbol was absent from
an initial source trial. That trial produced the correct complete EXE and
**677 ordered DOS relocations**, but the complete MAP differed: the
absolute symbol was absent and multiple unrelated equal-address aliases
were sorted differently by TLINK. Inspecting the actual original member
revealed a second PUBDEF with literal record payload identifying the
absolute symbol. Declaring the natural TASM equivalent with
`__setenvp__ equ 0` followed by `public __setenvp__` restored both the
original public metadata and the **entire original MAP**. No MAP file was
postprocessed.

The source also corrects two genuine instruction-level issues discovered
by the original native OMF: the environment cursor loop must branch to
the *entry-storage* instruction, not six bytes earlier to the termination
check; and the final CODE references must copy the `__environ` pointers
**into `__C0environ`**, not the reverse. After correcting these,
**all 88 original CODE bytes and the full 11 fields (including frame,
target, addend and literal order)** match the original Japanese member.

`scripts/build_th03_mainl_after344_work.py startup-environment-init` reuses
the pinned **377-source** full native parent. It builds only this new
member, then runs two serialized TASM/TLIB/TLINK passes to produce the
complete original Japanese **67,372-byte MAINL EXE and byte-equal MAP**.
The 893-slot original CRT carrier now contains **378 complete source-backed
members**, **515 original contextual members**, and **124,689 original-equal
logical CODE bytes**, with a new six-byte INIT source extent.
All full source hashes, native OBJ/LIB/EXE/MAP vectors, phase logs and
parent receipts are retained under `.analysis/work/after344-*` and
reviewed by `scripts/review_th03_mainl_after344_work.py` and
`tests/test_mainl_after344_work.py`. The original full Borland OMF program
metadata still differs from TASM's, despite literally equal PUBDEF and
FIXUPP fields. No cold replay, formally accepted Factory scope or canonical
packed-game credit is claimed.

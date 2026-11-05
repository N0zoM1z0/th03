# Original CRT heap-break manager: complete source, original native linker proof

The previously tracked `src/mainl/crt/fbrk.asm` has been independently
recompiled and brought into the live source-bound MAINL CRT chain. This
**does not** accept an earlier note or source file at face value: the
original Japanese CL.LIB **member 167** was separately parsed as OMF and
used as the authoritative target, then compared against an independent
TASM build. The member is the complete **352-byte `_TEXT` CODE** and **2-byte
initialized `_DATA`** program, with empty BSS, original `_TEXT`/`_DATA`/`_BSS`
segment order, eight imported symbols, and **33 original literal ordered
FIXUPP fields** including exact frame, site, target and addend.

The private near `grow_break` function performs heap-granule alignment,
DOS segment resizing and break-state updates. Two complete near public
functions, `__brk` at CODE+142 and `__sbrk` at CODE+209, retain the original
huge-pointer and signed increment arithmetic, heap bounds testing, failure
paths, and near ABI. The original two-byte `granule_count` state is retained.

## Provenance correction: the original library is not the alternate OBJ

The historical extracted standalone `vendor/fbrk.obj` has **the same
materialized CODE/DATA and named import targets**, but its EXTDEF ordering
and DGROUP segment ordering differ from the actual pinned CL.LIB member.
Its group record is `08ff02ff03`, versus the true library `08ff03ff02`.
Six near-call fixups at CODE+162,+181,+225,+266,+283,+302 are TARGET-frame
in the alternate vendor program but CODE-frame in the library. Raw EXTDEF
numeric target indices cannot therefore be compared without resolving their
names; the builder and direct regression both verify this explicitly rather
than silently preferring the alternate standalone OBJ.

The source-produced native fbrk program has byte-for-byte equal CODE and
DATA and **all 33 original ordered FIXUPP records** from the real library.
The complete original Borland OMF program-record serialization still differs
in other metadata, and that distinction is preserved in the receipt.

`scripts/build_th03_mainl_after345_work.py heap-break-manager` reuses the
complete **378-source** inherited native receipts, and builds the modified
893-slot CRT library and Japanese linked program **twice**, without cold
replay. Both native rounds match the complete original decoded **67,372-byte
MAINL EXE and MAP**, including the 677 ordered DOS MZ relocation entries.
The new carrier includes **379 source-backed CRT members**, **514 untouched
contextual programs** and **125,041 source-compiled original-equal CODE
bytes** (increase 352). Both raw OBJ/LIB/EXE/MAP rounds, phase logs and
source/driver/parent SHA receipts are retained in `.analysis/work/after345-*`.
A scoped reviewer and original-member tests are available as
`scripts/review_th03_mainl_after345_work.py` and
`tests/test_mainl_after345_work.py`.

This is native working-source evidence, **not** a new formal Factory-accepted
extent, packed-file credit or whole-game exactness. No full cold replay.

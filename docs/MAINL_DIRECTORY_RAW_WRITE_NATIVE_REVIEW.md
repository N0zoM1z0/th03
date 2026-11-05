# Full original Borland DOS current-directory and raw-write CRT functions

This increment directly revalidates and binds two pre-existing complete
native 8086 source files to **the original pinned Japanese CL.LIB** rather
than assuming older source notes or alternate standalone vendor objects are
correct. The actual original OMF machine CODE, every public/import symbol,
segment and DGROUP ordering, and **eight relocation fields in original
literal FIXUPP order** are checked independently against new TASM objects.

| Original member slot | Full CODE | ABI and behavior |
| --- | ---: | --- |
| `getdcwd` (239) | 157 bytes | `__getdcwd`: DOS INT 21h AH=47h directory retrieval, drive conversion, optional heap allocation, ERANGE/ENOMEM and far copy paths |
| `writea` (332) | 91 bytes | `__rtl_write` and `__write` at CODE+0,+63: INT 21h AH=40h raw output, far buffer, file flag handling and original near `__IOERROR` path |

The direct original library member for `getdcwd` has **5** relocation fields,
imports `_malloc`, `_errno`, `_strcpy`, `_strlen`, and its original far
public at +0. `writea` has **3** original fields, `_IOERROR` and `__openfd`
imports, and both original far public symbols. Both are fully materialized
CODE, with zero original DATA/BSS and group order `08ff03ff02`. The full
literal source-produced FIXUPP lists and their ordered frames match the
pinned CL.LIB. The `getdcwd` source object **also reproduces the entire original
Borland member record program byte-for-byte** in both rounds. The `writea`
full program record metadata differs despite its identical literal original
FIXUPP list; only its CODE/import/frame and link parity are claimed.

`writea` includes the actual `src/mainl/crt/stdio_layout.inc` constants. The
new `after349` builder and reviewer **bind that included source to a SHA256
in the native receipt**. No source dependency is excluded from the proof.

`scripts/build_th03_mainl_after349_work.py directory-and-raw-write` takes
the source/receipt-verified **393-member** parent carrier, recompiles both
original members, reconstructs all **893** CRT positions, and runs two
independent native TASM/TLIB/TLINK rounds. Both reproduce byte-for-byte the
original decoded Japanese **67,372-byte MAINL EXE and full MAP**, including
**677 ordered MZ relocations**. The live carrier contains **395 complete
source-backed members**, **498 unchanged contextual original members**, and
**127,254 original-equal CRT CODE bytes**, an increase of **248**. Full
original member/round OBJ/LIB/EXE/MAP, writer logs, parent SHA bindings and
the local test/reviewer are retained under `.analysis/work/after349-*`,
`scripts/review_th03_mainl_after349_work.py` and
`tests/test_mainl_after349_work.py`.

No full cold replay, binary output patch, formal Factory-accepted extent or
packed-file ownership is inferred from the native source-bound verification.

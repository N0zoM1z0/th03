# Original DOSCMD/DOSENV pair: literal source-produced Borland OMF match

The tracked `src/mainl/crt/doscmd.asm` and `src/mainl/crt/dosenv.asm` are
full original Japanese Borland CRT near constructors, not short wrappers.
Both have independently verified full 16-bit native CODE, all original far
imports and `RET 12` near callee argument cleanup ABI:

| Original CL.LIB member | Original CODE | Full implementation |
| --- | ---: | --- |
| `doscmd` (342) | 311 bytes | `__DOSCMD`: count string/argv bytes, allocate and construct counted DOS command tail with CR/NUL termination |
| `dosenv` (25) | 365 bytes | `__DOSENV`: count environment entries, allocate paragraph-aligned block, copy strings and preserve DOS double-NUL/trailing program field |

The initial code inspection independently confirms one original near public,
`_malloc`, `_strlen`, `__stpcpy` as imported far functions in that order,
five original far relocation fields per member, original empty DATA/BSS,
`DGROUP` order `08ff02ff03` and all original CODE bytes. The historical
[constructor review](MAINL_DOSCONSTRUCT_NATIVE_REVIEW.md) is background
only: this layer rechecks the *actual* pinned CL.LIB programs.

The alternate standalone vendor OBJs have the same CODE and equivalent
relocation sites/targets, but different ordered FIXUPP records from the
pinned original library members. The source builder uses the real library
members; **both original ordered FIXUPP lists are literally equal to TASM's**
and the entire **original CL.LIB member OMF record program** is also
byte-for-byte identical to each source-produced program in both producer
rounds. There are no executable target-byte arrays, altered object records
or patched linked outputs.

`scripts/build_th03_mainl_after340_work.py dos-command-environment` extends
the real source/receipt-bound **372-member** native Japanese CRT chain,
including the earlier original `LoadProg` and `exec` source-backed members.
Two independent native TASM/TLIB/TLINK rounds reconstruct all **893** CRT
library slots, with **374 complete source-backed members** and **519
unchanged original contextual members**, and produce the complete original
Japanese decoded MAINL **67,372-byte EXE and MAP**, including **677 ordered
MZ relocations**. Source-built original-equal logical CRT CODE totals
**120,849 bytes**, an increase of **676** from this pair. Raw full native
OBJ/LIB/EXE/MAP producer vectors and phase logs, source hashes, original
members and parent SHA receipt DAG are retained under
`.analysis/work/after340-*`, reviewed by
`scripts/review_th03_mainl_after340_work.py` and
`tests/test_mainl_after340_work.py` without a full cold replay.

This is a scoped working CRT source achievement, **not** new Factory
acceptance, packed-file credit or whole-game exactness.

# `__fullpath` large DOS/DBCS algorithm: original library source-bound audit

This audit recovers the **complete 834-byte** native main-entry and two
preceding path-check helpers already authored in
`src/mainl/crt/fullpath.asm`. The helpers occupy CODE+0 and CODE+31;
`__fullpath` is the exported far function at CODE+89. The original
16-bit control flow allocates a 161-byte temporary path, identifies drive
letters and drive-relative paths, obtains current directories, handles
separator normalization, searches DBCS-aware path components, and preserves
the original failure, allocation and copy paths. This is one complete
larger routine, not just a leaf or a synthetic CODE byte array.

## Important original-provenance correction

The original Japanese CL.LIB member **235** is the authoritative original
library object for this source-bound carrier. Its OMF program **is not**
byte-identical to the separate the standalone vendor `fullpath.obj` extracted under the local `TH03ML/vendor` working directory.
The original library member has 19 OMF program records including Turbo
Assembler comments and split LNAMES; the separate vendor OBJ has 10
records. The program-record sizes differ (1,252 versus 1,159 bytes).

A separate direct TASM compile of the tracked source confirmed exactly
**834 CODE bytes**, no DATA/BSS, the `_TEXT`/`_DATA`/`_BSS` segments,
11 imports, the exported far public at +89, and all 18 source relocation
fields. Comparing against the **actual original CL.LIB member** (not the
standalone vendor OBJ) also confirms literal ordered FIXUPP fields,
including the DGROUP-framed imported `__ctype` relocation. The standalone
vendor OBJ carries the **same logical CODE and relocations**, but orders
FIXUPPs differently. The standalone program cannot be used as an
unexamined stand-in for the original library records.

The builder wraps original library program records with an empty OMF THEADR
**only for in-memory parsing**, without changing the original program or
native product. It checks the standalone vendor artifact's complete logical
profile against the library, and then compiles `fullpath.asm` with TASM.
An initial ad hoc TASM trial retained a different file timestamp in
COMENT metadata (five differing program bytes). The source-bound producer
sets the original stable file timestamp: **both full 1,252-byte program
record streams then match the actual original library member byte-for-byte**,
not merely the CODE or relocation fields. The synthetic THEADR is excluded
from this exact program-record comparison.

## Scoped native proof

`scripts/build_th03_mainl_after322_work.py dos-fullpath` consumes the
322-member source-bound parent, preserves every source/receipt binding and
original member, and runs **two** serialized TASM/TLIB/TLINK rounds. Both
produce an exact original 1,252-byte CL.LIB member record and the exact
Japanese decoded MAINL EXE and MAP, with all 677 MZ
relocations, and reconstitute all 893 CRT members: **323** full source
producers and **570** contextual original members, for **106,705 CODE
bytes** of original-equal CRT working source. Raw OBJ/LIB/EXE/MAP and
logs are retained under `.analysis/work/after322-*` and checked by
`scripts/review_th03_mainl_after322_work.py` and
`tests/test_mainl_after322_work.py`. No full cold replay was run.

This proof concerns the source-bound working CRT member and linked binary.
It does **not** promote new Factory-accepted extent, canonical packed-unit
or whole-game source-ownership credit.

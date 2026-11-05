# Complete original Borland `string(TSubString&)` constructor and C++ RTTI

The actual Japanese CL.LIB member **394** (`ctor6`) is now reconstructed as
real original 16-bit TASM source in `src/mainl/crt/ctor6.asm`. The full
`@string@$bctr$qmx10TSubString` implementation handles substring storage,
reference allocation and copy-on-write, out-of-range and allocation failure
paths, the far C++ constructor ABI and matching cleanup — not an imported
stub or a copy of executable machine-code arrays.

The original OMF has `_TEXT` **126 CODE bytes** (five-byte far unwind thunk,
typed exception records and a far reference destructor helper), and
`_TEXTC` **495 CODE bytes**, covering the complete 234-byte constructor
and five genuine RTTI structures at +234 (`TStringRef *`), +257 (`xalloc`),
+323 (`xmsg`), +379 (`TStringRef`) and +449 (`TReference`). `_DATA` and
`_BSS` are empty. The original public, all eight imports, segment geometry,
and group `0aff02ff03` are exact.

All **621 original CODE bytes** and **22 original literal ordered FIXUPPs**
match the pinned Japanese library, including seven in `_TEXT` and fifteen
in `_TEXTC`. Each fixup's frame, target method, identity, width and addend
match too. The recovered `.asm` emits true symbolic instruction and typed
`dw`/`dd` declarations at the original offsets; it uses no binary patches
or target executable code arrays. The full Borland OBJ record program
still differs in other non-semantic metadata and is not claimed identical.

`scripts/build_th03_mainl_after378_work.py string-tsubstring-constructor-boss`
consumes the verified **474-member** parent carrier, recompiles this entire
original member and rebuilds the full **893-position** Japanese CL.LIB and
complete MAINL link in **two independent native TASM/TLIB/TLINK rounds**.
Both reproduce the pinned original decoded **67,372-byte EXE and full MAP
byte-for-byte**, including all **677 ordered DOS MZ relocations**.
The source-backed working CRT reaches **475 complete original-equal CRT
members**, **418 unchanged contextual original programs** and **151,008
source-compiled original-equal CODE bytes** (+621). Raw original and native
OBJ/LIB/EXE/MAP vectors, producer logs, source hashes and bound parent
receipts are retained in `.analysis/work/after378-*`. Targeted evidence is
`tests/test_mainl_after378_work.py` and
`scripts/review_th03_mainl_after378_work.py`.

This is a working-source and linked-output verification checkpoint; it is
not formal Factory accepted source ownership or canonical packed-game
credit. No full cold replay was run.

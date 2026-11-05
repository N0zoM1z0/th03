# All 17 original Borland `strings` methods: 2,958 CODE and 102 DATA bytes

The original Japanese CL.LIB member **428** (`strings`) is reconstructed as
`src/mainl/crt/strings.asm` using native 8086 instruction source and
compiler-ABI type declarations — not a target-byte array. The full original
object has **587 bytes `_TEXT` CODE**, **2,371 bytes `_TEXTC` CODE**,
**102 bytes initialized `_DATA`**, and empty `_BSS`. This member contains
**17 complete public far C++ methods**, including string destruction, three
bounds-check methods, `TStringRef` construction/destruction, reserve,
check_freeboard, grow_to, round_capacity, the full 446-byte splice body, and
six global option setters. The six original exported DATA words at offsets
0,2,4,6,8,10 have values **1,0,1,63,64,63**, followed by three genuine
independent zero-terminated `String reference out of range` messages at
DATA+12,+42,+72. No DATA padding or fake initialized bytes were added.

The entire `_TEXT` segment includes a five-byte real far exception unwind
thunk, native Borland typed exception state/catch-list descriptors at
CODE+5..302, and all four real far exception copy/destructor helper bodies
at +303,+356,+433,+510. The `_TEXTC` segment implements all exported
methods at exact original CODE+0,+134,+324,+514,+701,+931,+1027,+1137,
+1241,+1339,+1402,+1848,+1877,+1906,+1935,+1964,+2006. It also
contains the five complete named original RTTI descriptors at
CODE+2035,+2113,+2179,+2235,+2293 for `string::lengtherror`, `xalloc`,
`xmsg`, `string`, and `string::outofrange`. Real `dw`/`dd` fields and symbolic
near/far addresses replace every nonexecutable compiler metadata record.

## Exact-order issue found by rechecking actual OMF rather than assumptions

A conventional forward-declared source matched **all 3,060 original
materialized CODE/DATA bytes** and all **166 original logical relocation
fields** including frame, target and addend. The program EXE body and MAP
matched, but **101 DOS MZ relocation entries** had different ordering.
Reversing all source declarations fixed the `_TEXT` portion but incorrectly
reversed the order of the three *separately materialized* `_TEXTC` CODE
runs. The authoritative Japanese original OMF has three CODE4 LEDATA runs at
0..1023, 1024..2047 and 2048..2370, each followed by its own **reverse-
ordered FIXUPP fields**.

The final source emits genuine original 8086 instruction / typed-data
statements using `ORG` at **actual source statements with relocation
references**. It preserves the three original CODE4 LEDATA groups in their
original ascending order, and within each group emits referenced source
statements in the original compiler's descending offset order. The same
original semantic relocation order is preserved for the `_TEXT` exception
metadata. Every file-backed byte remains materialized by the real source;
`ORG` merely selects the original instruction/field's location, with no
filler, synthetic CODE arrays, binary patches or rewritten OBJ records.
The original **complete 166-field FIXUPP order, frame, site and target now
match literally**, not just after sorting. The original *full Borland OMF
member record serialization* still differs (TASM's non-semantic COMENT and
LEDATA program encoding are not original); no full OBJ equality is claimed.

## Two-round source-bound native evidence

`scripts/build_th03_mainl_after343_work.py string-class-boss` extends the
verified 376-member parent and produces a complete 893-slot CRT carrier
with **377 original-equal source-produced members**, **516 unchanged
contextual vendor members** and **124,601 original-equal logical CRT CODE
bytes** (+2,958), plus the 102 initialized DATA bytes in this member.
Both independent native TASM/TLIB/TLINK rounds reproduce the complete
original Japanese decoded MAINL **67,372-byte EXE and MAP byte-for-byte**,
including all **677 original DOS MZ relocations in original order**.
Original pinned library program, full raw dual-round OBJ/LIB/EXE/MAP,
writer logs and source/parent/driver SHA receipts are retained under
`.analysis/work/after343-*`. The scoped reviewer and independent raw OMF
checks are in `scripts/review_th03_mainl_after343_work.py` and
`tests/test_mainl_after343_work.py`. This does not entail a full cold replay.

All progress here is source-bound **working CRT source**; no formal Factory
accepted decoded extent, canonical packed-unit credit or whole-game source
ownership is inferred solely from exact native linking.

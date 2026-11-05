# Second large original C++ string insertion member: bounded substring insert

`src/mainl/crt/insert2.asm` reconstructs the complete original Japanese
Borland CL.LIB member **408** implementing
`string::insert(unsigned, const string&, unsigned, unsigned)`.
It includes **1,036 original-equal CODE bytes** in two independent native
CODE segments (`_TEXT` 365; `_TEXTC` 671), **30 initialized DATA bytes**
and the original empty BSS segment. Its only exported far method is
`@string@insert$quimx6stringuiui`, with all twelve original imports and
**43 distinct logical OMF relocation fields**, including CODE, DATA and
cross-segment typed C++ exception pointers.

The first exception/RTTI segment and diagnostic DATA were compared directly
against the pinned `insert1` and `insert2` original objects before reusing
semantic source. They are **not identical raw bytes**: original internal
RTTI address addends change with the length of each public insert routine.
The new member has two additional 16-bit range clamps: it bounds the
requested substring offset by the source length, and the requested substring
count by the remaining source length. It selects stack-resident bounds via
original SS:offset pointers, forms the substring's actual far data pointer,
then calls `TStringRef::splice` with Borland's native far ABI. The original
out-of-range exception construction, clone-on-write, unwind callbacks and
all five typed RTTI descriptors are present as *source declarations*, not
opaque executable byte arrays or patched objects.

An isolated direct TASM compilation produced byte-identical complete CODE
and DATA, the original segment/Public/Ext/Group layout, and all 43
relocations with matching site, frame, width, target and addend. The
source-bound incremental builder
`scripts/build_th03_mainl_after325_work.py string-insert-range` consumes the
329-member parent without a cold replay, and runs TASM/TLIB/TLINK **twice**.
Each round reproduces the full Japanese decoded MAINL EXE and MAP (all 677
DOS relocations) and keeps 893 CRT slots unchanged in order, with **330
source members**, **563** original contextual members, and **108,810
working-source CRT CODE bytes**. The retained raw objects, library, executable,
map and phase logs are checked by `scripts/review_th03_mainl_after325_work.py`
and `tests/test_mainl_after325_work.py`.

The original ordered FIXUPP record sequence differs from TASM; exact
original OMF program-record serialization is **not** claimed even though
full materialized CODE/DATA and logical relocation targets match. The new
working-source member is not a Factory-accepted canonical ownership fact.

# Complete original Borland string::clone: reference count and typed RTTI

The original pinned Japanese CL.LIB **member 383** (`clone`) now has a
complete symbolic 8086 source implementation at `src/mainl/crt/clone.asm`.
The original far `@string@clone$qv` method includes reference decrement,
copy-on-write allocation, `TStringRef` construction and exception cleanup,
not just a wrapper. The original `_TEXT` holds **41 CODE bytes** (far unwind
thunk and typed exception state); `_TEXTC` has **287 CODE bytes**: the full
148-byte method and original RTTI descriptors for `TStringRef *`,
`TStringRef` and `TReference`. DATA and BSS are empty.

All **328 original CODE bytes**, six imported Borland names, far public
name/offset, segment geometry/group `0aff02ff03` and **12 original FIXUPP
fields in literal record order** match the true original CL.LIB member.
Two fields are in `_TEXT` and ten in `_TEXTC`. The source emits real 8086
instructions plus typed `dw`/`dd` RTTI at the original `ORG` boundaries,
without opaque executable bytes or binary/OBJ patching. The full Borland
original OMF program-record serialization remains different in ancillary
records; byte-for-byte equality of the individual OBJ is not claimed.

`scripts/build_th03_mainl_after382_work.py string-clone-reference-boss`
consumes the **487-source** original Japanese CRT receipt chain, compiles
only `clone`, and rebuilds all original **893 CRT library slots** with
native TASM/TLIB/TLINK in **two independent rounds**. Both reproduce the
pinned original decoded Japanese **67,372-byte EXE and full MAP** byte-for-byte,
including **677 ordered DOS MZ relocation entries**. The working CRT reaches
**488 original-equal source-backed members**, leaving **405 unchanged
contextual original programs**, with **154,610 original-equal source CODE
bytes**, +328. Original/source OBJ/LIB/EXE/MAP vectors, source/parent/driver
SHA receipts, tool logs, scoped review and independent OMF tests are retained
in `.analysis/work/after382-*`,
`scripts/review_th03_mainl_after382_work.py`, and
`tests/test_mainl_after382_work.py`.

This proves scoped working-source CRT equivalence, not a new formal Factory
accepted decoded extent, canonical packed-game credit, or complete source
ownership; no full cold replay was executed.

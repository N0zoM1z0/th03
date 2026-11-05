# Six full Borland string/TSubString case-conversion APIs and exception RTTI

The original Japanese CL.LIB member **432** (`uprlwr`) is reconstructed as a
complete natural 8086 implementation in `src/mainl/crt/uprlwr.asm`, not
as an API stub or a serialized machine-code array. Its original `_TEXT`
segment has **177 CODE bytes**: a real far unwind thunk and compiler typed
exception cleanup/catch-state tables. `_TEXTC` contains **735 CODE bytes**:
all six full exported C++ case-conversion methods plus the original `string *`
pointer-type RTTI at `_TEXTC+658` and the original `string` class RTTI at
`_TEXTC+677`. The original `_DATA` and `_BSS` are empty.

| `_TEXTC` offset | Original far public API | Complete scope |
| ---: | --- | --- |
| 0 | `@string@to_lower$qv` | in-place lowercase with clone-on-write |
| 57 | `@string@to_upper$qv` | in-place uppercase with clone-on-write |
| 114 | `@to_lower$qmx6string` | copy-construction, exception-cleaned lowercase |
| 240 | `@to_upper$qmx6string` | copy-construction, exception-cleaned uppercase |
| 366 | `@TSubString@to_lower$qv` | original substring lowercase and COW logic |
| 512 | `@TSubString@to_upper$qv` | original substring uppercase and COW logic |

There are **11 original external Borland imports** and **48 complete OMF
relocation fields**. All original CODE bytes, public offsets and aliases,
segment/group ordering (`0aff02ff03`), and the entire **original ordered
FIXUPP field list, frames, targets and addends** are reproduced.

## Verified original codegen rather than copied binary

The actual CL.LIB separates executable methods at `_TEXTC+0..657`, the
19-byte pointer-type record at +658..676 and the string class RTTI at
+677..734. These are authored as real instructions and typed `dw`/`dd`, with
symbolic addresses to the actual original C++ class destructor. The original
CODE1 metadata similarly uses real compiler descriptors rather than
erroneously disassembled zero bytes. Original Borland OMF FIXUPPs appear
in descending offset order in each CODE LEDATA run; the source uses `ORG`
only at genuine 8086 or typed metadata boundaries to reproduce that order.
This does not invent executable padding, change original CODE or patch a
native object.

Two case-conversion instructions in `TSubString` at `_TEXTC+392` and +538
originally compare a far word with sign-extended `-1` (`83 ... FF`). TASM's
explicit `byte -1` spelling incorrectly writes immediate `00`; replacing
it with the real `cmp word ptr es:[bx+4],-1` instruction recreates the
original bytes. These two original codegen differences were discovered by
actual OMF CODE-byte comparison and are independently regression-tested.

`scripts/build_th03_mainl_after355_work.py string-substring-case-boss`
reuses all previous **406** source/receipt-bound CRT members and builds the
original **893-slot** library through native TASM/TLIB/TLINK in **two
independent serialized rounds**. Both rounds exactly reproduce the complete
original Japanese decoded **67,372-byte MAINL EXE and MAP** with all
**677 ordered DOS MZ relocations**. Working-source CRT now contains **407
complete source-backed members**, **486 unchanged original contextual
programs**, and **131,355 source-compiled original-equal CODE bytes** —
this member adds **912**. Original pinned OMF program, both raw native
OBJ/LIB/EXE/MAP rounds, source/parent/driver SHA receipts and tool logs
are retained in `.analysis/work/after355-*`, independently checked by
`scripts/review_th03_mainl_after355_work.py` and
`tests/test_mainl_after355_work.py`.

The full original Borland OMF record serialization is **not** claimed
byte-identical, despite all logical and ordered FIXUPP fields matching.
No full cold replay or formal Factory-accepted / packed-file credit is
claimed from this working-source CRT proof.

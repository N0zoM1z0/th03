# Original xmsg 955-byte C++ exception boss and ordered Japanese MZ

`src/mainl/crt/xmsg.asm` reconstructs the **entire original Japanese** Borland
`xmsg` member 337, with **955 original CODE bytes**, zero DATA/BSS, eight far
imports, five independent far C++ API entry points, typed exception-block
metadata and the original `xmsg`/`string*`/`string` RTTI declarations.

| Original far public | Original `_TEXT` offset | Covered responsibility |
| --- | ---: | --- |
| `@xmsg@$bctr$qmx6string` | 36 | allocate/construct with string and exception-refcount state |
| `@xmsg@$bctr$qmx4xmsg` | 239 | copy construction and owned string/refcount bookkeeping |
| `@xmsg@$bdtr$qv` | 410 | string destruction, conditional handle deletion |
| `@xmsg@raise$qv` | 518 | typed C++ throw via real Borland on-stack exception frame and RTTI |
| `@xmsg@$basg$qmx4xmsg` | 637 | self-assignment, string destruction, copy construction, unwind |

The complete source includes real 8086 opcodes, stack and far-call ABI,
reference count adjustment, constructors/destructor, exception descriptors
and typed object/class-name data **inside the CODE segment**. The original
49 FIXUPP fields all match by original segment, site, width, frame, target
and addend. The source uses semantic labels and real relocatable `dd`/`dw`
structures; there are no opaque machine-CODE arrays, link patches or
post-assembly fixup edits.

## Important: original MZ order must be proved, not inferred from CODE

A conventional forward-declared source built **byte-identical CODE** and
49/49 logically equal FIXUPP fields, yet the full Japanese EXE differed in
**29 MZ-header bytes**, all confined to 18 differently ordered relocations.
The complete EXE body and MAP were already equal. A broad reverse-section
experiment still left six of those slots out of order.

The original Borland FIXUPP inventory is emitted from higher CODE offsets to
lower offsets. TASM normally emits relocations in a different order, even
when every target matches. The final source declares original typed RTTI,
exception frames and executable instruction blocks **in reverse physical
offset order** using `ORG` at real instruction/block boundaries. Neither
padding nor fake target bytes are inserted. This preserves the original
source semantics while driving TLINK to emit the exact original 18 relocation
entries in order:

`927,884,852,752,705,644,601,546,525,512,504,474,326,246,203,119,43,0`

Absolute offsets here are relative to the first xmsg MZ relocation
(absolute 21588), not to the start of the loaded program. The resulting
complete Japanese EXE and MAP match byte-for-byte. Crucially, the original
**literal ordered OMF FIXUPP sequence does not equal the TASM sequence**;
whole-OBJ record equality is not claimed.

## Scope and reproducibility

`scripts/build_th03_mainl_after327_work.py xmsg-exception-boss` uses the
validated original 331-member source-bound CRT carrier, not a cold rebuild.
Two independently serialized native TASM/TLIB/TLINK rounds reproduce all
original 893 CL.LIB slots, 332 source-backed providers, 561 unchanged
contextual original programs, the complete 67,372-byte original decoded
MAINL EXE and MAP, and 677 ordered MZ relocations. New source-backed CRT
CODE is **110,841 bytes** (increase **955**). All original native OBJ/LIB/
EXE/MAP and phase logs are retained under `.analysis/work/after327-*` and
bound to source and receipt hashes. The reviewer and the two direct native
OBJ/MZ tests live in `scripts/review_th03_mainl_after327_work.py` and
`tests/test_mainl_after327_work.py`.

This source-bound working CRT gain is **not** Factory-accepted source ownership,
canonical packed-file credit or proof of original complete Borland OBJ
serialization. No full cold replay was performed.

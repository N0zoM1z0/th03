# Complete original string default constructor and initial capacity handling

The pinned Japanese CL.LIB member **389** (`ctor1`) has been recovered as
complete symbolic 8086 native source at `src/mainl/crt/ctor1.asm`. The
exported `@string@$bctr$qv` constructor contains the real original
reference-counted initial allocation, `TStringRef` initialization and
exception/deallocation paths, rather than an API forwarding stub.

Original `_TEXT` holds **126 CODE bytes**: far unwind thunk, compiler typed
exception record and complete far reference cleanup helper. `_TEXTC` holds
**434 CODE bytes**, including the full **173-byte default constructor** and
five typed C++ RTTI descriptors for `TStringRef *`, `xalloc`, `xmsg`,
`TStringRef` and `TReference`. Original DATA/BSS are empty.

The original imported `@string@initial_capac` is a **word DATA variable**
framed through DGROUP, not a far function call. The actual instruction
at `_TEXTC+72` pushes that word through a relocation field at +74 with
original target method 2, target 7, frame method 1, addend 0. The source
reproduces this DATA reference symbolically, alongside eight other
original Borland imports. All **560 original CODE bytes**, public offset,
segment group `0aff02ff03` and all **23 original literal ordered FIXUPP
fields** match the original, including frame, target, width and addend.
Actual instructions and typed RTTI/exception records are original-offset
`ORG` source, not binary target-code arrays or patched EXE/OBJ bytes.
Complete Borland OMF record serialization still differs in unrelated
metadata and is not claimed byte-identical.

`scripts/build_th03_mainl_after388_work.py string-default-constructor-boss`
extends the verified **510-member** CRT source/receipt chain, reassembles
only this full original member and reconstructs all **893 original library
positions** in **two independent native TASM/TLIB/TLINK rounds**. Both
exactly reproduce the pinned original **67,372-byte decoded Japanese EXE
and complete MAP**, including all **677 original ordered DOS MZ
relocations**. The working CRT reaches **511 source-backed complete members**,
**382 unchanged original contextual programs** and **159,111 original-equal
source-compiled logical CODE bytes**, an increase of **560**. All raw
original/source OBJ/LIB/EXE/MAP vectors, phase logs and source/parent/driver
SHA receipts, along with the independent reviewer and tests, are retained
under `.analysis/work/after388-*`,
`scripts/review_th03_mainl_after388_work.py` and
`tests/test_mainl_after388_work.py`.

This is working CRT source proof, not formal Factory source acceptance,
canonical packed-image credit or complete game source ownership. No full
cold replay was executed.

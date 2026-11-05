# Complete original C-string constructor `ctor3`: 747 CODE and six RTTI types

The Japanese Borland CL.LIB member **391** (`ctor3`) has now been recovered
as real symbolic 8086 source at `src/mainl/crt/ctor3.asm`. The far exported
constructor `@string@$bctr$qnxc` implements the original null/empty input,
`_strlen`, reference allocation, `TStringRef` construction and complete
exceptional cleanup paths rather than a forwarding wrapper.

The original `_TEXT` segment contains **207 CODE bytes**, including the
actual far unwinder, typed exception state and two complete refcount/deletion
cleanup methods. `_TEXTC` contains **540 CODE bytes**: the entire original
201-byte constructor plus six compiler-typed RTTI descriptors starting at
+201, +224, +302, +368, +424 and +494 (`TStringRef *`,
`string::lengtherror`, `xalloc`, `xmsg`, `TStringRef`, `TReference`). DATA and
BSS are both empty.

Every original **747 CODE bytes**, all nine imported Borland symbols, the
original far public, segment geometry/DGROUP record `0aff02ff03`, and all
**29 original ordered OMF FIXUPP fields** are reproduced, including 11 in
`_TEXT`, 18 in `_TEXTC`, and their precise original frame, target, width,
site and addend. Executable content is natural 8086 mnemonics and the RTTI
is typed symbolic `dw`/`dd` source at the actual BCC offsets; neither
machine-code byte arrays nor patched binaries/OBJs were used. Ancillary
Borland OMF record metadata still differs, so full original member-record
identity is not claimed.

`scripts/build_th03_mainl_after385_work.py string-cstr-constructor-boss`
inherits the verified **500-source** CRT chain and reassembles only this
full member, recreating all **893 original CL.LIB slots** and the complete
original decoded Japanese MAINL EXE/MAP in **two independent native
TASM/TLIB/TLINK rounds**. Both reproduce the pinned **67,372-byte EXE and
full MAP byte-for-byte**, including all **677 ordered DOS MZ relocations**.
The working CRT reaches **501 complete original-equal source members**,
**392 unchanged contextual original programs** and **156,547 source-built
original-equal CODE bytes**, a gain of 747. Raw original/native OBJ/LIB/
EXE/MAP, writer logs, source/parent/driver hashes and scoped review remain
under `.analysis/work/after385-*`,
`scripts/review_th03_mainl_after385_work.py` and
`tests/test_mainl_after385_work.py`.

This is scoped working-source verification, not new formal Factory accepted
ownership, canonical packed-image credit or proof of complete game source.
No full native cold replay was run.

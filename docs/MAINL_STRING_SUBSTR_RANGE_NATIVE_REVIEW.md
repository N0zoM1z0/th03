# Complete original Borland string::substr(pos, len) C++ exception boss

The pinned Japanese CL.LIB **member 431** (`substr2`) is reconstructed as
natural symbolic 8086 instructions and genuine typed C++ metadata in
`src/mainl/crt/substr2.asm`. Its exported far method
`@string@substr$xquiui` includes the full two-index range checks,
`string::assert_index`, bounded substring copying, error handling and
original exception/destructor cleanup. It is an entire implementation,
not a wrapper or opaque target-machine-code byte array.

Original `_TEXT` holds **199 CODE bytes** (far unwind thunk, compiler
exception state, two far destructor helpers), and `_TEXTC` holds **373 CODE
bytes** (the complete 96-byte method and five typed RTTI descriptors for
`string *`, `string::outofrange`, `xalloc`, `xmsg` and `string`). DATA/BSS are
empty. The two original NUL terminators in the out-of-range RTTI type name
were verified in the actual original OMF, rather than assumed from a
previous generator.

All **572 original CODE bytes**, eight imported Borland names, public
symbol and offset, segment geometry/DGROUP `0aff02ff03` and **24 literal
original ordered FIXUPP fields** match the pinned Japanese CL.LIB member
exactly in site, width, frame, target and addend (11 fields in `_TEXT`, 13
in `_TEXTC`). Symbolic instructions and typed metadata are emitted at
original source boundaries with `ORG`; no executable target-byte arrays,
postassembly object rewrites or patched EXEs are used. The full original
Borland OMF record serialization still differs in auxiliary metadata and
is not claimed byte-identical.

`scripts/build_th03_mainl_after386_work.py string-substr-range-boss`
revalidates the existing **501-source** Japanese CRT carrier and rebuilds
this one complete original member, all **893 original CL.LIB slots**, and
the decoded MAINL link in **two independent native TASM/TLIB/TLINK rounds**.
Both recreate the pinned original **67,372-byte Japanese EXE and full MAP
byte-for-byte**, with all **677 DOS MZ relocations in original order**. The
source-bound CRT reaches **502 complete original-equal members**, **391
unchanged original contextual programs** and **157,119 original-equal
source CODE bytes**, an increase of 572. Raw original/source OBJ/LIB/
EXE/MAP, phase logs, SHA-bound parent/source receipts, scoped reviewer and
OMF/MZ tests are retained in `.analysis/work/after386-*`,
`scripts/review_th03_mainl_after386_work.py` and
`tests/test_mainl_after386_work.py`.

This is scoped working CRT source evidence, not a new Factory-accepted
source extent, packed-image unit credit or whole-game source completeness.
No full cold replay was performed.

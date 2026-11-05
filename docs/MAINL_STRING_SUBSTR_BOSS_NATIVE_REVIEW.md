# Complete original string::substr: indexed bounds and typed exception RTTI

The original Japanese Borland CL.LIB member **430** (`substr1`) now has a
complete natural symbolic 8086 implementation in `src/mainl/crt/substr1.asm`.
Its public far C++ method `@string@substr$xqui` performs the original
indexed substring extraction, bounds assertions, buffer/reference handling,
string construction and exception cleanup, not a forwarding wrapper.

The first `_TEXT` CODE segment has **199 bytes**: an actual far unwind
thunk, typed exception state and two complete far cleanup helpers. The
`_TEXTC` segment has **371 bytes**: the complete 94-byte method and five
original typed RTTI descriptors (`string *`, `string::outofrange`, `xalloc`,
`xmsg`, `string`). DATA and BSS are empty. The original
`string::outofrange` RTTI name has **two trailing NUL bytes**, not one;
this was independently established from actual CL.LIB OMF and reproduced as
its original typed byte/word layout rather than hidden with padding bytes.

All **570 original CODE bytes**, eight imports, public/segment group
`0aff02ff03` and **24 complete literal original ordered FIXUPP fields**
match the pinned CL.LIB member, including 11 `_TEXT` and 13 `_TEXTC` fields,
frame, site, width, target and addend. Real x86 and typed `dw`/`dd`
statements are assembled with `ORG` at their original positions; no
executable machine-code arrays or binary object patches are used. Full
Borland OMF program-record serialization still differs in unrelated
metadata and is not claimed byte-identical.

`scripts/build_th03_mainl_after383_work.py string-substr-exception-boss`
revalidates the verified **488-member** parent chain, compiles only this
complete member and reconstructs all original **893 CRT slots**, then runs
two separate native TASM/TLIB/TLINK rounds. Both reproduce the original
pinned **67,372-byte decoded Japanese MAINL EXE and full MAP byte-for-byte**,
including **677 ordered DOS MZ relocations**. Working source now covers
**489 original-equal members**, **404 unchanged contextual original
programs** and **155,180 source-compiled original-equal logical CODE bytes**,
an increase of **570**. Native OBJ/LIB/EXE/MAP, tool logs, SHA receipts,
scoped reviewer and independent tests are under `.analysis/work/after383-*`,
`scripts/review_th03_mainl_after383_work.py` and
`tests/test_mainl_after383_work.py`.

This is scoped working CRT source verification, not new formal Factory
accepted source ownership, canonical packed-game credit or a whole-game
exactness claim; no full cold replay was run.

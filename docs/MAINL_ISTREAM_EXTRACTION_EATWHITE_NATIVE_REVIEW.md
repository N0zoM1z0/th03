# Complete original istream get(), extraction operators, and eatwhite()

Five entire original Japanese Borland CRT C++ stream member programs are
recovered in full symbolic 8086 source: native `istream::get()`, three
signed/unsigned/ordinary character-reference overloads of `operator>>`,
and the whitespace classifier `istream::eatwhite()`. They preserve the actual
original buffer get-area, virtual `do_get`, `ipfx` state, EOF/fail handling,
far C++ return ABI, and real `__ctype`-driven whitespace test.

| Original CL.LIB member | CODE | Exported original C++ method |
| --- | ---: | --- |
| `istget` (775) | 190 | `@istream@get$qv` |
| `istepchr` (767) | 246 | `@istream@$brsh$qmc` |
| `isteschr` (768) | 246 | `@istream@$brsh$qmzc` |
| `isteuchr` (770) | 246 | `@istream@$brsh$qmuc` |
| `isteatwh` (759) | 234 | `@istream@eatwhite$qv` |

All original `_TEXTA` CODE, zero DATA/BSS, original group `08ff02ff03`,
far public offsets and all imported symbols match the **actual pinned
Japanese CL.LIB**. All **1,162 CODE bytes and ten original FIXUPP fields**
are identical, including their literal Borland record order. `isteatwh`
combines far `ios::setstate` and a **group-framed byte relocation to
`__ctype+1` at CODE+190**; that data-table reference must not be misclassified
as a far-call fixup. The source uses actual `ORG` statement boundaries to
reproduce the original FIXUPP order without opaque CODE byte arrays or
post-link edits. Complete Borland OMF program-record serialization still
differs in nonsemantic metadata and is not claimed equal.

`scripts/build_th03_mainl_after367_work.py istream-extract-eatwhite`
inherits the verified **438-source** CRT working carrier and uses the
native 16-bit TASM/TLIB/TLINK pipeline in **two independent production
rounds**, replacing only the five complete selected members in the original
893-slot library. Both reproduce the original **67,372-byte decoded
Japanese MAINL EXE and full MAP byte-for-byte**, including all **677
original ordered MZ relocations**. The resulting CRT working source now
contains **443 complete original-equal members**, **450 unchanged contextual
original members** and **140,583 original-equal logical CODE bytes** (+1,162).
Original CL.LIB OMF member, raw native OBJ/LIB/EXE/MAP pairs, writer logs,
source/parent/driver SHA receipt and all independent regression tests are
retained under `.analysis/work/after367-*`,
`scripts/review_th03_mainl_after367_work.py` and
`tests/test_mainl_after367_work.py`.

This is working CRT source proof, not formal Factory source acceptance,
canonical packed-file ownership or whole-game exactness. No full cold replay.

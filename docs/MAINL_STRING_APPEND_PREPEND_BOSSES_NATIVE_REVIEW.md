# Three complete original Borland C++ append and prepend exception bosses

The pinned Japanese Borland CL.LIB members **379**, **380** and **419**
are reconstructed as real symbolic 8086 in `src/mainl/crt/append2.asm`,
`append3.asm` and `prepend.asm`. Each implementation retains the original
bounds/substring paths, full copy-on-write reference handling, buffer
splicing, exception cleanup and true far C++ calling convention. They
are separate complete programs, not wrappers or assembled machine-code
byte arrays.

| Original member | Full CODE | Public far C++ method |
| --- | ---: | --- |
| `append2` (379) | 506 | `@string@append$qnxc` |
| `append3` (380) | 577 | `@string@append$qnxcuiui` |
| `prepend` (419) | 568 | `@string@prepend$qnxcuiui` |

All three members contain a **177-byte `_TEXT`** segment with an original
far unwind thunk, typed exception frame and two complete destructor
helpers. Their `_TEXTC` segments contain, respectively, 329, 400 and 391
bytes of complete method code plus **three genuine C++ RTTI descriptors**
each: `string::lengtherror`, `xalloc` and `xmsg`. The original DATA/BSS
are empty. Together they add **1,651 source-compiled original CODE bytes**
and **63 original OMF FIXUPP fields** — 21 per member, including original
sites, frame/target/addend and literal descending Borland record order.
Each original import list, public offset, segment ABI and DGROUP record
`0aff02ff03` is reproduced. Original executable instructions and typed
RTTI/data statements are symbolically assembled at their real offsets
with `ORG`, not embedded as binary target-byte arrays or post-link patches.
Full original Borland OMF program serialization still differs in other
metadata and is not claimed byte-identical.

`scripts/build_th03_mainl_after376_work.py string-append-prepend-bosses`
extends the **470-source** original Japanese CRT carrier, assembles all
three entire new members and reconstructs the original **893-slot CL.LIB**
and decoded Japanese MAINL link in **two independent native TASM/TLIB/TLINK
rounds**. Both reproduce the original pinned **67,372-byte EXE and entire
MAP byte-for-byte**, including **677 DOS MZ relocations in original order**.
This source-bound working CRT reaches **473 original-equal CRT members**,
**420 original contextual vendor members**, and **149,671 original-equal
CODE bytes**, a net increase of **1,651**. Raw original/source OBJ/LIB/
EXE/MAP vectors, writer logs, source/parent/driver SHA receipts, scoped
review and direct regression are under `.analysis/work/after376-*`,
`scripts/review_th03_mainl_after376_work.py` and
`tests/test_mainl_after376_work.py`.

No full cold replay, formal Factory source acceptance, canonical
packed-file credit or whole-game source completeness is claimed.

# Six original Japanese near/far MBCS case-insensitive string comparisons

The pinned Japanese CL.LIB programs for six 16-bit case-insensitive string
comparisons are fully reconstructed as native 8086 source. This includes
the Japanese-aware whole-string and length-limited `jstricmp` APIs and the
full near/far `mbsicmp` pair; it is **not** a generic ASCII-only substitute.
The original DBCS lead-byte scans, upper/lower folding, signed compare
results, and near/far pointer/length ABI are preserved in separate members.

| Original CL.LIB member | CODE | Original far public |
| --- | ---: | --- |
| `JSTRICMP` (646) | 247 | `_jstricmp` |
| `FJSTRICM` (691) | 247 | `__fjstricmp` |
| `JSTRNICM` (648) | 259 | `_jstrnicmp` |
| `FJSTRNIC` (693) | 259 | `__fjstrnicmp` |
| `MBSICMP` (606) | 198 | `__mbsicmp` |
| `FMBSICMP` (662) | 198 | `__fmbsicmp` |

All **1,408 original CODE bytes** and **16 original FIXUPP fields** match
the real Japanese CL.LIB; zero initialized DATA/BSS, original `_TEXT`
segment/public names, group `08ff02ff03` and external character-table
symbols are also intact. The 16 FIXUPPs are byte-table references to the
original `__mbctype+1` and `__ctype+1` with DGROUP frame1, and TASM
reproduces the **literal original descending record order**, not merely a
sorted relocation set. This is achieved by reordering real original 8086
source instruction blocks with `ORG` at their original offsets; no target
CODE arrays, binary patches, or artificial initialized padding are used.
The full Borland OMF member-record serialization still differs in other
metadata and is not claimed identical.

`scripts/build_th03_mainl_after370_work.py japanese-mbcs-comparators`
consumes the verified **445-source** original CRT parent and compiles only
these six changed whole original members, then reconstructs all **893
CRT library slots** and the full decoded Japanese MAINL program through
**two serialized native TASM/TLIB/TLINK rounds**. Both reproduce the
original **67,372-byte EXE and MAP** byte-for-byte, including all **677
ordered DOS MZ relocations**. The working CRT reaches **451 complete
source-backed members**, **442 unchanged original contextual members**,
and **143,127 source-built original-equal CODE bytes**, a gain of **1,408**.
Complete original/native OBJ/LIB/EXE/MAP pairs, writer logs, and
source/parent/driver hashes remain under `.analysis/work/after370-*`,
with independent original OMF/MZ checks in
`tests/test_mainl_after370_work.py` and scoped review in
`scripts/review_th03_mainl_after370_work.py`.

These are working-source, not formally Factory-accepted decoded extents or
canonical packed-product ownership; no full native cold replay was run.

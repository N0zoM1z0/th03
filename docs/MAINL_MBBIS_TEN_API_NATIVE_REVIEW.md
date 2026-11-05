# Ten original Borland MBBIS byte-classification APIs, exact native output

This increment completes the previously dirty `src/mainl/crt/MBBIS.asm`
source rather than discarding or bypassing it. The actual original Japanese
CL.LIB member **579** is fully recreated in symbolic 8086 source:
**345 bytes of `_TEXT` CODE**, no DATA/BSS, all ten original far public
functions and exactly **15 original group-framed byte classification
FIXUPPs**. The original group is `08ff02ff03`, with two actual imports
`__ctype` and `__mbctype`.

| Original CODE offset | Exported method |
| ---: | --- |
| 0 | `__ismbbkalpha` |
| 24 | `__ismbbkpunct` |
| 48 | `__ismbbkana` |
| 72 | `__ismbbalpha` |
| 117 | `__ismbbpunct` |
| 162 | `__ismbbalnum` |
| 207 | `__ismbbprint` |
| 252 | `__ismbbgraph` |
| 297 | `__ismbblead` |
| 321 | `__ismbbtrail` |

The implementation preserves the original Japanese/PC-98 multibyte character
classes, graphic/alphabetic/punctuation masks, and original byte-table index
`+1` semantics. Original FIXUPP locations descend exactly:
`335,311,281,268,236,223,191,178,146,133,101,88,62,38,14`.
Each is an actual TASM symbol reference to `__ctype+1` or `__mbctype+1`,
not a generated machine-code array. All **345 CODE bytes, 10 public symbols,
15 fields and their original literal order** agree with the pinned CL.LIB.
Full original Borland OMF program serialization still differs in unrelated
metadata and is not claimed equal.

`scripts/build_th03_mainl_after368_work.py mbbis-ten-classifiers` extends
the complete source/receipt-verified **443-member** CRT parent, compiles
this entire 10-API member and recreates the original **893-slot** library
and decoded Japanese MAINL link with native TASM/TLIB/TLINK in **two
independent rounds**. Both native rounds reproduce the pinned original
**67,372-byte Japanese EXE and complete MAP byte-for-byte**, including
all **677 ordered DOS MZ relocations**. The working CRT now has **444
complete original-equal source members**, **449 unchanged original
contextual programs**, and **140,928 source-compiled original-equal CODE
bytes** (+345). Full original and native raw OBJ/LIB/EXE/MAP, writer logs,
source/parent/driver SHA receipts and targeted reviewer/test are retained
under `.analysis/work/after368-*`,
`scripts/review_th03_mainl_after368_work.py` and
`tests/test_mainl_after368_work.py`.

This is source-bound working CRT evidence; no full cold replay, formal
Factory acceptance, canonical packed-unit credit or whole-game source
exactness is inferred from native linking alone.

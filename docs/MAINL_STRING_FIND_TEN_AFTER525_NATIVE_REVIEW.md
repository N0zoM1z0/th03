# Ten complete string find/compare/resize/status members — after525

The ten remaining dual-CODE members in original Japanese CL.LIB string/regexp
slots 384–426 now have complete maintained source:

| Slot / member | Far API scope | `_TEXT` | `_TEXTC` | FIXUPPs |
| --- | --- | ---: | ---: | ---: |
| 384 / [compare1](../src/mainl/crt/compare1.asm) | const string comparison | 15 | 113 | 8 |
| 399 / [find2](../src/mainl/crt/find2.asm) | TRegexp match and result length | 5 | 118 | 1 |
| 400 / [find3](../src/mainl/crt/find3.asm) | string regexp find, local length | 15 | 63 | 6 |
| 401 / [find4](../src/mainl/crt/find4.asm) | string regexp find, caller length | 15 | 64 | 6 |
| 402 / [fndfrst](../src/mainl/crt/fndfrst.asm) | find_first_of | 15 | 146 | 6 |
| 403 / [fndfrstn](../src/mainl/crt/fndfrstn.asm) | find_first_not_of | 15 | 114 | 6 |
| 404 / [fndlast](../src/mainl/crt/fndlast.asm) | find_last_of | 15 | 153 | 6 |
| 405 / [fndlastn](../src/mainl/crt/fndlastn.asm) | find_last_not_of | 15 | 153 | 6 |
| 424 / [resize](../src/mainl/crt/resize.asm) | string resize | 5 | 127 | 2 |
| 426 / [status](../src/mainl/crt/status.asm) | TRegexp status read and clear | 15 | 55 | 5 |

All **1,236 CODE-segment bytes** match without exclusions: **1,156 executable
bytes and 80 inline registration-control bytes**. Every new member has zero
initialized DATA and zero BSS. Original `_TEXT`, `_DATA`, `_BSS`, `_TEXTC`
ordering, GROUP layout, import chronology and the ten far publics are retained.
All **52 literal ordered OMF FIXUPP fields** match their original sites, kinds,
widths, frames, targets and addends. Original raw OBJ program-record identity
is not claimed.

The source preserves actual strcmp/stricmp selection, the real regexp matcher
and length reference, forward set membership through strpbrk/strspn, and the
original reverse strchr loop. The reverse loop's start=0 and index-0 behavior
is retained. Its input byte is sign-extended by the original 8086 CBW; it is
not widened to a 32-bit instruction. The existing first-not-of length test
is preserved as emitted rather than replaced with a repaired algorithm.

The two reverse bodies differ only in membership-branch polarity. Their
[bounded common body](../src/mainl/crt/string_reverse_find_body.inl) expands
separately for each TU's real public and CODE owner. The original local
five-byte unwind in find2/resize is a distinct
[bounded include](../src/mainl/crt/string_unwind_only.inl), with no added
exception table. The other eight owners use the unchanged 15-byte empty
registration include. Resize retains clone/splice, while status preserves
its read-and-clear side effect. No defensive behavior was added.

The [after525 producer](../scripts/build_th03_mainl_after525_work.py) validates
the after524 parent TU/include hashes and extends the unchanged native pair.
Two TASM/TLIB/TLINK rounds reproduce the complete **67,372-byte Japanese MAINL
EXE, original MAP and 677 literal ordered MZ relocations**. All earlier 742
source members and 141 remaining vendor members stay in the original
893-member order. Both complete output vectors are identical to each other.

The [independent reviewer](../scripts/review_th03_mainl_after525_work.py) binds
all ten TUs, three include hashes, recipe/parent receipt, actual writer logs
and both full OBJ/LIB/EXE/MAP vectors. All evidence and scratch are retained.
No full cold replay, new runtime model or redundant test matrix was used.

Current working-source CRT: **752/893 complete members, 200,898 original-equal
CODE-segment bytes**. No vendor-context members remain in slots **384–426**;
this closes that original 43-member block in the working source library.
It does not grant formal Factory canonical packed-file acceptance, which
remains **0/250**, or establish a whole-game completion percentage.

Receipt: `.analysis/work/mainl-after525-string-find-resize-status-ten-build.json`

SHA-256: `5426bee81630d6492e4644cf78ef870b95a8e7d26a4eea7d63e3cfc42bb46981`.

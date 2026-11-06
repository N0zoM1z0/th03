# Eight complete string/regexp members — after524

Eight original Japanese CRT members now have complete maintained source,
both original CODE segments, and literal ordered OMF fields:

| Slot / member | Far API scope | `_TEXT` | `_TEXTC` | FIXUPPs |
| --- | --- | ---: | ---: | ---: |
| 385 / [compare2](../src/mainl/crt/compare2.asm) | const string substring comparison | 15 | 200 | 8 |
| 386 / [copy1](../src/mainl/crt/copy1.asm) | string prefix copy | 96 | 223 | 13 |
| 410 / [oprasgn1](../src/mainl/crt/oprasgn1.asm) | TSubString assignment from string | 15 | 177 | 7 |
| 411 / [oprasgn2](../src/mainl/crt/oprasgn2.asm) | TRegexp copy assignment | 96 | 216 | 14 |
| 412 / [oprasgn3](../src/mainl/crt/oprasgn3.asm) | TRegexp assignment from text | 96 | 200 | 14 |
| 415 / [oprcall3](../src/mainl/crt/oprcall3.asm) | mutable string regexp slice | 15 | 176 | 7 |
| 416 / [oprcall4](../src/mainl/crt/oprcall4.asm) | const string regexp slice | 15 | 176 | 7 |
| 417 / [opreql](../src/mainl/crt/opreql.asm) | const TSubString text equality | 15 | 181 | 9 |

The **1,912 CODE-segment bytes** comprise **1,442 executable bytes and 470
inline exception/RTTI bytes**. `opreql` also preserves one initialized DATA
byte, the actual empty string literal. It is a typed character constant,
not padding. Every original CODE and DATA byte matches without exclusions.

The original native order remains `_TEXT`, `_DATA`, `_BSS`, `_TEXTC`, with
the original GROUP and all eight far public entries. All **79 literal
ordered OMF FIXUPP fields** match their original sites, widths, relocation
kinds, frames, imports/segments and addends. Raw original Borland OBJ
program-record identity is not claimed.

`copy1` retains the original count clamp and count-plus-one memcpy. Regexp
assignment keeps the original self-assignment test, deletion and pattern
copy/generation. Comparison and equality preserve the real 16-bit
`string::case_sensitive` global, strncmp/strnicmp selection, null text
substitution and original invalid-substring handling. Substring assignment
keeps copy-on-write clone and the native splice argument/length arithmetic.
No defensive checks or allocation behavior were added.

Three wrappers reuse the unchanged, source-bound xmsg cleanup and typed
RTTI includes proved at after523. The new bounded
[empty exception owner](../src/mainl/crt/string_empty_unwind.inl) preserves
five unwind bytes and ten real control bytes per TU, including the original
BP-1Eh registration slot even when the function allocates more locals.

The two regexp slice bodies are proved identical in the original members.
Their [bounded body include](../src/mainl/crt/string_regexp_slice_body.inl)
expands separately for each TU's real far public entry; it preserves the
hidden result pointer, real find call, optional eight-byte allocation and
original return register sequence. No native contribution is merged away.

The [after524 producer](../scripts/build_th03_mainl_after524_work.py) checks
the after523 parent TU/include bindings and extends its unchanged native
pair. Two TASM/TLIB/TLINK rounds reproduce the complete **67,372-byte
Japanese MAINL EXE and original MAP**, with all **677 literal ordered MZ
relocations** unchanged. All earlier 734 source members and 151 remaining
vendor members stay in the original 893-member order.

The [independent reviewer](../scripts/review_th03_mainl_after524_work.py)
checks all eight TUs, four include hashes, recipe/parent receipt, actual
writer logs and both full OBJ/LIB/EXE/MAP vectors. All evidence and scratch
are retained. No full cold replay, new runtime model or redundant test
matrix was used.

Current working-source CRT: **742/893 complete members, 199,662 original-equal
CODE-segment bytes**. This adds eight complete members / 1,912 CODE-segment
bytes and one DATA byte. Formal Factory canonical packed-file acceptance
remains **0/250**; whole-game completion is unknown.

Receipt: `.analysis/work/mainl-after524-string-regexp-copy-compare-assign-eight-build.json`

SHA-256: `b9c9fffbd56d725b77c1091acf56dc03197d69efddf0f580d077567e1bff9179`.

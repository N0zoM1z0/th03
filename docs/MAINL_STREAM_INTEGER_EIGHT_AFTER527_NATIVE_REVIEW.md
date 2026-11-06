# Eight complete stream assignment/integer extraction members — after527

The eight vendor-context members left in original Japanese CL.LIB slots
740–824 at after526 are now complete maintained source:

| Slot / member | Far API scope | CODE bytes | Literal FIXUPPs |
| --- | --- | ---: | ---: |
| 740 / [iostasn2](../src/mainl/crt/iostasn2.asm) | iostream_withassign from streambuf | 36 | 1 |
| 749 / [istasn1](../src/mainl/crt/istasn1.asm) | istream_withassign from istream | 44 | 1 |
| 750 / [istasn2](../src/mainl/crt/istasn2.asm) | istream_withassign from streambuf | 36 | 1 |
| 764 / [isteint](../src/mainl/crt/isteint.asm) | signed int extraction | 61 | 1 |
| 769 / [istesh](../src/mainl/crt/istesh.asm) | signed short extraction | 61 | 1 |
| 771 / [isteuint](../src/mainl/crt/isteuint.asm) | unsigned int extraction | 61 | 1 |
| 772 / [isteulng](../src/mainl/crt/isteulng.asm) | unsigned long extraction | 68 | 1 |
| 773 / [isteush](../src/mainl/crt/isteush.asm) | unsigned short extraction | 61 | 1 |

All **428 executable CODE bytes** and all **eight literal ordered OMF fields**
match without exclusions or new frame exceptions. Every member retains its
original `_TEXTA`, empty `_DATA`, empty `_BSS`, GROUP, segment packing/alignment,
far public and import identity. Raw Borland OBJ program-record identity is
not claimed.

The five extractors use the original four-byte SS temporary and delegated
32-bit reader. They test the original stream-state mask 0x86 before writing
the caller's far destination. The four 16-bit results preserve low-word
truncation; the unsigned-long wrapper preserves high/low word writes and its
original signed-long reader delegation. No range checks, pointer defenses
or repaired EOF behavior were added. Original argument cleanup and DX:AX
istream-reference return are preserved.

The [bounded extraction include](../src/mainl/crt/stream_int_extract.inl)
expands into each original 61/68-byte owner. The two streambuf assignments
share a separately proved [bounded body](../src/mainl/crt/stream_buf_assign.inl),
while the stream-to-stream assignment retains its real buffer lookup and
ios::init call. Existing after526 source files are unchanged.

The [after527 producer](../scripts/build_th03_mainl_after527_work.py) validates
the after526 parent TU/include hashes and rechecks its raw, explicitly
disclosed FP/near-call frame descriptions. Two native TASM/TLIB/TLINK rounds
reproduce the complete **67,372-byte Japanese MAINL EXE, original MAP and all
677 literal ordered MZ relocations**. The full vectors are identical between
rounds; all earlier 766 source members, 119 remaining vendor members and
the original 893-member order are preserved.

The initial 33-character assignment-include filename triggered a TASM32
crash. Short include names compile unchanged bodies correctly. The original
failed workdir `probe/after527`, logs, and hash-inventoried receipt/recipe
archive at `.analysis/work/probe/stream-integer-long-include-failure/` remain
retained. The successful stage uses short DOS workdir `probe/af527b` and
retained raw outputs/writer logs with the `af527b-` prefix; their actual paths
are bound in the after527 receipt. No Wine prefix reset or evidence cleanup
was performed.

The [independent reviewer](../scripts/review_th03_mainl_after527_work.py)
checks all eight TUs, two include hashes, recipe/parent receipt, actual writer
logs and both full OBJ/LIB/EXE/MAP vectors. All evidence and scratch remain.
No full cold replay, new runtime model or redundant test matrix was used.

Current working-source CRT: **774/893 complete members, 202,930 original-equal
CODE-segment bytes**. Original slots **740–824 now all source-link** in this
working library. Formal Factory canonical packed-file acceptance remains
**0/250**; whole-game completion is unknown.

Receipt: `.analysis/work/mainl-after527-stream-integer-assign-final-eight-build.json`

SHA-256: `e353d9add7801b06681b4a81df6b50f0d4cf13a66bf1fd019fdf04fb1be425d8`.

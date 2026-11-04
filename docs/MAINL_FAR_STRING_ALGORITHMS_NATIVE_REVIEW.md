# TH03 Japanese CRT: complete far-string search, comparison and transforms

Thirteen genuinely **selected original** Borland large-model CRT members
have been restored to true 16-bit symbolic 8086 assembler source. They are
complete algorithms for far-pointer character searches and comparisons,
not wrappers or copied machine-CODE arrays:

| Original CRT slot | Module | Complete CODE |
| ---: | --- | ---: |
| 459 | `fstrstr` | 108 |
| 458 | `fstrspn` | 82 |
| 454 | `fstrpbrk` | 80 |
| 444 | `fstrcspn` | 73 |
| 452 | `fstrnicm` | 68 |
| 446 | `fstricmp` | 65 |
| 440 | `fstrcat` | 63 |
| 456 | `fstrrev` | 52 |
| 434 | `fmemchr` | 37 |
| 435 | `fmemcmp` | 40 |
| 447 | `fstrlen` | 33 |
| 448 | `fstrlwr` | 38 |
| 461 | `fstrupr` | 38 |

The source retains original far ES/DS ownership, 16-bit byte/word scan,
comparison and REP string instruction forms, original branch behavior,
unchecked caller pointers and exact far return ABI. All original public
names and CODE+0 offsets, empty external imports, empty DATA/BSS and the
**original per-member DGROUP order** are preserved (some use `_BSS,_DATA`,
others `_DATA,_BSS`). No original machine-code byte-array initializers,
padding or patched native objects.

The genuine selected BCC object revealed a subtle original 8086 encoding
issue: `XCHG DX,CX` versus `XCHG CX,DX`, `XCHG BX,DI` versus `XCHG DI,BX`,
and `XCHG DI,SI` versus `XCHG SI,DI` have identical mathematical effects but
may assemble to different ModRM fields. This affected four instructions in
`fstrstr`, one in `fstrcat`, and one in `fstrrev`. The symbolic operands
were deliberately oriented to reproduce **the original opcode**; no output
byte patch or alternative altered ABI was accepted.

All thirteen selected original CRT program slots now reassemble normally in
TASM 5.0 `/m /mx /kh32768 /t` with **777/777 original CODE bytes** and the
literal original **empty OMF FIXUPP inventory**. This is original payload
and reloc-field proof, not a claim of complete literal OBJ-record equality
for every other record type.

`scripts/build_th03_mainl_after155_work.py far-string-algorithms` validates
the full source-bound 62→155 original member receipt DAG, then produces two
independent normal TASM/TLIB/TLINK rounds adding only these 13 members.
Both reconstruct the complete original **67,372-byte decoded Japanese
MAINL EXE and MAP byte-for-byte**, including all **677 ordered DOS MZ
relocations**, leaving **725** original contextual vendor program records
unchanged. Working CRT grows to **168 source-built members / 72,053 original-
equal CODE bytes**. This is working source progress, not formally accepted
ledger credit or whole-game source completion. No full cold replay was run.

Proof: `review_th03_mainl_after155_work.py far-string-algorithms` and
`tests.test_mainl_after155_work`, with two complete native OBJ/LIB/EXE/MAP
pairs, original writer logs and hash-bound receipts under
`.analysis/work/after155-*` and `.analysis/work/mainl-after155-*`.

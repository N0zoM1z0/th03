# Four complete dual-CODE string exception members — after523

The four largest remaining original Japanese CRT members at after522 are now
maintained as complete source TUs:

| Original slot / member | Far API | `_TEXT` | `_TEXTC` | Ordered FIXUPPs |
| --- | --- | ---: | ---: | ---: |
| 387 / [copy2](../src/mainl/crt/copy2.asm) | `string::copy(char*, unsigned, unsigned)` | 96 | 237 | 13 |
| 390 / [ctor2](../src/mainl/crt/ctor2.asm) | `string::string(const string&)` | 96 | 233 | 14 |
| 413 / [oprcall1](../src/mainl/crt/oprcall1.asm) | `string::operator()(unsigned)` | 96 | 232 | 14 |
| 414 / [oprcall2](../src/mainl/crt/oprcall2.asm) | `TSubString::operator()(unsigned)` | 96 | 251 | 14 |

All four original segment inventories remain separate and ordered:
`_TEXT`, empty `_DATA`, empty `_BSS`, `_TEXTC`, with the original DGROUP.
Their **1,337 CODE-segment bytes** comprise **757 executable bytes and 580
inline exception/RTTI bytes**. These figures are not extra physical MAINL
bytes, and metadata is not treated as disassembled instructions.

The proved common [local exception owner](../src/mainl/crt/string_xmsg_unwind.inl)
is a bounded per-TU include: the five-byte unwind, original exception header
and BP-1Eh registration frame, and the complete 77-byte xmsg cleanup. It
retains destructor-count updates, real xmsg destruction, optional delete,
and the original null-object branch. It contributes its own 96 bytes to each
original member; no linker-level sharing or segment flattening is introduced.

The [typed RTTI include](../src/mainl/crt/string_xmsg_rtti.inl) supplies one
derived `string::outofrange` or `xalloc` descriptor, its symbolic cleanup
pointer, the typed base descriptor, and the xmsg RTTI/destructor fields.
Native statement chunks preserve original FIXUPP chronology. Every byte in
both CODE segments is materialized once: no padding, missing-byte allowances,
target instruction arrays, or object patches are used.

The API bodies preserve actual range assertions, copy-on-write cloning,
substring offsets, optional constructor allocation and reference counting.
`copy2` retains the original unchecked subtraction and count-plus-one memcpy;
no defensive behavior is added. The exception ABI requires **AX = SEG of the
local unwind owner**, while BX contains its exception-frame offset. Complete
field comparison distinguishes that segment relocation from an incorrect
OFFSET spelling even though both raw object operands initially contain zero.

All **55 literal ordered OMF FIXUPP fields** match, including relocation kind,
width, frame, symbolic target and addend. Both CODE segments, initialized-byte
coverage, import order, far publics and GROUP layout match the original
CL.LIB members. Complete Borland raw OBJ program-record identity is not claimed.

The [after523 producer](../scripts/build_th03_mainl_after523_work.py) extends
the unchanged after522 source-bound pair using only four new TASM assemblies
per round and native TLIB/TLINK. Both full **67,372-byte decoded MAINL EXEs,
original MAPs and 677 literal ordered MZ relocations** match the Japanese
target. The original 893-member order, all earlier 730 source members and
159 remaining vendor members are preserved.

The [independent reviewer](../scripts/review_th03_mainl_after523_work.py) binds
the four TUs, both include hashes, producer, parent receipt, actual writer logs
and both complete OBJ/LIB/EXE/MAP vectors. No full cold replay, new runtime
model or redundant test matrix was performed. All new raw evidence and scratch
are retained under the existing storage restrictions.

Current working-source CRT: **734/893 complete members, 197,750 original-equal
CODE-segment bytes**. This adds four complete members / 1,337 CODE-segment bytes.
Formal Factory canonical packed-file unit acceptance remains **0/250**;
whole-game completion is unknown.

Receipt: `.analysis/work/mainl-after523-string-dual-code-exception-four-build.json`

SHA-256: `d1068ab8fe10b58bddf58f7c95048267d21b8915c064962a05d799db838c74ad`.

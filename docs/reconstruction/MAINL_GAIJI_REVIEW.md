# Complete MAINL gaiji candidate review

Four disjoint decoded extents add 434 independently reviewed bytes: backup /
restore 64 at 0C72..0CB1, BFNT registration 150 at 0CB2..0D47, reading 108 at
0D48..0DB3, and writing 112 at 0DB4..0E23. Nine complete bodies total 430 bytes
/227 instructions, including seven emitted NOPCALL NOPs; four trailing EVEN
NOPs complete the extents. Private GETFONTW and SETFONTW are tested through
their complete public callers. Prior native heap 628, stack 76, BFNT skip 34,
header read 59 and DOS-open 26 are 823 context bytes, without duplicate credit.
All 1,257 scoped CODE/producer bytes and the ten bytes of backup state/header
template match both cold products, with empty ordered relocation lists.

```sh
python3 scripts/review_th03_mainl_gaiji.py --output .analysis/NEW_GAIJI_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_gaiji_review.py -v
```

Receipt: `.analysis/sol-mainl-gaiji-review-20261006.json`, SHA-256
`862d1c5a3085db80ee350eb9e1257f46d0a6a632b870edf880f083dce8eb74dc`.
Its 782 guarded inputs retain the preceding graphics receipt's stored/decoded
lineage and both fresh MAINL compiler products from the pinned complete MAIN
cold replay. Twenty-eight consulted frozen providers match both cold trees.
ASM/INC normalize only LF/CRLF. Prior MAIN forwarders and seven MAIN-only
Tupfile substitutions remain explicit scaffold lineage, without gaiji changes.
Root OMF identity is TASM5/th03_mainl.asm; normalized hashes match both cold
rounds and their original receipt. The 152 archived repository inputs retain
the original snapshot hashes. This diagnostic runs no new compiler build.

Both MAPs place every scoped body inside root _TEXT at 0272,size10944 and
confirm all seven public gaiji entries. Four decoded module rows add no
maintained source, canonical stored-file offset or exact acceptance. Root
CODE/DATA/BSS, CRT, complete linker ownership, real DOS/device behavior and
canonical DIET packaging remain separate open work.

| Complete body | Decoded offset | Bytes /instructions | Return |
| --- | --- | ---: | --- |
| GAIJI_BACKUP | 0C72 | 36 /18 | RETF |
| GAIJI_RESTORE | 0C96 | 28 /15 | RETF |
| GAIJI_ENTRY_BFNT | 0CB2 | 150 /82 | RETF4 |
| Private GETFONTW | 0D48 | 33 /17 | near RET |
| GAIJI_READ | 0D6A | 37 /21 | RETF6 |
| GAIJI_READ_ALL | 0D90 | 36 /16 | RETF4 |
| Private SETFONTW | 0DB4 | 33 /17 | near RET |
| GAIJI_WRITE | 0DD6 | 39 /23 | RETF6 |
| GAIJI_WRITE_ALL | 0DFE | 38 /18 | RETF4 |

## Native execution and declared models

Each of three images passes 2,302 terminal scenarios, 2,322 top-level calls and
26,030 native entries: totals 6,966 calls and 78,090 entries. All instructions
in the nine new bodies are visited. Twelve separate 1,000-instruction budgets
retain 24 open backup/heap frames and no physical stores or font writes.
They exercise a supplied cyclic used-block heap chain; they are validated
prefixes, without a fabricated return or allocation success.

Tests cover all 256 low-byte character codes and five high-word aliases,
IF0/1 and DF0/1, incoming Carry0/1 for both ALL entries, unaligned/wrapping
pointers, backup allocation boundaries, native automatic DOS assignment and
failure, repeated backup/restore, malformed BFNT headers, seek/close failure,
short/stale/carry-marked reads, and connected backup/write/load/restore calls.
Actual native procedures include both near font helpers, heap/stack/header /
skip/open context, real calls, RETFs/RETs and caller stack locals.

The independent scalar model compares AX/Carry where defined, IF/DF, native
entry counts, complete DOS requests, ordered IN/OUT site/width/value/live IF /
DF, all 8,192 modeled font bytes, final device latches, and every byte of
1MiB physical memory outside the declared 64KiB stack after each return or
budget prefix. Epilogue guards check actual frames, Pascal cleanup and
BP/SI/DI/DS preservation. Other clobbered registers are observed and compared
across images. Full arithmetic flag preservation is not claimed. Cross-image
comparison omits whole-memory hashes because unrelated PI/DGROUP bytes
differ; each image still receives its own complete memory comparison.

MZ relocates to 2000, DGROUP2E3F and stack4000. The fixtures supply heap /
stack state and optional segment headers. Synthetic pattern/heap memory
spans 50000..A0000 inclusive, initialized by `(index*37+3)&255`, including
whole offsetFFFF word stores. Source filename is synthetic at 5000:0100.
Font data is a separate 256×16×2 byte model, initialized by character, row,
half and seed. It interprets byte OUT68 access modes 0B/0A, A1/A3 code latches,
A5 row/half latch and A9 data transfers. READ requests right half before left;
STOSW stores left byte then right. WRITE loads that word and emits left then
right. Native IN/OUT instructions drive the model, not helper replacements.
Actual CG RAM, timing, hardware eligibility, text flicker and asynchronous
interrupts remain unproved. No MEM_READ hook is installed.

DOS21 open3D/read3F/seek42/close3E and heap48/49 replies are explicit models,
including AX/Carry, short/stale data, handle and destination. Registration's
header local is at SS:FF9A under the declared caller frame. BFNT magic is read
from target DGROUP051C; backup word055A and mono template055C (`16,16,0,255`)
are separately observed data. The latter ten raw bytes match both products;
this does not accept the complete DATA graph or game assets/filesystem.

Eight controls reject truncated/incorrect cleanup, missing PUSH CS, unknown
calls/indirect/far edges, operand/neighbor branches, wrong port widths/sites,
unknown DOS sites, altered producer/template data, bare private helper entry,
wrong near/far frames, invalid font latch mode, whole-span stores outside
declared state, stale completion and segment aliases. A positive control
executes a real near CALL/RET inside a complete public far frame. Mutants are
test fixtures, not recovered product source.

## Behaviors to preserve

Single READ/WRITE fetch Pascal arguments by moving SP under CLI, then execute
STI unconditionally. All subsequent font transfers therefore have IF1 even
when the caller entered with IF0. ALL entries retain incoming IF. None executes
CLD: LODSW/STOSW preserve DF and wrap each updated offset at 16 bits. DF1
therefore walks backwards through caller buffers and can write beyond the
8KiB allocated backup area despite completing all 256 glyphs. Connected
backup/restore with the same DF reproduces the original modeled font bank,
while the independent physical-memory comparison retains those stores.

Single entries discard the character high byte and form `5680+low_byte`,
masking AL to7F. ALL entries use ADC for the first character before any flag
clearing. Incoming Carry1 selects glyph1 first; the next iteration also
selects glyph1, leaving glyph0 untouched. Reads duplicate glyph1 into the
first two output records; writes overwrite glyph1 twice and discard the first
input record. Later iterations run normally. Backup/restore and BFNT loading
clear Carry before calling ALL, but direct public ALL callers must supply the
intended flags.

BACKUP rejects an existing nonzero marker, requests 512 heap paragraphs,
stores the returned segment and reads the full font bank. It returns0 on
failure and1 on success. RESTORE clears the marker before writing and freeing
the buffer, then returns1 even if native free rejects an invalid segment.
The invalid-free fixture retains Carry1 and a cleared marker. Repeated
RESTORE with marker0 returns0. The cyclic heap budget remains inside native
allocation before any marker/font mutation.

ENTRY_BFNT opens, allocates one 8KiB stack region, reads a native 32-byte
header and requires color0 and the four mono template words. HEADER_READ
retains DF and does not enforce its returned read length when Carry0. A
default forward header fails under DF1. Extension seek Carry is ignored.
The data read is accepted solely when AX==8192: Carry1/AX8192 still writes the
modeled font bank and returns1, including stale buffer contents when the DOS
failure fixture supplied no bytes. Every allocated path releases the original
stack mark; every successful open path closes, without exposing close failure
as registration failure. Actual filesystem and complete game callers remain
open rather than being inferred from these interface scenarios.

Byte0C71 is observed00 in all three images, between the preceding public GDC
near RET and GAIJI_BACKUP at0C72. The frozen FUNC macro has an initial EVEN
outside the preceding procedure; its producer attribution remains an
inference. That byte is observed separately and receives no function or
independent-unit credit. Decoding from0C71 would cross the verified XOR at
0C72. The complete gaiji bodies begin at their actual instruction boundaries.

The separate MAP/ledger interval union now covers 6,720 of 10,944 root _TEXT
bytes, leaving 4,224 without independent unit rows and zero overlap. Replay
`scripts/review_th03_mainl_coverage.py --output .analysis/NEW_MAINL_COVERAGE.json`.
The previous 5,133/4,658-gap snapshots remain historical evidence. Gaps can
include prior native context, alignment and CRT; they are not an unknown
semantic byte count.

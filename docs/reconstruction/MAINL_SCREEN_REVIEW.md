# Complete MAINL screen candidate review

Three disjoint decoded extents add 222 independently reviewed bytes: mode
78 at 0E24..0E71, clear 36 at 0E72..0E95, and private plane/public copy 108
at 0E96..0F01. Four complete bodies total 218 bytes /95 instructions,
including two emitted NOPCALL NOPs; four trailing EVEN NOPs complete the
extents. Private COPY_PLANE runs through its complete public caller. Native
heap 628 and stack 76 are 704 prior context bytes, without duplicate credit.
All 926 scoped CODE/producer bytes and 28 separately observed clip/VRAM DATA
bytes match both cold products, with empty ordered relocation lists.

```sh
python3 scripts/review_th03_mainl_screen.py --output .analysis/NEW_SCREEN_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_screen_review.py
```

Receipt: `.analysis/sol-mainl-screen-review-20261006.json`, SHA-256
`f773b9b9871b32b98f625efc881c04aecff7749dfd65ea984721fdc5bcee8a86`; 793 guarded inputs.

The guarded receipt retains the preceding gaiji receipt's stored/decoded
lineage and both fresh MAINL compiler products from the pinned complete MAIN
cold replay. Twenty-three consulted frozen providers match both cold trees.
ASM/INC normalize only LF/CRLF. Prior MAIN forwarders and seven MAIN-only
Tupfile substitutions remain explicit scaffold lineage, without screen changes.
Root OMF identity is TASM5/th03_mainl.asm; normalized hashes match both cold
rounds and their original receipt. The 152 archived repository inputs retain
the original snapshot hashes. This diagnostic runs no new compiler build.

Both MAPs place every scoped body inside root _TEXT at 0272,size10944 and
confirm GRAPH_400LINE/CLEAR/COPY_PAGE entries. Three decoded module rows add
no maintained source, canonical stored-file offset or exact acceptance.
Complete root CODE/DATA/BSS, CRT/linker ownership, actual DOS/BIOS/device
behavior and canonical DIET packaging remain separate open work.

| Complete body | Decoded offset | Bytes /instructions | Return |
| --- | --- | ---: | --- |
| GRAPH_400LINE | 0E24 | 77 /26 | RETF |
| GRAPH_CLEAR | 0E72 | 35 /19 | RETF |
| Private COPY_PLANE | 0E96 | 21 /11 | near RET |
| GRAPH_COPY_PAGE | 0EAC | 85 /39 | RETF2 |

## Native execution and declared models

Each of three images passes 1,188 terminal scenarios, 1,200 top-level calls
and 2,112 native entries: totals 3,600 calls and 6,336 entries. All instructions
in the four new bodies are visited. Twelve separate prefixes complete five
native automatic assignments to segment0 each, then stop at the actual retry
entry with two open copy/stack frames. They match the independent scalar
prefix, including ten DOS requests each, DATA mutation and full physical
memory. They are not returns; no ports or screen stores occur. The declared
1,000-instruction cap is a secondary limit; the actual stop is the five-
assignment semantic budget at SMEM_WGET entry, with TOP still0.

Tests cover all 256 BDA clock-byte values, explicit Carry0/1 BIOS responses,
IF0/1 and DF0/1, selected word counts through65535 at allocation/offset/count boundaries,
six page-word aliases, native heap collisions and automatic assignment /
failure, connected mode/clear/copy calls, and temporary-buffer aliasing with
the selected video aperture. Actual private near CALL/RET and far/Pascal
stack calls execute; helpers are not replaced by callbacks.

The independent scalar model compares AX/Carry where defined, IF/DF, native
entry counts, complete BIOS/DOS requests, ordered byte OUT site/value/live
IF/DF, ordered stores from the four new bodies, both synthetic video banks,
mode/tile latches,
and every byte of 1MiB physical memory outside the declared 64KiB stack after
each return or budget prefix. Epilogue guards check actual frames, RETF2
cleanup and BP/SI/DI/DS preservation. Other clobbered registers are recorded
and compared across images. Full arithmetic flag preservation is not claimed.
Cross-image comparison omits whole-memory hashes because unrelated PI/DGROUP
bytes differ; each image still receives its own complete memory comparison.

MZ relocates to 2000, DGROUP2E3F and stack4000. Fixtures supply heap/stack state
and optional headers. Patterned memory spans 50000..A0000 inclusive using
`(index*37+3)&255`. Four 32KiB synthetic apertures start at A8000, B0000,
B8000 and E0000. Each bank is initialized by `(page*97+plane*53+offset*13+11)&255`.
Every native OUTA6 saves all four current apertures into the selected bank,
then loads bank0/1. CPU stores and sequential native MOVSW reads use the actual
mapped physical memory, including aliasing; no MEM_READ hook is installed.
Synthetic overflow regions C0000..C8000 and E8000..F0000 inclusive use
`(index*29+A5)&255` and are not banked. Whole offsetFFFF word stores are retained.
These regions do not establish real video/ROM/bus behavior.

BIOS18/AH42/CHC0 replies explicitly supply AX/Carry only; initial caller AX1111
and CX3333 yield requests AX4211/CXC033. Real BIOS register effects and page
selection are open. DOS21/48/49 replies use the existing declared allocation
model. GRCG byte OUT7C/7E records mode and four tile values; actual accelerated
multi-plane writes, timing and asynchronous interrupts are not modeled.
GRAPH_CLEAR's flat CPU stores therefore do not prove physical screen clearing.

Clip DATA0522..0531 and VRAM DATA0564..056F are separate raw observations.
Only the declared mutable words are writable in the execution fixture; full
DATA/BSS ownership and game initialization remain unaccepted.

Eight controls reject truncation/incorrect cleanup, missing PUSH CS, unknown
calls/indirect/far edges, operand/neighbor branches, wrong service or port
sites/widths, altered producer bytes, bare private helper entry, wrong native
near/far frames, invalid page values, whole-span stores outside declared state,
stale completion and segment aliases. Positive controls execute eight real
private near frames and actual synthetic bank exchange. Mutants are test
fixtures, not recovered product source.

## Behaviors to preserve

GRAPH_400LINE issues BIOS18 then overwrites clip/VRAM fields regardless of
the supplied BIOS Carry. It sets segmentA800, words16000, lines400, inclusive
clip bounds639/399 and bottom address31920. Byte0000:054D mask04 selects zoom
0000 or4000. graph_VramWidth is untouched. Declared returns observe AX399,
Carry0, ES0 and preserved IF/DF; the actual BIOS interface can have additional
effects that this model does not prove.

GRAPH_CLEAR masks interrupts only around its first GRCG mode OUT. PUSHF/POPF
restores incoming IF before the four tile OUTs and REP STOSW; IF0 remains0.
The upstream comment claiming that interrupts are enabled contradicts these
instructions and native execution. No CLD is executed. DF1 writes backwards
from offset0 with 16-bit wrapping, retaining all resulting physical stores.
The final mode is0 and all four modeled tiles are0; DI is restored and AX /
Carry are0 in the declared fixture.

GRAPH_COPY_PAGE requests `u16(words*2)` bytes from native SMEM_WGET. Allocation
failure returns AX0/Carry1 without video ports. Success disables GRCG, masks
the page argument to its low bit, and calls COPY_PLANE eight times, reading
then writing each plane through the temporary segment. Each helper toggles
the access page, swaps source/destination segments, and sets the next count
to `u16(final_DI)>>1`. The last selected page is the requested low bit. Native
SMEM_RELEASE receives the original temporary mark; success returns AX1.

The frozen private-helper contract requires DF0, but the public entry never
executes CLD. Diagnostic DF1 results deliberately exercise outside that
precondition: words7 transfers7 words first, then32761 on the next leg, and
the four plane pairs perform 131,072 word stores overall. The nominal14-byte
allocation cannot bound those stores. Even with DF0, words32768 wraps DI to0
after the first leg; subsequent legs transfer0. Count32769 similarly reduces
later legs to1. Sequential scalar accesses retain overlapping temporary/video
buffers instead of incorrectly snapshotting source bytes. These observations
do not establish that complete game callers violate the helper precondition.

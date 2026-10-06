# Complete MAINL EGC, box fill and near GDC candidate review

Three disjoint decoded extents add475 independently reviewed bytes: EGC98 at
0724..0785, box fills366 at0AC8..0C35 and public near GDC11 at0C66..0C70.
Six complete bodies total470 bytes /225 instructions, including five interior
EVEN NOPs; five additional trailing NOPs complete the extents. Prior GRCG
color/off46 body bytes are native context, without duplicate credit. Their
two trailing NOPs remain uncredited. All523 scoped CODE/producer bytes and
the34-byte read-only EDGES table match both cold products, with empty ordered
relocation lists. Three decoded module rows add no maintained source,
canonical stored-file offset or exact acceptance.

```sh
python3 scripts/review_th03_mainl_graphics.py --output .analysis/NEW_GRAPHICS_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_graphics_review.py -v
```

Receipt: `.analysis/sol-mainl-graphics-review-20261006.json`, SHA-256
`3b6525b43cf3f75885987ba9c190d0cf70bb2329e42d7fe7808c999c47773bd1`.
Its731 guarded inputs retain the prior BFNT/super stored/decoded lineage and
bind both recently completed cold MAINL products from
`sol-main-restored-aggregate-20261006`. This diagnostic performs no new build:
the pinned cold receipt supplies two fresh compiler rounds, full product
hashes and dependency-timestamp-normalized root OMF hashes. Its152 archived
repository inputs are checked against the original snapshot hashes. Later
live ledger updates do not rewrite that immutable build snapshot.

Eleven consulted frozen providers are compared with both cold source trees.
ASM/INC normalize only LF/CRLF; seven prior MAIN-only Tupfile substitutions
and MAIN-owned forwarders remain explicit scaffold lineage. Graphics includes
are unchanged. Both root objects identify TASM5 /th03_mainl.asm and agree
after dependency timestamp normalization. MAP containment puts every body
inside root _TEXT at0272,size10944. All nine scoped public entries/aliases are
checked in both MAP files. Other root CODE, DATA/BSS, CRT, linker ownership
and physical DIET packaging remain separate open work.

| Complete body | Decoded offset | Bytes /instructions | Return |
| --- | --- | ---: | --- |
| EGC_ON | 0724 | 21 /11 | RETF |
| EGC_OFF | 073A | 31 /15 | RETF |
| EGC_START /EGC_END alias | 075A | 43 /20 | RETF |
| GRCG_BOXFILL with private return prefix | 0AC8; public0ACE | 213 /102 | RETF8 |
| GRCG_BYTEBOXFILL_X | 0B9E | 151 /71 | RETF8 |
| Public gdc_outpw | 0C66 | 11 /6 | near RET |
| Prior GRCG_SETCOLOR | 0C36 | 41 /21 | RETF4 |
| Prior GRCG_OFF | 0C60 | 5 /3 | RETF |

## Native execution and limits

Each of three images passes3220 scenarios,3240 terminal calls and4272 native
entries. Totals are9720 terminal calls and12816 entries. Twelve separate
1000-instruction budget observations retain open frames and963 checked store
events each; they do not claim returns. IF0/1 and DF0/1, all64 combinations of
the six arithmetic flags, mode/color aliases, GDC byte order, all16 pixel
left masks, width boundaries, both coordinate orders, signed extremes,
nonzero/zero clipping, four byte-address/width parity paths and a connected
EGC/color/pixel/byte/off sequence execute natively. Every reachable guarded
instruction is visited; the only unvisited static boundaries are unreachable
post-return EVEN NOPs at0B89 and0C13.

The independent scalar model compares ordered physical stores, port site /
width /value /live IF /DF, native entries, defined arithmetic flags, AX/ES
where modeled, and all1MiB of physical memory outside the declared64K stack.
Probe epilogues separately check actual near/far frames, Pascal cleanup and
preserved registers. Other clobbered registers are observations, compared
across images. Undefined XOR AF is excluded from the scalar flag contract.
Cross-image rows omit whole-memory hashes because unrelated PI and DGROUP
bytes differ; each image still receives its own complete memory comparison.

MZ relocates to2000, DGROUP2E3F and stack4000. Fixtures supply ClipXL0522,
ClipXW0524, ClipYT0528, ClipYH052A and ClipYT_seg052E. EDGES0532 retains all17
observed word masks and is checked independently by byte swapping the first
N pixel bits. Default clipping is0..639 /0..399; the nonzero fixture starts
at37,19 with relative bounds180,73 and segmentA85F. Flat synthetic physical
VRAM spansA8000..C0000 inclusive, covering modular offset wraps and whole
word-store spans. This broad allowed span is not a hardware plane model.
GRCG/EGC latch, masking, bus timing, display, real asynchronous interrupts
and full game callers remain unproved. No DOS or BIOS calls are intercepted.
No MEM_READ hook is installed.

Eight focused controls reject truncation/cleanup, unknown/indirect/far calls,
missing PUSH CS, branches into operands/neighbors, altered port widths/sites,
unexpected input/interrupts, changed masks/alignment, wrong real frames,
whole-span stores outside declared VRAM, stale completion and segment aliases.
Positive controls execute real PUSH CS/near CALL/RETF and the public near
frame. Synthetic mutants are guard verification, never product source.

## Observed semantics to preserve

EGC_ON emits five byte writes on7C/6A. OFF emits two word writes on4A0/4A8
and four byte writes on6A/7C. START and END are the same public address:
they call native ON, emit five word register writes, then call native OFF.
The final state is the OFF sequence; END also performs the initialization
transient. AX becomesFF06 and DX4A8; XOR AX in START changes arithmetic flags.
All EGC entries retain IF/DF. GDC is explicitly public near source, so its
native near frame is reviewed directly. It writes low AL then high AH as two
byte OUTA0 instructions, separated by two short jumps; returned AL equals AH.
The jump sequence is observed encoding, without a physical timing guarantee.

SETCOLOR pushes flags, disables interrupts for mode and four tile outputs,
then restores flags. Mode/color high words are ignored; four low color bits
select FF/00 tile values. OFF clears AL, writes mode0 and changes arithmetic
flags while preserving AH, IF and DF. These bodies remain prior context.

Pixel BOXFILL disables interrupts while fetching Pascal arguments by moving
SP, then unconditionally enables them before any clipping or early return.
It orders each coordinate pair, clips with a mixture of signed comparisons,
unsigned saturation and sign-bit tests, and computes segment-base /word masks
with16-bit arithmetic. Signed subtraction overflow therefore matters: the
Y-bottom JS test differs from a signed less-than comparison. Masks are
byte-swapped words; the first-pixel edge is0080, not8000. Wide rows emit first
mask, full middle words and last mask; short rows emit their intersection.
Row termination is DI subtraction borrow, not an independent height count.

BYTEBOXFILL clips only Y and never orders endpoints or checks horizontal
bounds. It computes ES before either early-return comparison. Four layouts
handle byte-origin/width parity; width and DI wrap16 bits. Both box functions
retain incoming DF and perform real STOS/REP stores. With DF1, the store
direction reverses while the row subtraction remains unchanged, changing
row progression and termination. Signed-extreme X can wrap the inclusive
width to zero orFFFF; the FFFF case is recorded as a checked execution prefix.
Preserve these observed behaviors when recovering natural source; do not
replace them with clipping or ABI improvements under an exactness claim.

The separate replayable MAP/ledger interval union now covers6286 of10944
root _TEXT bytes, leaving4658 without independent unit rows and zero overlap.
Run `scripts/review_th03_mainl_coverage.py --output .analysis/NEW_MAINL_COVERAGE.json`.
The old5133-gap snapshot is preserved; these gaps can contain prior native
context and producer alignment, so they are not an unknown-semantics count.

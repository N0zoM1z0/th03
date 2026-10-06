# Complete MAINL drawing, scroll and show candidate review

Six disjoint decoded extents add 1,680 independently reviewed bytes: gaiji
drawing148 at0F58..0FEB, clipped packed drawing212 at162C..16FF, scroll88 at
1700..1757, show6 at1758..175D, unclipped packed drawing202 at2C68..2D31 and
read-only RotTbl1024 at1AAA..1EA9. Five complete public bodies and two shared
return tails total654 bytes /287 instructions, including two interior EVEN
NOPs. Two trailing EVEN NOPs complete656 instruction/producer bytes. RotTbl
is CODE-resident data, not a function or 1,024 additional instructions.
Prior public near GDC helper11 bytes /6 instructions is native context,
without duplicate credit. All1,691 scoped CODE/producer/table bytes and28
separate clip/VRAM DATA bytes match both cold products, with empty ordered
relocation lists.

Offsets, segments, ports and encoded words below are hexadecimal; byte and
instruction counts are decimal.

```sh
python3 scripts/review_th03_mainl_draw.py --output .analysis/NEW_DRAW_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_draw_review.py
```

Receipt: `.analysis/sol-mainl-draw-review-20261006.json`, SHA-256
`e5cf07b16edd05e7c0883c8283fe8707c257f5c0b70bb080c0061237297a2608`; 808 guarded inputs.

The receipt retains the preceding screen receipt's stored/decoded lineage
and both fresh MAINL compiler products from the pinned complete MAIN cold
replay. Nine consulted frozen providers match both trees. ASM normalize only
LF/CRLF. Prior maintained MAIN forwarders and seven MAIN-only Tupfile remaps
remain explicit scaffold lineage. The TASM5/th03_mainl.asm root OMF normalized
identity agrees across both cold rounds and their original receipt; all152
archived repository inputs retain their snapshot hashes. This diagnostic
runs no new compiler build or product-source migration.

Both MAPs place all scopes inside root _TEXT at0272,size10944 and confirm five
new public entries, GDC helper and RotTbl. Six decoded module rows have empty
source and canonical stored-file offset fields. Root CODE/DATA/BSS, CRT/linker
ownership, actual BIOS/GRCG/GDC/font behavior and canonical DIET packaging
remain separate open work; neither source nor exact acceptance is granted.

| Complete body or tail | Decoded offset | Bytes /instructions | Return |
| --- | --- | ---: | --- |
| GRAPH_GAIJI_PUTC | 0F58 | 147 /69 | RETF8 |
| Clipped PACK early return tail | 162C | 6 /4 | RETF10 |
| GRAPH_PACK_PUT_8 | 1632 | 206 /85 | RETF10 |
| GRAPH_SCROLLUP | 1700 | 88 /40 | RETF2 |
| GRAPH_SHOW | 1758 | 5 /3 | RETF |
| Unclipped PACK early return tail | 2C68 | 6 /4 | RETF10 |
| GRAPH_PACK_PUT_8_NOCLIP | 2C6E | 196 /82 | RETF10 |

The early-return tails are reached by branches from the complete public
callers and pop their actual saved DI/SI/BP before RETF10. They are not entered
as independent far functions. Four real near CALL/RET pairs in SCROLLUP use
the prior GDC helper, which emits AL then copies AH to AL and emits that byte.
It leaves both AX bytes equal to the original high byte; it does not rotate
and restore the original word.

## Native execution and explicit models

Each of three images passes7,196 terminal scenarios /7,212 top-level calls
and13,868 native entries: totals21,636 calls and41,604 entries. All287 new
instructions are visited. Forty-eight separate1,000-instruction GDC budgets
remain in the polling loop with48 open public frames and no stores or OUTs.
The static prefix has14 instructions and the loop four; each budget must
perform247 byte INs and stop at1724 before TEST. Expected phase/count comes
from the decoded partition independently of execution observations. These
prefixes do not fabricate readiness, parameter output, preservation at an
epilogue or a public return.

Scenarios include all256 low-byte characters with Carry0/1×IF0/1×DF0/1,
six character-word aliases, all16 low colors at eight pixel shifts, wrapping
coordinates, all256 source-byte values in each of four PACK slots for both
entries, signed X/length boundaries, vertical clip/wrap combinations,
unaligned/wrapping source offsets and source/video aliasing. SCROLLUP covers
all401 normal/sentinel line values through400 plusFFFF at zoom0/4000,
additional line/zoom boundaries, all256 status bytes, delayed readiness and
declared busy budgets. SHOW uses explicit BIOS AX/Carry responses. Connected
calls retain memory/device state while supplying the same declared fresh
caller registers/flags at each public entry.

The independent scalar compares AX/Carry where specified, IF/DF, native
entry counts, complete BIOS requests, every ordered byte IN/OUT including
site/value/live IF/DF, all ordered physical stores from the new bodies, device
latches and every byte of1MiB physical memory outside the declared64KiB
stack. Guards check actual far/Pascal/near frames and BP/SI/DI/DS preservation
after returns. Other clobbered registers are recorded and compared across
images; full arithmetic flag preservation is not claimed. Every trace is
compared in full before recording count/SHA-256 and bounded first/last port
samples. Cross-image comparison omits whole-memory hashes because unrelated
PI/DGROUP bytes differ; each image receives its own full memory comparison.

MZ relocates to2000, DGROUP2E3F and stack4000. Source memory50000..5FFFF uses
`(index*37+3)&255`. Synthetic flat video/overflow memory A8000..FFFFF uses
`(index*17+5)&255`; it is neither a physical VRAM/ROM/bus model nor a banked
aperture. Declared clip/video segments includeA800/A801; physical whole-word
stores at offsetFFFF are retained. Source fixture bytes wrap their16-bit
offsets and can alias the drawing apertures. Native CPU reads and stores,
including RotTbl reads, execute without a MEM_READ hook.

The read-only font model defines all256 high latches×128 masked low latches.
For latch index `high*128+low`, row and half, the byte is
`(index*29+row*7+half*113+seed)&255`; row-latch mask20h selects half0, otherwise
half1. Modes0B/0A and A1/A3/A5/A9 operations are checked explicitly. Actual
font contents, eligibility, timing and GRCG accelerated multi-plane writes
remain unproved. GRCG records mode and four tiles; CPU video stores are flat.
GDC status is an explicit supplied sequence with a held final byte. All
command/parameter OUTs are native; actual FIFO timing/display effects are
open. BIOS18/AH40 at175A supplies AX/Carry only; request AX4011 follows the
declared AX1111 caller. Actual BIOS register/device effects remain open.

Unicorn's declared x86 model masks variable shift counts to five bits.
Unusual zoom low bytes32/33/255 and FFFF are diagnostic model cases, not
physical V30 shift-semantics proof. Normal supplied zoom0/4000 uses low count0.
Separate clip0522..0531/VRAM0564..056F raw DATA equality grants no complete
DATA graph, assets or initialization acceptance.

Eight controls reject incomplete/incorrect cleanup, unknown native/indirect /
far edges, operand/table/neighbor branches, wrong service/port sites/widths,
producer mutations and one-bit mutations in every RotTbl entry. Runtime
controls exercise four actual near frames, reject bare helpers/shared tails,
wrong return frames, font mode/latches, unknown BIOS/GRCG requests, whole-span
stores outside the declared video region, stale completion and segment
aliases. A separate synthetic polling prefix checks actual native budget
phase/input counts without a fabricated return. Scalar controls verify CLD,
negative-X source direction, ADC Carry, IF/DF and scroll parameter splitting.
Mutants are fixtures, not product source.

## Behaviors to preserve

GAIJI_PUTC uses ADC after argument fetch, before any flag-clearing instruction:
incoming Carry1 increments the full16-bit character before `AND FF7F`.
Unlike single font READ/WRITE, the character high byte participates. GRCG
mode output masks IF, then POPF restores incoming IF before tiles and CG reads.
No CLD is executed. Normal rows store a shifted16-bit font word plus a third
byte at the updated DI and advance80 bytes; DF1 changes that row advance to76
and places the third byte two bytes before the initial word, including wrap.
There is no clipping. Final CG mode is0A and GRCG mode0; low four color bits
select the recorded tiles. Hardware RMW plane effects are outside this model.

PACK treats X and length as signed16-bit, arithmetic-shifts both by3 and uses
a hard-coded80-byte horizontal width. Negative X adds its negative group
count to the remaining length; it also adds four times that negative count
to SI. That moves the source backwards, rather than skipping source bytes
corresponding to clipped pixels. The native vectors preserve this behavior.
Y-clipped PACK subtracts ClipYT with16-bit wrap and uses an unsigned comparison
against inclusive ClipYH, then draws relative to ClipYT_Seg. NOCLIP ignores
ClipYT/ClipYH and uses the supplied Y directly with the same segment. Both
clear DF only after passing clipping/length rejection; rejected calls retain
incoming DF. They emit no GRCG ports in the frozen USE_GRCG=0 build.

RotTbl maps two nibbles to one two-bit pair in each plane byte. An independent
per-pixel projection proves all256 entries, and native basis vectors exercise
every byte in each of the four input slots for both PACK entries. Each group
reads four sequential source bytes before writing four plane bytes. The
second store wraps `DI+8000h` within the original ES; later plane segments
change BH by10h/28h and restore it by38h. Sixteen-bit source, offset and segment
behavior, source/video alias effects and the native epilogues remain intact.

SCROLLUP clamps unsigned line values at graph_VramLines. Out-of-range values
therefore use that full line count, rather than normalizing the stored split
to0. It emits command70 followed by four words: `u16(line*40)`, the scaled
remaining line count shifted4 with zoom high byte ORed in, zero, and the
scaled leading line count shifted4 with the same OR. The frozen comment's
claim of display equivalence to line0 is not hardware-verified here. Readiness
requires status bit04; unrelated status bits alone do not release the loop.
The public procedure retains IF/DF and never times out on its own. SHOW emits
the native BIOS request and returns with the declared response; the void ABI
does not promise a success result.

The separate MAP/ledger interval union now covers8,622 of10,944 root _TEXT
bytes, leaving2,322 without independent unit rows and zero overlap. This
includes read-only CODE data, not just function instructions. Replay
`scripts/review_th03_mainl_coverage.py --output .analysis/NEW_MAINL_COVERAGE.json`.
Prior snapshots remain historical evidence. Gaps can include prior native
context/alignment/CRT and are not an unknown semantic byte count.

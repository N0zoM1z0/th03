# Complete MAINL palette and wait candidate review

Eight frozen library includes cover 690 body bytes /313 instructions and two
trailing NOPs, totaling 692 new decoded bytes. The previously reviewed 26-byte
DOS-open helper executes as native context without duplicate progress credit.
All 718 scoped raw bytes and empty original ordered relocation sets agree with
both cached products. This adds five disjoint decoded module rows, without
maintained MAINL source, canonical stored-file offsets or exact acceptance.

```sh
python3 scripts/review_th03_mainl_palette.py --output .analysis/NEW_PALETTE_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_palette_review.py -v
```

Receipt: `.analysis/sol-mainl-palette-review-20261006.json`, SHA-256
`24faf33ba4e44f0f700f3b033f98a07bb95d3914c7c9fe5d79cfc41dade0c388`.
Its 501 guarded inputs retain the prior stack receipt's target/decoded/cached
lineage. Twenty-three consulted frozen providers bind both cached trees;
ASM/INC comparisons normalize only LF/CRLF. Seven prior MAIN-only Tupfile
substitutions are checked explicitly, with no MAINL palette substitution.
Both root OMF objects are valid TASM5/th03_mainl.asm, equal after dependency
timestamp normalization. MAP containment places every reviewed body inside
the generated root _TEXT carrier. Surrounding root bytes remain unaccepted.

| Include | Decoded offset | Body bytes /instructions | Far cleanup |
| --- | --- | ---: | ---: |
| BFNT_PALETTE_SET | 04C6 | 64 /28 | 6 |
| PALETTE_BLACK_IN | 0536 | 67 /29 | 2 |
| PALETTE_BLACK_OUT | 057A | 62 /28 | 2 |
| PALETTE_SHOW | 17D0 | 266 /133 | 0 |
| PALETTE_ENTRY_RGB | 1A68 | 66 /28 | 4 |
| VSYNC_WAIT | 2064 | 38 /17 | 0 |
| PALETTE_WHITE_IN | 208A | 63 /25 | 2 |
| PALETTE_WHITE_OUT | 20CA | 64 /25 | 2 |

NOPs at 0579 and 20C9 are trailing EVEN results. SHOW's interior NOP at 1839
belongs to its complete body. RotTbl beginning at 1AAA is DATA and excluded
from instruction decoding; the following heap include at 210A is also excluded.
The five new ledger extents are 04C6/64, 0536/130, 17D0/266, 1A68/66 and
2064/166. No contiguous 692-byte extent or neighboring ownership is invented.

## Native execution and model boundaries

Each image has 2498 terminal scenarios /2504 top-level invocations and 4916
native entries, plus eight separate budget observations. Across three images,
7512 calls return, executing 14748 terminal native entries. Another 24 budget
observations execute 246 entries. All included bodies and nested calls use
actual instructions, PUSH-CS far-call frames and native RETFs. Full 1MiB
outside the declared 64K stack is checked after every terminal call against
an independent physical-memory scalar algorithm. Scoped state, ports, DOS
requests and native counts agree across images; unrelated PI encoding and
DGROUP0849 differences keep whole-memory hashes per-image.

The image relocates to 2000, DGROUP to 2E3F and the stack to 4000. Fixtures
initialize the 48-byte palette at DS141E, Tone0578, Note05AA, Mask0848,
Count144E and Sharing0558; a separate 5000 segment contains the filename and
synthetic BFNT header. Only the original INT21/AH3D,3F,3E sites are modeled.
Reads inject explicit 0..48-byte payloads with independent AX/CF and optional
failure payloads. No real files or BFNT assets are opened. All port values are
synthetic device responses, and count changes at the native wait comparison
are an explicit clock fixture. No ISR, interrupt delivery or physical display
proof follows from those models.

The guard permits only palette/Tone stores, stack stores and a one-byte 0/FF
write to CS18B8, the LCD XOR instruction's immediate operand. Native branches,
call sites, returns, DOS sites and port widths/destinations are checked.
Unknown requests, ports, writes, escapes or frames stop execution and raise
outside FFI. No MEM_READ hook is installed. BP/SI/DI/DS/ES and far cleanup are
checked at every public return. SHOW clears DF, as do fades that call it;
loaders and WAIT preserve incoming DF. Other void-function registers and
flags are observations rather than invented public return contracts.

Eight controls reject truncation, cleanup/interior-return changes, operand or
neighbor branches, missing PUSH CS, unknown call/indirect/far edges, unknown
DOS/port sites, mutable opcode/target and producer changes, unowned whole-span
stores, invalid DOS AH/read destination/count and port width, native frame
damage, stale completion and segment aliases. Positive controls execute an
allowed CS operand store and actual return, and verify SHOW's DF requirement.
Runtime mutants retain untampered static metadata to exercise the guards;
synthetic instructions receive no source acceptance.

## RGB and LCD output

SHOW interprets Tone as signed: negative words use zero; nonnegative words
are locally capped at 200. The stored Tone is unchanged. Let M=15 and
F=200-Tone above 100, otherwise M=0 and F=Tone. Each RGB component emits
`(((component >> 4) XOR M) * F / 100) XOR M`, with integer floor division.
For each of 16 colors, output order is selector A8, red AC, green AA, blue AE.

The LCD branch preserves the native component selection: red is
`(red >> 4) AND M`, green is `green >> 4`, and blue is `blue AND M`.
Consequently ordinary brightness clears red and blue, while white transitions
use blue's low nibble. The same multiplication/XOR transformation follows.
Weighted intensity is `4*green + 2*red + blue + max(red,green,blue)`;
the gray level is `max(ceil(floor(weighted*3/20)/2)-2, 0)`, in 0..7.
These are observed code formulas, with no inferred correction for display
specifications. Matrices check all 256 component-byte values at Tone100/150,
varied mixed colors and signed/capping boundaries under both DF states.

LCD detection first outputs A0 to F6, then reads 871E. FF causes a fallback
read of AE8E. Inversion depends on bit0 of the first value or bit2 of the
fallback: a clear bit patches the XOR immediate to FF, otherwise zero.
The three gray bits emit 0/15 to blue AE, red AC and green AA. All detection
paths and the actual mutable instruction execute. A load/show/re-entry chain
switches white RGB, ordinary LCD and ordinary RGB; returning to RGB retains
the preceding LCD operand byte without using it.

## Loader status and retained data

BFNT checks only header color bit80 before reading 48 bytes into the palette.
An absent bit or read CF-set returns FFF3/CF1. A failed read can retain an
injected partial payload without rotation. On CF-clear it accepts any returned
AX count, rotates all sixteen B/R/G triples into R/G/B, including stale bytes,
and returns zero/CF0. CL4 is unused; this path performs no nibble scaling.
The header-offset FFFF fixture checks native word wrap of its color-field
address. Remaining BFNT parsing, stream position and assets stay open.

RGB calls the actual DOS-open helper, preserving its low-byte sharing mode
and AX-zero/CF-clear acceptance. Open failure returns FFFE/CF1. After a
successful open, it reads 48 bytes, then converts every palette byte with
`byte OR ((byte << 4) AND FF)`, including old bytes and failed-read payloads.
It closes the handle regardless of read status. Read failure returns
FFF3/CF1; read success returns AX0 with the close operation's CF. Thus AX0/CF1
is possible. Short reads and AX counts 0/1/47/48/FFFF are not validated.

## Fades and waiting

Each fade stores its initial Tone and waits once before showing. It shows
17 intermediate tones, waits the signed positive speed after each, and then
stores/shows the exact endpoint: black-in 0,6,..96,100; black-out
100,94,..4,0; white-in 200,194,..104,100; white-out 100,106,..196,200.
All have 18 SHOW entries. Signed nonpositive speed skips those intermediate
delays but retains the initial wait; positive speed performs 1+17*speed waits.
Speeds 0/1/2/8000/FFFF execute to return with the count fixture under both DF
states and RGB/LCD modes. A speed32767 case is a finite execution budget,
not a claim that a valid positive-speed fade cannot terminate.

WAIT tests only Mask's low byte. A nonzero byte waits for the Count word to
change, including FFFF-to-zero wrap. A high-byte-only mask0100 uses the port
path: A0 bit20 must first clear, then rise. Masks0/1/FF/100/101/FFFF and both
count boundaries execute. Stalled count, permanently-high and permanently-low
port fixtures retain distinct budget stops and their precise partial traces.
The positive-speed budget retains its first complete black SHOW, Tone0 and
native subsequent waits. Full memory outside the stack is checked in each
budget case. VSYNC installation/handler/cleanup, actual interrupt delivery,
physical palette/LCD behavior, complete game callers, root DATA/BSS/CRT,
cold localized production and canonical DIET packaging/full Oracles stay open.

# ZUN -4 sprite16 driver candidate review

The complete frozen `libs/sprite16/sprite16.asm` candidate was reviewed:
2120 lines, 55 complete procedures, startup, mixed code/data, command parser,
resident interrupt interface and hardware helpers. It remains reference
material. No maintained driver source, exact extent or function is added.
The cached driver differs from the decoded target in ten bytes. Its literal
zero gaps also need producer ownership before migration; reproducing them as
unexplained padding would violate this repository's source policy.

Replay the diagnostic without Wine or database observations:

```sh
python3 scripts/review_th03_zun_driver.py --output .analysis/NEW_DRIVER_REVIEW.json
python3 -m unittest discover -s tests -p test_zun_driver_review.py -v
```

The reviewed receipt is `.analysis/sol-zun-driver-review-20261006.json`.
It binds the frozen source, canonical stored ZUN, its DIET restoration receipt,
decoded image and both existing cold scaffold driver outputs. These are cached
compiler outputs, not fresh maintained-source builds. Source-labelled ranges
are provisional diagnostics; the script checks complete instruction coverage,
return boundaries, direct branch destinations and direct call entries.
Indirect calls are recorded without inventing a complete control-flow proof.

## Identity and storage

The frozen revision is `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
Source SHA-256 is
`3c41a162342930b121096efb2ca5ae283706dc8adeed3d001302a0b82add40b8`.
Although the source's IDA header names TH04, its original input MD5
`712edd4642948a68f70365dc4db06c62` equals the **complete TH03 decoded driver**
MD5. This is an upstream-input association verified against local target bytes,
not independent pristine attestation or inherited TH04 exactness.

The driver is 4224 bytes at decoded ZUN file offset `0x32A2`, ending before
the -5 payload at `0x4322`. Its SHA-256 is
`9122344545f977ee0be7e3326814518a8ec1d3b670bd848d7deef459054594cb`.
Its outer COM address is `0x33A2`; the wrapper copies it to `CS:0100`.
All addresses below refer to this latter driver namespace. None is a canonical
packed-file offset. Stored ZUN remains unchanged and locally attested only.

## Complete source and ABI review

The TU declares `.386`, `.model use16 tiny`, `_TEXT segment use16`, `org 100h`.
Code and initialized data occupy the same segment. The cached MAP's `_DATA`
is empty. The source depends on `libs/master.lib/macros.inc` and
`th01/hardware/egc.inc`; these are frozen candidates, not localized product
dependencies. Frozen Tupfile flags select `/dTHIEF`, producing the ZUNSP
branding instead of SPRITE16. This is a real conditional data choice.

| Driver address | Complete reviewed scope and behavior |
| --- | --- |
| `0100–010B` | Two-byte startup JMP; nine-byte `SPRITE16` signature with NUL and one-byte version 4 |
| `010C–0229` | Startup/exit, DOS resize, two buffer allocations, version/mask-test/sprite commands; five near procedures |
| `022A–033F` | Interrupt dispatcher, install and uninstall; one IRET procedure and two near procedures |
| `0340–0363` | Six DX-to-CS-word service setters |
| `0364–0515` | Clipped sprite copy, EGC blit and row copy; three near procedures |
| `0520–0630` | Mask/VRAM and command helpers; seven near procedures |
| `0640–06A4` | Formatted output, string output, DOS-character output, integer and case helpers; six near procedures |
| `06B0–091B` | Formatter, four character/classification helpers, 32-bit integer conversion and reversal; seven near procedures |
| `0920–0A88` | Tokenization, argument iteration, optional number and option dispatch; nine near procedures |
| `0A90–0BC5` | General number, decimal/hex/binary and ON/OFF parsers; five near procedures |
| `0BD0–0C75` | EGC setup/teardown and two string helpers; four near procedures |
| `0C80–117F` | Error/banner/usage strings, stack, resident state, command/service tables, graphics state and argument pointers |

These groups account for all 55 source procedures. The receipt lists every
individual range and direct edge. Their bodies total 2844 bytes. Outside them
are the two-byte startup instruction, ten signature/version bytes, 88 bytes
of source-labelled gaps (71 literal zeros, one NOP and a 16-byte digit table),
and 1280 trailing bytes. These sum to 4224. Gap classification describes the
candidate; it does not grant authored ownership to arbitrary zeros.

The interrupt entry doubles AH and indexes the nine-word service table at
`103E`: `0520,0540,0364,0340,0346,034C,0352,0358,035E`. It stores the selected
near address in the shared word at `0F45`, enables interrupts, calls it and
returns with IRET. There is no AH bounds check. Reentrancy/interrupt ordering
must be preserved and reviewed against the callers; no serialization was
invented. Ordinary internal calls use the 16-bit near stack. `0676` consumes
one word argument with `RET 2`. The formatter uses a 16-bit stack frame and
32-bit integer operands, including far strings; its mixed widths matter.

The installer compares ten signature/version bytes at resident offset `0102`,
allocates **1000 decimal paragraphs twice** (16000 bytes each), stores the two
segments at `0F3C/0F3E`, saves the old interrupt segment/offset at `0F38/0F3A`,
and installs `CS:022A` into the configured vector (default `42h`). Residency
uses DOS `INT 21h AX=3100h`; actual DOS allocation/free and TSR lifetime have
not been executed in this review. The 512-byte zero region `0D38–0F37` is a
real stack, with initial SP `0F38`. It must not be confused with unexplained
interprocedure gaps. The paragraph count at odd address `0F43` and dispatch
word at `0F45` retain their byte packing.

Sprite clipping uses the 200-line viewport and 80-byte row stride. Its complete
`0364` caller saves nine registers including segments and passes the resulting
range into the EGC helper. The row loop has no invented zero-height guard.
The helper macros expand to genuine `OUT` operations: EGC mode changes on
port `6Ah`, GRCG mode on `7Ch`, and word register writes through DX. These
hardware effects are statically reviewed only. No PC-98 graphics Oracle passes.

The formatter at `06B0` uses `ENTER 50h,0`, width/left/zero padding and
`c/u/d/x/X/b/s` conversion with escaped newline/carriage-return/tab handling.
The converter at `089F` preserves EAX/EBX/ECX/EDX, divides by ECX and indexes
the `08DC` digit table; lowercase selection uses bit `20h`. Output buffering
has no recovered capacity check. The DOS output wrapper at `0640` has a local
`D0h`-byte buffer. These unchecked contracts must not be silently repaired.

The token parser stores word pointers in the 128-byte array at `1072–10F1`,
with count at `1070` and iterator at `10F2`. It recognizes spaces, tabs,
commas, quotes, NUL/CR and semicolon termination without a recovered capacity
check. The option table at `101C` has eight string/handler pairs and a zero
sentinel. Numeric parsing supports one/two quoted characters, `$` hex,
`H/B` suffixes, signed decimal and ON/OFF fallback; 16-bit wrap is preserved.
The graphics state occupies `1050–106F`, including defaults `000F`, `0001`,
`28FC`, `FFFF`, `FFF0`. Remaining trailing bytes are actual strings and
candidate literal zeros; all bytes outside procedure bodies equal both cached
candidates, but data ownership and natural zero producers remain open.

## Raw and bounded runtime observations

Both pinned cached driver outputs have identical complete ranges/control-flow
diagnostics. 52 bodies are raw equal; the other three contain four differences:

| Driver IP | Procedure | Target bytes | Cached bytes | Same decoded instruction |
| --- | --- | --- | --- | --- |
| `0398` | `0364` | `83 F8 00` | `3D 00 00` | CMP AX,0 |
| `040C` | `0402` | `83 E0 FE` | `25 FE FF` | AND AX,FFFEh |
| `041D` | `0402` | `83 E0 0F` | `25 0F 00` | AND AX,000Fh |
| `08B1` | `089F` | `67 2E 8A 92 DC 08 00 00` | `2E 67 8A 92 DC 08 00 00` | MOV DL,CS:[EDX+08DCh] |

Full raw equality fails. No semantic comparison, prefix normalization, filler
or target-byte emission is used to promote acceptance. Wine is unavailable
in the current sandbox, so natural assembler remedies have not been tested.

Three constructed Unicorn CPU cases run against the target and each cached
candidate (nine observations). They preserve two source-visible hazards:

* Uninstall with vector `3000:022A` and saved old vector `4567:ABCD` writes
  **`4567:0000`**. It loads the saved offset into AX, then clears AX to set ES
  to the IVT segment and stores the cleared AX. Execution stops at the first
  DOS free request (`INT 21h AX=4900h`); no DOS free semantics are emulated.
* Optional numeric helper `0A24`, with one argument pointing to `123`, returns
  AX=0 and consumes the argument. With no arguments and previous SI pointing
  to that same string, it returns AX=123. Its CF branch skips conversion when
  an argument exists and attempts conversion from the previous SI otherwise.
  This constructed result does not mean every absent argument produces 123.

The receipt records Capstone/Unicorn distribution versions. Tests reject
truncated code, bad return distance, source overlaps, branches into operands
or gaps, and direct calls into procedure interiors. None of these CPU cases
establishes DOS, resident concurrency, PC-98 hardware or game runtime behavior.

## Acceptance and remaining work

The bounded payload is boundary-reviewed with no maintained source and blank
canonical file offset. New evidence distinguishes upstream metadata, local
decoded target analysis, cached compiler/raw failure and constructed runtime.
MAIN's existing exact counts remain unchanged. The 505-file intake and its
69 accepted/scoped MAIN CODE paths remain open for other artifacts and data.

Migration requires localized includes, natural ownership for all zero regions,
reviewed entry/interrupt/caller contracts, fresh cold assembler/link output,
complete raw equality, stored packaging lineage/ownership and the complete
Oracle set. Current Wine and Ghidra execution probes fail under the restricted
sandbox, and `.git` is read-only. These environment failures cannot turn this
cached diagnostic into a successful fresh replay or requested commit.

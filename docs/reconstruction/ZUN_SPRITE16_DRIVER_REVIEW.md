# ZUN -4 sprite16 driver candidate review

The complete frozen `libs/sprite16/sprite16.asm` candidate was reviewed:
2120 lines, 55 complete procedures, startup, mixed code/data, command parser,
resident interrupt interface and hardware helpers. The complete driver remains reference
material except for the bounded six-setter source migration described below.
No exact extent or accepted function is added.
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
or target-byte emission is used to promote acceptance. That 2026-10-06 cached review did not execute Wine. The later native
encoding probes below were executed under the working Factory toolchain.

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

## Historical acceptance and environment limits (before 2026-10-21)

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

## 2026-10-21 encoding probes: closed without a remedy

The parent ran bounded TASM 5 probes, not a full driver rebuild. Raw checksummed
OMF from V03 proves that SMART and explicit signed constants retain the same
AX-special encodings: 3D 00 00, 25 FE FF, 25 0F 00. Its ordinary CS/EDX
load still emits 2E 67. V04 proves that BYTE PTR on those immediate constants
does not change the encodings either. Do not claim these spellings fix the driver.

The V03 object is 288 bytes, SHA256
3909a790f52f02f18d51853e76b5b5f723cd7e722a559c4c4eab76c21c2a5354;
V04 is 242 bytes, SHA256
26fa2d7df51ae604e3b9b03a1ba4ce34c6e7f1d66ba158649d450b14077f8ab2.
They are retained in drive_c/ZDENC03/probe.obj and ZDENC04/probe.obj
under .analysis/toolchain/wineprefix.

Completion receipts under .analysis/zun-driver-encoding-output-20261021-vNN/:
- V03: 562e7e5971490f3d99ecc4b845acfe0212c59b7f42998086b05fe83c530ab2a4.
- V04: f0ec59e79363f4f072191a31097df84dcc89930f356438536b258ddca463e1d0.
- V01 stopped before Popen because its exact-boundary supervisor allowance was
  too short. Its premature native counter is corrected only in a separate
  disposition, never by editing that failed receipt.
- V02's mixed syntax/listing probe and V05's IDEAL/SEGCS probe crashed inside
  TASM before producing an object. Neither supplies usable encoding evidence.
  Both retained certain owned cleanup, valid raw registry transitions and lock
  release. All failed logs and receipts remain unchanged.

The original sprite16.doc identifies Promisence Soft, SPRITE16 v0.04
(1996-03-14), and the API, but does not identify the original compiler/assembler.
The IDA-derived assembly is not evidence of that producer. No alternative tool
is selected merely to manufacture matching bytes. The bounded spelling
investigation is closed pending concrete producer evidence; the ten-byte
whole-driver gap remains.

## First consumed maintained group: six resident setters

src/zun/driver_services.inl now owns the six complete AH=3..8 setters at
driver IP 0340–0363, corresponding to 36 bytes in the reviewed candidate.
They write DX to six WORD fields through CS and return near, preserving flags
and all general registers. The fields remain owned by the containing driver:
mono enable 1064, mono color 1066, overlap 1068, access plane 106E,
ROP 106A, and mask 106C. No resident allocation, device operation, data
storage or padding is synthesized by this include.

This is consumed by the explicit opt-in source stage:

    python3 scripts/stage_th03_zun_driver_services.py --output .analysis/FRESH_STAGE

The stage replaces exactly those six procedure definitions in the raw-pinned
reference scaffold, renames every corresponding service-table and state
reference, and emits six public semantic procedure symbols. The rest of the
driver, including its still-unowned zero gaps, remains explicitly retained
candidate material. Two hash-pinned retained macro includes are staged under
retained/; the maintained include has no reference-game dependencies.
The source-only check expands the include and verifies unchanged complete
instruction/data tokens apart from the deliberate symbol names/public entries.

The stager supplies a fixed assembly/link recipe with /dTHIEF, but does not
execute it. This checkpoint proves source consumption and unchanged source
semantics, not new machine output. Immediate next step: one parent-owned fresh
hybrid assembly/link, verify all six boundaries and complete candidate raw
equality, and preserve the known ten target differences. Later groups can then
migrate behind the same explicit driver layout. Default replay, wrapper/DIET
acceptance, hardware/TSR claims and the whole-game denominator remain unchanged.

## 2026-10-21 fresh six-setter hybrid proof

The parent executed the maintained stage's two native commands, TASM assembly
and TLINK tiny-COM linking, in fresh drive_c/ZDHYB01. Both exited zero with
certain owned cleanup and lock release. This is a single hybrid materialization,
not two-cold or complete-driver ownership. Its complete 4,224-byte COM equals
the retained candidate, SHA256
bab3769aa32184cdc71364138bc616b59faa9f2ae79f49837006f1cf87cc9c5c.
The known ten target differences remain at payload-relative offsets 0298, 0299,
030C, 030D, 030E, 031D, 031E, 031F, 07B1 and 07B2. No bytes were rewritten.

The six semantic procedure boundaries agree in checksummed OMF and both raw
MAP public tables. All six complete 6-byte bodies equal the target. Retained
output under .analysis/zun-driver-hybrid-output-20261021-v01/ includes:
- completion.json: d3183376b6f415823614512f92255d25d15d22758145b65c697a708f493d8e11
- validation.json: 211b9b918cfa8003ab6e83fa24db3bb67d73814d411c02f36c2e2e5c5b3625b8
- driver.obj in ZDHYB01: bb435c9e075efebffeae466fed5b2e6487043432232c54a50aa175713de67bf4
- driver.map in ZDHYB01: de21ee5eb46ef6d7b0bbf4801378a79314e57ebb4ea5c7ddb25d902abae7eb83

scripts/verify_th03_zun_driver_hybrid.py preserves complete candidate/target
identities, raw comparison, the ten differing offsets and exact OMF/MAP
boundaries. Its explicit setters scope revalidates these retained artifacts;
resident-services scope additionally requires all eight new boundaries and
complete bodies below. It is a diagnostic verifier, not an acceptance gate
or a full driver relocation audit. The SVG annotates only the proven six
setters / 36 bytes, with no change to bars, accepted counts or denominator.

## Consumed resident lifecycle group: source-only continuation

src/zun/driver_resident.inl owns the eight contiguous complete procedures
at 010C–033F, 564 instruction bytes: entry, two-buffer allocation, interrupt
number option, MASKTEST adapter, SPRITE adapter, interrupt dispatch, resident
install and uninstall. The existing opt-in stager now requires this include
as well as driver_services.inl: 14 maintained procedures / 600 instruction
bytes in total. The first 12 payload bytes, all remaining procedures, fields,
messages, tables, zero gaps and retained macro includes remain outside this
ownership claim. This is not a whole-driver translation unit.

All eight procedures have semantic public names and documented call/interrupt
contracts. Symbolic references in the retained scaffold are renamed consistently;
expanding both maintained includes and reversing those names preserves the
complete active instruction/data token stream. No storage or padding is added.
The interrupt dispatcher remains far/IRET, keeps its unchecked AH service-table
index and shared target slot, and preserves its original STI. The uninstaller's
XOR AX discards the previously loaded saved vector offset before storing it;
that observed behavior is deliberately preserved, not silently repaired.

The new group has source-level composition and staging checks only in this
checkpoint. Its native OMF/MAP and complete raw-byte proof are still pending.
Immediate next step is the same bounded two-command parent-owned hybrid build,
now verifying all 14 public procedure boundaries and all 600 owned bytes.
No accepted ledger/default-wrapper/DIET change or real DOS/device/TSR behavior
claim is implied by either the six-setter proof or this larger source group.

## 2026-10-21 resident/services native proof and command-source continuation

The second parent-owned hybrid build, drive_c/ZDHYB02, successfully assembled
and linked the 14-procedure resident/services source. Complete raw COM equality
with the same 4,224-byte candidate is preserved, as are exactly the ten target
differences. All 14 procedure boundaries agree in OMF and both MAP public tables;
all 600 complete owned body bytes equal the target. Both native exits were zero,
with certain owned cleanup, no errors and released shared lock. This is one
materialization of the expanded source, not a two-cold acceptance claim.

Retained completion .analysis/zun-driver-hybrid-output-20261021-v02/completion.json:
f2a1e7413270b3254a61c4a28e61a23625fe020fa0e876f8670b23a25b184831.
Raw driver.obj SHA256 b422bb0e22193c8f48a494fc26724895904b28cf8abdb60c4b4b3b4faee7867a;
driver.map 7346d1437a1a5c0afdef6592e16a6d4bbc0ef6d2a85b76448fad4e4b27386ba2;
driver.com remains bab3769aa32184cdc71364138bc616b59faa9f2ae79f49837006f1cf87cc9c5c.
The SVG now annotates this actual 14-procedure / 600-byte hybrid proof, not the
additional source-only work below. Accepted counts and bars remain unchanged.

The next source group is substantial but bounded: 16 complete procedures /
725 bytes, consumed through three logical maintained includes:
- driver_command.inl: nine tokenization, argument and option procedures,
  0920–0A88, 361 bytes.
- driver_numbers.inl: five number/switch parsers, 0A90–0BC5, 310 bytes.
- driver_strings.inl: length and folded comparison, 0C40–0C75, 54 bytes.

The stage now consumes 30 procedures / 1,325 instruction bytes in total. It
preserves the complete expanded instruction/data token stream and leaves every
inter-group gap in the retained scaffold. The new command group's native proof
is pending. The verifier's explicit command-resident-services scope requires
all 30 OMF/MAP boundaries and complete owned body equality after the next build.

Comments preserve observed contracts rather than improving them: optional-number
A24 consumes a present argument but returns zero, while absence parses the
caller's previous SI; hexadecimal parsing accepts some punctuation; numeric
overflow wraps at 16 bits. Semicolon ends parsing only at a token's beginning,
text adjacent to a closing quote is skipped, and dispatch reads/advances a
pointer before checking the remaining count. No capacity checks or safer
malformed-input semantics are silently added. Numeric suffix parsing requires
writable strings, relevant LODSB paths require DF=0, and string comparison returns
CMP flags rather than an integer. These are source observations, not new runtime
coverage or DOS/device safety claims.

Remaining procedure ownership is two logical groups: 12 graphics/EGC procedures
(814 bytes) and 13 text-format/output procedures (705 bytes). Separate remaining
layout ownership includes the 2-byte entry jump, 10-byte signature/version,
88 bytes of labelled inter-procedure gaps and 1,280 bytes of trailing data.
The four instruction-encoding choices/ten target bytes, full data/layout ownership,
whole decoded wrapper, outer DIET and real DOS/TSR/device behavior remain distinct
open obligations. No default graph or accepted ledger is changed here.

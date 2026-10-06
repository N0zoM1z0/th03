# ZUN -5 resident root and direct helper review

The complete `th03/res_yume.cpp` root, its included `th02/res_init.cpp` and
`th02/formats/cfg_init.c`, relevant resident/config declarations, and direct
master-library helper bodies were reviewed. Two complete root functions have
decoded boundary/ABI review: `cfg_init` (97 bytes) and `main` (225 bytes).
Eleven direct helper bodies add 423 diagnostic bytes. None becomes maintained
source or exact. Startup and the remaining Borland runtime/library code are
still open, so this is **not a complete -5 product review**.

```sh
python3 scripts/review_th03_zun_resident.py --output .analysis/NEW_RESIDENT_REVIEW.json
python3 -m unittest discover -s tests -p test_zun_resident_review.py -v
```

The reviewed receipt is `.analysis/sol-zun-resident-review-20261006.json`.
All 5618 decoded -5 bytes equal both pinned cached scaffold outputs, including
their unreviewed startup/runtime areas. This whole-payload raw diagnostic does
not grant ownership over those areas or constitute a fresh maintained build.
The canonical stored ZUN remains unchanged, `candidate-local-attested`, with
unknown independent pristine attestation.

## Inputs and compiler coordinates

The frozen revision is `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
Root source SHA-256:
`c66c09511fe49bfa7a02cbb6640558bc4939da91636f3b39505917bcddc5e8bc`.
Decoded -5 SHA-256:
`cfe11aff09ae2bb92e6775c3d0aead8ae610e6bc2ad7e0551ec9f42e838734b8`.
The payload occupies decoded outer file `4322–5913`, runtime origin `4422`,
and is copied to inner runtime `CS:0100`. All following offsets use this
inner namespace; no fabricated canonical packed-file offset is entered.

The frozen Tupfile selects a tiny-model link of `th03/res_yume.cpp` and
`bin/masters.lib`. Cached response files identify `c0t.obj`, that root object,
masters, emulation/math/C runtime libraries and TLINK `-c -s -t`.
Cached MAP gives root CODE `0367` size `0142`, initialized DATA `131E` size
`0133`, and zero root BSS. Both consulted root OMF objects pass framing and
checksums, record translator `TC86 Borland C++ 4.02`, and have equal hashes
after dependency timestamp normalization. The complete build receipt and
selected inputs are hash-checked; current tool execution does not succeed.

The script binds 26 consulted frozen source/provider files to both private
source trees. C/C++ headers and `func.inc` match exact original bytes; the ten
consulted assembly providers differ only by explicit CRLF line conversion.
No instruction, target-byte, string encoding or arbitrary whitespace mask is
used. Additional OMF dependencies such as PC-98 interface headers and Borland
`dos.h/_defs.h` remain visible in the receipt and need separate declaration/
dependency review. Consulted-file association does not accept every header.

## Root functions and resident data

| Inner address | Complete size | Scope and ABI |
| --- | ---: | --- |
| `0367` | 97 | `cfg_init`, 16-bit near C++ function, one word segment argument, caller cleanup |
| `03C8` | 225 | `main`, near cdecl, word argc and near argv pointer, returns AX |

Both use ENTER frames (`6`/`8` bytes), preserve SI/DI/BP and near RET. The
root directly calls near Pascal master helpers, whose RET cleanup sizes are
recorded separately. `cfg_init` calls the Borland near structure-copy helper
with two far pointer arguments and CX=5. It restores DS through that helper.
The retained caller argument remains on the cdecl stack when either root
function returns. Segment-register ownership cannot be inferred from hosted
C++ defaults or replaced with flat pointers.

The frozen resident declaration uses `RES_ID="YUMEConfig"`, an 11-byte ID
field, one-byte flags/booleans/player encodings, a four-byte signed long,
two eight-byte scores and 198 unused tail bytes. Candidate field offsets
from those declarations are below. Only the ID length, 256-byte size, paragraph
count and zero-loop boundaries are directly exercised by this root; the other
field offsets remain declaration-based layout inference pending caller and
ABI/layout Oracles.

| Candidate offset | Declaration |
| --- | --- |
| `00–0A` | ID array including nominal NUL slot |
| `0B` | rank |
| `0C–0D` | two paletted optional characters |
| `0E–0F` | two CPU flags |
| `10–13` | random long |
| `14–17` | unused byte, BGM mode, key mode, winner ID |
| `18–27` | two scores |
| `28` | game mode |
| `29–31` | nine story opponents |
| `32–39` | unused byte, stage, lives, menu flag, credits, animation, skill, demo |
| `3A–FF` | 198 unused bytes |

`ResData` asks for ID length 10 and `(256+15)>>4 = 16` paragraphs. Its create
helper copies ten ID bytes. Main clears offsets **11 through 255**, leaving
offset 10 untouched. With a constructed allocation filled with `A5h`, the
result is ten ID bytes, `A5h`, then 245 zero bytes. Do not insert a terminating
NUL or use a blanket memset to make the structure prettier. Search compares
ten ID bytes and exactly sixteen paragraphs; it does not inspect that NUL slot.

Main obtains the resident segment before printing its logo and clearing the
graph buffer. It interprets `/R`/`-R` and `/D`/`-D` only when `argc==2`.
Extra arguments bypass option handling: `/R ignored` installs when absent.
Removal returns 1 if absent, otherwise requests a free, prints its message
and returns 0 regardless of the modeled free error. Already resident,
invalid single argument and first allocation failure return 1. Installation
sets debug only for the single debug option, clears resident bytes, calls
`cfg_init` and returns 0 regardless of configuration errors.

## Configuration file contract

The candidate five-byte `cfg_options_t` is BGM/key/rank plus a two-byte unused
field. Its initialized bytes are `01 00 01 00 00`; the two-byte resident
segment and one-byte debug flag follow in `cfg_t`, totaling eight bytes.
These widths and five-byte structure copy/write are observed in decoded code.
`debug` is at DS:`131E`, options at `131F`, filename `yume.cfg` at `1324` and
resident ID string at `132D`. Source Japanese strings and ASCII data stay in
the root's initialized DATA contribution, not invented runtime resources.

`cfg_init` opens read/write using `AX=3D02h`. It takes the seek path only for
a **signed handle greater than zero**. Existing positive handle: seek to 5,
write the segment word and debug byte, close; the first five bytes and any
tail beyond offset 7 remain intact. A valid handle 0 takes the create path,
requesting archive attribute `20h`, writing defaults, segment and debug, and
thereby replacing the modeled previous contents. The originally opened handle
is not explicitly closed on this path; CRT exit/kernel behavior is unreviewed.

No seek, write or close result is checked. Modeled seek failure leaves the
position at zero and the following writes replace bytes 0–2. Modeled create
failure still leads to writes/close with a negative handle. Modeled write
failure can leave an empty file. All these return normally from `cfg_init`
and main returns 0. Do not turn this into a corrected transactional writer or
add error propagation during reconstruction. Removal leaves the configuration
segment word unchanged; later real callers/file handling must be reviewed.

## Complete direct helper boundaries

| Inner address | Body bytes | Source/helper and cleanup |
| --- | ---: | --- |
| `04AA` | 35 | `GRAPH_CLEAR`, near RET |
| `04CE` | 72 | `RESDATA_EXIST`, RET 6 |
| `0516` | 117 | `RESDATA_CREATE`, RET 6 |
| `058C` | 16 | `DOS_FREE` / `MEM_FREE` alias, RET 2 |
| `059C` | 21 | `DOS_AXDX`, RET 4 |
| `05B2` | 20 | `DOS_CREATE`, RET 4 |
| `05C6` | 39 | `DOS_PUTS2`, RET 2 |
| `05EE` | 21 | `DOS_CLOSE` / `FONTFILE_CLOSE` alias, RET 2 |
| `0604` | 26 | `DOS_WRITE`, RET 8 |
| `061E` | 28 | `DOS_SEEK`, RET 8 |
| `07CA` | 28 | Borland `N_SCOPY@`, RET 8, compiler helper only |

These 423 bytes plus root 322 give 745 diagnostic body bytes. Natural master
`func/endfunc` EVEN directives explain library alignment NOPs; MAP coordinates
are not independent authored ownership. Compiler startup, heap, stdio,
argv and exit code outside these bodies remain unreviewed.

`GRAPH_CLEAR` writes `80h` to port `7Ch`, four zeros to `7Eh`, zeroes 16000
words through ES=`A800h`, and turns mode off through `7Ch`. It temporarily
uses CLI around the first mode write with PUSHF/POPF; source notes about
enabling interrupts do not override those instructions. DI is preserved,
other working registers and ES are clobbered. Modeled flat memory and OUT
records do not establish GRCG plane behavior or a PC-98 VRAM Oracle.

`RESDATA_EXIST` obtains the MCB list with DOS AH=`52h`, executes CLD, traverses
MCBs, ignores owner zero and checks exact paragraph count and ID prefix. It
returns a segment word or zero, with near pointer arguments under the tiny
model. `RESDATA_CREATE` repeats the search, saves allocation strategy, switches
to strategy 1 and allocates. If the returned segment exceeds CS, it frees that
block, switches to strategy 2 and allocates again. It marks the preceding MCB
owner `FFFFh`, copies the ID and restores strategy before returning.

The **second allocation has no CF check**. In the explicit DOS model, first
segment `3000h` exceeds CS=`2000h`; second allocation fails with AX=8 and CF=1.
The code treats 8 as a segment, writes owner `FFFFh` at linear `0071`, copies
the ID at linear `0080–0089`, and main clears `008B–017F`. It then writes
segment `0008h` into the modeled config and returns 0. This is a constructed
memory-manager result, not an observed game/kernel failure. Preserve the
instructions and record the missing guard rather than silently adding one.

The DOS helpers preserve their near Pascal cleanup and explicit far buffer
contract for writes. Error conversion differs among helpers; main ignores
free's status and configuration ignores returned I/O values. `DOS_PUTS2`
expands LF to CR/LF through AH=2. `N_SCOPY@` loads far DS:SI/ES:DI pointers,
clears DF, copies words then the odd byte, and restores DS/SI/DI/BP; it remains
compiler-owned even though this root executes it.

## Runtime observations and acceptance

Twenty constructed main calls run against target and each cached candidate
(60 observations), covering default/debug/removal/existing/invalid/extra
arguments, first allocation failure, fallback success/failure, MCB chaining,
wrong ID/size, positive/zero file handles and create/seek/write/close/free
failures. Register/stack returns, allocation strategy restoration, file bytes,
allocation memory, output hashes and port vector agree in all three images.
Seven synthetic tests reject wrong size/returns, data/unreviewed-runtime branch
targets, interior calls, indirect edges and unmodeled interrupts. Callback
errors are raised after emulation rather than escaping ctypes.

Each call **starts directly at main**, with constructed argv, MCB list,
allocation and file returns. It bypasses CRT startup/argument parsing/exit,
uses no real filesystem/DOS/free/MCB manager, and implements no GRCG plane
semantics. No file from the private game is modified. Successful comparisons
are bounded CPU/interface-model support, not actual DOS or game-runtime proof.

Both root units are boundary-reviewed with blank canonical file offsets and
no source. Source localization/encoding, natural compilation, ABI/layout and
relocation/packaging ownership, cold aggregate builds and complete Oracles are
still required before absorption. Wine/Ghidra execution probes currently fail
and `.git` is read-only; the full ReC98 TH03 review/migration goal remains open.

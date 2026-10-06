# OP and MAINL decoded source-coordinate review

This is a diagnostic review of the frozen direct-link queue and three bounded
MAINL functions. It adds no maintained source or exact owner. The selected stored
Ghidra databases were re-attested before this review; their packed functions were
not used as game-code observations. Canonical targets remain unchanged.

## Lineage and replay

The decoded inputs are the complete, hash-pinned outputs of
`sol-diet-restoration-20261006-b`. Their restoration receipts bind the stored
targets to the derived images. The compiler inputs are OP/MAINL products and
detailed MAPs from both rounds of `sol-main-randring-probe-20261006`. This is the
full scaffold with maintained MAIN overlays, not an unmodified reference or
authored OP/MAINL build. Source membership and source hashes come from the frozen
ReC98 revision in `config/th03_decoded_code_review.toml`.

```sh
python3 scripts/review_th03_decoded_code.py --output .analysis/decoded-code-review.json
```

The script pins the cold and restoration receipts, verifies canonical target and
decoded identities, requires every direct-link source in the detailed CODE MAP,
rejects overlapping/out-of-image contributions and straddling relocation words,
compares unmodified bytes and the original ordered relocation records, and checks
both cold rounds. The three manually reviewed functions additionally require
the candidate public entry, carrier containment, complete decoding and reviewed
return. Seven synthetic failure controls cover malformed/overlapping MAP rows,
bounds, relocation ordering, unmasked relocated words, and incomplete/wrong-return
function decoding. Repeated diagnostic output is identical.

A matching slice at a compiler coordinate does not establish target ownership.
Zero-sized CODE declarations get no byte or source credit. Neither raw nor
relocation equality here proves DATA/BSS, linkage, packing, runtime behavior or
the complete Oracle set. Generated roots and shared code remain separately scoped.

## Direct-link diagnostics

All counts below describe candidate coordinates. The detailed ignored evidence is
`.analysis/sol-decoded-code-20261006.json`, which retains every CODE contribution,
including compiler/library modules, and each original relocation sequence.

| Product | Direct files | Nonempty files with matching slices and ordered relocations | Nonempty CODE contributions | Different program bytes | Different CODE slice bytes |
|---|---:|---:|---:|---:|---:|
| OP | 27 | 13 | 100 | 4867 | 4865 |
| MAINL | 33 | 28 | 108 | 340 | 339 |

OP has a 4096-byte decoded target header and a 3584-byte candidate header. Both
program images are 59770 bytes. MAINL has 4096-byte headers and 63276-byte
program images on both sides. Comparing program images here only locates
differences: full-file equality still fails for both products.

The table lists every direct file. `same` means all nonempty candidate CODE
contributions have matching raw slices and ordered relocation records. `empty`
means no nonempty CODE contribution; neither result grants acceptance.

| Product | Direct file | Nonempty candidate CODE bytes | Differing slice bytes | Ordered relocations | Diagnostic |
|---|---|---:|---:|---|---|
| OP | `th01/vplanset.cpp` | 41 | 0 | same | same |
| OP | `th02/exit_dos.cpp` | 25 | 0 | same | same |
| OP | `th02/frmdely1.cpp` | 21 | 0 | same | same |
| OP | `th02/frmdely2.cpp` | 21 | 21 | same | differs |
| OP | `th02/snd_load.cpp` | 112 | 0 | same | same |
| OP | `th02/snd_mode.c` | 30 | 0 | same | same |
| OP | `th02/snd_pmdr.c` | 58 | 0 | same | same |
| OP | `th03/cdg_load.cpp` | 593 | 562 | differs | differs |
| OP | `th03/cdg_p_na.asm` | 114 | 112 | same | differs |
| OP | `th03/cdg_put.asm` | 382 | 0 | same | same |
| OP | `th03/exit.cpp` | 67 | 0 | same | same |
| OP | `th03/grppsafx.cpp` | 613 | 603 | differs | differs |
| OP | `th03/hfliplut.asm` | 30 | 29 | same | differs |
| OP | `th03/initop.cpp` | 105 | 94 | differs | differs |
| OP | `th03/inp_m_w.cpp` | 367 | 355 | differs | differs |
| OP | `th03/input_s.cpp` | 417 | 0 | same | same |
| OP | `th03/op_01.cpp` | 3094 | 14 | same | differs |
| OP | `th03/op_02.cpp` | 165 | 0 | same | same |
| OP | `th03/op_main.cpp` | 902 | 19 | same | differs |
| OP | `th03/op_music.cpp` | 2244 | 16 | same | differs |
| OP | `th03/op_sel.cpp` | 3013 | 28 | differs | differs |
| OP | `th03/pi_load.cpp` | 70 | 67 | differs | differs |
| OP | `th03/pi_put.cpp` | 173 | 168 | differs | differs |
| OP | `th03/polar.cpp` | 26 | 0 | same | same |
| OP | `th03/scoredat.cpp` | 229 | 0 | same | same |
| OP | `th03/snd_kaja.cpp` | 30 | 30 | same | differs |
| OP | `th03_op.asm` | 11730 | 0 | same | same |
| MAINL | `th01/vplanset.cpp` | 41 | 0 | same | same |
| MAINL | `th02/frmdely1.cpp` | 21 | 0 | same | same |
| MAINL | `th02/snd_dlyv.c` | 28 | 0 | same | same |
| MAINL | `th02/snd_load.cpp` | 112 | 0 | same | same |
| MAINL | `th02/snd_mode.c` | 30 | 0 | same | same |
| MAINL | `th02/snd_pmdr.c` | 58 | 0 | same | same |
| MAINL | `th02/snd_se_r.cpp` | 12 | 0 | same | same |
| MAINL | `th03/cdg_load.cpp` | 593 | 0 | same | same |
| MAINL | `th03/cdg_p_na.asm` | 114 | 0 | same | same |
| MAINL | `th03/cdg_put.asm` | 382 | 0 | same | same |
| MAINL | `th03/cfg_lres.cpp` | 49 | 0 | same | same |
| MAINL | `th03/cutscene.cpp` | 3195 | 3 | same | differs |
| MAINL | `th03/exit.cpp` | 67 | 0 | same | same |
| MAINL | `th03/exitmain.cpp` | 40 | 0 | same | same |
| MAINL | `th03/grppsafx.cpp` | 613 | 0 | same | same |
| MAINL | `th03/hfliplut.asm` | 30 | 0 | same | same |
| MAINL | `th03/initmain.cpp` | 62 | 0 | same | same |
| MAINL | `th03/inp_m_w.cpp` | 367 | 0 | same | same |
| MAINL | `th03/inp_wait.cpp` | 126 | 0 | same | same |
| MAINL | `th03/input_s.cpp` | 417 | 0 | same | same |
| MAINL | `th03/mainl_sc.cpp` | 338 | 0 | same | same |
| MAINL | `th03/pi_load.cpp` | 70 | 0 | same | same |
| MAINL | `th03/pi_put.cpp` | 173 | 168 | differs | differs |
| MAINL | `th03/pi_put_i.cpp` | 135 | 132 | differs | differs |
| MAINL | `th03/pi_put_q.cpp` | 177 | 0 | same | same |
| MAINL | `th03/regist.cpp` | 2720 | 6 | same | differs |
| MAINL | `th03/scoredat.cpp` | 229 | 0 | same | same |
| MAINL | `th03/snd_dlym.cpp` | 49 | 0 | same | same |
| MAINL | `th03/snd_kaja.cpp` | 30 | 0 | same | same |
| MAINL | `th03/snd_se.cpp` | 120 | 0 | same | same |
| MAINL | `th03/staff.cpp` | 76 | 0 | same | same |
| MAINL | `th03/vector.cpp` | 160 | 0 | same | same |
| MAINL | `th03_mainl.asm` | 17119 | 30 | differs | differs |

## Three complete MAINL functions

The manual decoded-body review covers the following complete functions, with
no producer padding or data bytes credited. Their CODE bytes and region-local
ordered relocation records match both frozen compiler rounds.

| Function | Decoded CS:IP | Body bytes | MZ relocation words | Return |
|---|---|---:|---:|---|
| cfg_load_resident_ptr | 095F:0003 | 49 | 3 | near RET |
| win_load | 095F:0034 | 282 | 11 | near RET |
| win_text_put | 095F:014E | 56 | 3 | near RET |

The CFG carrier is `th03/cfg_lres.cpp`, including
`th03/formats/cfg_lres.cpp`; both screen functions belong to
`th03/mainl_sc.cpp`, including `th03/mainl/screens.cpp`. Their complete 49- and
338-byte contributions partition exactly into these functions. Candidate source
hashes, target/candidate body hashes and complete disassembly are in the receipt.
Addresses are in the decoded namespace. Unit rows deliberately have no canonical
stored-file offset or maintained source path.

`cfg_load_resident_ptr` uses ENTER 8 and saves SI. It opens the DGROUP filename at
035A, reads eight bytes into SS:BP-8, closes the file, extracts the segment word
at BP-3 (configuration offset 5), writes it to resident segment 21EC, writes zero
to resident offset 21EA, returns the segment in AX, restores SI/BP and uses RET.
The frozen GAME=3 cfg_options_t has five packed bytes; cfg_t then adds the
two-byte segment pointer and one debug byte. The library calls are far Pascal;
the function does not test open/read errors or initialize a failed-read buffer.
The GAME=5 DOS branch in cfg_impl.hpp is not part of this body.

`win_load` uses ENTER 2, keeping the scalar packed character byte at BP-1 and
message byte at BP-2. It loads palette/logo resources, selects the winner using
resident byte offset 17, and tests story-stage byte offset 33 only for winner 0.
Stages 6 and 7 choose messages 9 and 10; other paths use the losing character
ID. Character ID is the zero-extended packed byte divided by two, and palette
ID is bit 0. It loads CDG slot 6, opens the selected far message filename, seeks
to message_id * 180 with a 32-bit position, reads three 60-byte lines at DGROUP
133C/1379/13B6, terminates them at 1378/13B5/13F2, closes and returns near.
The declared 183-byte win_text, two character bytes at 13F3/13F4 and bool at
13F5 explain the candidate 186-byte BSS contribution; this is layout corroboration,
not file-backed BSS equality. No filename/resource contents were imported.

`win_text_put` saves BP and calls graph_putsa_fx three times with 16-bit
coordinates x=80, y=272/288/304, attribute 002F and the three far DS:offset
line pointers. The 386 operand-size PUSH pairs real word arguments; preserve
their order and the far Pascal cleanup when maintaining the source. RET ends
the complete 56-byte function. No gameplay or device-runtime proof is claimed.

## Concrete failures and remaining scope

The target byte immediately after MAINL input_s at decoded program offset CD09
is NOP, while the candidate starts pi_put there with PUSH BP. Thus the candidate
pi_put and pi_put_i slices differ substantially at those coordinates. This is a
boundary/alignment observation; it does not prove either complete function wrong
or authorize an inserted padding byte. Establish target boundaries and the natural
producer before changing source. MAINL generated STAFF_TEXT has identical 348
bytes but a different original relocation sequence, independently preventing
acceptance of that region. OP has additional shared-code shifts and source-local
differences; the receipt preserves the first differing byte for each candidate
contribution without searching for an equality-maximizing alignment.

None of these comparisons resolves stored packing/stub ownership, the full product
graph, external data, library provenance, unlinked files, assets, headers or
conditional branches. The 505-file conservative intake and 69 scoped CODE
review paths keep their previous scoped counts. Continue actual source/target
review rather than promoting these diagnostic matches to accepted owners.

Subsequent complete STAFF CODE review adds three decoded boundary-reviewed
functions (424 bytes) in `docs/reconstruction/MAINL_STAFF_REVIEW.md`. It retains
the generated region's relocation-order failure and adds explicit CPU/interface
models; no maintained source or exact totals change.

The subsequent whole cutscene analysis in `MAINL_CUTSCENE_REVIEW.md` establishes
target PI palette/put entries from actual callers at `0C7E:052A/054F` (cached
entries `0529/054E`), with equal complete 37/136-byte corresponding bodies.
The entry producer remains open; original root call operands still differ by
three bytes. No offset search, padding insertion or exact promotion is applied.

The complete registration/score-data review in `MAINL_REGIST_REVIEW.md` adds
two decoded module boundary rows, fourteen/three complete bodies (2720/229
bytes) and 456 CPU/interface calls. Registration retains six raw call-operand
failures; score-data cached raw equality adds no exact or maintained-source
credit. Generated DATA/BSS and complete devices/dependencies/cold packaging
remain open, alongside the broader intake.

`MAINL_SNOW_REVIEW.md` adds one bounded generated-root snow/frame cluster of
seven bodies (464 bytes), retaining three clear-encoding raw differences and
six reversed original relocation sites. Its actual blitter/LCG/vector operations
and 918 CPU/clock/music cases remain scoped diagnostics; private bitmap/table
checks add no source, exact or whole-generated-root acceptance.

`MAINL_TRANSITIONS_REVIEW.md` completes candidate review of the remaining ten
MAINL_03_TEXT bodies (2875 bytes / 949 instructions), covering the whole 3339
CODE bytes with the separate snow cluster. It retains seventeen additional
native encoding failures and original ordered relocation failures. Its 393
CPU/interface calls execute native E-plane and transition/verdict/root code
under explicit snow/clock/graphics/font/library models, preserving observed
arithmetic and wait/fade/free hazards. These ten decoded boundary entries
provide no source/exact credit or generated DATA/BSS/resource, physical-device,
cold-build or canonical packaging acceptance. Other root segments stay open.

`MAINL_ROOT_REVIEW.md` adds the complete handwritten/generated root
CUTSCENE_TEXT contribution at 0186..0B3D: nine procedures (2470 bytes), an
18-byte table and 1368 CPU/interface invocations. Ten raw PI operands and
original relocation order remain failures. This is disjoint from the compiled
cutscene TU starting at0B3E. Explicit foreign models grant no maintained source,
exact, physical-device/CRT or complete product ownership acceptance; `_TEXT`
libraries and root DATA/BSS/resources remain open.

`MAINL_LIFECYCLE_REVIEW.md` adds three complete decoded lifecycle functions
(169 bytes) with a 41-byte plane-helper diagnostic. Their complete raw bodies
and original relocation lists agree in both caches; source association records
old forwarders to maintained MAIN implementations rather than attributing
those outputs to unchanged frozen carriers. Actual CPU/interface replay and
MAIN caller-prefix stops grant no inherited exactness, maintained MAINL source,
cold build, complete device/CRT or canonical packaging acceptance.

`MAINL_CDG_PUT_REVIEW.md` adds complete native CDG drawing candidate review
over two TUs (493 body bytes plus three observed EVEN bytes). Both cached raw
contributions and original ordered relocations agree. Actual self-modifying
blitters run261 invocations against full flat-store specifications and explicit
GRCG/lookup/source fixtures, without physical RMW/page or asset proof. Three
decoded function entries grant no source, cold ownership, canonical packaging
or exact acceptance.

`MAINL_CDG_LOAD_REVIEW.md` adds five complete decoded functions in one593-byte
loading/freeing TU (219instructions). Both complete cached contributions and
24 original ordered relocations agree. Actual native callers/internal bodies
and936 top-level interface-model invocations check whole DGROUP and ordered
file/heap requests, preserving word promotion, ignored statuses, stale/short
headers, count0 pointers and unchecked slot/noalpha aliases. No payload assets,
real heap/DOS, maintained source, cold build or canonical packaging/exact
acceptance follows from these decoded candidate observations.

`MAINL_PI_REVIEW.md` adds five complete decoded PI wrapper functions across
four TUs (555bytes/197instructions), with actual76-byte GRAPH_PI_FREE and
36-byte CRT memcpy diagnostics. Shifted complete bodies agree, but fixedraw
and relocation failures remain for firstthree; loading/quarter whole raw/order
agree. Cached loading redirects to maintained MAINsource without inherited
MAINL acceptance. Its708 top-level CPU calls preserve word/far-pointer,
metadata/counter/top/quarter/slot, native-copy/DF and retained-image contracts
under four explicit interfaces. All340 cached raw program-byte failures have
a replayable complete classification; this does not establish ownership or
review of remaining equal bytes. No maintained source, PIasset/device/heap/DOS,
cold build, canonical packing or exact credit is added.

`MAINL_INPUT_REVIEW.md` adds twelve complete decoded functions (910 bytes /
313 instructions) and an actual21-byte frame helper. Whole cached TUs and six
original ordered relocations agree; producer lineage explicitly records
three maintained MAIN forwarders. The762 top-level CPU calls/clock budgets
preserve actual song-measure AX clobber, two-pass key union, mode/joystick,
zero-frame and release-before-limit behavior. The frozen codestring's omitted
neighbor is an open producer hypothesis, without NOP ownership. No maintained
MAINL source, physical input/music/frame, cold packing or exact credit follows.

Complete MAINL sound review covers eight TUs: nine bodies535bytes /163instructions
plus four trailing producer bytes; all539 cached raw bytes and empty relocation
sets agree. Mode/PMD/reset remain frozen TH02 producers; only SE/KAJA and
contextual delay helper forward maintained MAIN code. The6975 native calls
(6927returns/48budgets) check fullDGROUP and explicit DOS/driver/signature/IRQ
models, including every33x33 priority pair and all33 effect lifetimes. Preserve
unchecked word indices/byte frames, ignored DOS status, fixed5000 reads, unbounded
filename scans, MIDI nonzero versus exactly1 routes and unsigned measure waits.
See `MAINL_SOUND_REVIEW.md` and `scripts/review_th03_mainl_sound.py`. Nine decoded
rows add no source/exact or accepted-intake credit; actual devices/files/payloads,
DATA/BSS/CRT, cold localized ownership and canonical packaging Oracles stay open.

Complete MAINL graph_putsa_fx review covers613bytes /226instructions plus native
GRCG46 /24 helper diagnostics; allraw and3ordered relocations match both caches.
Sixteen frozen providers and three private TC4 headers establish candidate
lineage, with no maintained MAIN remap. The1980 top-level calls (1974returns /
6budgets) check full64K flat stores, DGROUP and actual ports under synthetic
ROM/converter fixtures. Preserve signed division/remainders, unchecked second
bytes, pointer wrap, right-clip-after-consumption and narrow weight arithmetic.
See `MAINL_TEXT_REVIEW.md` and `scripts/review_th03_mainl_text.py`. One decoded
row adds no source/exact or accepted-intake credit; physical font/GRCG/pages,
CRT/data ownership, cold localization and canonical packaging Oracles open.

Complete MAINL vector/flip-table review covers twoTUs190bytes: three bodies189 /
70instructions and one diagnostic producer byte. All raw/1ordered relocation
agree with both caches. Vector retains frozenCPP; hflip root overlays maintained
MAIN ASM, with both cached OMF producers verified. Actual IATAN2 107bytes /
54instructions executes, including native INT_MIN divide faults and lowbyte XLAT
out-of-domain results. The22221 calls (22131returns/90traps) check fullDGROUP,
far outputs/alias order, all angles/quadrants, rounded table bytes and all256 LUT
stores. See `MAINL_MATH_REVIEW.md` and `scripts/review_th03_mainl_math.py`. Three
decoded rows add no source/exact credit; generated root/data/CRT ownership,
localized cold production and canonical packaging/complete Oracles remain open.


Complete MAINL PFOPEN review covers the TH03 bounded include281bytes /97
instructions plus1producer NOP, with actual near STR_IEQ56bytes /29instructions
as context. All338raw bytes/empty ordered relocations agree with both caches;
17frozen providers establish the maintained MAIN include overlay and root OMF
identity. The318 calls (312returns/6search budgets) check fullDATA/heap/buffers
under5 explicit buffer/heap models. Preserve end-marker fallthrough to seek and
error5, byte-only allocation errno, ignored statuses, filename-field overread
and conditional DF clearing. See `MAINL_PFOPEN_REVIEW.md` and
`scripts/review_th03_mainl_pfopen.py`. One decoded row adds no source/exact or
accepted-intake credit; adjacent graph return tail excluded. Cold localization,
root/dependency/DATA/BSS/CRT ownership and canonical packaging/Oracles stay open.


Complete MAINL archive-reader review covers5library includes356bytes:8bodies353 /
126instructions plus3source/producer bytes, with actual native near pointer
dispatch and far returns. Allraw/empty ordered relocations agree with2caches;
17frozen providers and root OMF/MAP identity bind the unchanged library source.
The4482 calls (4476returns/6nonterminal max-offset boundaries) check fullPFILE/
output/DGROUP under4 buffer/heap models, including257byte RLE expansion and
65536 successful native relative decodes. Preserve pre-read counters, distinct
AH status tests, unsigned seek argument mutation, output wrap/alias and ignored
seek/close/free status. See `MAINL_PFREAD_REVIEW.md` and
`scripts/review_th03_mainl_pfread.py`. Eight decoded rows add no source/exact or
accepted-intake credit; actual buffers/heap/hooks, combined calls, cold root/
DATA/BSS/CRT ownership and canonical packaging/full Oracles remain open.


Complete MAINL buffered-file review covers8frozen library bodies500bytes /
162instructions plus4NOPs, including the single DOS_ROPEN/FONTFILE_OPEN alias.
All504raw bytes/empty ordered relocations agree with2caches;19providers/root
OMF/MAP establish disjoint ownership. The5328top calls allreturn, with native
BFILL/BGETC/DOS-open and explicitDOS/heap boundaries; tenchains perimage check
open/read/close and seek/read. Preserve failedBSEEK leftFFFF stale-buffer reads
versusBSEEK_ zero/refill, word allocation wrap, byte errno, trustedfillcounts,
signedBREAD size, lowoffsetwrap and live metadata aliases. See
`MAINL_BUFFER_REVIEW.md` and `scripts/review_th03_mainl_buffer.py`. Eight decoded
rows add no source/exact oraccepted-intake credit; priorarchive receipts retain
separatebuffer models. Combined archive/hook, coldroot/DATA/BSS/CRT ownership
and canonical packaging/full Oracles remain open.


Complete MAINL archive INT21 hook review covers605bytes:3procedures549CODE /
225instructions,50tables,5CSstate and1NOP. Allraw/1ordered relocation agree
with2caches;32frozen providers/rootOMF and maintained MAIN PFOPEN overlay
identity verified. The4194top calls allreturn, including connected native
archive/buffer bodies1198contextual bytes and real handlerIRET. DOS, heap and
high-level installation files remain models; fullmemory outside stack and
interrupt register/flag returns checked. Preserve universalAH46error fromMOV/
inheritedZF, conditional directory leak, zero-size64Kdecrypt, filenameoverflow,
signedseek routing andIOCTLcount masks. See `MAINL_PFINT21_REVIEW.md` and
`scripts/review_th03_mainl_pfint21.py`. One decoded module row adds no source/
exact oraccepted-intake credit; native contexts not credited twice. Physical
vectors/DOS/files/heap, coldroot/DATA/BSS/CRT ownership and canonical packaging/
complete Oracles remain open.

Complete MAINL file-library review covers9frozen includes:11bodies783bytes /
311instructions +3NOPs, with native DOS_AXDX/FILESIZE78 /40 +2NOPs; priorDOS-open
26contextual bytes not credited twice. All892raw/ordered relocations agree
with2caches;22providers/root OMF/MAP verified. The6363top calls allreturn,
checking actualRETFs and fullphysicalmemory outside stack under explicitDOS/
filecursor fixtures. Preserve directreadCF ignoring, directwriteFFFF versus
buffered1, finalrestoreCF sizecorruption, append'smissingcreatefallback,
close-dependentEXIST, exactfullbuffer deferredflush, stickyEOF/DF/wrap/aliases.
See `MAINL_FILE_REVIEW.md` and `scripts/review_th03_mainl_file.py`. Two decoded
module rows add no source/exact oraccepted-intake credit; priorhook/graphics
receipts retainfile models. Combinedruntime, physicalDOS/files/heap, coldroot/
DATA/BSS/CRT ownership and canonical packaging/complete Oracles remain open.

Complete MAINL heap review covers5frozen includes8entries625body bytes /
257instructions +3NOPs, all628raw/emptyordered relocations equal2caches.
16providers/root OMF/MAP verified, including EVEN macros and seven explicit
priorMAIN-only scaffold substitutions. The3906top calls return;12malformed
cycle calls retainbudget stops. Native sharedtails/RETFs and wholephysical
memory outside stack checked under soleDOS48/49 models. Preserve longID
retention/roundingwrap, lazyfailure stalefields, uncheckedtopfree/no upperbound,
TH03unassign missingliveallocationguards andAX1 afterfailedfree, reserve/gap/
hole/coalescing behavior. See `MAINL_HEAP_REVIEW.md` and
`scripts/review_th03_mainl_heap.py`. One decoded module row adds no source/
exact oraccepted-intake credit; earliercallers retainheap models. Stack/CRT
allocators, combinedruntime/realDOS/lifetime, coldroot/DATA/BSS/ownership and
canonical packaging/complete Oracles remain open.

Complete MAINL stack review covers2frozen includes74body bytes /30instructions
+2NOPs=76, plus628prior nativeheap context notcreditedtwice. All704raw/empty
ordered relocations agree2caches;18providers/rootOMF/MAP verified. The1746top
calls return withactualRETFs andprivateassignmentprefix/publicentry recheck;
wholephysicalmemory outside stack and128releaseflag caseschecked. Preserve
uncheckedrelease/flagABI, equality/zero-get constraints, 17bitrounding,
CF-honoringlazyfailure andnativeheap/stackcollision. See `MAINL_SMEM_REVIEW.md`
and `scripts/review_th03_mainl_smem.py`. One decodedmodule row adds no source/
exact oraccepted-intake credit. CRTallocation, completegamecallers/physicalDOS/
lifetime, coldroot/DATA/BSS/ownership and canonicalpackaging/full Oracles open.

Complete MAINL palette/wait review covers eight frozen includes: 690 body
bytes /313 instructions plus two NOPs, 692 new bytes in five disjoint decoded
extents. Prior native DOS-open26 is context only. All718 raw bytes and empty
ordered relocations agree with both caches; 23 providers, root OMF and MAP
containment are verified. The7512 terminal top calls execute14748 native
entries, with24 separate budget observations. Native palette/load/fade/wait,
mutable CODE and far returns match independent full memory outside the stack
under explicit DOS, port and count-change fixtures. Preserve local signed
Tone clamping, LCD asymmetric nibble selection, short/failed-read stale data,
close-CF propagation, signed fade speed and low-byte mask waiting. See
`MAINL_PALETTE_REVIEW.md` and `scripts/review_th03_mainl_palette.py`.
Five decoded module rows add no source/exact or accepted-intake credit.
VSYNC installation/handler, real display/interrupt/files, complete callers,
cold root/DATA/BSS/CRT and canonical packaging/full Oracles remain open.

Complete MAINL VSYNC/vector/mode review covers three frozen includes, 361 body
bytes /166 instructions plus four saved CS bytes and three NOPs:368 new bytes.
Prior native WAIT38 is context only. All406 raw bytes and original ordered
relocations agree with both caches; 28 providers, root OMF/MAP and native
DGROUP site1FE5 are verified. The41556 terminal top calls execute88944 native
entries, with60 separate budgets. Actual procedures/RETFs/IRETs and connected
WAIT/counter handler match independent full memory outside the stack under
explicit DOS/BIOS/port/callback/manual-entry fixtures. Preserve repeated-start
phase, delay-carry skipping, valid-marker IRQ2-only restoration, callback BP
contract, low-byte vector/ignoredCF and mode status/ES clobbers. See
`MAINL_VSYNC_REVIEW.md` and `scripts/review_th03_mainl_vsync.py`.
Three decoded module rows add no source/exact or accepted-intake credit.
Physical/asynchronous IRQ eligibility, devices, complete callers/CRT/root/
DATA/BSS, cold source/layout and canonical packaging/full Oracles stay open.

Complete MAINL BFNT/super/DOS-close review owns1542 new decoded bytes in three
disjoint extents:1533 complete CODE bytes/742 instructions and nine producer
NOPs. Prior native heap/stack/palette/open794 is context only. All2336 raw bytes
and empty ordered relocations agree with both caches;53 frozen providers and
root OMF/MAP are guarded. The2892 terminal calls execute22908 native entries,
with30 separate budget observations. Actual conversion, registration, masks,
near/far returns, mutable CODE and flat VRAM stores match independent full
physical memory under explicit DOS/character-free/port fixtures. Preserve
BFNT SI/DI exchange, second-allocation mark leak, oversized-read FFF3/CF0,
extension carry ignored by the loader, sparse/zero-size registration and
DATA-based tail cancellation, plus zero-size/DF/signed-row-add draw behavior.
See `MAINL_SUPER_REVIEW.md` and `scripts/review_th03_mainl_super.py`.
Three decoded module rows add no source/exact or accepted-intake credit.
Physical GRCG/DOS/resources/character cleanup, remaining CRT/root/DATA/BSS,
complete callers/cold source and canonical packaging/full Oracles stay open.

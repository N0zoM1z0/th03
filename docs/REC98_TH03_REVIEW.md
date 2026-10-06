# ReC98 TH03 intake review

The review scope is frozen at ReC98 revision
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. The complete intake queue is
`config/rec98_th03_inventory.csv`; scoped review decisions are in
`config/rec98_th03_reviews.csv`. Regenerate or check the queue with:

```sh
python3 scripts/inventory_rec98_th03.py
python3 scripts/inventory_rec98_th03.py --check
```

The queue contains every tracked `th03/` file and root TH03 assembly/include,
every direct OP/MAIN/MAINL translation unit declared in the frozen Tupfile,
the named ZUN source subgraphs, its explicit `libs/kaja/ongchk.com` binary input,
and recursively referenced source includes. The corrected queue has 505 files.
Conditional includes are traversed conservatively, so cross-game branches
remain candidates until their TH03 relevance is reviewed. Unlinked TH03 files
remain visible as `unassigned`. Asset rows contain only names and hashes;
game assets and proprietary tools must never be imported. Unresolved includes
identify generated inputs or other dependency gaps requiring review.

This queue is not a compiler dependency graph or an acceptance ledger. A row
with `reviewed_code_artifacts` records only the local CODE extent review for
that artifact, backed by `config/units.csv` and the maintained replay manifest.
It does not close other artifacts, headers, initialized data, BSS layouts,
resources, packing, startup, scaffold assembly, or complete product ownership.
`boundary_review_artifacts` also records candidate boundary reviews; it grants
no exact credit. The enemy owner is a complete maintained candidate whose
ordered relocation gate remains unresolved, as documented in
`docs/reconstruction/MAIN_ENEMY_REVIEW.md`.
Remaining whole-file/artifact review is open. A separate MAINL CODE diagnostic
index now records all 33 frozen direct source paths in
`config/rec98_th03_candidate_reviews.csv`. Their 36 nonzero carriers contain
27,753 bytes: 27,752 independently reviewed, one unowned PI neighbor byte
and zero overlap. Thirty-two rows have complete CODE interval coverage;
five retain raw differences and three retain ordered relocation failures.
Failed evidence is preserved explicitly. See
`docs/reconstruction/MAINL_LINKED_CODE_INTAKE_REVIEW.md` and run
`python3 scripts/review_rec98_th03_mainl_intake.py --check`.
This index grants no whole-file, source or exact acceptance and does not change
the 69 scoped maintained MAIN paths. Twelve MAINL CDG/text rows now have independently
proved source presence in `src/shared/formats/cdg_load.cpp`, `cdg_put.asm` and
`cdg_noalpha.asm` and `src/shared/graphics/text.cpp`; index acceptance stays false and their1702-byte interval
credit is preserved without duplication. The same physical objects have
independent OP bindings. Both artifacts pass two
fresh cold carrier/raw/original-relocation/native replays; complete products
retain their own failures. See `reconstruction/SHARED_CDG_LOAD_REVIEW.md` and
`reconstruction/SHARED_CDG_DRAW_REVIEW.md` and `reconstruction/SHARED_TEXT_REVIEW.md`.
Upstream exactness is never inherited. Compatibility forwarders retain explicitly declared dependencies
on the frozen scaffold until the declarations can be localized and attested.

The existing thirteen MAIN source owners were rechecked in two cold builds
by `sol-rec98-baseline-20261005`: all forty functions and fourteen extents
passed the configured local gates. The baseline remains a bounded replay,
not a complete maintained game build.

Current MAIN acceptance contains thirty-eight maintained source owners / forty-three
CODE extents / 101 functions / 11628 owned bytes. Sixty-nine intake paths
have scoped CODE decisions, including the frozen wrappers and implementations
for hitbox, combo, gauge, movement, ordinary shots, player state, resident pointer,
extra-attack wrapper, hit circles, static HUD, playfield, sprite16 wrappers, MRS, shared sound/hardware and original collision/reversal assembly, and five complete handwritten includes
within the generated MAIN root carrier, plus all eight random-getter macro
expansions. The carrier itself remains unaccepted.
Header/dependency and
other-artifact review remains separate.

OP/MAINL root input hashes now bind to guarded DIET restorations of the pinned
Japanese stored targets. ZUN restores to flat COM. The diagnostic recipe and
namespace/acceptance limits are documented in
`docs/reconstruction/TH03_DIET_STORAGE_REVIEW.md`; none of these restoration
facts grants source acceptance or closes the remaining file/artifact queue.

The ZUN wrapper has three maintained source-present assembler candidates. Its
complete directory/component review and fourteen bounded dispatch observations
are documented in `docs/reconstruction/ZUN_LAUNCHER_REVIEW.md`. These decoded
candidates do not add accepted CODE paths; a successful fresh cold replay and
stored packaging/complete Oracles remain outstanding.

The complete frozen `libs/sprite16/sprite16.asm` ZUN -4 driver also has a
decoded payload boundary/source/ABI review, documented in
`docs/reconstruction/ZUN_SPRITE16_DRIVER_REVIEW.md`. Its 55 provisional
procedure diagnostics and code/data accounting cover the whole 4224-byte
payload. Complete cached raw equality fails by ten bytes; natural zero-gap
ownership and complete Oracles remain open. Two observed hazards are preserved
in bounded CPU probes. This adds no maintained driver source, exact function
or accepted intake CODE path, and does not close shared-header/artifact review.

The entire `th02_zuninit.asm` used as TH03 ZUN -2 has a separate candidate
review in `docs/reconstruction/ZUN_INIT_REVIEW.md`: all nine procedures and
783 data bytes, with complete 1390-byte cached target equality and explicit
compiler source line-ending association. Fifty-four bounded CPU/model cases
exercise DOS branch/vector behavior and interrupt/text contracts. The payload
is boundary-reviewed only; fresh maintained source/compiler encoding and
complete Oracles are still required. The broader queue remains open.

ZUN -5 has complete `res_yume` root/included implementation review and direct
helper contracts in `docs/reconstruction/ZUN_RESIDENT_REVIEW.md`: two root
functions (322 bytes), eleven helper diagnostics (423 bytes), whole cached
payload raw equality and sixty bounded main-only CPU/interface-model cases.
Only the two root functions receive boundary-reviewed ledger entries. Startup,
remaining CRT/library and whole-artifact/dependency review are still open.
Source/encoding/compiler/packaging and complete Oracles remain required; this
does not increase the 69 scoped accepted intake CODE paths or exact totals.

The complete `th01/zunsoft.cpp` ZUN -3 root is reviewed in
`docs/reconstruction/ZUN_SOFT_REVIEW.md`: ten functions, 1299 CODE bytes and
DATA/BSS declaration scope, whole 10096-byte cached raw equality, 3900 bounded
root CPU/model calls and explicit compiler-helper/foreign-interface separation.
Only root functions are boundary-reviewed; actual graphics/BFNT libraries,
assets, startup/CRT and whole-artifact ownership remain open. No maintained
logo source or accepted intake CODE path is added.

The binary-only `libs/kaja/ongchk.com` ZUN -1 input has a complete 926-byte
review in `docs/reconstruction/ZUN_ONGCHK_REVIEW.md`. All bytes match the
decoded target; 892 CODE / 34 initialized-data bytes and external workspace
are accounted separately. Thirty terminal CPU/port-model cases and four
explicit nonterminal polling observations preserve the PSP length-byte
priority parser, result classes and timeout/shared-tail contracts. No binary,
maintained source, compiler observation or exact credit is imported. Physical
devices, source recovery and stored packaging/complete Oracles remain open.

MAINL's complete 424-byte STAFF CODE segment has a separate bounded review in
`docs/reconstruction/MAINL_STAFF_REVIEW.md`: two generated-root functions and
the full C++ `flake_put` body, with both cached raw matches, sixteen provider
associations and 1947 CPU/model calls. The generated region still fails original
ordered relocations. Three new decoded boundary rows grant no maintained source,
accepted intake CODE path or exact credit. Complete device runtime, assets,
storage and whole-product ownership remain open.

The whole MAINL cutscene TU has source/control-flow/ABI candidate analysis in
`docs/reconstruction/MAINL_CUTSCENE_REVIEW.md`: thirteen bodies (3122 bytes),
72 switch-table bytes and one observed alignment byte. Three raw PI call-operand
differences remain; actual callers establish shifted target helper entries with
equal 37/136-byte bodies, without closing the producer. Selected 195 CPU calls
reject the upstream universal-CF comment and retain far-offset/loader hazards.
An additional 72-call box/cursor CPU review (`MAINL_BOX_REVIEW.md`) executes
full rectangle transfers and selected `n/s` paths under flat plane/interface
models; NULL/failed-free hazards and word-only offset wrap are retained.
Ninety complete interpreter-loop CPU/model cases and three missing-STOP budget
observations (`MAINL_ANIMATE_REVIEW.md`) retain NUL skipping, unvalidated
second-byte consumption, input speedup and actual box cleanup. Remaining opcode
branches and physical devices remain open. An additional seventy-two
picture/packed CPU calls (`MAINL_PICTURE_REVIEW.md`) check loop/port/pointer
contracts and scalar conversion while preserving invalid-index/negative-clip
behavior. Far-return transitions use an explicit model for a reproduced
memory-read-hook engine defect; EGC mask pixels/page banks remain unproved;
no maintained source or accepted intake CODE path is added.

Complete MAINL registration/score-data candidate review covers seventeen bodies
(2720/229 bytes) in `MAINL_REGIST_REVIEW.md`. Registration retains six raw PI
call-operand differences; score-data cached raw equality grants no source or
exact acceptance. The 456 CPU/interface calls retain cursor255 outside-section
writes, stale-buffer acceptance after failed reads, all-rank unlock on recreate,
rank offset wrap and accumulated filename/viewer side effects. Files, inputs,
rendering, sound and other foreign interfaces remain explicit models. Two
decoded boundary-reviewed module rows add no accepted intake CODE path or
authored credit; cold localization, generated DATA/BSS, devices, ownership and
packaging/complete Oracles remain open.

The bounded generated snow/frame cluster has seven complete bodies (464 bytes)
reviewed in `MAINL_SNOW_REVIEW.md`, with actual blitter, IRand and vector2
dependencies (187 bytes). The 918 CPU/clock/music cases preserve unchecked
capacity, single coordinate correction, inherited DF and adaptation order.
Independent private BMP extraction matches generated/target sprite data and
scalar sine/cosine data agrees. Three raw clear encodings, six reversed original
relocation sites and a neighboring unowned data byte remain failures. No asset
import, source/exact acceptance or additional accepted intake CODE path follows;
remaining generated root segments, devices, cold layout and complete
packaging/ownership Oracles remain open.

The remaining ten MAINL_03_TEXT bodies (2875 bytes / 949 instructions) have
complete candidate source/control-flow/ABI review in
`MAINL_TRANSITIONS_REVIEW.md`. With the separate snow cluster they cover the
whole 3339-byte carrier, without authored credit. Seventeen native encoding
bytes and multiple original relocation sequences still fail. Across target
and two caches, 393 CPU/interface calls preserve dissolve residual bits,
zero-width looping, short-duration division fault and staff score/skill,
input/fade/free contracts. Native E-plane operations execute; snow, clock,
graphics, font and other foreign interfaces are models. Ten new decoded
function rows add no maintained source, exact owner or accepted intake CODE
path. Remaining root segments, DATA/BSS/resources, physical devices, cold
source/layout and canonical packaging/complete Oracles remain open.

`MAINL_ROOT_REVIEW.md` completes candidate analysis of the root's 2488-byte
CUTSCENE_TEXT contribution: nine procedures (2470 bytes / 810 instructions)
and an 18-byte switch table. Across target/two caches, 1368 actual root-body
invocations retain story indexing, filename mutation, continue score/credit,
clock and returned-exec contracts under explicit foreign interface models.
Ten raw PI operands and original 114-site relocation ordering remain failures.
One decoded module boundary row adds no maintained source, exact owner or
accepted intake CODE path. Root libraries, shared dependencies, DATA/BSS/assets,
physical devices/CRT, cold source and canonical packaging Oracles stay open.

`MAINL_LIFECYCLE_REVIEW.md` covers the complete initialization/general-exit/
exit-to-MAIN TUs (169 bytes) and the direct 41-byte plane helper. Cached raw
bodies and original relocations agree; producer association explicitly includes
three carriers remapped to maintained MAIN source, alongside unchanged frozen
providers. The 153 actual CPU/interface invocations preserve AX/CF gate,
plane stores, near-call/far-return frames, exit order and actual caller-prefix
failure fallthrough. Three decoded function rows add no authored source,
accepted intake path or inherited exactness. Cold MAINL localization, full
libraries/DGROUP/BSS/devices/CRT and canonical packaging Oracles remain open.

`MAINL_CDG_PUT_REVIEW.md` covers both complete native drawing TUs (496 bytes):
three bodies493/200instructions and three observed EVEN bytes. All cached raw
bytes and original ordered relocations agree. The261 actual blitter invocations
check code-operand patches/re-entry and complete flat stores, preserving zero
width, negative-top/left, slot/offset wrap and DF behavior. GRCG/lookup/source/
plane fixtures are explicit models; real RMW/pages/assets remain unproved.
Three decoded function rows add no maintained source, accepted intake path or
exact credit; cold ownership, DATA/BSS/devices and packaging Oracles stay open.

The subsequent `SHARED_CDG_DRAW_REVIEW.md` independently binds OP and MAINL,
localizes both complete ASM carriers and proves two fresh cold rounds. All496
raw bytes, original ordered relocations and original nondependency OMF records
match. Each source image runs120 invocations/all200 instruction positions,
including two independently checked nonterminal width0 prefixes. Persistent
SMC/VRAM reentry, full physical1MiB outside stack, frames and ordered effects
are checked. Six existing MAINL rows gain source presence without new interval
credit. Source vectors cover20products/350gameobjects; nine Research changes
remain separately recorded. Physical graphics/IRQ, global declarations,
complete products and exact acceptance remain open.

`MAINL_CDG_LOAD_REVIEW.md` covers the complete593-byte loading/freeing C++ TU:
five functions/219instructions with equal cached raw bytes and24 original
ordered relocations. Eight frozen providers bind unchanged to both caches.
The936 actual top-level CPU/interface calls check full DGROUP and requests,
preserving word-promotion/size wrap, stale headers/ignored file and allocation
results, unchecked slots, noalpha alias/reset and follow-up frees. Six library
interfaces model header/file/heap requests without payload assets or real
allocation. Five decoded function rows add no source, accepted intake path or
exact credit; cold localized ownership, DATA/BSS/CRT/libraries and packaging
Oracles remain open.

`MAINL_PI_REVIEW.md` covers all four complete PI wrapper TUs (555bytes,
five bodies/197instructions), with native76-byte free/36-byte memcpy diagnostics.
Complete bodies agree at reviewed coordinates, while firstthree entries shift1
and fixedraw/relocations fail; loading/quarter whole raw/order agree. Cached
loading source explicitly redirects to maintained MAIN, without inherited
MAINL acceptance. Its708 native/interface calls check wholeDGROUP and preserve
pointer carry loss, interlace unsigned/even-counter hazards, unchecked quarter/
slot/top and retained pointers. Five decoded rows grant no source/intake/exact
credit. All340 cached program-byte failures are now classified across reviewed
scopes; equal-byte owners, DATA/BSS/resources/libraries/CRT and packing remain
open. No actual PIdecoder, allocator or physical graphics acceptance is claimed.

`MAINL_INPUT_REVIEW.md` covers the complete three-TU input chain: twelve
functions,910 bytes/313 instructions and a21-byte native frame-helper diagnostic.
All cached raw bodies and six original relocation sites agree. Three old
carriers redirect to maintained MAIN implementations, with no inherited
MAINL acceptance. The762 native calls/CPU budgets preserve two-pass keyboard
OR, mode merges, song-measure AX overwrite, zero-frame first polling and
release-before-limit ordering under explicit device/clock models. Original
529NOP ownership remains open despite the unused frozen codestring's possible
role in PI displacement. Twelve decoded rows add no authored source, accepted
intake path or exact credit; devices/DATA/BSS/cold producer/packaging remain open.

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

The subsequent `SHARED_TEXT_REVIEW.md` independently binds OP and MAINL and
localizes the complete613-byte CPP plus one bounded glyph macro include. Two
fresh cold rounds match original raw bytes, three ordered relocations, complete
original nondependency OMF records and public/MAP ownership. Each artifact/image
runs673 invocations/all250 positions, including three independently checked
nonterminal prefixes and persistent VRAM reentry. The single MAINL row gains
source presence without duplicate interval credit. All20products equal the
preceding drawing proof;349othergameobjects remain unchanged. Actual CRT/font/
GRCG/pages, global DATA/BSS, complete products and exact acceptance stay open.

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

Complete root MAINL PI decoder/release review covers1600 independent decoded
bytes, including the shared loader error tail and private color/byte/refill
helpers.22 frozen providers/root OMF/public MAP and2330 scoped CODE/producer
plus10DATA bytes agree with both fresh cold products. The immutable base
receipt and successful borrower/refill supplement total3420 terminal calls
and60 semantic prefixes;706/711 instruction positions execute, with five
unreachable EVEN NOPs retained in raw/structural coverage. Resource leaks,
ignored read status/length, failed-extension parsing and zero-copy cycles
remain observed behavior. See `reconstruction/MAINL_PI_DECODER_REVIEW.md`,
`scripts/review_th03_mainl_pi_decoder.py` and its borrower supplement. Two
independent decoded rows add no maintained source/exact or accepted intake
CODE-path credit. ROOT/CRT/DATA/BSS/other-artifact/packing/full Oracles remain
open; previous wrapper and coverage receipts keep their original scope.

Complete remaining MAINL root-helper/producer review covers sixteen decoded
gaps722 bytes:701 body bytes/351 positions and21 producers. All1003 scoped
CODE/producer bytes including prior PFOPEN281 context and290 initialized
DATA bytes match both cold products with empty ordered relocations.39 frozen
providers/root OMF/thirteen public MAP entries bind lineage. The25335 tail
calls return25305 times and stop at30 actual DIV faults;72 separate semantic
prefixes retain open frames. Native STR_IEQ separately executes through318
legacy PFOPEN calls, with312 returns/six search budgets.344/351 positions
execute; an atan NOP and unreferenced SAJOUT retain structural/raw coverage.
Preserve absent-joystick entry SI, unchecked second resident allocation,
MCB cycles, palette alias store/read order and text DF/BIOS geometry. See
`reconstruction/MAINL_ROOT_TAIL_REVIEW.md` and
`scripts/review_th03_mainl_root_tail.py`. Sixteen independent decoded rows
add no maintained source/exact or accepted MAIN intake credit. Remaining
startup/CRT/DATA/BSS/device/complete callers and full artifact Oracles stay
open;505 files and69 scoped MAIN CODE paths retain their separate scope.

Complete MAINL CRT break/pointer substrate review covers six linked compiler
CODE carriers, 628 bytes /277 instruction positions, plus111 bounded
initialized DATA bytes. All raw slices/empty ordered relocations match both
cold products. Six locally pinned CL.LIB members, twelve public MAP entries,
two DATA contributions and39 symbolic fixups reproduce the linked CODE,
including one same-CODE far-call relaxation. Six stale A3 naming-comment
checksums are reported without repair; all other selected records are checked.
All33,741 terminal calls /77,142 native entries agree with independent
integer/address models and whole physical memory outside the stack. Preserve
signed negative-MiB sbrk aliases, DOS BXFFFF/success collisions, word-wrapped
paragraph rounding, failure heap-top changes and INT_MIN errno conversion.
See `reconstruction/MAINL_CRT_BREAK_REVIEW.md` and
`scripts/review_th03_mainl_crt_break.py`. Compiled Borland dependencies are
separate from ReC98 authored source; six decoded rows add no maintained
source/exact or accepted MAIN intake credit. Complete allocators/new/delete,
startup/exception/DATA/BSS/lifetime and all-artifact Oracles remain open.

`OP_CONFIGURATION_REVIEW.md` adds seven decoded OP candidate units totaling
472 bytes: three complete near configuration functions and whole far
DOS-exit/plane/mode/init functions. Across target/two cold products12,960
terminal calls execute every selected instruction, with native compiler-copy
context and explicit file/driver/library reply models. Unshifted367 bytes
match, while original initialization0571 versus cold0570 retains raw and
ordered relocation failure. Four direct source carriers have bounded complete
CODE-body review; `op_01.cpp` has only its271-byte configuration portion.
Frozen sound codestring remains candidate producer evidence, not imported
encoding. No maintained OP source/exact or complete file/header/storage
acceptance follows; the complete intake goal remains open.

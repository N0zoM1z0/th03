# TH03 — agent handoff (2026-11-05; after479 working source)

**Snapshot warning:** after439 is the last **fully storage-audited and
cleaned** source checkpoint, but the current locally reviewed working-source
checkpoint is **after479** (section 1a). Do **not** infer a clean
worktree, complete source acceptance or cleanup eligibility from this
frozen table. Inspect latest `git status -sb`, `git log` and the actual
`build_th03_mainl_after*_work.py`/receipts before taking action.

**Start here, not at a historical progress snapshot.** Inspect `git status -sb`
and `git log -5 --oneline` before acting. Treat **all existing dirty changes**
as work to continue; do not reset or bypass them. Work on pinned original
Japanese PC-98 targets, commit each substantial improvement as
`gpt-web: xxx`, make multiple scoped commits where useful, **do not run
routine full cold replay**, and do not push unless requested.
Read [AGENTS.md](../AGENTS.md), [the workflow](RE_WORKFLOW.md) and
[the architecture](ARCHITECTURE.md) before changing native build recipes.

## 1. Last fully audited cleanup checkpoint (not formal acceptance)

| Japanese MAINL CRT evidence | Audited after439 snapshot |
| --- | ---: |
| Original CL.LIB member slots | **893** |
| Complete members linked from maintained source | **647** |
| Remaining contextual vendor members | **246** |
| Source-built original-equal CRT CODE | **174,691 bytes** |
| Original decoded Japanese MAINL EXE | **67,372 bytes** |
| Ordered DOS MZ relocations | **677** |
| Actual fresh native TASM/TLIB/TLINK rounds | **2; both EXE and MAP byte-exact** |
| Protected native receipt DAG | **177 stages, 4,464 files** |
| Factory accepted-source proof for this expansion | **Not established** |

Pinned after439 source receipt (not latest source after new layers):
`.analysis/work/mainl-after439-streambuf-base-default-constructor-boss-build.json`
(SHA-256 `dd0a1a82695b00e2a3aeaa4e93a609450b50e834e4dd80b228c2eddaef5e8788`).
Original source-bound producer: `scripts/build_th03_mainl_after439_work.py`.
Focused reviewer: `scripts/review_th03_mainl_after439_work.py` mode
`streambuf-base-default-constructor-boss`. This after439 source checkpoint was
committed as `86e3843`; the after439 cleanup and documentation commits do
not change its retained proof. Later source checkpoints are separate. Original targets have
`candidate-local-attested` provenance, **not** independently proved
pristine-dump provenance.

**Critical distinction.** Byte-exact decoded MAINL EXE/MAP and complete
logical OMF fields for working-source CRT members do **not** imply every
Borland OBJ record or literal ordered FIXUPP is identical to TASM output.
Some known ordering and near-frame differences are deliberately disclosed
in individual review files. These also do **not** establish whole-game
source ownership or Factory/canonical packed-file acceptance.

## 1a. Current working-source checkpoint — independently verified after479

**Current working-source CRT is after479, not the frozen after439
storage audit or historical after474 handoff.** The new native producer
verifies its unchanged after478 parent and preserves two fresh
TASM/TLIB/TLINK original-equal EXE/MAP rounds. No ancestor cold
replay or new Factory accepted-source credit was claimed.

| Japanese MAINL working CRT | Reviewed after479 |
| --- | ---: |
| Original Japanese Borland CL.LIB member slots | **893** |
| Complete source-linked original CRT members | **687** |
| Remaining contextual original vendor members | **206** |
| Complete original-equal source-built CODE | **183,153 bytes** |
| This session's new typed initialized DATA / INITDATA | **9 / 6 bytes** |
| Decoded Japanese EXE / ordered MZ relocations | **67,372 bytes / 677** |
| New native TASM/TLIB/TLINK rounds at latest stage | **2, both EXE/MAP original-equal** |
| New Factory accepted-source credit | **None established** |

**This session completed five separately committed original CRT
members** totalling **873 CODE, 9 initialized DATA and 6 INITDATA bytes**,
each with two new native TASM/TLIB/TLINK rounds, independent
original member CODE/data/OMF comparison, a dedicated reviewer,
and focused tests:

- after475 chsize (original CL.LIB slot 203): **199 CODE**, original
  DOS file growth/truncation with repeated zero-filled 128-byte
  writes, native seek restoration, two original literal ordered
  OMF FIXUPPs. Corrected original growth-loop reset target;
  commit 73cf67d.
- after476 mnsbase (790): **205 CODE**, private FAR ios basefield
  setter and public setbase manipulator constructor, real
  six-byte C++ allocation and two symbolic private CODE function
  pointer fields; all six original logical OMF FIXUPPs match.
  Commit 5280475.
- after477 pc98timr (508): **162 CODE + 5 DATA**, private IRQ
  handler plus public PC-98 timer controller, INT 1Ch registration,
  real persistent FAR callback and 13 logical FIXUPPs. Correct
  segment-of-DGROUP reference and original busy-wait target;
  commit 5b36a70.
- after478 cibmdely (524): **188 CODE + 4 DATA + 6 INITDATA**,
  complete IBM PIT read/calibration, public delay, conio mode
  gating, near 32-bit multiply, true CRT initializer at CODE+35
  with all seven **literal ordered** original FIXUPPs;
  commit bf032ea.
- after479 fmovmem (439): **119 CODE**, the genuine overlap-safe
  FAR memory-copy leaf, both original FAR publics, N_PCMP
  near comparator, direction flag and MOVSB/REP MOVSW paths,
  single **literal ordered** original FIXUPP;
  commit ae038d7.

**Current verified source-bound root:**

    .analysis/work/mainl-after479-far-overlap-safe-memmove-leaf-build.json
    SHA-256 c39374958cabd01399f68c7e631e244147fc1b234fba3d0b2bd19eccbfa1d7d8

Latest producer: scripts/build_th03_mainl_after479_work.py
(mode far-overlap-safe-memmove-leaf).
Independent reviewer: scripts/review_th03_mainl_after479_work.py.
Focused tests: tests.test_mainl_after479_work.
The five new after475–after479 source/driver hashes,
entire parent receipt chain, all source-bound writer logs and
**both complete raw OBJ/LIB/EXE/MAP output vectors per stage**
were checked together. No full cold replay was performed.
**Preserve every old and new receipt, raw native round and log.
The last storage-audited after439 cleanup remains fail-closed
for all newer layers.**

**Large cplx2 boss now has a fourth complete semantic FAR body,
with two exact unresolved compiler-codegen gaps.** This is
substantive PARTIAL work (commit 1ba9656), not another complete
CRT source member. New maintained x87 source:
src/mainl/crt/cplx2_four_functions_partial.asm
and separately tested two-round native probe:
scripts/probe_th03_cplx2_acos_partial.py.
The source contains three previously source-equal division
procedures (original CODE+0..691), plus the complete
acos(complex) body (original CODE+692..1078). The first
**1,069 original CODE bytes outside two internal direct FAR
calls** match TASM byte-for-byte; the original **1,079-byte**
prefix is a **1,077-byte** native source object because TASM
compiles both original five-byte same-CODE direct FAR calls
(CODE+799 and CODE+984, to arg at CODE+1079) as four-byte
PUSH CS / NEAR CALL sequences. No padding, fake original
bytes or OBJ patch is used. Of **161 original FIXUPPs** in
the four-function prefix, the other **159** match by site,
target identity, width and addend after the two
documented one-byte shifts. **143 original frame-method-4
FPU references** are emitted using TASM method 5; the two
original local direct FAR call OMF fields remain missing.
Only 12 original DATA bytes (+16..27) are represented;
original DATA+0..15 is implicit. Reproduction and
limitations are in
[the cplx2 acos focused review](MAINL_CPLX2_ACOS_FOUR_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md).
The preceding
[three exact division functions](MAINL_CPLX2_THREE_DIVISION_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
remain preserved. **The 5,598-byte cplx2 member and the
1,947-byte isteldbl remain unsourced and earn zero new
complete-source CRT or Factory credit.**

**Proof limits:** source-built complete CODE/DATA and original-equal
EXE/MAP do not establish every original Borland OBJ record or
literal ordered FIXUPP equality. after475/478/479 now have
literal ordered original FIXUPP equality; after476/477
have complete logical but differing literal FIXUPP ordering.
The cplx2 partial source remains two bytes short of its
four-function original CODE span with 143 disclosed frame
differences. The Japanese target provenance is still
candidate-local-attested, not independently pristine proven.
MAINL canonical packed-file credit remains **0/250**; whole-game
source exactness and total reconstruction percentage remain open.

## 1b. Previous working-source checkpoint — after474 (historical)



**Historical after474 working-source checkpoint, now superseded by after479.** The after474 producer checks the
entire inherited source-bound after473 carrier, runs two native
TASM/TLIB/TLINK rounds and retains complete source/driver/parent
hashes. No ancestor cold replay or new formal Factory source
acceptance is claimed.

| Japanese MAINL working CRT | Verified after474 |
| --- | ---: |
| Original Borland CL.LIB members | **893** |
| Complete source-linked original CRT members | **682** |
| Remaining contextual vendor members | **211** |
| Complete original-equal source-built CODE | **182,280 bytes** |
| This session's new BSS | **4 bytes** |
| Original Japanese decoded EXE / MZ relocations | **67,372 bytes / 677** |
| New native TASM/TLIB/TLINK rounds at latest stage | **2, both EXE/MAP exact** |
| New formal Factory source credit for this expansion | **Not established** |

**Six newly complete original CRT members** add **1,076 CODE bytes**
and four BSS bytes this session. Each has separately committed natural
8086 source, independent original CL.LIB CODE/OMF inspection,
two new full native OBJ/LIB/EXE/MAP round outputs, a scoped reviewer
and passing tests:

- after469 hlsearch (466): **209 CODE**, generic private near FAR
  heap search core, FAR comparator, insert-enabled __hlsearch and
  find-only __hlfind. Only one original N_PADA@ near TARGET-frame
  versus TASM CODE-frame difference at CODE+52 — commit dfc116f.
- after470 read (276): **207 CODE**, full ___read DOS text-mode I/O,
  CR/LF translation, Ctrl-Z seek, original ES:SI LODS and I/O error
  handling. All **eight literal ordered original FIXUPPs** match;
  native BSS-before-DATA GROUP also restored — commit c6bccf3.
- after471 int86 (175): **207 CODE**, complete FAR _int86 and
  _int86x entrypoints, dynamic stack-resident INT nn trampoline,
  segment/FLAGS register images, native carry/error handling;
  both **literal ordered FIXUPPs** match — commit e2d1554.
- after472 fstrtok (460): **203 CODE + 4 BSS**, true persistent FAR
  tokenizer state and two real delimiter scan loops, with
  **12 exact logical BSS relocation fields**. Strict CODE
  review corrected a nonoriginal empty-delimiter branch — 0a9a931.
- after473 putw (274): **125 CODE**, real FILE fast-buffer low/high
  byte writes and two separate FAR __fputc fallbacks, preserving
  original unaligned high-byte argument load — commit 7c803e0.
- after474 eof (216): **125 CODE**, true DOS device IOCTL,
  current/end/restore seek position probes and near __IOERROR,
  all **three literal ordered FIXUPPs** exact — commit 98366f7.

**Historical after474 root source-bound receipt:**

    .analysis/work/mainl-after474-dos-file-eof-seek-probe-leaf-build.json
    SHA-256 54bcf62b4f7cec2e7c8527734ba9823abb8f6f634ae0e8033bcccb37ff8047bc

Producer: scripts/build_th03_mainl_after474_work.py,
mode dos-file-eof-seek-probe-leaf.
Independent reviewer: scripts/review_th03_mainl_after474_work.py.
Focused test: tests.test_mainl_after474_work.
The six after469–after474 receipts' complete parent chains,
source+driver hashes, all writer log hashes and both full raw
OBJ/LIB/EXE/MAP vectors were checked together. Both new rounds
link to the original decoded Japanese MAINL EXE and complete MAP.
**Protect every inherited receipt, writer log and two-round
native output; the old after439 cleanup is fail-closed and
does not authorize deletion of these artifacts.**

**Large cplx2 boss advanced materially but remains unfinished.**
Commit 9a7de88 contains genuinely compilable native EMUL x87
source for its first **three entire division FAR functions**
(CODE+0,+166,+405, total **692/5,598 original CODE bytes**).
The standalone scoped verifier builds twice and compares the
entire 692-byte original code prefix and all **97 exact
relocation sites, symbol target identities, widths and
addends** against the original CL.LIB member. The first 90
of those are **original Borland location-frame method 4**,
whereas TASM EMUL emits target-frame method 5. This
original-vs-native discrepancy is explicitly retained and
**not silently normalized to false raw OMF equality**.
One TASM COMENT native timestamp byte can differ between
the raw round-1 and round-2 object SHA hashes; all other OMF
records compare identically, and original CODE parity is
unchanged. Reproduction and remaining scope are recorded in
[the cplx2 three-division-functions review](MAINL_CPLX2_THREE_DIVISION_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md).
**cplx2 is not another complete CRT source member and earns
zero complete source or Factory credit.** Its remaining
4,906 CODE bytes and 19 other public functions remain.

**Current proof limitations:** code/relocation/native link parity
does not mean every original Borland OMF program record is
literal-equal to TASM output, nor does an incremental source
commit grant Factory acceptance. after469 has its one
documented NEAR frame gap; after472/473 have Borland/TASM
literal FIXUPP chronology differences; after470/471/474
match their original literal ordered FIXUPPs. Pinned Japanese
targets remain candidate-local-attested, not independently
proven pristine dumps. MAINL canonical packed-file accepted
units remain **0/250**. Whole-game reconstruction percentage
is not implied or asserted.

## 1c. Previous working-source checkpoint — after468 (historical)



**Historical after468 source build, superseded by after474.**
After468 verifies the retained after467 parent evidence and complete
unchanged source-bound carrier before two fresh TASM/TLIB/TLINK rounds.
No full cold replay or new Factory accepted-source credit was claimed.

| Japanese MAINL working CRT | Verified after468 |
| --- | ---: |
| Original CL.LIB slots | **893** |
| Complete source-linked original CRT members | **676** |
| Remaining contextual vendor members | **217** |
| Original-equal source-built CODE | **181,204 bytes** |
| This session newly source-built DATA / INITDATA | **16 / 6 bytes** |
| Full decoded Japanese EXE / MZ relocations | **67,372 bytes / 677** |
| New native build rounds | **2, both EXE/MAP byte-exact** |
| New formal Factory source credit | **Not established** |

**Seven separately committed original CRT source members** add
**1,424 CODE, 16 DATA and 6 INITDATA bytes** this session. All
are complete original-scope source, checked individually against
the real Japanese Borland CL.LIB programs, with their own fresh
two-round TASM/TLIB/TLINK output, focused reviewer and tests:

- after462 vdelxf (142): **215 CODE**, FAR vector-delete,
  hidden array metadata, true 32-bit multiply/reference-count
  adjustment and both far deletion paths. One exact, site-locked
  N_LXMUL near frame discrepancy at CODE+118 — commit 7ae4d0b.
- after463 _ftime (183): **235 CODE**, DOS date/time far helpers,
  midnight refresh, timezone division and real DST/Unix
  conversion. Two exact, site-locked imported NEAR frame differences
  at CODE+119 and +159 — commit c4f85d8.
- after464 ccomgptx (512): **210 CODE**, all three PC-98/IBM
  FAR gettext/puttext/getputtextsize dispatchers and 12 exact
  logical OMF fixups — commit c1f49d8.
- after465 _pathops (186): **208 CODE + 16 DATA + 6 INITDATA**,
  full DOS 21h/6300h DBCS path initialization, two FAR predicates,
  symbolic CRT INITDATA+2 -> CODE+0 registration and all
  **eight literal ordered original FIXUPPs** — commit 0726bd6.
- after466 lconv (242): **212 CODE**, ten live locale FAR
  strings, eight monetary/format flags and 41 original logical
  OMF fields — commit e29d66f.
- after467 dostimu (37): **214 CODE**, original packed DOS time
  to UTC with leap-year/month-day and DST adjustments.
  All **five literal ordered original FIXUPPs** match — bf08a49.
- after468 getw (66): **130 CODE**, complete FILE-buffer
  two-byte leaf, both genuine far fgetc fallbacks and EOF logic,
  two original logical FIXUPPs — commit cf68a71.

**Historical after468 complete source-bound root receipt:**

    .analysis/work/mainl-after468-stdio-getw-two-byte-leaf-build.json
    SHA-256 9d6994a911d7e5d2f3575a7d7db269b612d87d7dc57e6698e15bbfe9dc22a036

Producer: scripts/build_th03_mainl_after468_work.py
(mode stdio-getw-two-byte-leaf). Independent reviewer:
scripts/review_th03_mainl_after468_work.py, focused tests:
tests.test_mainl_after468_work. The entire after461–468 parent
receipt chain, new source/driver hashes, all seven per-stage
log phases, and both complete raw OBJ/LIB/EXE/MAP vectors
per new stage were verified on 2026-11-05 without cold replay.
**Protect every inherited source receipt and raw native round;
the old after439 cleanup remains fail-closed and is not a
permission to delete new evidence.**

**Giant original x87 boss research (not source-linked credit):**
A separately tested, read-only OMF parser was committed as
dbe9dee: scripts/probe_th03_mainl_large_fixups.py.
It independently reads all **112** original fixups of isteldbl
(1,947 CODE), including 85 frame-method-4 references, and
all **860** of cplx2 (5,598 CODE), including 734 method-4
references. The original cplx2 DATA SEGDEF is 63 bytes, but
only the final 47 are materialized; DATA+0..15 is implicit.
Its six-byte INITDATA has an original CODE+5575 pointer at
INITDATA+2. See
[large x87 location-frame OMF findings](MAINL_LARGE_X87_LOCATION_FRAME_OMF_ANALYSIS.md)
and tests.test_mainl_large_x87_location_frames.
**These two large members remain unsourced.** Never silently
normalize their method-4 original frame metadata or count
them as maintained-source units.

Two inherited generator issues were found, diagnosed and fixed
rather than bypassed: broad numeric replacement had changed
after467 review's fixed original EXE length from 67,372 to
67,472; after468 initially expected 219 contextual vendor
members in its 675-source parent instead of 218. The first
reviewer was corrected, the second parent check restored,
and the ignored local stage helper now uses field-anchored
substitutions instead of uncontrolled number replacements.

**Proof limits:** native CODE/DATA and decoded EXE/MAP equality
plus complete original logical OMF sites does not establish
literal ordered FIXUPP equality or original raw OBJ identity
for every member. After462/463 have disclosed narrow near-call
frames, after464/466/468 have literal record-order differences,
while after465/467 reproduce their literal FIXUPPs. The pinned
Japanese source remains candidate-local-attested rather than
independently proven pristine. MAINL canonical packed-file
accepted credit remains **0/250**.

## 1d. Previous working-source checkpoint — after461 (historical)



**Historical after461 source evidence, superseded by after468.**
After461 verifies the retained source-bound receipts through after460;
the native producer builds only the affected original member, with two
fresh TASM/TLIB/TLINK rounds and complete original-equal decoded EXE/MAP.
No ancestor native cold replay or Factory source acceptance is implied.

| Japanese MAINL CRT evidence | Verified after461 |
| --- | ---: |
| Original CL.LIB members | **893** |
| Original source-linked CRT members | **669** |
| Remaining contextual vendor members | **224** |
| Complete native source-built original-equal CODE | **179,780 bytes** |
| Complete native EXE / original DOS MZ relocations | **67,372 bytes / 677** |
| Native producer rounds for this stage | **2; both EXE/MAP byte-exact** |
| Added canonical MAINL/Factory source credit | **None** |

This session completed **six original members** as individually committed
natural source, adding **1,648 source-built CODE bytes and 588 initialized
DATA bytes**. Each has its own fresh, retained two-round native output
vector, a source- and driver-hash-bound producer, independent original OMF
review, and a passing focused test:

- after456 / vidinfo (570): **231 CODE / 16 DATA**; full PC-98 video
  mode conversion, text info and 8-entry typed mode map, all 14 logical
  OMF fields. Exactly one Borland TARGET-frame vs TASM CODE-frame
  near call to WHEREXY at site 192, independently guarded. Commit 79f08e2.
- after457 / iomacro (80): **234 CODE**, six real stdio fast/fallback
  FAR entries getc/getchar/putchar/putc/feof/ferror. All 12 original
  **literal ordered FIXUPPs** match. Commit 18815f9.
- after458 / setjmp (365): **214 CODE**, original FAR setjmp/longjmp,
  complete saved 16-bit register/SS:SP/FLAGS image and exception-aware
  local/global unwind. All four **literal ordered FIXUPPs** match.
  Commit a423753.
- after459 / MBTOMB (638): **207 CODE / 432 DATA**, bidirectional Shift-JIS
  conversion and five genuinely typed Japanese character mapping
  tables, with six exact logical OMF fields. Commit 0531d29.
- after460 / bcd1 (195): **398 CODE / 140 DATA**, full original BCD
  exponent helper and four FAR conversion/power exports. TASM5
  **EMUL** naturally emits the original FIERQQ/FIDRQQ/FIWRQQ
  simulator fields; ten 80-bit power constants retain the original
  Borland significands, not TASM's alternate decimal rounding.
  All 23 logical FIXUPPs match. Commit 07ab742.
- after461 / cplx1 (208): **364 CODE**, four original complex arithmetic
  FAR exports and 55 exact logical FPU emulator/FAR call OMF references.
  Closing/reopening the SAME original CODE segment after the first
  genuine FIWRQQ emission gives both the original imported symbol
  order and a genuine FAR new-object call, avoiding TASM's invalid
  near-call optimization. Commit 891635b.

The historical after461 complete **source-bound root** was:

    .analysis/work/mainl-after461-complex-x87-multiply-boss-build.json
    SHA-256 a534ca99448cdbcd44decb8721e6b3d0ce66fc8dbc2fab034840068cf63f48b0

Producer: scripts/build_th03_mainl_after461_work.py
mode complex-x87-multiply-boss. Independent reviewer:
scripts/review_th03_mainl_after461_work.py; focused tests:
tests.test_mainl_after461_work. The complete unchanged after455 parent
is retained at
.analysis/work/mainl-after455-multibyte-strtok-state-machine-build.json
(SHA-256 ea3cfc8ba5e1112f9fce3cce8943a4380079ecd5b92ce2770cd55220ba550163).
All new source receipts, writer logs and **both raw OBJ/LIB/EXE/MAP
rounds** are protected dependencies. Do not run the frozen after439
cleanup script or use a generic generated-file preview to delete them.
Earlier per-member review/chronology is in the
[working CRT index](MAINL_WORKING_CRT_RECOVERY_INDEX.md).

**Proof limitations:** full CODE/DATA and linked decoded EXE/MAP
equality, the original ABI and complete *logical* FIXUPP equality
do not prove the original complete Borland OBJ record serialization,
nor literal FIXUPP chronology for all members. After456 has its
one exact near frame gap; after457/458 have literal ordered FIXUPP
equality; after459/460/461 retain their own disclosed original-vs-TASM
literal ordering differences. Provenance remains candidate-local-attested,
not independently confirmed pristine Japanese dumps. MAINL canonical
packed-file accepted units still remain **0/250**.

Next demanding candidates to investigate using their **actual current
source membership** include cplx2 (5,598 CODE / 63 DATA; 22 publics,
24 imports), isteldbl (1,947 CODE / 14 DATA) and other unsourced
complex/iostream functions. The x87 EMUL mechanism is now established
at two different complete original members; do not infer every larger
member will necessarily share their exact build characteristics.
The unresolved h_ldiv MAP alias-order discrepancy remains open.

## 1e. Previous source-bound checkpoint — verified after448 (historical)


At this historical checkpoint, the Japanese MAINL after448 incremental
working CRT was independently reviewed against the *retained original* and
the complete after447 parent proof; no ancestor cold build was replayed.
This is **not** the frozen after439 storage-cleanup audit or formally
accepted Factory source credit.

| Japanese MAINL working CRT | Reviewed after448 |
| --- | ---: |
| Original CL.LIB member slots | **893** |
| Source-linked original CRT members | **656** |
| Remaining contextual vendor members | **237** |
| Complete original-equal source CODE | **176,605 bytes** |
| Complete source-bound native rounds | **2, EXE and MAP original-equal** |
| Original decoded EXE / ordered relocations | **67,372 bytes / 677** |
| Factory accepted-source credit for this expansion | **None established** |

This session recovered **five** additional original library members,
**1,089 CODE and 40 DATA bytes**, each with two fresh native producer
rounds, a focused reviewer/test, and its own source commit:

- after444: istctr1 / istream() default constructor, 254 CODE/20 DATA,
  actual ios subobject, two vtables, real adjusting destructor thunk,
  12 exact original logical FIXUPPs — commit c9bf380.
- after445: ostctr1 / ostream() default constructor, 245 CODE/20 DATA,
  ios + typed RTTI and adjusting thunk, 12 original logical FIXUPPs.
  The copied test-name mistake was corrected, tests rerun and latest
  commit amended to acebdfb; no producer source/receipt drift.
- after446: srbdalc / strstreambuf::doallocate, 141 CODE, real callback
  allocator versus new[] and setb registration, two original logical
  FIXUPPs — commit cac3fa1.
- after447: _strcoll / __strcoll + _LevelCollate, 265 CODE, real locale
  weight and strength state machine, all three **literal ordered**
  original FIXUPPs including the two near GetNextKeyWeight calls.
  This is a distinct provider from the short C-locale strcoll.asm —
  commit c9ed146.
- after448: cibmscrl / __IBM_SCROLL, 184 CODE, complete DBCS edge
  cleanup and text BIOS dispatch. Original CODE+140 uses **wclrnorm**,
  not the initially suspected wgarbage; six global state relocations
  are original-exact. Seven documented Borland TARGET-frame method 5
  vs TASM CODE-frame method 0 near imported calls are locked by
  their individual (site,target) pairs and independently audited in
  the review and tests — commit f465f66.

The previously completed after440–443 source family and receipts remain
in the chronological [working CRT index](MAINL_WORKING_CRT_RECOVERY_INDEX.md).
The current **source-bound root receipt** is:

    .analysis/work/mainl-after448-ibm-console-scroll-dbcs-boss-build.json
    SHA-256 828aba16372f8b63731d30f923a481d1a6f6e6b5004b4078acc1d7ccbcbb64a6

Producer: scripts/build_th03_mainl_after448_work.py,
mode ibm-console-scroll-dbcs-boss.
Independent reviewer: scripts/review_th03_mainl_after448_work.py.
Focused tests: tests.test_mainl_after448_work.
Every active parent receipt, all native TASM/TLIB/TLINK writer logs,
and **both complete raw OBJ/LIB/EXE/MAP pairs for all new stages**
must be preserved. The newest source receipt is **not** a license to
apply the frozen after439 cleanup script.

**Important limits:** complete source CODE/DATA equality and byte-exact
decoded EXE/MAP do not establish raw original Borland OBJ identity,
literal FIXUPP equality for every member, original Japanese dump
provenance beyond candidate-local-attested, or new Factory acceptance.
In particular after448 has exactly seven independently proven OMF
near-frame gaps. Its reviewer checks this controlled exception instead
of silently claiming full original relocation fields.

## 2. Separate acceptance/ledger status

- The MAINL canonical packed-file ledger is currently **0/250** eligible
  nonexcluded exact units (251 rows including one excluded). `status.py`
  reports the decoded MAINL product **pending**, with **no new accepted
  source credit** for the CRT source-expansion chain.
- Historical notes claiming **211 decoded MAINL extents / 288 procedures /
  36,946 bytes** of accepted source are **not current acceptance**. The
  current maintained far-heap source/recipe/unchanged-cold-context guard
  is not passing. Re-attest that scope independently before reinstating
  decoded acceptance; do not delete the underlying source work.
- MAIN's 106 file-backed units/459 ledger functions, OP's 60 decoded
  accepted extents (14,985 bytes) and ZUN's 77 decoded extents are **other
  acceptance scopes**; do not add them into a made-up whole-game percent.
  Consult [generated progress](PROGRESS.md) and `scripts/status.py`.

## 3. Handoff work — practical sequence

Run **scoped checks** from the repository root; the Python 3.12 historical
modules may require loading `setuptools` and a higher recursion limit,
which current review/test entrypoints already handle.

```sh
git status -sb
git log -5 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after479_work.py far-overlap-safe-memmove-leaf
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after479_work -v
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_cplx2_acos_partial_native -v
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_large_x87_location_frames -v
# Historical storage test deliberately fails closed with after440+ layers;
# do not treat tests.test_mainl_after439_storage_cleanup as a current gate.
.venv/bin/python scripts/status.py
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
```

For each **new** original CRT member: verify its active unsourced membership
with `parent.retained()` and `carry[0][0]` before coding. Missing `.asm`
**does not prove** unsourced: e.g. `cneccrsr` is already source-linked.
Inspect the live original OMF (complete CODE, initialized DATA, BSS,
publics, imports, SEGDEF/GROUP and every relocation), not just the
installed vendor library: `setblock` has a known active-target versus
installed-`CL.LIB` GROUP provenance difference. Check original *logical*
**and** *literal ordered* FIXUPPs independently. Use natural 8086 ASM/C/C++
with genuine symbols and 16-bit ABI. In complex C++ constructors/destructors,
**zero-valued unlinked OMF words may be real symbolic RTTI/vtable pointers**:
`filebuf`'s destructor also exports `@filebuf@openprot` at DATA+0. Never
replace these with unexplained numeric words merely to match bytes.

Reuse the unchanged inherited source-bound native receipt rather than
replaying the entire cold chain. Build only the affected scope in **two
fresh native rounds**, preserve both complete OBJ/LIB/EXE/MAP outputs and
writer logs, run its matching reviewer/tests and then commit. Do not
mistake a local commit, TASM exit or linked EXE equality for formal
Factory acceptance.

**Current unowned directions** include the large cplx2 and isteldbl
modules named above. Earlier handoff hypotheses that bcd1 and cplx1
could not generate Borland-style floating FIXUPPs are now disproved
by original-equal after460/after461 native source, with the precise
TASM EMUL directive and original x87 data widths. Recheck the real
source carrier before claiming any remaining member.

The unresolved `h_ldiv` source has **174 original-equal CODE bytes** but
TASM/Borland MAP alias order differs: it is **not counted** in the frozen after439 647-member snapshot. See [the h_ldiv investigation](MAINL_H_LDIV_SCOPED_CODE_ONLY_REVIEW.md).
Other narrow OMF differences are recorded in [OMF gaps](MAINL_OMF_GAPS.md).

All older per-member reviews and chronological milestone links are in
[the historical MAINL working CRT recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md),
**not** the current acceptance ledger. Do not repeat completed source
members just because a previous candidate list named them.

## 4. Storage policy: no further deletion with newer layers

The [after439 storage audit](STORAGE_HANDOFF_CURRENT.md) is the **last
fully applied cleanup audit**, not a deletion permission for later source
stages. Its frozen DAG has **177 stages, 4,464 uniquely protected
receipt/log/OBJ/LIB/EXE/MAP paths** (approximately
275.62 MiB allocated). Preserve them, the pinned original Japanese
targets, Wine/Borland tools, `.venv`, Ghidra/JDK provenance, runtime/cold
inputs, old-named `reference.tar`, source, ledgers and the `h_ldiv`
investigation. A generic `clean_generated.py --apply` or receipt-prune
preview is **not** a dependency oracle and must not be blanket-applied.

The pinned `scripts/cleanup_mainl_after439_handoff.py` was dry-run by
default and now **fails closed** because after440+ source layers exist. This
is correct protection, not a bug or invitation to weaken the guard. A 2026-11-05 audit removed only **15 completed superseded
alternative-mode files** (1.54 MiB allocated) and regenerable Python
caches; it kept the alternate's JSON metadata, all live proofs and all
unresolved investigations. The exact removed-path manifest is at
`.analysis/work/handoff-after439-retired-20261105.txt`. There were **zero remaining eligible files at the after439 checkout**.
The current checkout has newer source stages, so the after439 command
now refuses any pruning; do not use old after388/319 tools either. The former 511-source rules are archived at
[after388 storage policy](STORAGE_HANDOFF_AFTER388.md).

```sh
python3 scripts/cleanup_mainl_after439_handoff.py  # now FAILS CLOSED with newer layers; do not --apply
.venv/bin/python scripts/clean_generated.py --caches-only --apply
# Never: .venv/bin/python scripts/clean_generated.py --apply
```

Before handing off, confirm `git diff --check`, latest scoped review and
`git status -sb`. Do not push local commits without explicit instruction.

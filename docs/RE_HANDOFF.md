# TH03 — agent handoff (2026-11-06; after507 working source)

**Snapshot warning:** after439 is the last **fully storage-audited and
cleaned** source checkpoint, but the current locally reviewed working-source
checkpoint is **after507** (section 1a). Do **not** infer a clean
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

## 1a. Current working-source checkpoint — independently verified after507

**Latest complete Japanese MAINL CRT source-bound checkpoint is after507**.
It is newer than the frozen after439 storage-cleanup snapshot.
Continue every existing dirty change; never reset incomplete source,
original vendor objects, writer logs or native output receipts.
No full cold replay, push or cleanup was performed.

| Japanese MAINL CRT working source | Verified after507 |
| --- | ---: |
| Original Japanese Borland CL.LIB member slots | **893** |
| Complete original source-linked CRT members | **715** |
| Remaining contextual original vendor members | **178** |
| Complete original-equal maintained-source CODE | **187,296 bytes** |
| Newly complete source CODE since after500 | **862 bytes** |
| Japanese decoded EXE / ordered MZ relocations | **67,372 bytes / 677** |
| New native TASM/TLIB/TLINK rounds per stage | **2, both EXE/MAP exact** |
| Formal Factory accepted-source credit for expansion | **None established** |

**Seven newly complete original CRT source members since after500**
are separately committed, tested, and independently reviewed:

- after501 stdtr (slot 877): **141 CODE + 30 DATA + 4 BSS**,
  complete ios destructor, RTTI, destructor vtable, and actual
  DATA/BSS-exported format/state symbols, seven logical OMF
  references — commit **5b19847**.
- after502 reada (slot 103): **78 CODE**, true DOS read and
  both original FAR interfaces, two exact literal ordered
  FIXUPPs — commit **c73f18d**.
- after503 istdget (slot 755): **158 CODE**, true virtual
  streambuf underflow, FIFO cursor and ios EOF-state handling,
  one literal original FAR FIXUPP — commit **e54127c**.
- after504 ostptr (slot 819): **135 CODE**, ostream FAR pointer
  formatting, actual ios flags and ulong insertion,
  seven original logical OMF references — commit **514229a**.
- after505 stpword (slot 881): **97 CODE + 4 DATA**, true ios
  pword FAR user-array slot with usersize expansion,
  four original logical OMF references — commit **5d86ef5**.
- after506 creat (slot 210): **156 CODE**, true DOS AH=3Ch
  create, umask/flags and installable exitopen FAR close callback,
  nine original literal ordered OMF references — commit **62aff3a**.
- after507 stiword (slot 880): **97 CODE + 4 DATA**, real ios
  iword FAR user-array slot and usersize expansion,
  four original logical OMF references — commits **f0250e0**
  and **ff562cc** (same member, count once).

**Current complete source-bound root receipt:**

    .analysis/work/mainl-after507-ios-iword-usersize-array-slot-boss-build.json
    SHA-256 168745267844a78be646340eeea6d19f152b7c59690a3bf211ac572329e15b18

Producer: scripts/build_th03_mainl_after507_work.py
(mode ios-iword-usersize-array-slot-boss).
Independent reviewer: scripts/review_th03_mainl_after507_work.py.
Focused tests: tests.test_mainl_after507_work.
Every after500→after507 parent receipt hash, source/driver hash,
seven per-stage writer-log hashes and **both full raw native
OBJ/LIB/EXE/MAP vectors in each of seven stages** were
independently verified. All latest Japanese EXE and MAP bytes
are original-equal, preserving all 677 ordered DOS MZ relocations.
Protect the complete receipt dependency DAG and inherited
TASM/TLIB/TLINK outputs; the old after439 cleanup is fail-closed.

**Giant original complex math boss advanced significantly, but
remains partial.** Original cplx2 has **5,598 CODE bytes and 22
FAR public math/stream functions**. Its natural 8086/x87 source now
implements **sixteen complete FAR bodies** through original
CODE+3973 (**3,974 original bytes**). Five full math bodies were
recovered since after500: log10, three distinct pow overloads,
and now sin(complex). The latest work here has three
important independently verified steps:

- **pow(double,complex)**, CODE+3226..3531 (306 bytes), with
  real negative-base handling and typed double pi; commits
  1976670 and 615ad80 (both on the same scoped advancement).
- **pow(complex,complex)**, CODE+3532..3740 (209 bytes),
  with genuine log/mul/exp and special zero-base paths;
  commit 4e159d8.
- **sin(complex)**, CODE+3741..3973 (233 bytes), a genuine
  80-bit FPU complex sine with original _cos then _sin import
  order and typed double -0.5 at DATA+44..51;
  commit 6a0db67.

The native TASM checker
scripts/probe_th03_cplx2_sin_partial.py rebuilds two rounds.
It attests **3,972 emitted CODE bytes** against the 3,974-byte
original prefix; the only two encoded length gaps are the
historical direct FAR calls in acos at original CODE+799/+984,
each emitted one byte shorter as PUSH CS + NEAR CALL.
All other **3,964 aligned CODE bytes**, every implemented
FAR public entrypoint, and all **36 original initialized
DATA bytes** at DATA+16..51 match. The sixteenth public
symbol required repeated PUBLIC declarations at the beginning
of the CODE section and by its real PROC; no machine bytes were
patched. Of **614 original prefix OMF FIXUPPs**, all **612
emitted native symbolic fields** match locations after the two
known shifts, symbol names, types, widths and addends. **530
original Borland frame-method-4 FPU fields** compile with
TASM method 5. These and the two same-CODE FAR calls remain
explicit differences, not complete original OMF equality.
See [sixteen-function partial proof](MAINL_CPLX2_SIN_SIXTEEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
and tests.test_cplx2_sin_partial_native.
Another **1,624 CODE bytes and six public routines**, full
DATA/INITDATA and original method-4 framing remain unfinished.
**cplx2 adds zero complete CRT members and zero formal Factory
accepted units** until the entire member is reproduced and linked.

**Another genuine large arithmetic core remains unaccepted:
h_ldiv (slot 67).** Commit **25ebb39** recovered all 174
original CODE bytes, 12 actual signed/unsigned DIV/MOD
near/FAR aliases and all original zero FIXUPPs.
A real linked 67,372-byte Japanese EXE and all 677
relocations match exactly. However the MAP differs
only in two reversed alias pairs at lines 1321/1322
and 1330/1331. Borland and TASM differ in same-address
PUBLIC order, and four source declaration-order probes
did not restore it. The scoped original code and
[MAP alias proof](MAINL_H_LDIV_TWELVE_API_MAP_ALIAS_PROBE.md)
are committed but the complete CRT member earns **zero
source-linked credit** until MAP parity is attained.
Do not patch the MAP or call this a fully accepted member.

**Proof/acceptance boundaries:** exact decoded EXE/MAP plus
complete reviewed source CODE/DATA and logical OMF fields
do not establish raw original Borland OBJ chronology for
every member. Pinned original Japanese targets are
candidate-local-attested rather than independently proven
pristine. MAINL canonical packed-file accepted ledger
remains **0/250**, and the whole-game reconstruction
percentage is unknown. No full cold replay was run.

## 1b. Previous working-source checkpoint — after500 (historical)



**Historical after500 complete CRT checkpoint, superseded by after507,
not the historical after497 or frozen after439 storage cleanup.**
All original Japanese objects, native receipts, raw build rounds and
writer logs are protected. Work on all existing dirty source rather
than discarding it; do not blanket-apply the old after439 cleanup,
repeat full cold replay or claim Factory acceptance from local links.

| Japanese MAINL CRT working source | Verified after500 |
| --- | ---: |
| Original Japanese Borland CL.LIB slots | **893** |
| Complete source-linked original CRT members | **708** |
| Contextual vendor members still retained | **185** |
| Original-equal source-built complete CODE | **186,434 bytes** |
| This session added CODE / BSS / INITDATA | **439 / 6 / 6 bytes** |
| Original decoded EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Fresh TASM/TLIB/TLINK rounds in every new stage | **2, both EXE/MAP byte-exact** |
| Formal Factory source acceptance for this expansion | **Not established** |

**Three new complete original CRT source members** were recovered,
each with distinct natural 8086 source, original OMF evidence,
two genuine TASM/TLIB/TLINK output rounds, a focused review and tests:

- after498 / creata (slot 211): **170 CODE**, complete private
  DOS 21h file creation core and four true FAR public APIs:
  __rtl_creat, __creat, _creattemp and _creatnew. All four
  **literal ordered original FIXUPPs** match — commit 21025fc.
- after499 / stusize (slot 889): **156 CODE**, full C++
  ios::usersize FAR allocation, old array copy and deletion,
  and zero-initialization of new user slots. All three logical
  FAR allocator/memcpy/free relocations match, though literal
  FIXUPP packet order differs — commit 666245e.
- after500 / clock0 (slot 11): **113 CODE, 6 BSS and 6 INITDATA**.
  Real clock() and private startup time-baseline initialization,
  actual __ftime and 32-bit N_LXMUL@. All ten logical original
  fixups match apart from the site-locked Borland target-frame
  versus TASM CODE-frame near-call difference at CODE+40.
  INITDATA+2 is a real symbolic CODE+68 pointer — commit 920a17b.

**Historical after500 source-bound root receipt:**

    .analysis/work/mainl-after500-dos-clock-baseline-initdata-leaf-build.json
    SHA-256 1ad0b29998e918995ee4c11de18df2ce83f76ad01f0649a337eaf7f4cd70b61e

Producer: scripts/build_th03_mainl_after500_work.py
(mode dos-clock-baseline-initdata-leaf).
Independent reviewer: scripts/review_th03_mainl_after500_work.py.
Focused tests: tests.test_mainl_after500_work.
The complete after497→after500 parent-receipt chain, source
and driver hashes, all seven execution logs per stage and
both full raw OBJ/LIB/EXE/MAP output vectors for every new
stage were independently checked. Both latest Japanese
decoded MAINL EXEs and MAPs equal the original target bytes,
including all 677 MZ relocation entries. The parent and
all historical evidence must remain intact.

**Giant cplx2 math boss: real progress but NOT a complete member.**
Natural x87 source now recovers **eleven complete FAR math
functions** spanning original CODE+0..2707 (**2,708 bytes**).
Three new entire bodies this session:

- cosh(complex), **234** original-equal CODE bytes at
  +2124..2357 — commit 6feff14.
- exp(complex), **206** original-equal CODE bytes at
  +2358..2563 — commit dffae56.
- log(complex), **144** original-equal CODE bytes at
  +2564..2707 — commit e90861d.

The scoped native checker
scripts/probe_th03_cplx2_log_partial.py builds two real
TASM rounds under the writer lock. Of **419 original
prefix OMF FIXUPPs**, **417 emitted native relocation
fields** match the original sites (accounting for the
two previous one-byte shifts), symbolic targets, kinds,
widths and addends. The same two original acos direct
FAR calls at CODE+799/+984 remain encoded one byte
shorter by TASM as PUSH CS plus NEAR CALL, giving a
2,706-byte native prefix and **2,698 exact aligned
source bytes outside those two calls**. **364 original
Borland location-frame method-4 FPU fixups** compile as
TASM method 5, with that difference explicitly preserved
instead of wrongly claiming full OMF record equivalence.
The original remaining **2,890 CODE bytes**, eleven public
functions, full DATA/INITDATA and exact frame handling
are still unfinished. See
[eleven-function report](MAINL_CPLX2_LOG_ELEVEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
and tests.test_cplx2_log_partial_native.

**Proof/acceptance boundaries:** cplx2 is **not** counted as
another source-linked complete CRT member and the scoped
native TASM result is not a full MAINL link. Exact decoded
EXE/MAP and reviewed original CODE/logical OMF do not
imply identical original Borland OBJ record serialization.
Pinned original files have candidate-local-attested, not
independently pristine-dump, provenance. MAINL canonical
packed-file accepted units remain **0/250** and no
whole-game percentage is asserted. No full cold replay,
Git push, reset or cleanup was performed.

## 1c. Previous working-source checkpoint — after497 (historical)



**Historical after497 source-bound CRT checkpoint, superseded
by the current after500. It superseded the earlier after495 layer.**
Do not delete any native original member, stage receipt, writer log or
raw OBJ/LIB/EXE/MAP output. All source work and explicit dirty
changes should be continued, not reset. No full cold replay was run.

| Japanese MAINL CRT working source | Verified after497 |
| --- | ---: |
| Original Japanese Borland CL.LIB members | **893** |
| Complete source-linked original CRT members | **705** |
| Remaining contextual original vendor members | **188** |
| Complete original-equal maintained-source CODE | **185,995 bytes** |
| New native DATA / BSS (after496–497) | **3 / 9 bytes** |
| Decoded original Japanese EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Fresh TASM/TLIB/TLINK rounds per new stage | **2, both EXE/MAP byte-exact** |
| Formal Factory accepted-source credit for this work | **None established** |

**Two new complete source-built CRT members** since after495:

- after496 / lock (slot **245**): **78 CODE**, complete FAR
  _lock and _unlock with real DOS INT 21h AX=5C00h / 5C01h,
  two precisely original-equal literal ordered near IOERROR
  FIXUPPs and true register argument ABI; commit **931066a**.
- after497 / getpass (slot **354**): **168 CODE, 3 DATA, 9 BSS**;
  real DOS no-echo input, prompt through the native stderr stream,
  private DOS console flush, eight-character limit and CR/LF
  output. All nine logical OMF sites/targets match, while native
  FIXUPP packet order differs; commit **d4a8b03**.

Their two-round source-bound native build outputs, focused
reviewers and unit tests are retained and passing. The complete
after489→after497 parent receipt hash chain, source and driver
hashes, seven native phase logs per stage, and both full
OBJ/LIB/EXE/MAP output vectors of all eight stages were
independently checked. Both latest EXE and MAP files match
the Japanese targets, including all 677 ordered MZ relocations.

**Current complete source-bound root receipt:**

    .analysis/work/mainl-after497-dos-getpass-noecho-bss-boss-build.json
    SHA-256 eb368bf22d6798d2d5ecaf16acb0d2453b0f353aa09d1fa5b001ab94e1170d2f

Latest native producer: scripts/build_th03_mainl_after497_work.py
(mode dos-getpass-noecho-bss-boss).
Focused reviewer: scripts/review_th03_mainl_after497_work.py.
Tests: tests.test_mainl_after497_work.

**Large Boss progress — cplx2 is still NOT complete.**
The genuine cplx2 math member has **5,598 CODE bytes and 22 FAR
public bodies**. Two more complete functions are now maintained
as independently compiled source:

- **atan(complex)**, original CODE+1608..1890, 283 byte-identical
  original instructions with real FPU math, FAR math calls,
  native result allocation; commit **af30461**.
- **cos(complex)**, original CODE+1891..2123, 233 byte-identical
  original instructions using real exp/sin/cos, original 80-bit
  intermediates and conditional FAR result allocation;
  commit **3cb3e1a**.

The scoped after-cos source now covers **eight complete FAR
function bodies, original CODE+0..2123 (2,124 original
bytes)**. Native TASM emits **2,122 bytes** because the same
two historical acos local direct FAR calls at original
CODE+799/+984 compile one byte shorter each (PUSH CS plus
NEAR CALL). All other **2,114 aligned native CODE bytes**
are original-equal. Of **337 original prefix FIXUPPs**, all
**335 emitted native references** match original sites
(after the two shifts), symbol targets and addends.
**295 original Borland frame-method-4 FPU references** compile
as method 5 in TASM, still explicitly disclosed, not erased.
Two missing original CODE-local FAR call fixups remain.
The independent [eighth-function evidence](MAINL_CPLX2_COS_EIGHT_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
and tests.test_cplx2_cos_partial_native reproduce this in
two native TASM-only rounds. The remaining **3,474 CODE bytes**
and **14 other FAR public bodies**, plus full original DATA/
INITDATA and exact original OMF framing, are still unfinished.
**cplx2 contributes zero complete CRT source-linked or formal
Factory accepted units.** Do not misuse its partial native OBJ
to claim an original-equal full MAINL linked product.

**Evidence and safety limits:** complete native CODE/DATA and
decoded EXE/MAP equality do not establish literal vendor OBJ
identity for every module. The original Japanese objects are
candidate-local-attested rather than independently proven
pristine dumps. No target executable binary patches, cold
replay, blanket cleanup, or Git push occurred. MAINL's
canonical packed-file accepted ledger remains **0/250**;
whole-game reconstruction percentage remains unknown.

## 1d. Previous working-source checkpoint — after495 (historical)

**Historical after495 MAINL CRT working-source checkpoint; superseded by
after497 and distinct from the frozen after439 storage audit.**
The original pinned CL.LIB and all accumulated native receipts,
raw OBJ/LIB/EXE/MAP, tool logs, source hashes, and link evidence
remain protected; the old after439 cleanup stays fail-closed.
No full cold replay or new formal Factory source acceptance was run.

| Japanese MAINL CRT working source | Verified after495 |
| --- | ---: |
| Original Japanese Borland CL.LIB members | **893** |
| Complete maintained-source CRT members | **703** |
| Original contextual vendor members remaining | **190** |
| Original-equal complete source-built CODE | **185,749 bytes** |
| This session newly built DATA / BSS / INITDATA | **25 / 13 / 6 bytes** |
| Original decoded Japanese EXE / ordered DOS MZ relocations | **67,372 bytes / 677** |
| Fresh native TASM/TLIB/TLINK rounds per latest stage | **2, both EXE/MAP byte-exact** |
| New formal Factory accepted-source credit | **None established** |

**Six complete new CRT members** added 914 original-equal CODE bytes
with **25 initialized DATA, 13 uninitialized BSS, and 6 CRT INITDATA
bytes**. Each member was independently compared with actual Japanese
Borland CL.LIB, passed its own new two-round source-bound
TASM/TLIB/TLINK producer with full original EXE/MAP equality,
and has a focused source, reviewer, unit tests, and its own
gpt-web commit:

- after490 cibmcolr (CL.LIB 522): **160 CODE** over six real IBM
  textcolor/textbackground/textattr/highvideo/lowvideo/normvideo
  FAR entrypoints. All 11 true __video+4/+6/+13 symbolic OMF
  references agree — commit 6954d6d.
- after491 stime (121): **170 CODE**; complete DOS _stime and _time
  FAR APIs, original date/time setters and rollover-safe
  date/time/date retry, all seven real DOS/Unix conversion
  fixups — commit f76d7f6.
- after492 mkname (89): **188 CODE, 9 DATA, 13 BSS**; complete
  native TMPNAM/MKNAME generation, TMP and .$$$ strings, persistent
  BSS pathname buffer, counter update and DOS file-attribute
  collision retry. Only CODE+64 __UTOA has the original
  TARGET-vs-CODE near-call frame difference — 6163585.
- after493 setupio (116): **164 CODE, 6 INITDATA**, authentic
  Borland FILE initialization and console buffering lifecycle,
  all **18 original literal ordered FIXUPPs**, including symbolic
  INITDATA+2 -> CODE+0. Strict original OMF analysis corrected
  six initially mistaken __openfd references to the actual
  __streams targets — 0e0527c.
- after494 exit (42): **170 CODE, 12 DATA**, four actual FAR
  process-exit APIs, at-exit LIFO, cleanup/restore/terminate
  paths, three typed mutable far callback pointers and 14
  original logical OMF references. The original DATA FIXUPP
  chronology 8,4,0 was reconstructed with symbolic descending
  ORG declarations. This specifically corrected the native
  EXE's two swapped MZ relocation-table entries and restored
  the complete original EXE/MAP without patching either —
  commit 0b95a8a.
- after495 rand (102): **62 CODE, 4 DATA**, true srand/rand
  32-bit Borland LCG with native N_LXMUL@, original 015A4E35h
  multiplier, addend one, and high-15-bit output. The single
  CODE+38 near TARGET-vs-CODE frame difference is site-bound —
  source commit 34dd85f. Supplemental commit f072d29 only
  adds tests/documentation for the same member and **does not**
  increase member or CODE counts.

**Latest protected complete source-bound root receipt:**

    .analysis/work/mainl-after495-original-srand-rand-lcg-leaf-build.json
    SHA-256 5153d201c7027cd448ebfd3dacd29065e67dbfb78ec4ca0c8e4289b4b5f4be71

Latest producer: scripts/build_th03_mainl_after495_work.py,
mode original-srand-rand-lcg-leaf. Focused independent reviewer:
scripts/review_th03_mainl_after495_work.py; targeted tests:
tests.test_mainl_after495_work.
The complete after489→after495 parent receipt sequence,
all six new source/driver hashes and seven writer-log
phases per stage, and every byte and SHA of **both full
OBJ/LIB/EXE/MAP native output vectors per stage** were
verified together. Both newest decoded Japanese MAINL
EXEs and MAPs agree byte-for-byte with original target.
Never treat the protected evidence DAG as cleanup candidates.

**Actual large cplx2 boss progress — partial, not source-linked:**
Commit da2b4a4 extends maintained natural x87 8086 code to
**six complete original FAR functions**: three division
operators, acos, arg, and now the full **391-byte
asin(complex)** at original CODE+1217..1607.
This covers the first **1,608 original CODE bytes** of
the **5,598-byte, 22-public** library member. The native
TASM six-function source is 1,606 CODE bytes because the
two previously documented acos same-CODE FAR calls
at original +799 and +984 compile one byte shorter.
The scoped two-round verifier confirms all other CODE
bytes original-equal and checks all 246 emitted OMF
locations/widths/symbolic targets/addends among the 248
original prefix FIXUPPs. Exactly 218 original Borland
location-frame method-4 FPU fixups appear as TASM method 5.
Critically, the first CODE-equal asin source still called
_cos before _sin; its original **EXTDEF/FIXUPP targets**
proved the genuine original asin calls _sin then _cos
at CODE+1388 and +1424. The source was corrected and
reverified before committing. See
[the six-function large-Boss partial review](MAINL_CPLX2_ASIN_SIX_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
and tests.test_cplx2_asin_partial_native.
**The remaining 3,990 CODE bytes, 16 other FAR functions,
full DATA/INITDATA and literal frame-4 OMF semantics remain
unrecovered. This cplx2 partial work adds zero complete CRT
source members, no full MAINL link proof and zero Factory credit.**

**Limits:** Complete decoded EXE/MAP plus original-equal CODE/DATA,
publics/imports and logical OMF sites do not imply full raw
Borland OBJ record identity. exit's original DATA
FIXUPP chronology is matched, but its raw Borland LEDATA
serialization differs from TASM; original literal FIXUPP
chronology in other members may differ. The near-call frame
exceptions in mkname/rand are narrowly site-locked.
Pinned Japanese targets remain candidate-local-attested,
not independently pristine-dump verified. MAINL canonical
packed-file acceptance remains **0/250**, with no supported
whole-game source percentage.

## 1e. Previous working-source checkpoint — after489 (historical)



**Historical after489 complete Japanese MAINL CRT working-source checkpoint, superseded by after495.** The last fully storage-audited/cleaned checkpoint is
still the frozen after439. All newer receipts, original objects,
writer logs and native rounds are protected evidence dependencies,
NOT cleanup candidates. No cold replay, push or formal Factory
source acceptance occurred during this source expansion.

| Japanese MAINL CRT | Reviewed after489 |
| --- | ---: |
| Original Borland CL.LIB members | **893** |
| Source-built complete original CRT members | **697** |
| Contextual original vendor members still retained | **196** |
| Complete original-equal maintained-source CODE | **184,835 bytes** |
| This session added initialized DATA | **12 bytes** |
| Original decoded Japanese EXE / ordered DOS MZ relocations | **67,372 bytes / 677** |
| Native full TASM/TLIB/TLINK rounds on latest stage | **2, both EXE/MAP byte-exact** |
| Factory accepted source credit for this expansion | **Not established** |

**Five new complete original CRT members** were recovered this
session, with **750 original-equal CODE and 12 initialized DATA
bytes**, in five independent native-source commits. Each received
a focused original CL.LIB segment, code, public/import and
OMF analysis, two fresh TASM/TLIB/TLINK native rounds with
complete OBJ/LIB/EXE/MAP files and writer logs, a separately
bound receipt, independent reviewer and passing unit tests:

- after485 / stctr1 (CL.LIB 875): **135 CODE + 12 DATA**,
  genuine default ios() FAR constructor, 40-byte object,
  54-byte typed RTTI at CODE+81, native destructor vtable
  and all six logical OMF references. Original default
  constructor **does not call ios::init**, unlike its separately
  verified streambuf overload — commit 41b10fe.
- after486 / ltoa1 (253): **124 CODE**, full _itoa, _ultoa
  and _ltoa FAR radix formatting interfaces, actual
  __LONGTOA backend. Three precisely site/target-locked
  Borland method-5 versus TASM method-0 imported near
  frames at CODE+41/+74/+118 — commit a3fdf92.
- after487 / contain (397): **200 CODE**, entire
  string::contains exception-aware C++ routine, original
  CODE+0..31 exception scope, CODE+142 typed string RTTI,
  true FAR temporary constructor, find and destructor,
  and all 11 logical original OMF fields — commit aed5fd5.
- after488 / intdos (176): **146 CODE**, both complete
  FAR _intdos/_intdosx with real DOS INT 21h, original
  DS/ES and FLAGS register images, and **both literal
  ordered original FIXUPPs** — commit 5040f53.
- after489 / hbsearch (465): **145 CODE**, complete
  FAR heap binary search using native N_LXMUL@,
  N_PADD@, real FAR comparator and signed branch
  semantics. Original near TARGET-frame method 5 vs
  TASM CODE-frame method 0 at exact CODE+41/+54/+111
  is explicitly audited — commit d39f2ea.

**Historical after489 complete source-bound root receipt:**

    .analysis/work/mainl-after489-far-heap-binary-search-boss-build.json
    SHA-256 ff00ce2ad88841c359d31c4c9be51b221c634740ed2df6aebd26c229f4826b36

Latest producer: scripts/build_th03_mainl_after489_work.py
(mode far-heap-binary-search-boss).
Independent reviewer: scripts/review_th03_mainl_after489_work.py.
Focused tests: tests.test_mainl_after489_work.
The complete after484→after489 parent-receipt chain,
source and driver hashes, all seven per-stage log phases,
and **both complete raw native OBJ/LIB/EXE/MAP vectors**
for every new stage were verified together. Both latest
decoded MAINL EXEs and MAPs equal their original target
files. The pinned Borland vendor programs are protected
context, not discardable source material. Do not run the
historical after439 cleanup against these new stages.

**Giant original complex math boss actually advanced, but is
still only partial source.** Commit 4c17fe6 extends native
cplx2 reconstruction to **five complete FAR function bodies**
(three division operators, acos and now arg), covering
the original CODE+0..1216 (**1,217 original CODE bytes**).
The new arg(complex) body at CODE+1079..1216 contributes
**138 entirely byte-equal original instructions** including
true x87 compares and the FAR atan2 call. A separate
two-round native TASM checker confirms all code bytes
outside the same two pre-existing local FAR-call shortenings
at original CODE+799 and +984. Among 184 original prefix
fixups, 182 native references match original sites,
symbolic targets, addends and location widths after the
two known call shifts. Exactly **163 original frame-method-4
FPU fixups** compile as method 5 and are explicitly disclosed,
not misreported as original raw OMF equality.
See [scoped five-function report](MAINL_CPLX2_ARG_FIVE_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md).
The rest of the **5,598-byte, 22-public** member remains
unowned and contributes **zero** complete CRT members and
no Factory credit. The native partial ASM output is not
a complete re-linked MAINL program.

**Evidence limits:** original source-built CODE/DATA,
logical relocation and decoded EXE/MAP equality do not
prove literal original Borland OBJ record equality for
all members. The 3+3 imported near-frame differences in
ltoa1/hbsearch remain site-bound, while intdos's two
FIXUPPs are literal-equal. cplx2 original method-4 and
intra-segment FAR-call encoding issues remain unresolved.
Pinned Japanese target provenance remains candidate-local-
attested, not independently pristine-dump verified.
MAINL's canonical packed-file accepted ledger remains
**0/250** with no whole-game percentage inferred.

## 1f. Previous working-source checkpoint — after479 (historical)



**Historical after479 CRT working-source checkpoint, superseded by after489.** The new native producer
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

## 1g. Previous working-source checkpoint — after474 (historical)



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

## 1h. Previous working-source checkpoint — after468 (historical)



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

## 1i. Previous working-source checkpoint — after461 (historical)



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

## 1j. Previous source-bound checkpoint — verified after448 (historical)


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
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after507_work.py ios-iword-usersize-array-slot-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after507_work -v
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_cplx2_sin_partial_native -v
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_h_ldiv_scoped_native -v
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_cplx2_asin_partial_native -v
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_cplx2_arg_partial_native -v
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

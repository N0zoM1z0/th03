# TH03 — agent handoff (2026-11-05; after455 working source)

**Snapshot warning:** after439 is the last **fully storage-audited and
cleaned** source checkpoint, but the current locally reviewed working-source
checkpoint is **after455** (section 1a). Do **not** infer a clean
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

## 1a. Current source-bound checkpoint — verified after455

This is the current Japanese MAINL **working-source** CRT checkpoint, not
a renewed storage cleanup or a new canonical/Factory source acceptance.
Its after455 receipt inherits and checks the entire preceding source-bound
DAG through after454; **no full cold replay** was performed.

| Japanese MAINL working CRT | Verified after455 |
| --- | ---: |
| Original CL.LIB members | **893** |
| Complete source-linked original CRT members | **663** |
| Remaining contextual vendor members | **230** |
| Complete source-built original-equal CODE | **178,132 bytes** |
| Original decoded Japanese EXE / MZ relocations | **67,372 bytes / 677** |
| Fresh TASM/TLIB/TLINK producer rounds at latest stage | **2; both EXE/MAP byte-exact** |
| New Factory accepted-source credit | **Not established** |

**This session** recovered seven further original CRT modules: **1,527
CODE and 164 initialized DATA bytes** in seven separate source commits.
All were independently compared with original Japanese Borland
CL.LIB CODE/DATA, segment layout, ordered imports/publics and logical
OMF relocation sites, not merely inferred from old handoff notes.
Each received its own two-round source-bound native producer,
reviewer, tests and commit (`gpt-web: xxx`):

- after449 `srbctr5` (index 838), 239 CODE / 52 DATA; unsigned-char
  strstreambuf far-buffer constructor, complete inherited RTTI, 11
  virtual method pointers and all 20 original logical FIXUPPs —
  `5e6b6e6`.
- after450 `srbctr6` (839), 239 CODE / 52 DATA; separate char-pointer
  constructor ABI, full RTTI/vtable and 20 original logical FIXUPPs,
  original source independently compared before adopting the sibling
  implementation — `912fab7`.
- after451 `sdbdtr` (826), 224 CODE / 52 DATA; complete stdiobuf FAR
  virtual destructor, actual indirect overflow(-1) dispatch, streambuf
  teardown and optional far delete, 19 logical FIXUPPs — `7700090`.
- after452 `fsbsbuf` (714), 191 CODE; complete filebuf::setbuf with
  original active-file guard, threshold range choice and real
  setb/setp/setg far callbacks, all three logical FIXUPPs — `74015ce`.
- after453 `fsbclose` (707), 174 CODE; complete filebuf::close with
  virtual flush, actual DOS close, state reset and both native result
  paths. Its **one literal original FIXUPP** at CODE+125 is identical
  to TASM — `14c541d`.
- after454 `FMBSTOK` (689), 230 CODE / 4 DATA; MBCS far tokenizer
  with its real saved far cursor, delimiter/DBCS handling and 12
  logical OMF fixups. A strict group mismatch was fixed **in source**:
  TASM emitted DATA/BSS in reverse order until the group declaration
  was corrected to restore original `08ff02ff03` — `017e965`.
- after455 `MBSTOK` (633), 230 CODE / 4 DATA; a separately verified
  MBCS tokenizer, with its own genuine saved cursor, different helper
  imports and all 12 logical fixups. An initial generated `_TEXTA`
  builder expectation was corrected to the actual original `_TEXT`
  after independently checking both the library and vendor OBJ —
  `9b244b3`.

**Current source-bound root receipt:**

    .analysis/work/mainl-after455-multibyte-strtok-state-machine-build.json
    SHA-256 ea3cfc8ba5e1112f9fce3cce8943a4380079ecd5b92ce2770cd55220ba550163

Latest producer: scripts/build_th03_mainl_after455_work.py,
mode `multibyte-strtok-state-machine`. Reviewer:
scripts/review_th03_mainl_after455_work.py, targeted tests:
tests.test_mainl_after455_work. The stage's two native rounds retain
all original raw OBJ/LIB/EXE/MAP outputs and writer logs. **Protect the
entire inherited source-bound receipt DAG and both rounds of every stage;
never run the after439 cleanup script against these newer layers.**

**Important limits:** the built original-equal decoded EXE/MAP and
complete CODE/DATA + logical OMF fields are *not* complete literal
original Borland OBJ identity. FMBSTOK/MBSTOK's literal FIXUPP record
chronology differs, while fsbclose has original literal FIXUPP equality.
Historical `cibmscrl` still has its exact seven near-call frame
differences. The Japanese target provenance is candidate-local-attested,
not independently proven pristine-dump provenance. MAINL's canonical
packed-file accepted credit remains zero; do not report this working
CRT expansion as Factory acceptance.

## 1b. Previous source-bound checkpoint — verified after448 (historical)


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
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after455_work.py multibyte-strtok-state-machine
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after455_work -v
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

**Still-unowned candidate directions** after the new source stages
include bcd1 (398 CODE / 140 DATA, original x87 emulation FIXUPPs),
cplx1 (364 CODE, floating emulator references), and the much larger
isteldbl (1,947 CODE). These were checked against the actual current
working-source membership, not merely missing filenames. The original
bcd1 and cplx1 imports and x87 relocation sites were inspected; a
minimal experimental TASM5 .8087 / EMULATOR-directive attempt failed
with an illegal-instruction error. The correct historical Borland
emulation mechanism remains **open**; do not fake its original FPU
FIXUPPs with raw target bytes or presume prior assumptions correct.
Other unowned leaf members remain possible complementary scopes;
`fsbclose` itself is now source-linked at after453. Recheck every candidate with parent
retained source membership and the original OMF before coding.

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

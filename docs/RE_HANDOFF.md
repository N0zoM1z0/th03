# TH03 — current agent handoff (verified 2026-11-05, after439)

**Start here, not at a historical progress snapshot.** Inspect `git status -sb`
and `git log -5 --oneline` before acting. Treat **all existing dirty changes**
as work to continue; do not reset or bypass them. Work on pinned original
Japanese PC-98 targets, commit each substantial improvement as
`gpt-web: xxx`, make multiple scoped commits where useful, **do not run
routine full cold replay**, and do not push unless requested.
Read [AGENTS.md](../AGENTS.md), [the workflow](RE_WORKFLOW.md) and
[the architecture](ARCHITECTURE.md) before changing native build recipes.

## 1. Current working-source checkpoint (not formal acceptance)

| Japanese MAINL CRT evidence | Verified at after439 |
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

Latest source receipt:
`.analysis/work/mainl-after439-streambuf-base-default-constructor-boss-build.json`
(SHA-256 `dd0a1a82695b00e2a3aeaa4e93a609450b50e834e4dd80b228c2eddaef5e8788`).
Original source-bound producer: `scripts/build_th03_mainl_after439_work.py`.
Focused reviewer: `scripts/review_th03_mainl_after439_work.py` mode
`streambuf-base-default-constructor-boss`. The last source checkpoint was
committed as `86e3843`; all later documentation/storage commits do **not**
change that source evidence. Original targets have
`candidate-local-attested` provenance, **not** independently proved
pristine-dump provenance.

**Critical distinction.** Byte-exact decoded MAINL EXE/MAP and complete
logical OMF fields for working-source CRT members do **not** imply every
Borland OBJ record or literal ordered FIXUPP is identical to TASM output.
Some known ordering and near-frame differences are deliberately disclosed
in individual review files. These also do **not** establish whole-game
source ownership or Factory/canonical packed-file acceptance.

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
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after439_work.py streambuf-base-default-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after439_work tests.test_mainl_after439_storage_cleanup -v
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

**Verified still-unowned candidate directions** at the previous source
checkpoint include `stbctr2`, `stbdtr`, `stbsetb`, `fsbattch`, `srbdalc`
and `cibmscrl`; **recheck** the live source membership before claiming
any of them. Balance large C++/BIOS Bosses with substantive leaf functions.
The unresolved `h_ldiv` source has **174 original-equal CODE bytes** but
TASM/Borland MAP alias order differs: it is **not counted** in the 647
members. See [the h_ldiv investigation](MAINL_H_LDIV_SCOPED_CODE_ONLY_REVIEW.md).
Other narrow OMF differences are recorded in [OMF gaps](MAINL_OMF_GAPS.md).

All older per-member reviews and chronological milestone links are in
[the historical MAINL working CRT recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md),
**not** the current acceptance ledger. Do not repeat completed source
members just because a previous candidate list named them.

## 4. Storage policy and agent cleanup

The up-to-date [after439 storage handoff](STORAGE_HANDOFF_CURRENT.md) is the
**only** current cleanup authority. The live native DAG has **177 stages,
4,464 uniquely protected receipt/log/OBJ/LIB/EXE/MAP paths** (approximately
275.62 MiB allocated). Preserve them, the pinned original Japanese
targets, Wine/Borland tools, `.venv`, Ghidra/JDK provenance, runtime/cold
inputs, old-named `reference.tar`, source, ledgers and the `h_ldiv`
investigation. A generic `clean_generated.py --apply` or receipt-prune
preview is **not** a dependency oracle and must not be blanket-applied.

The new pinned `scripts/cleanup_mainl_after439_handoff.py` is dry-run by
default and fails closed if a later source layer or altered latest receipt
appears. A 2026-11-05 audit removed only **15 completed superseded
alternative-mode files** (1.54 MiB allocated) and regenerable Python
caches; it kept the alternate's JSON metadata, all live proofs and all
unresolved investigations. The exact removed-path manifest is at
`.analysis/work/handoff-after439-retired-20261105.txt`. The current
preview selects **0 more files**; do not use old after388/319 cleanup
scripts on this checkout. The former 511-source rules are archived at
[after388 storage policy](STORAGE_HANDOFF_AFTER388.md).

```sh
python3 scripts/cleanup_mainl_after439_handoff.py        # audited dry run; 0 candidates currently
.venv/bin/python scripts/clean_generated.py --caches-only --apply
# Never: .venv/bin/python scripts/clean_generated.py --apply
```

Before handing off, confirm `git diff --check`, latest scoped review and
`git status -sb`. Do not push local commits without explicit instruction.

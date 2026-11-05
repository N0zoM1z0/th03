# TH03 — agent handoff (verified 2026-11-05, after390)

**Start here.** Work on the actual Japanese PC-98 originals. Inspect
`git status -sb` and the last commits; continue **all** dirty edits rather
than reverting or avoiding them. The current Git `main` branch has local
commits not necessarily pushed. Do not push without authorization. Every
meaningful reconstruction advance should be committed as `gpt-web: ...`;
make several scoped commits where practical. Read
[AGENTS.md](../AGENTS.md), [workflow](RE_WORKFLOW.md), and
[architecture](ARCHITECTURE.md) before changing a product recipe.

## 1. Current original Japanese MAINL CRT checkpoint

| Property | Verified working-source evidence |
| --- | ---: |
| Original CL.LIB member slots | **893** |
| Complete members compiled from maintained source | **513** |
| Remaining unchanged contextual vendor member programs | **380** |
| Source-built, original-equal logical CRT CODE | **159,721 bytes** |
| Original decoded Japanese MAINL EXE size | **67,372 bytes** |
| Original ordered DOS MZ relocations | **677** |
| Actual native TASM/TLIB/TLINK production rounds | **2, byte-identical EXE and MAP** |
| Latest source build | `after390 / dos-critical-error-boss` |
| Formal Factory acceptance of this 513-member CRT expansion | **No** |

**Source-bound proof:**
`scripts/review_th03_mainl_after390_work.py dos-critical-error-boss`
and `tests.test_mainl_after390_work`, using
`.analysis/work/mainl-after390-dos-critical-error-boss-build.json`.
The current reviewer checks the inherited **128-stage** receipt DAG,
source/driver/parent hashes, selected original member CODE/DATA/ABI, two
complete raw native OBJ/LIB/EXE/MAP rounds and writer logs. It is **not**
a full cold replay. The 513 individual members are not claimed to have
byte-identical original Borland OBJ *record serialization*; literal
ordered FIXUPP equality is separately recorded per module.

The original targets in `config/targets.toml` have
`candidate-local-attested` provenance, **not** independently established
pristine-dump origin. MAINL.EXE is the ending program. Do not substitute
translated/patched binaries, TH04 products, stored packed images, or
artificial target-byte arrays for native source recovery.

## 2. Acceptance and ledger: distinguish the claims

- [Generated progress](PROGRESS.md) is generated from ledgers, **not** from
  the 513-source working CRT. The packed-file canonical MAINL ledger remains
  **0 exact units**. `scripts/status.py` currently reports MAINL decoded
  product **pending**, `0/250` nonexcluded ledger units and no newly accepted
  bytes. `config/units.csv` has **251 MAINL rows**, including one excluded;
  do not confuse this denominator with source-present units.
- Earlier documentation reported **211 decoded MAINL extents / 288
  procedures / 36,946 bytes** of accepted source. This is a *historical
  reviewed figure*, **not currently attested acceptance**: the live
  `mainl_product_status()` verifier currently fails at the maintained far
  heap native source/recipe/unchanged-cold-context guard. Re-establish that
  guard independently before restoring any active decoded-acceptance claim.
  Do not erase the older source work or treat this status gate as proof that
  the underlying program has changed.
- MAIN has 106 exact file-backed units and 459 exact functions, totaling
  78,737 ledger bytes. OP has 60 currently decoded-accepted extents
  (14,985 bytes), ZUN 77 decoded-accepted extents (8,635 bytes); these
  **are different scopes**, not portions of a single whole-game percentage.
- Current WORKING MAINL EXE/MAP equality, OMF site/frame fidelity,
  previously reviewed decoded scope, and Factory/packed-file acceptance
  are four different facts. The whole-game source completion percentage
  remains unknown.

## 3. Important history and outstanding technical issues

After390 adds the full 300-byte original DOS INT 24h critical-error boss
with 12-byte shared BSS, four far public APIs and 20 logical exact OMF
fixups. The original Japanese EXE/MAP are byte-exact in both source-bound
rounds. See [the INT 24h native review](MAINL_DOS_HARDERR_NATIVE_REVIEW.md).
After388 added the original default `string` constructor. After389 adds the
complete original 310-byte `_locking` DOS file-locking boss with 16 exact
logical OMF FIXUPPs, five relocation-backed jump-table entries and exact
two-round Japanese EXE/MAP; literal Borland FIXUPP record *order* still
differs. See [the _locking native review](MAINL_DOS_LOCKING_BOSS_NATIVE_REVIEW.md).

The former 200-line chronological source list has been moved to the
[MAINL working CRT recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md).
That index links the original per-member review files. Recent milestones
include `ctor3`, `substr2`, eight near/far MBCS routines, and the complete
`ctor1` default constructor. Avoid redoing them simply because an older
note recommended them. Inspect the actual member and status first.

- **`h_ldiv`** (`src/mainl/crt/h_ldiv.asm`) has original-equal **174
  CODE bytes and 12 aliases**, but TASM and Borland still order two
  same-address aliases differently in the **MAP**. It is deliberately
  **not counted** in the 513 source-linked members. See
  [its bounded investigation](MAINL_H_LDIV_SCOPED_CODE_ONLY_REVIEW.md)
  and `tests.test_mainl_h_ldiv_original_scope`. Preserve its source and
  diagnostic evidence, do not reorder a MAP to fake acceptance.
- **`doslock`** retains two original-vs-TASM near-call FIXUPP frame
  differences despite complete linked EXE/MAP equality. `setargv` has
  original-equal logical relocation fields but different raw BCC FIXUPP
  record order. See their scoped review files; don't generalize these gaps
  to every member.
- **`xxv`** has original CODE/DATA/BSS and logical relocation equality
  but different literal OMF FIXUPP chronology. **`cnectxmd`** has a
  reviewed near-call TARGET/CODE-frame distinction plus raw record-order
  differences. See [OMF gaps](MAINL_OMF_GAPS.md). Conversely `checks`
  *does* now reproduce its 89 literal ordered FIXUPPs; older attempts
  that said otherwise are superseded.
- The original full game and accepted source-to-packed reconstruction
  remain open, even when this decoded MAINL program links exactly.

Remaining useful targets include complete larger CRT C++ functions and
small near/far functions, plus product-module MAIN/OP/ZUN ownership. Choose
based on **actual** original CL.LIB/IDA/Ghidra evidence, not old guessed
candidate lists. Keep both Boss and leaf work moving.

## 4. Handoff commands (scoped; no full cold replay)

Run from the repository root using the installed `.venv` and local Wine
prefix; serialize native writers. A recent Python 3.12 toolchain requires
loading `setuptools`' compatibility shim and raising the recursion limit
inside some deep historical CLI/test entrypoints (already handled by the
latest reviewer/test).

```sh
git status -sb
git log -5 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after390_work.py dos-critical-error-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after390_work -v
.venv/bin/python scripts/status.py
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
```

For a new source replacement: check the raw original CL.LIB member,
**complete** CODE/DATA/BSS/INIT/EXIT and public/import/ABI, logical and
**literal ordered** original FIXUPPs, and both actual byte-exact decoded
Japanese EXE/MAP rounds. Commit each substantial result and update the
latest handoff counts/commands. Do not run full cold replay for an unchanged
parent; a successful Git commit or a plain assembler exit is not Oracle
acceptance.

## 5. Storage and cleanup

[Current protected native DAG / storage cleanup guide](STORAGE_HANDOFF_CURRENT.md)
explains what can be deleted and how to preview it safely. **Keep all
128 active source-bound stages**: build receipts, every phase log, and both
raw native OBJ/LIB/EXE/MAP rounds. Also keep targets, .venv, Wine/Borland
prefix, Ghidra/JDK attestations, source/ledgers, runtime images and the
old-named `reference.tar` input. At the prior after388 cleanup, 256 retired/scratch files were safely removed
(**7.04 MiB**) plus approximately **5.4 MiB** of regenerable caches, with
the same source reviewer still passing. The older
[2026-11-05 319-member audit](STORAGE_HANDOFF_2026-11-05.md) is a **historical
snapshot only**; its frozen cleanup tool intentionally refuses to run on
this newer checkout. Never run a blanket `clean_generated.py --apply` on
this active MAINL DAG. The guarded after388 cleanup script is obsolete for the newer source checkpoint;
do not apply it until its audit has been refreshed.

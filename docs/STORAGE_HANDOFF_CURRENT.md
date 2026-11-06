# TH03 current protected-storage audit — after520 (2026-11-06)

**Current source is after527.** This applied after520 audit still protects its
original evidence prefix, but its deletion guard now fails closed. Retain all
after521–after527 outputs and scratch until a fresh source-DAG/SHA-256 audit; the
historical dry-run commands below do not authorize cleanup of the new stage.

**This is the latest applied storage audit.** The older after439
177-stage/4,464-file audit remains intact as a
[historical record](STORAGE_HANDOFF_AFTER439.md);
its old guard is NOT the current cleanup tool.

## Active dependency graph: 258 stages, 5,760 protected files

The pinned [after520 audit tool](../scripts/cleanup_mainl_after520_handoff.py)
follows the live, literal source-parent chain from the sole
after520 builder back to after317 and its 55 fixed original
stages. It verifies **258 unique active source-bound stages**
and enumerates **5,760 live files** from their receipts:
all source-bound JSON receipts, writer logs, and **both**
raw OBJ/LIB/EXE/MAP rounds at each stage.

Current protected root:

`.analysis/work/mainl-after520-fstreambase-virtual-setbuf-ios-state-build.json`

SHA-256: `f32c534f42d520f2c07a3acce769857d01ef310c04c00b419b585bf650994d8e`.

Before deletion and again afterward, the audit validates
source/driver SHA-256 and every active writer log/raw output
SHA-256. It also checks the original after439 root SHA,
fails closed if the latest receipt or graph changes, and
fails closed when any after521+ native source builder
or receipt appears. New source advances require a **new
pinned active dependency audit**, not a relaxed old guard.

## Actually deleted: one completed, superseded after506 variant

The finished alternative mode
`after506 / ios-iword-usersize-array-slot-boss` had
**15 raw output/log files** outside the active parent
DAG and not cited in tracked source/documents. The real
after506 source parent is
`dos-creat-exitopen-close-callback-boss`, and
ios::iword was linked by the actual after507 stage.
The alternative's **small historical JSON receipt remains**;
its retired raw outputs cannot be inspected/replayed
without rebuilding that alternative.

Exactly **15 files** and **1,642,496 allocated bytes
(1.57 MiB)** were deleted after the pinned guard,
complete source DAG and every original raw output hash
were validated. The private manifest preserves each
deleted relative path, original SHA-256, file size and
allocated block count:

`.analysis/work/handoff-after520-retired-20261106.json`

Manifest SHA-256: `ffed6609142ed39414970fb15a35f88b467488792cff0ed61f6b705cc7425392`.

A second guarded dry-run returned **zero eligible files**.
The independent source reviewer and the new
`tests.test_mainl_after520_storage_cleanup` test
confirm the active receipt DAG remains intact, with
two byte-identical native Japanese MAINL EXE/MAP rounds,
67,372 EXE bytes and 677 ordered MZ relocations.

## Regenerable cache-only pruning (separate from native evidence)

After the active native source/hash review and the focused tests passed,
the official cache-only maintenance command was executed:

`.venv/bin/python scripts/clean_generated.py --caches-only --apply`

It removed only these three fully regenerable directories:

| Directory | Allocated before cleanup |
| --- | ---: |
| `scripts/__pycache__` | 9,024 KiB |
| `scripts/lib/__pycache__` | 480 KiB |
| `tests/__pycache__` | 924 KiB |
| **Total** | **10,428 KiB = 10.18 MiB** |

The cleanup tool reported approximately 9.3 MiB of logical
file content; the larger 10.18 MiB figure is the actual
allocated-block total reported by `du` before deletion.
The three directory trees were absent immediately afterward.
The command does **not** remove `.analysis` proof data or
the Wine/toolchain prefix. The action log is retained at:

`.analysis/work/after520-cache-cleanup-applied.txt`

**Total disk allocation reclaimed in this handoff: approximately
11.75 MiB** (1.57 MiB from audited retired native artifacts,
10.18 MiB from regenerable caches). Python bytecode will
regenerate as future tests and reviewers run, so this is
the immediate savings, not a permanent fixed disk reduction.

## Safe commands and prohibited cleanup methods

~~~sh
python3 scripts/cleanup_mainl_after520_handoff.py --list     # dry-run; 0 candidates
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after520_storage_cleanup -v
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after520_work.py fstreambase-virtual-setbuf-ios-state
.venv/bin/python scripts/clean_generated.py --caches-only # preview disposable bytecode/cache only
~~~

The **original Japanese targets, Wine/Borland toolchain,
Ghidra/JDK, original reference archives, runtime and cold
evidence, other products, accepted ledgers, and all currently
protected receipt/log/OBJ/LIB/EXE/MAP files** remain in place.
No archive compression, hardlink substitution, game-target
rewriting or unguarded native deletion is authorized.

Do **not** run blanket
`.venv/bin/python scripts/clean_generated.py --apply`,
`--prune-unreferenced-receipts`, any historical
after439/after388 cleanup with bypassed guards,
or a general file-age sweep. The other data under
`.analysis/work` is **not automatically disposable**:
there are legitimate legacy observations, h_ldiv
alias-order diagnostics, unaccepted experiments and
independent MAIN/OP/ZUN evidence.

The original after439 audit, including its own
15-file historical pruning manifest and proofs,
is [preserved here](STORAGE_HANDOFF_AFTER439.md).
For authoritative source progress and next work,
see [current handoff](RE_HANDOFF.md).

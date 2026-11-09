# TH03 current storage and evidence policy — after1024 baseline (rechecked 2026-11-09)

Use the [current source handoff](RE_HANDOFF.md) for current MAIN, OP, MAINL
and ZUN status. The after596 MAIN and after587 MAINL pairs are historical
ancestors, not current broad source acceptance. This page records what has
ACTUALLY been deleted or packed; it is not a license to age-prune native work.
The complete earlier after554 storage record is preserved as
[a historical snapshot](STORAGE_HANDOFF_ARCHIVE_AFTER554.md).

## Most recent applied safe cleanup (after1024)

The [after1024 actual cleanup audit](STORAGE_HANDOFF_AFTER1024.md)
removed **448 Python bytecode cache files**: 10,503,368 logical bytes
and **11,243,520 allocated bytes**. It then repacked Git with
--no-prune and all reflog expiry disabled. All **21,319 Git object
IDs, types and sizes**, both refs, all three reflog files and the full
fsck output were identical before and after. The .git apparent size
fell by **4,201,304 bytes** (24,424,896 to 20,223,592).

The cleanup deleted **zero .analysis proof files or native receipt
trees**. Original OBJ/LIB/EXE/MAP, targets, Wine/Borland tools, Ghidra
state, source snapshots, writer logs and both compiler rounds remain
untouched. Python caches can regenerate after later imports. The
before/after inventories and per-file cache hashes are retained under
.analysis/handoff/after1024-safe-git-cache/.

## 2026-11-09 read-only storage re-audit

The official cache-only preview was rerun:

    .venv/bin/python scripts/clean_generated.py --caches-only

It reported **0.0 MiB eligible** under the approved `scripts/` and `tests/`
cache paths. No cleanup was applied because there was nothing eligible to
remove. Other discovered bytecode caches (for example inside `.venv/` and
`src/shared/math/`) are outside this cleaner's allowlist and were left alone.

The repository occupies about **5.8 GiB**, of which `.analysis/` is about
**5.6 GiB**. The largest protected areas are `.analysis/toolchain/` (about
2.7 GiB, including the game's Wine prefix) and `.analysis/work/` (about
2.0 GiB, containing native build/proof work). The nine character BOSS proof
workspaces, both-round outputs, source-bound reports, Ghidra state, targets
and toolchain inputs remain protected. This inventory did not establish a
safe unreferenced native-output set, so no `.analysis` file or receipt tree
was deleted.

The after1024 cache-only cleanup and non-pruning Git repack therefore remain
the latest applied storage cleanup. Any future native-output retirement still
requires a fresh complete dependency audit, a one-time explicit allowlist and
post-deletion review; age and directory size are not evidence of disposability.

## Earlier applied safe cleanup (after928)

The [after928 actual cleanup audit](STORAGE_HANDOFF_AFTER928.md)
records **24,928,256 gross allocated bytes (~23.77 MiB)** reclaimed:
**24,117,248 bytes** by an audited **non-pruning Git repack** and
**811,008 bytes** by the official Python bytecode **cache-only** cleaner.
The full inventory of **20,463 Git objects** (including unreachable
objects), all branch refs, all **2,788 reflog records**, and full
fsck were identical before and after repacking. The 41 deleted Python
cache files have a preserved per-file SHA-256 manifest.

The after928 cleanup also deleted **zero native proof files**. Its
savings are historical and must not be added again to after1024.

## Earlier applied bounded cleanup (after710)

The handoff cleanup added **only six externally unreferenced, incomplete
source-verifier tool-configuration attempts** to the retired set, and
ran the official regenerable cache-only command. It removed **12
private trial directories / 93 files / 1,847,296 allocated bytes
(1.76 MiB exact)**; Python cache cleanup reported **approximately
9.5 MiB gross**, and imports can regenerate those caches.
Each deleted file is identified by path, size and SHA-256 in the
preserved private after710 audit manifest. Both current after709
and retained after703 two-round original-native MAIN proofs
still pass read-only review after the deletion. See
[the exact after710 cleanup record](STORAGE_HANDOFF_AFTER710.md).

The **after597** audit below remains an earlier (much larger)
disposable BOSS-tree action; its 95,522,816-byte total is a
**historical after597 subtotal**, not the current combined
total. Do not add that amount to each newer receipt or treat
either audit as authorization to prune the active original
source-bound DAG.

## Protection boundary: what must stay

- Original Japanese targets, ReC98 sources/reference archives, Wine/Borland
  prefix, Ghidra/JDK, pinned library/CRT files and tooling are immutable inputs.
- Preserved historical after596 MAIN and after587 MAINL source-native receipt DAGs, all
  parent stages, actual consumed source snapshots, OBJ/LIB/EXE/MAP,
  linker responses, writer logs and BOTH independent rounds must stay.
- Historical active BOSS proof directories: after559 Chiyuri
  gptweb-chiyuri-559-proof-r1/r2 and after561 all sixteen
  gptweb-561-{boss}-r1/r2 source/receipt folders are still directly used
  by live original-source reviewers. The after560 native rounds remain
  separately referenced in historical source evidence.
- Last applied deletion of source-linked native CRT proof output is
  the historical after520 audit: **258 stages / 5,760 protected files**.
  Its exact 15-file retired branch reclaimed **1,642,496 allocated bytes**
  (see [the after520 record](STORAGE_HANDOFF_AFTER520.md)).
  These counts protect only the older after520 prefix, not the full
  after521–596 evidence DAG; the old cleanup script rejects newer roots.

## Actually removed in the after597 disposable-only audit

Exactly three isolated, unreferenced exploratory compiler-workspace
snapshots were retired. Each was outside the active after559/561 proof
IDs, with no external references from tracked code/docs/config or textual
.analysis/work receipts AT THE TIME OF DELETION. The current maintenance
docs name the retired runs only for audit traceability; they are not
new runtime/proof dependencies. The active original BOSS reviewers were
checked both before and after deletion, and their proof hashes survived.

| Original private run | Files | Allocated bytes |
| --- | ---: | ---: |
| Early Chiyuri exploratory run (gptweb-chiyuri-559) | 1,779 | 26,324,992 |
| Early Chiyuri native trial (gptweb-chiyuri-559-native-r1) | 1,779 | 26,324,992 |
| Abandoned Marisa compiler test (gptweb-marisa-561-native-test) | 1,773 | 26,288,128 |
| **Only these three unused trials** | **5,331** | **78,938,112** |

Physical allocated-block savings are **75.28 MiB**. No original target,
source file, accepted OBJ, active compiler output or current native evidence
was altered. The original tiny receipt/compile logs of all three retired
trials are retained under the private audit directory with a per-file
path/size/SHA-256 manifest of everything deleted:

    .analysis/handoff/after597-disposable-proof-trials/report.json
    .analysis/handoff/after597-disposable-proof-trials/deleted-tree-manifest.json

The source-controlled, strict allowlist verifier is
scripts/cleanup_after597_handoff_storage.py. Review without deleting:

    .venv/bin/python scripts/cleanup_after597_handoff_storage.py --verify

Do NOT reuse its --apply mode on any other directories, or apply a generic
work/probe, source archive or history garbage collection.

## Cache and Git storage maintenance

Python bytecode under scripts/__pycache__ and scripts/lib/__pycache__
(and tests/__pycache__ if present) is regenerable. The official
scripts/clean_generated.py --caches-only option is the only approved
current cache deletion route. Unlike source proof paths, caches can
regenerate on later imports, so immediate storage savings are not
durable source-evidence retirement.

The after597 action also removed only regenerable Python bytecode
through the official cache-only command, then repacked Git with
--no-prune / no reflog expiry. All 17,926 Git object IDs, types and sizes,
including unreachable objects, compare IDENTICALLY before/after; both
full Git fsck runs passed.

| After597 operation | Gross allocated bytes reclaimed | MiB |
| --- | ---: | ---: |
| Audited three abandoned native exploration roots | 78,938,112 | 75.28 |
| Official cache-only Python bytecode cleanup | 11,841,536 | 11.29 |
| Git GC without object pruning or reflog expiry | 4,743,168 | 4.52 |
| **Total actually retired allocation** | **95,522,816** | **91.10** |

These figures are measured file/allocated-block savings, excluding the
small private audit archive and any later cache regeneration. No lossless
compression, hardlink substitution or direct edit of binary proof products
was used. Supporting before/after Git object inventory, fsck logs,
cache report and retired-file manifest are retained under:

    .analysis/handoff/after597-disposable-proof-trials/

The earlier after554 maintenance did only Git gc --no-prune and
cache-only cleanup, saving **67,534,848 allocated bytes (64.41 MiB)**,
with all earlier work artifacts intact. Its audit and complete before/after
inventory are in the archived after554 storage record; those savings
must not be added again to the after597 deletion above.

Never delete or compress active compiled proof records merely because
they are large. The current MAINL stage work tree spans many dependent
historical native attempts; a fresh full source-DAG hash audit is mandatory
before any future source-output deletion. All other BOSS working trees,
after520/after554 historical roots and original program files stay protected.

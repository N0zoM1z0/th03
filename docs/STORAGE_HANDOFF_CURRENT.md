# TH03 current storage and evidence policy — after928 handoff (2026-11-08)

Use the [current source handoff](RE_HANDOFF.md) for after596 MAIN / after587
MAINL. This page records what has ACTUALLY been deleted or packed; it is
not a license to age-prune native work. The complete earlier after554 storage
record is preserved as [a historical snapshot](STORAGE_HANDOFF_ARCHIVE_AFTER554.md).

## Most recent applied safe cleanup (after928)

The [after928 actual cleanup audit](STORAGE_HANDOFF_AFTER928.md)
records **24,928,256 gross allocated bytes (~23.77 MiB)** reclaimed:
**24,117,248 bytes** by an audited **non-pruning Git repack** and
**811,008 bytes** by the official Python bytecode **cache-only** cleaner.
The full inventory of **20,463 Git objects** (including unreachable
objects), all branch refs, all **2,788 reflog records**, and full `fsck`
were identical before and after repacking. The 41 deleted Python
cache files have a preserved per-file SHA-256 manifest.

The cleanup **did not delete any `.analysis` proof stage, original
OBJ/EXE/MAP, Wine/Borland tool, target, historical compiler receipt or
negative experiment**. The large `.analysis` proof dependency trees
remain protected. Unlike prior source-proof audits, after928 claims
**zero deleted native proof files**. The cache saving may regenerate
on later imports. Do not repeat the gross savings when calculating
storage reclaimed in a future maintenance session.

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

The **after597** audit below remains the previous (much larger)
disposable BOSS-tree action; its 95,522,816-byte total is a
**historical after597 subtotal**, not the current combined
total. Do not add that amount to each newer receipt or treat
either audit as authorization to prune the active original
source-bound DAG.

## Protection boundary: what must stay

- Original Japanese targets, ReC98 sources/reference archives, Wine/Borland
  prefix, Ghidra/JDK, pinned library/CRT files and tooling are immutable inputs.
- Current after596 MAIN and after587 MAINL source-native receipt DAGs, all
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

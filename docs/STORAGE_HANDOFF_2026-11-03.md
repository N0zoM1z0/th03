# TH03 handoff storage audit — 2026-11-03

> **Historical snapshot, not current status.** The 62-source and 134 MiB
> measurements below describe **2026-11-03 only**. For the current 319-source
> checkpoint and up-to-date retained-proof storage rules, read the
> [2026-11-05 handoff](RE_HANDOFF.md) and
> [new storage audit](STORAGE_HANDOFF_2026-11-05.md).

**Purpose:** save allocated storage without breaking the retained original
Japanese native-source verification or deleting pinned targets.

## Audited selective cleanup

| Removed (ignored/untracked only) | Count | Reclaimed allocated bytes |
| --- | ---: | ---: |
| Completed Wine DOS `TH03ML/probe/` compilation trial directories | 67 dirs | 3,346,432 |
| Unreferenced, superseded `.analysis/work/storage-cleanup-20261030*` receipts and logs | 8 files | 1,642,496 |
| Regenerable Python `__pycache__` files under `scripts/`, `scripts/lib/` and `tests/` | 149 files | 2,383,872 |
| **Total** | | **7,372,800 bytes (7.03 MiB)** |

Every discarded DOS probe child was a real directory without symlinks;
the parent scratch folder remains available for new compiler trials.
The 2026-10-30 cleanup inventories had been superseded and were not
referenced by committed scripts, source, tests, config or documentation.
Historical review documents were **not** deleted.

The approximately **1.3 GiB Wine prefix** includes required Borland/
Wine runtime and toolchain files and must remain. The remaining
approximately **134 MiB `.analysis/work/`** includes live two-round
original CRT library, decoded Japanese EXE/MAP, object files,
source transports, context/response inputs, phase logs and bound
receipts. Intermediate builders dynamically open earlier output
vectors. Deleting or replacing those as if they were redundant
would break source proof and parent validations. Identical round
files were not hard-linked: the current writers can overwrite
files in place, risking corruption of linked proof files.

## Post-cleanup verification

The current 62-source CRT, complete native xx and original four-segment
tzset reviews passed **after scratch cleanup**. Current source proof
still reports **62 members, 28,599 CODE bytes, 831 untouched vendor
members**, two exact original MAINL EXE/MAP rounds and **677 MZ
relocations**. Native xx matches **12,622 CODE bytes, 187 ordered
fields and all 50 linked bodies**; tzset matches **48 ordered native
OMF fields**. Six scoped tests, preflight, generated-progress check,
tracking validation and whitespace checks passed.

The accepted28-provider CRT, formal accepted-ledger publication, pinned
Japanese targets, Wine tools, retained cold inputs, Ghidra and ReC98
were not changed; **no full cold replay** was performed.

For the next agent: see the [compact current handoff](RE_HANDOFF.md),
[generated progress](PROGRESS.md) and [workflow working-file rules](RE_WORKFLOW.md#working-files).
Future cleanup should audit actual source-bound reviewer reads.
Do not bulk-delete the raw `.analysis/work/` pairs or the old-named
`reference.tar`, an actual OP/MAINL source input.

# TH03 storage handoff — after554 maintenance (2026-11-06)

**Validated native source root: after554 / `e7697e1`.** After555 was interrupted
before any native build; its15 draft files are SHA-verified in the private
[research archive](AFTER555_UNBUILT_RESEARCH.md). This handoff adds no source
acceptance and deletes **zero native proof artifacts**.

## Current cleanup boundary

The last applied **native-deletion** audit is still the historical after520
prefix:258 stages /5,760 referenced receipt/log/native files. Its root is
`.analysis/work/mainl-after520-fstreambase-virtual-setbuf-ios-state-build.json`,
SHA-256 `f32c534f42d520f2c07a3acce769857d01ef310c04c00b419b585bf650994d8e`.
Those counts are not the complete current after554 dependency graph.

`cleanup_mainl_after520_handoff.py` deliberately **rejects this checkout** on
newer source stages. Its old zero-candidate result is historical. Do not run its
old apply/review/test sequence as a present maintenance recipe. Before deleting
any native output, a new source-bound DAG audit must include all after521–554
parents, both raw rounds, source/recipe inputs, actual consumed scratch copies
and diagnostic manifests, with explicit SHA-256 guards.

The after439/388/319-source commands and general `clean_generated.py` analysis
preview are not substitutes. No age-based sweep, blanket `--apply`, unreferenced
receipt pruning, native archive compression or hardlink substitution. Preserve
all targets, Wine/Borland and Ghidra/JDK tools, reference archives and the prefix.

## Actually performed in this handoff

| Operation | Allocated bytes reclaimed | MiB |
| --- | ---: | ---: |
| Git repack with `gc --no-prune` | 55,885,824 | 53.30 |
| Regenerable Python bytecode caches | 11,649,024 | 11.11 |
| **Immediate total** | **67,534,848** | **64.41** |

Git work used one CPU at nice10 and one packing thread. Object pruning,
reflog expiry and worktree expiry were disabled. Every one of the17,363
pre-existing Git object IDs/types/sizes is identical before/after, including
unreachable objects; `git fsck --full --no-dangling` passed on both sides.
Documentation commits add new objects afterward without removing old ones.

The official `scripts/clean_generated.py --caches-only --apply` removed only
`scripts/__pycache__`, `scripts/lib/__pycache__` and `tests/__pycache__` after a
preview. It preserved `.analysis`. Python caches regenerate during future
checks, so this is an immediate measurement, not permanent guaranteed savings.

A complete before/after inventory verified **all12,785 existing private work
files /664,948,935 logical bytes** unchanged by path, size and SHA-256. This is
preservation of the whole `.analysis/work` tree, **not** a newly certified active
DAG or permission to prune other files. Both native rounds/logs, diagnostics,
old ledgers and publication snapshots remain available.

Private audit directory: `.analysis/handoff/after554-maintenance/`.

- `report.json`: SHA-256
  `213b898f6811170f6636d93c44c10a6f0a8c84b9db30c50403e452171e3d7a05`.
- `work-artifacts-before.json`: complete private-work inventory, SHA-256
  `677819e9e7de00a39fd533b38862d88162fd1826f18e6c30e432401f658a1fab`.
- `git-objects-before.txt` / `git-objects-after.txt`: byte-identical object
  inventories, SHA-256
  `3774963046fd2494538b836fe68b5929afa9053bab3e8dd9578bf3e57b624762`.
- `run_maintenance.py` and command logs: exact action record. It is a completed
  one-off operation, not an idempotent or approved native-deletion tool.

The workspace was approximately3.7 GiB before maintenance. Most allocation is
useful installed state: about1.3 GiB of Wine Windows files and1.2 GiB of private
analysis tools. These were retained. Git/cache savings should not be presented
as deleted native outputs or as a new source-reconstruction milestone.

## Future safe maintenance

```sh
.venv/bin/python scripts/clean_generated.py --caches-only # preview
# Apply only the reviewed cache list; never replace this with blanket --apply.
```

After cleanup, run the current scoped reviewer, tracking/progress checks and
`git diff --check`; no cold/native rebuild is needed for unchanged source.
Use [the current handoff](RE_HANDOFF.md) for source roots and next work.
The exact older15-file deletion and11.75 MiB historical cleanup remain documented
in [the preserved after520 record](STORAGE_HANDOFF_AFTER520.md), rather than
being conflated with the present operation.

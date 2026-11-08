# TH03 after928 — applied safe Git/cache cleanup, full proof preservation

**Applied and audited 2026-11-08.** The goal was to reduce disposable
local storage before another agent takes over, **without discarding
source-native evidence** or original PC-98 toolchain/target inputs.
This is an actual completed cleanup record, not a recommendation to
run an open-ended stale-artifact pruner.

## Actual reclaimed allocations

| Applied operation | Before | After | Allocated bytes reclaimed |
| --- | ---: | ---: | ---: |
| Safe non-pruning Git object repack (`.git`) | 44,199,936 B | 20,082,688 B | **24,117,248 B** |
| Official regenerable Python bytecode cleanup | 41 files / 811,008 B allocated | 0 files in the three allowed trees immediately after cleanup | **811,008 B** |
| **Total measured gross reclaim** | | | **24,928,256 B (~23.77 MiB)** |

The cache figure is **gross and transient**: later Python imports may
regenerate those cache files. The Git repack savings are a real reduction
in duplicated loose-object storage. This does not count historical
after520/after554/after597/after710 cleanup again.

### Git was repacked, never history-pruned

The exact command was:

```
git -c gc.reflogExpire=never -c gc.reflogExpireUnreachable=never \
    -c gc.pruneExpire=never gc --no-prune --quiet
```

Before/after preservation checks were made, including **unreachable
objects**:

- All **20,463 Git object IDs, object types and raw object sizes** were
  identical. The sorted full-object inventory SHA-256 before and after
  is `8224564e3b9bc8eacac562d0bbe5928eee0f82e6e87aef945752375c753802ae`.
- All local refs and object IDs were identical (inventory SHA-256
  `48589c532fadf6c56b916241b99e3281c85e1b50d69f3563b8c1e556a45cbf74`).
- All **2,788 reflog entries** were identical (SHA-256
  `07506fded96a96319ccd075343dd657bd71b5e68dc2a75e2500a72eaffcbb588`).
- `git fsck --full --no-reflogs` succeeded before and after.
  Existing harmless dangling entries are retained, not pruned.
- The final Git inventory has **0 loose** and 20,463 packed objects.
  No reset, checkout loss, branch rewrite, remote push or reflog expiry
  was performed.

The ignored, locally preserved full inventory, refs, reflogs, `fsck`
output, before/after object counts and exact cleanup manifests live at:

```
.analysis/handoff/after928-safe-git-cache/
```

### Only the approved Python cache directories were removed

Executed the official source-controlled cleaner, rather than manual
`find ... -delete` or deleting ignored proof trees:

```
.venv/bin/python scripts/clean_generated.py --caches-only --apply
```

Allowed trees: `scripts/__pycache__`, `scripts/lib/__pycache__` and
`tests/__pycache__`. The per-file **SHA-256, logical size, allocated
block size and relative path** of all 41 removed bytecode files are
preserved in `cache-manifest-before.json` under the private audit path.
The manifest SHA-256 is
`27f1aa08cbb06837abf0613d6ec08dff1a5cf71b94e09ffc920be84990750d96`.
No toolchain, `.analysis`, object, executable, test source or tracking
file was removed by this operation.

## Explicitly retained: large but not proved disposable

The ignored `.analysis` subtree is approximately **4.6 GiB** on this
worktree, including approximately **2.2 GiB of the original Wine/
Borland toolchain prefix** and **1.5 GiB of preserved `.analysis/work`
native reconstruction evidence**. Other historical BOSS native compiler
rounds remain proof dependencies. About 380 incomplete exatt-stage
folders have no final `report.json`, but they are **small genuine
negative/diagnostic traces**; their current referential status has not
been fully audited. There is **no authorization** to bulk-prune them or
old complete writer rounds by name or age.

The active source-bound evidence chain, after927 original TC4 two-round
OBJ/EXE/MAP and writer logs, historical source snapshots, successful
and failed codegen trials, original PC-98 targets, installed toolchains,
original CRT, source and independent proof inputs all remain untouched.
The independent read-only after927 and other current-source reviewer
checks still pass. Future large-space retirement requires a new
**explicit allowlist, source/receipt-DAG reachability audit and pre-
delete per-file SHA-256 manifest**. Do not reuse a previous cleanup
script's guarded `--apply` for a different stage.

For the actual current state and next-agent task priorities, use
[the short active handoff](RE_HANDOFF.md) and
[the current storage policy](STORAGE_HANDOFF_CURRENT.md).

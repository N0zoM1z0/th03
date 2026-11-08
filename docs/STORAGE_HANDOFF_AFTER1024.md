# TH03 after1024 — safe cache cleanup and non-pruning Git repack

**Applied and audited 2026-11-08.** This handoff cleanup removed only
regenerable Python bytecode and repacked Git without pruning history.
No .analysis proof stage, native OBJ/LIB/EXE/MAP, target, compiler,
Wine prefix, Ghidra project or source file was deleted.

## Applied cache-only cleanup

The official bounded command was used:

    .venv/bin/python scripts/clean_generated.py --caches-only --apply

It removed exactly three regenerable cache directories:

- scripts/__pycache__
- scripts/lib/__pycache__
- tests/__pycache__

The pre-cleanup manifest records **448 files**, **10,503,368 logical
bytes** and **11,243,520 allocated bytes**. Every file has a relative
path, logical size, allocated size and SHA-256. The manifest is:

    .analysis/handoff/after1024-safe-git-cache/cache-manifest-before.json

Manifest SHA-256:

    ffe90301f268e142b36b1ea364c9467f75236c60e263da20c93b7275a5cec0a7

All three cache directories were confirmed absent after the command.
Python may regenerate these caches during later imports.

## Applied non-pruning Git repack

The following command packed the 856 loose objects without expiring
reflogs or pruning unreachable objects:

    git -c gc.reflogExpire=never \
        -c gc.reflogExpireUnreachable=never \
        -c gc.pruneExpire=never gc --no-prune --quiet

Before and after inventories were compared byte-for-byte:

- All **21,319 object IDs, types and raw sizes** are identical.
  Inventory SHA-256:
  d1bb43d57b184c5231bd353c488dcb39e6f6f917f778ad2fda0e0092695cc160
- Both refs are identical. Inventory SHA-256:
  b1d2e3a9d2894f36adac36c7e65da36df1bc17ca328277364dad823748de6baf
- All three reflog files and their hashes are identical. Inventory
  SHA-256:
  322b6ed51318fd2afa2f0e7413fe1147fa3250ab9209f66d74a8b61329b69b59
- git fsck --full --no-reflogs output is identical before and after,
  SHA-256:
  5bbc8dea63addfe7536d0ae9b7a66f6f42036f8163ea187a471b9cbb04a05aff

Git moved from **856 loose + 20,463 packed objects** to **0 loose +
21,319 packed objects**, retaining two packfiles. The .git apparent
size decreased from **24,424,896** to **20,223,592 bytes**, a reduction
of **4,201,304 apparent bytes**. This is a repack, not history deletion.

## Audit files

All before/after inventories, fsck output, counts, sizes, and the cache
manifest are retained under:

    .analysis/handoff/after1024-safe-git-cache/

The summary is report.json, SHA-256:

    a5c812f9325d67eca1447f77312f19c44247b14656b50fa32330df11dcd6cb4c

## Handoff boundary

No native proof output was retired. The active source-bound receipt DAG,
both original compiler rounds, normal MAIN links, Japanese targets and
the installed toolchain remain intact. The earlier after928, after710,
after597 and after520 records are historical, separately measured
operations; do not add their savings again.

Do not run clean_generated.py --prune-unreferenced-receipts, old
after439/388/319/511 cleanup tools, or a generic .analysis purge.
The only routine deletion authorized here is the official cache-only
route. Any native proof deletion requires a new complete dependency
audit, a one-time explicit allowlist and independent post-deletion
reviewers.

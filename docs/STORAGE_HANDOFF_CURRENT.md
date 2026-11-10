# TH03 storage and evidence retention — current policy (2026-11-10)

Consult the [active TH03 handoff](RE_HANDOFF.md) for current source status
and the [generated progress](PROGRESS.md) for actual native proof stages.
`.analysis/` is **not** a disposable build directory: it contains retained
source-bound compiler and linker evidence, private tool inputs, original
Japanese targets and analyzer state. The historical after596 MAIN and
after587 MAINL parents are still proof dependencies, not current broad
source acceptance.

## Most recent applied cleanup

On 2026-11-10, an audited, **failed and receipt-less** Ellen compiler trial
(`.analysis/th03-main-exatt-ellen-cpp/af1093a`) was reduced to its compiler
failure log. Its 1,757 byte-identical pinned-baseline source copies and
redundant `reference.tar` were deleted, while **all 15 distinct source
files**, the failure log and a 1,772-file SHA-256 manifest were preserved
in a private audit. **26,845,184 allocated bytes gross / 26,382,336 bytes
net (25.16 MiB)** were recovered. See the
[exact after1307 audit](STORAGE_HANDOFF_AFTER1307.md). This is a bounded
exception, **not** permission to remove native proof workspaces.

A fresh official cache-only preview reported **0.0 MiB eligible**:

```sh
.venv/bin/python scripts/clean_generated.py --caches-only
```

No cache-only deletion was applied on this date. The checkout currently uses
approximately **7.1 GiB in `.analysis/`**, dominated by the game-specific
`.analysis/toolchain/` (**3.2 GiB**, including Wine) and `.analysis/work/`
(**2.6 GiB**, containing compiler/link outputs and receipts). Successful
historical BOSS/Extra Attack trial snapshots occupy much of the remaining
space and were **not** classified as disposable.

### Additional lossless maintenance on 2026-11-10

The historical broad unittest diagnostic `script-audit-baseline.log` is now
`.analysis/work/script-audit-baseline.log.gz`. Decompression reproduces all
17,414,688 original bytes and SHA-256
`1217ec969eea6269ba64f4e161663398cefc243763798ba3d7bfa07a3b2a1a7a`.
A reference search found only its documentation link, which was updated;
no executable or private receipt consumes the log or its hash. This archived
test output is distinct from native compiler/linker writer logs.
Replacing the plain diagnostic with its verified gzip recovered
**16,879,616 allocated bytes** while retaining the complete failure details.

A non-pruning `git -c pack.threads=1 repack -a -d --keep-unreachable`
also recovered **24,412,160 allocated bytes**. All **23,907 object IDs**,
refs and reflog contents were identical before and after, and both full
Git fsck checks passed. No Git history was expired or discarded.

The private audit at
`.analysis/handoff/20261110-storage-maintenance/` retains the diagnostic
hashes, Git object inventory, ref/reflog inventory and fsck logs. After
allowing for this audit, these two actions recovered approximately
**38.4 MiB net**, in addition to the earlier failed-Ellen cleanup.
The startup preflight verified all 65 current MAIN scopes; a bounded
post-maintenance Mima Extra Attack review (`af1306e`) also passed.
No native proof output or source snapshot was removed by these actions.

## Protection boundary

- Keep original Japanese targets and pinned ReC98 resources, compiler,
  linker, game-specific Wine prefix, Ghidra projects and shared runtime.
- Keep the **entire active source-bound receipt DAG**, including parent
  configurations, two original native compile/link rounds, full original
  OBJ/LIB/EXE/MAP artifacts, raw relocations, source snapshots and writer
  logs. Keep useful negative compiler evidence and recorded quirks.
- Keep any historical successful source/semantic receipt and its consumed
  inputs unless a fresh, **explicit per-path dependency audit** proves it
  no longer contributes to any supported proof or reproducible historical
  finding. `du` size, old stage numbers and current Git references alone
  do **not** justify deleting it.
- The official `scripts/clean_generated.py --caches-only` route is safe for
  its narrow, regenerable Python-cache allowlist. Never use retired generic
  receipt pruning, whole-workspace deletion or old cleanup-script `--apply`
  options as a shortcut.
- Before another bounded cleanup, identify exact files, verify references
  from source/config/docs and private receipts, preserve hashes and any
  distinct source, name the **one-time allowlist**, and verify relevant
  affected native scopes **after** deletion. Do not rerun a full cold replay.

## Earlier audits (historical, not new cleanup authorization)

- [After1024](STORAGE_HANDOFF_AFTER1024.md): 448 regenerable Python cache
  files removed and a non-pruning Git repack with all 21,319 historical
  object IDs preserved; **no native proof outputs removed**.
- [After928](STORAGE_HANDOFF_AFTER928.md): earlier no-prune Git repack and
  cache-only deletion; historical accounting must not be added twice.
- [After710](STORAGE_HANDOFF_AFTER710.md): twelve specifically unreferenced
  failed verifier-config trial trees retired by a one-time audit.
- [After597](STORAGE_HANDOFF_AFTER597.md): three explicitly audited,
  unreferenced exploratory compiler workspaces retired, not the successful
  source-native BOSS proof DAG.
- [After520](STORAGE_HANDOFF_AFTER520.md) and
  [after554 archive](STORAGE_HANDOFF_ARCHIVE_AFTER554.md): older bounded
  provenance; their retention/deletion limits do **not** cover current stages.

The failed-experiment deletion is limited to `af1093a` and is recorded in
its own private manifest. The additional maintenance archives only the
named unittest diagnostic and repacks Git without pruning. No other
`.analysis/` files were deleted.

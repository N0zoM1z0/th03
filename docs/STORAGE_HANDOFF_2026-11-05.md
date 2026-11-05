# TH03 handoff storage audit — 2026-11-05

This is the storage state for the **319-source** Japanese MAINL working CRT
checkpoint, not the historical 62-source figures from the
[2026-11-03 audit](STORAGE_HANDOFF_2026-11-03.md).
The [current handoff](RE_HANDOFF.md) is the live source/acceptance status.

## Actually removed (ignored/rebuildable, not tracked source)

| Deliberately retired output | Deleted | Allocated storage reclaimed |
| --- | ---: | ---: |
| Completed **superseded alternative** `after*` CRT modes: old raw OBJ/LIB/EXE/MAP and writer logs | 301 files, 15 modes | **21.87 MiB** |
| Disposable `TH03ML/probe/gptweb-*` Wine/TASM trial folders | 63 directories | **2.78 MiB** |
| `gptweb_*`, `xxv-experiment-*`, `xxv-diagnostic-*` scratch analyses and temporary cleanup previews | 59 files | **0.82 MiB** |
| Regenerable Python `__pycache__` in scripts/lib/tests | 3 directory trees | **approximately 3.8 MiB** |
| **Combined** | | **approximately 29.3 MiB** |

The 301 removed names are recorded in the ignored local manifest
`.analysis/work/handoff-2026-11-05-retired-variants.txt` (not a Git-tracked
source artifact). The helper
`python3 scripts/cleanup_mainl_handoff_artifacts.py` is a **dry-run by
default**; `--apply` deleted only files explicitly listed in completed
noncurrent alternate-mode receipts. It read the checked-in latest builder's
literal parent layers, verified the **latest complete receipt SHA-256**, and
protected every receipt, log and output in that live dependency chain.
The check deliberately **fails closed** if a newer source layer appears
or the latest receipt hash changes. It must be re-audited before reuse at a
newer source checkpoint. No hardlinks, compressed stand-ins, patched OBJs
or altered executable files were used to save space.

**Historical alternate-mode build/review JSONs remain as metadata** and
tracked per-module review documents remain untouched. Their now-retired
raw vectors **are not directly runnable proofs**: an agent exploring an
obsolete intermediate mode must regenerate that mode's producer outputs.
The current mainline DAG and current reviewer do **not** depend on those
superseded branches. Historical claims should not be treated as current
acceptance without rerunning the affected proof.

## Deliberately protected

- The live **55 inherited layers plus latest 319-source layer** have **1,700
  explicitly retained raw receipt, phase-log and OBJ/LIB/EXE/MAP paths**.
  They were excluded by path from deletion. Parent hashes, original
  selected member identities and the independent two-round native output
  remain intact; do **not** prune earlier `after*-round*` pairs on age alone.
- `.analysis/toolchain/wineprefix/` (about **1.3 GiB**) contains the
  necessary Borland and Wine tools. Only the named `probe/gptweb-*`
  disposable trial folders inside the project worktree were deleted.
- The fixed **original Japanese target binaries**, `.analysis/targets`,
  accepted-source ledgers and acceptance JSONs (including the large
  `mainl-exception-previous-acceptance.json`), `.analysis/runtime/images`,
  Ghidra artifacts, repository source and Git history were **not** deleted.
  The apparently old-named `reference.tar` is still a relevant source input.
- `.analysis/work` decreased from roughly **244 MiB to 221 MiB** before
  normal reviewer/cache regeneration. The rest of the recovery is in the
  Wine probe and Python cache directories. This is not a claim that the
  whole 1.3 GiB runtime/toolchain is disposable.

## Safeguards and post-cleanup verification

Before deletion, the full active reviewer reported **319 original-source
members / 104,838 original-equal CODE bytes**, two byte-for-byte original
Japanese EXE/MAP rounds, **677 ordered MZ relocations**, with no full cold
replay. The same reviewer and targeted tests are rerun after cleanup.

For a new agent, run the *current* scoped evidence checks, not an old
alternative branch or another cold replay:

```sh
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after317_work.py nec-delay-mbyte
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after317_work -v
.venv/bin/python scripts/validate_tracking.py
git diff --check
```

`python3 scripts/clean_generated.py` is a useful **preview**, not a proof
oracle: on 2026-11-05 its general preview listed about **156 MiB**,
**including actually required** mainline native outputs/logs. Do **not**
run its blanket `--apply` on this worktree. Its scoped `--caches-only`
option is appropriate for regenerable Python caches. There is no need to
run full cold replay to verify this handoff cleanup.

# TH03 storage and evidence retention — current policy (2026-11-10)

Retention follows the current reconstruction dependencies, not every historical
reference. The user's 2026-11-10 clarification supersedes the earlier blanket
rule that successful old trials and documented paths must all remain unpacked.
Use [generated progress](PROGRESS.md) to identify current source-bound proofs
and [the active handoff](RE_HANDOFF.md) for current work.

## Shared runtime and local state

Factory provides Wine, Ghidra and JDK executables. Wine resolves through
`.factory/shared-tools/wine/bin/wine` to `/usr/bin/wine-stable`; the local
`.analysis/toolchain/wineprefix` holds this game's registry, compiler profiles
and working directories. Those working directories are build output, not an
installed shared toolchain.

Byte-identical, root-owned Wine system modules now link to the same installed
Wine package under `/usr/lib/{x86_64,i386}-linux-gnu/wine/`. Every replacement
was checked against its original SHA-256. Registry files, Borland SDKs, local
custom modules and game state remain isolated. See [shared tools](SHARED_TOOLS.md).

## Applied current-dependency cleanup

The earlier directory-level size summary hid approximately 1.9 GiB of trial
work inside the Wine prefix and over 1 GiB of duplicated Wine system modules.
The new audit measured **7.01 GiB before / approximately 2.45 GiB after**,
recovering approximately **4.56 GiB net**, including archive/audit costs.

| One-time action | Paths affected | Gross allocated bytes recovered |
| --- | ---: | ---: |
| Retire superseded MAIN Wine probe stages | 2,969 directories | 1,690,705,920 |
| Retire superseded MAIN saved-output stages | 2,950 directories | 1,931,300,864 |
| Retire unused MAINL Wine probe stages | 126 directories | 147,595,264 |
| Share identical Wine system modules | 1,363 files | 1,166,254,080 |

The 6,045 retired directories contained 108,000 files. Useful source variants,
responses, compiler logs and original reports survive in a **36,546,606-byte**
compressed context archive, verified member by member before deletion.
Obsolete OBJ/EXE/MAP outputs were discarded. Historical receipt contents were
not rewritten; they describe their original runs and may reference retired
raw outputs. Use current selected stages for runnable native verification.

The exact one-time allowlist, all retired file hashes, current dependency
paths, shared-module hashes, archive and execution log are retained privately
in `.analysis/handoff/20261110-active-storage-audit/`. This audit used:

- Read-access tracing of the complete current preflight, including all 65
  MAIN reviews, MAINL current source reviews and OP/MAINL/ZUN publications.
- Recursive references from the JSON actually consumed by those checks,
  including resolved paths, plus the object/provider dependencies in retained
  native linker responses. The open `input_s` link experiments remain intact.
- Hash checks of **9,780 current dependency files** before and after retirement.

Current native outputs, both rounds, writer logs and the retained cold parents
were preserved. After cleanup, `af1310s` rebuilt the complete Mima Extra Attack
owner in two original TC4 rounds and repeated both full normal MAIN links;
CODE, ordered fields, layouts, Japanese image and relocations matched.
The original frozen proof inputs were reused, with no full cold rebuild.

## Rules for the next cleanup

- Keep pinned Japanese targets, compiler/SDK identities, analyzer projects,
  isolated mutable game state and the shared tool selectors.
- Keep current selected proof outputs and the actual transitive native/source
  inputs needed to verify or rebuild their affected scopes, including both
  raw OBJ/LIB/EXE/MAP rounds, ordered relocations and writer logs.
- Documentation links, age and a historical successful result are not retention
  roots. Retire superseded trials after checking current readers, receipt
  inputs and linker dependencies. Keep useful failed source variants and
  findings compactly; do not keep every duplicate executable indefinitely.
- Use a bounded explicit allowlist. Verify the affected current scopes after
  cleanup and run a real compiler/linker smoke if the runtime or build inputs
  were touched. Never change receipts to manufacture a pass.
- `clean_generated.py --caches-only` handles routine regenerable caches.
  Its historical broad preview is not the current proof dependency boundary;
  retired generic receipt-pruning commands remain disabled.

## Earlier bounded actions

The [after1307 audit](STORAGE_HANDOFF_AFTER1307.md) separately recovered
25.16 MiB from one failed Ellen checkout. Later lossless diagnostic compression
and a non-pruning Git repack recovered 38.4 MiB; their original audit remains
at `.analysis/handoff/20261110-storage-maintenance/`. Those savings preceded
the 7.01 GiB baseline above and must not be counted twice. The broad unittest
log remains readable at `.analysis/work/script-audit-baseline.log.gz`.

Older [after1024](STORAGE_HANDOFF_AFTER1024.md),
[after928](STORAGE_HANDOFF_AFTER928.md),
[after710](STORAGE_HANDOFF_AFTER710.md),
[after597](STORAGE_HANDOFF_AFTER597.md) and
[after520](STORAGE_HANDOFF_AFTER520.md) documents describe only their own
historical actions. Their allowlists do not authorize another deletion.

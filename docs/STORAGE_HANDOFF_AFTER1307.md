# 2026-11-10 — bounded cleanup of one failed Ellen compiler snapshot

This is an **applied, audited** cleanup, not a generic proof-pruning rule.
The original `af1093a` Ellen Extra Attack compiler experiment failed with
`Unable to open include file 'src/main/player/exatt_entity.hpp'`. Its
private root `.analysis/th03-main-exatt-ellen-cpp/af1093a/` contained a
compiler error log, a copy of the reference tarball, and a source checkout;
it had **no successful receipt.json, original OBJ proof, or normal TLINK
receipt**. The only checked-in reference to the stage was historical
analysis of the missing-header failure, not a dependency on its checkout.

A file-by-file comparison against the retained pinned `_reference/ReC98`
checkout found **1,757 of 1,772** source files byte-for-byte identical.
The other **15 files (12,457 logical bytes)** were copied with their
original relative paths into a retained private audit. The 11,079,680-byte
`reference.tar` had the same SHA-256 as the retained
`af1093b/reference.tar` (and other historical stages). The original
`af1093a/compiler.log` remains at its original path; another copy was also
saved in the audit.

**Only two explicitly audited paths were deleted:**

- `.analysis/th03-main-exatt-ellen-cpp/af1093a/source/`
- `.analysis/th03-main-exatt-ellen-cpp/af1093a/reference.tar`

The private, append-only-style audit material is retained under
`.analysis/handoff/after1307-failed-ellen-compiler-source/`:
`audit.json`, `file-hashes.json` (all 1,772 paths, sizes, SHA-256 and
baseline-identity results), `unique-overlay/` (all 15 distinct files),
and `compiler.log`. The remaining original failure log and the surviving
reference tarball were rechecked after deletion.

| Measured physical disk allocation | Bytes | MiB |
| --- | ---: | ---: |
| Gross reclaimed from that failed experiment | 26,845,184 | 25.60 |
| New retained audit material | 462,848 | 0.44 |
| **Net reclaimed** | **26,382,336** | **25.16** |

No active or historical successful proof/report, `.analysis/work` stage,
original target, native OBJ/LIB/EXE/MAP round, writer log, Wine prefix,
Borland tool or analyzer project was removed. The **65 current selected
MAIN native stages** and the separate `input_s` link blocker are unaffected.

The official `scripts/clean_generated.py --caches-only` dry-run found
**0.0 MiB** eligible before this cleanup, so no routine cache deletion was
applied. Other large proof directories were intentionally retained: size,
age or a repeated reference tarball alone do not establish that a successful
historical compiler receipt is disposable.

This one-time audit **does not authorize deleting** `af1093b` or any other
stage, pruning `.analysis/work`, recreating a missing snapshot, or applying
old generic receipt-cleanup tools. Future candidates require their own
complete dependency check and explicit bounded allowlist.

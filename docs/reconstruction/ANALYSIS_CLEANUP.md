# Private analysis cleanup

The2026-10-06 cleanup removed16182 unreferenced files (189572651 bytes,
approximately181 MiB) from seven explicitly selected abandoned cold build runs
without `receipt.json`. It retained failure transcripts, review helpers and
all literal file references found in tracked files or retained JSON proofs.
The1494 private receipt input paths had identical existence and SHA-256 states
before and after deletion. Existing historical missing/stale inputs were not
changed or claimed repaired.

Receipt: `.analysis/sol-abandoned-build-cleanup-20261006.json`; SHA-256
`7fb6b1a306fb17f81180ebe9b64e8d584af223795c58bb3abeb923ebcbcce61a`.
Its manifest records each removed path, size and hash, the retained reference
corpus hashes and selected directories. Original targets, attestation inputs,
accepted/compiler receipts, diagnostic observations, toolchain/Wine prefix and
current menu cold builds are outside the deletion scope. No code or acceptance
progress is credited for cleanup.

Replay `python3 scripts/clean_th03_failed_analysis.py --output
.analysis/NEW_CLEANUP_PLAN.json` for a fresh dry run; `--apply` deletes only the
unreferenced files selected by that run. A new receipt in any selected directory
stops cleanup. It freezes the reference corpus and validates candidates before
deleting, then compares all retained private input states. Further reclamation
must inspect references first: large native-observation JSON files and completed
compiler snapshots still supply evidence.

Music Room preparation cleanup subsequently removed three unreferenced files,
2165 bytes: two intermediate extraction lists and a superseded draft test log.
Literal reference scans found no retained dependencies; all197 preceding entry
receipt inputs retained their hashes. The corrected58-test log, diagnostic and
compiler proof inputs, and the incomplete native-budget failure log remain.
Receipt: `.analysis/sol-op-music-temp-cleanup-20261006.json`; SHA-256
`cae22ce2c578370d58f542b9e0cf3fe796621885b5411cce4e3ed1a9fb803d54`. No acceptance credit is assigned for cleanup.

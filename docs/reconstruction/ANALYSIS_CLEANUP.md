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

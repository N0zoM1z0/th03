# Private analysis cleanup

The shared math migration removed one unreferenced stopped precompiler
preparation after two corrected cold rounds passed:1928files/21507828bytes
(about20.5MiB). All1871 retained private input states stayed unchanged. The
complete failure transcript and original replay snapshot remain separate;
there was no compiler execution or cold-build log in that failed preparation.
Successful source/diagnostic/coverage trees and all protected targets/tools/
Ghidra states remain intact. Receipt
`.analysis/sol-shared-math-temporary-cleanup-20261006.json`, SHA256
`bad213f06dfc5e2a790e194e8b13cdbd180936bc8c6317620428c7242ff74e39`,5guards.
Historical missing/stale input states were unchanged; no proof rebasing.

The shared text migration removed one unreferenced first cold preparation:
2504files/31040136bytes (about29.6MiB), after the corrected two-round proof passed.
All1823 retained private input states remained unchanged. The complete first
failure/cold transcripts and original replay script remain separate, as do both
successful cold trees and every current proof input. Receipt
`.analysis/sol-shared-text-temporary-cleanup-20261006.json`, SHA256
`69dd12272b91686f8259af848e695b5200f0297de4f0da4b875c4b4c21b68e51`,6guards.

The generic cleaner initially stopped at three historical Factory function
query transcripts named `.json`; inspection confirmed plain text, unchanged
against their explicit ledger output hashes. The cleaner now recognizes only
the recorded Factory tool, function-query command/output binding and exact
current SHA. Changed text, other query kinds/output names and malformed
`receipt.json` still stop before deletion. Fifteen isolated destructive controls
pass, including four new exception/negative checks. The three historical text
files themselves stay unchanged. Earlier cleanup receipts retain their original
helper hashes; subsequent authorized helper changes do not rebase those guards.

The shared CDG migration subsequently removed two unreferenced failed cold
preparations after the successful two-round source proof:4962 files,
61841191 bytes (about59MiB). Complete failure/cold transcripts remain separate,
as do current source/diagnostic/coverage/OMF proof inputs. All1723 retained
private input path states stayed unchanged across deletion. Receipt
`.analysis/sol-shared-cdg-load-temporary-cleanup-20261006.json`, SHA256
`3bb5b89e62d752348f237c736972e0e1cc2c4aa1572983f662395ca1af414bf3`.
Canonical targets, toolchain/Wine prefix, Ghidra, accepted receipts and their
archives/snapshots were excluded; historical missing/stale inputs were not
repaired. The372 diagnostic,378 source and393 coverage guards matched at cleanup
time. Subsequent authorized ledger/helper changes make the old coverage receipt
historical; its guards are not rebased. The later shared drawing migration
passed both cold rounds on its first run, with no failed preparation trees to
remove; its successful proof trees and input snapshots are retained.

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

## Guarded generated cleanup

`scripts/clean_generated.py` now protects input dictionaries in retained JSON
proofs, their lexical aliases and resolved local destinations. Entire cold
directories containing `receipt.json` are preserved, including archives,
snapshots and outputs absent from the input dictionary. Guarded cache inputs
outside `.analysis/` also survive. Unreadable receipts stop before deletion;
missing historical inputs remain missing. Eleven isolated deletion controls
pass in `.analysis/sol-proof-cleanup-controls-20261006-final.log`, including
malformed ledger JSON and ledger symlink aliases. The preceding nine-case
control log remains separate historical evidence.

The default remains a dry run. No broad cleanup is executed while selection
review/cold compilation is active. Direct evidence-ledger protection alone was
insufficient to preserve receipt dependencies; this change closes that gap.

## Character-selection preparation cleanup

After two independent source cold replays completed,7128unreferenced files
(71733816bytes, about68.4MiB) were removed from three failed/superseded layout
preparations and five temporary outputs. The current frozen-source layout
probe supersedes the earlier full-CPP preparation probe. Its complete proof
tree is retained, together with current source cold outputs, archives, targets,
toolchain, Ghidra and every referenced proof dependency. The candidate CPP
draft was discarded outside product ownership; only the bounded CODE inl is
maintained. The first macro-escaping compiler failure was copied verbatim to
`.analysis/sol-op-select-layout-first-compiler-failure-20261006.log`.

Cleanup receipt `.analysis/sol-op-select-temporary-cleanup-20261006.json`,
SHA256 `5712b574d06d817102fcd9b3c579053c6ddce4a37f089fe59e85968f4baa88de`, records all1843retained input states
unchanged across deletion, with333current source and5current layout guards
rechecked. A separate `.analysis/sol-op-select-retained-input-states-20261006.json`
keeps the post-cleanup hash/missing map. This records cleanup-time state; later
authorized ledger updates can make older ledger-input snapshots historical.
Existing missing/stale inputs were not repaired. No broad `--apply` was run.

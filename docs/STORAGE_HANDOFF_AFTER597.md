# After597 audited retirement: three unreferenced exploratory BOSS trials

The saved private audit records the actual 2026-11-07 disposal. The
source-controlled allowlist implementation is
scripts/cleanup_after597_handoff_storage.py. The operation removed only
5,331 files in three self-contained, superseded exploratory proof-run
directories (78,938,112 allocated bytes / about 75.28 MiB). The earlier
after559 Chiyuri and after561 eight-BOSS source-native proof round inputs
remain intact and passed their read-only reviewers.

The three roots were selected through an inventory of all nine BOSS
source-proof top-level workspaces, original analysis of active 559/561
source-proof receipt IDs, and an external-reference scan of Git
tracked sources/docs/config/tests plus textual .analysis/work and
handoff receipts. None of the three exact retired IDs had an external
reference. The deletion bound also pinned these unchanged proof roots:

- after559 Chiyuri (both actually referenced original TC4 rounds)
- after561 eight-BOSS source compiler receipts (16 original OMF outputs)
- after596 full MAIN native source link
- after587 full MAINL native source link
- after520 historical source-linked CRT prefix

No cold replay or original product source compilation was run to decide
disposability. All three original exploratory receipt.json and
compiler.log pairs were copied into the private audit BEFORE removal.
Every file had its original path, logical length, allocated block count
and SHA-256 recorded; none was symlinked or hardlinked.
The full private original deletion manifest has SHA-256:

    5d538351525fc90a817cc3bff14da63eeb8ef1a055267975eec1e1c87adc0a5a

Private audit:
.analysis/handoff/after597-disposable-proof-trials/report.json

After deletion the standalone script --verify passed. There was no
deletion of .analysis/work, the 209-MiB MAINL scratch proof DAG,
original Wine/TC4/Ghidra tools, active native proof trees, or curated
negative CODE/OMF hypotheses needed by existing documentation.
Those three retired trial source workspaces may be regenerated from
the intact maintained code and original native tools, but must not
be silently counted as active Factory acceptance evidence.

The historical source-linked after520 deletion is a separate
258-stage / 5,760-protected-file prefix with a 1,642,496-byte
retirement audit; see STORAGE_HANDOFF_AFTER520.md.
The after554 Git/cache-only maintenance is preserved in
STORAGE_HANDOFF_ARCHIVE_AFTER554.md and is not this operation.

## Separately audited cache and Git allocation savings

After the three unreferenced BOSS experiments were retired, the official
cache-only cleanup removed 11,841,536 bytes of currently allocated,
regenerable scripts/tests Python bytecode. No .analysis files were selected.
This cache saving is temporary and may diminish when Python imports run again.

A single-thread, no-prune Git GC with reflog expiry disabled reduced .git
from 23,248,896 to 18,505,728 allocated bytes, saving 4,743,168 bytes.
The entire Git object inventory, INCLUDING unreachable objects, was
recorded before and after: all 17,926 object IDs, types and byte lengths
were identical. Both git fsck --full --no-dangling passes completed.
The before/after inventory SHA-256 is:

    b7a42d61f7e3d844b004b5185f2479b4a6fad7a6d64b84d73fef1c88a0f27421

Corresponding private audit material:
- .analysis/handoff/after597-disposable-proof-trials/git-maintenance.json
- .analysis/handoff/after597-disposable-proof-trials/git-objects-before.txt
- .analysis/handoff/after597-disposable-proof-trials/git-objects-after.txt
- .analysis/handoff/after597-disposable-proof-trials/git-fsck-before.log
- .analysis/handoff/after597-disposable-proof-trials/git-fsck-after.log
- .analysis/handoff/after597-disposable-proof-trials/python-cache-maintenance.json

Total gross after597 allocated bytes reclaimed across these three
independent operations: 95,522,816 bytes, about 91.10 MiB. This is
actual measured storage maintenance, NOT 91 MiB of recovered game
source, new acceptance credit or an excuse to delete active native
executable/object evidence. The before-after manifest and small audit
snapshots themselves consume additional private disk space.

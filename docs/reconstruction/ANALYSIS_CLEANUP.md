# Private reconstruction artifact retention and cleanup

**Current maintenance checkpoint: 2026-10-08.** `.analysis/` is ignored
private working state, not source control. Its size includes original target
observations, attested compiler/Ghidra tooling, diagnostic images, complete
successful cold replay proofs and disposable temporary builds. **Age and size
alone do not prove that a file is disposable.** Old 2026-10-06 closeout
statistics and earlier smaller cleanup campaigns are historical, not a
statement of the present source/Oracle baseline.

## Required / guarded material

Retain:

- Immutable Japanese TH03 target and derived/stored/decoded reference input
  bytes used by current evidence. Do not alter the original byte provenance.
- `.analysis/toolchain/`, `.analysis/targets/`, `.analysis/runtime/`,
  `.analysis/ghidra/`, `.tools/`, `ghidra-project/` and `_reference/` **in full**.
  Wine prefix files, linkers/compilers, Ghidra databases and symlinked
  runtime state cannot be recovered merely by leaving one receipt behind.
- All concrete `.analysis` paths used by tracked configuration and current
  Markdown (not just paths appearing in the evidence CSV), transitive JSON
  input guards, and any hash-bound recorded Factory text query. The earliest
  randring cold scaffold's OP/MAINL/ZUN generated EXE/MAP files are live
  inputs of `config/th03_decoded_code_review.toml` and
  `config/th03_zun_launcher.toml` and must not be removed.
- Entire completed cold receipt trees that are still referenced by the
  evidence ledger/docs, including frozen source, reference archive, object
  outputs and complete logs. Preserve meaningful referenced compiler and
  failed-gate transcripts; never weaken the accepted byte/MAP/ordered-MZ
  Oracle to accommodate a cleanup.

Disposable: unreferenced completed/failed receipt **directories as units**,
unused experimental objects/source trees, build/dist/out/cache directories
and unguarded Python/pytest/mypy caches. Do not strip files out of a
**referenced** receipt tree. A current dry run/rebuild must finish before any
new apply. `scripts/clean_generated.py` follows these constraints; concrete
tracked-document references are protected in both aggressive receipt
pruning **and** ordinary cleanup (a 2026-10-08 protection fix with tests).

## Owner-authorized 2026-10-08 cleanup

Initial `.analysis/` disk allocation: approximately **14 GiB**; MAIN exact
replays used approximately **7.2 GiB**, much of it unrelated historic cold
workspace duplication. The audited first pass was:

    python3 -B scripts/clean_generated.py --prune-unreferenced-receipts --keep-analysis .analysis/cleanup-20261008
    python3 -B scripts/clean_generated.py --prune-unreferenced-receipts --keep-analysis .analysis/cleanup-20261008 --apply

It removed **275 whole-tree/file/cache entries**, accounting for roughly
**4,376 MiB (4.27 GiB)**. The normalized dry-run and actual deletion path
sets matched exactly. **12 protected SHA-256 input guards matched before and
after**, including the current HUD/Hyper exact receipts, historic diagnostic
cold EXEs/MAPs, active Marisa and frontier reviews and original targets.
Target/toolchain/runtime/Ghidra directories were unchanged. A one-line
bookkeeping error in the *audit* initially included the dry-run summary in the
candidate count; that was corrected and the path list and protected hashes
were reverified, without reapplying any deletion.

Audit and path-by-path logs:

    .analysis/cleanup-20261008/receipt.json
    .analysis/cleanup-20261008/plan.log
    .analysis/cleanup-20261008/applied.log

A second guarded pass was performed **after the handoff was condensed**:

    python3 -B scripts/clean_generated.py --prune-unreferenced-receipts --keep-analysis .analysis/cleanup-20261008 --keep-analysis .analysis/cleanup-20261008-followup --apply

Its plan was reviewed before deletion. It pruned exactly **five** newly
unreferenced historic checkpoint directories/logs, another **111.2 MiB**,
and reverified the exact deletion path set plus the same 12 SHA-256 guards.
Follow-up audit:
`.analysis/cleanup-20261008-followup/receipt.json`.
The two major 2026-10-08 passes removed **280 file/tree entries and
approximately 4,487.2 MiB (4.38 GiB)**. After post-cleanup verification,
three regenerated Python cache trees (another 4.8 MiB) were removed by
conservative **non-aggressive** cleanup; exact plan and apply logs are stored
in `.analysis/cleanup-20261008-followup/`. **Grand total: 283 entries,
approximately 4,492.0 MiB (4.39 GiB) reclaimed.** Re-running the final
original-code Oracle creates one intentionally retained 73 MiB full proof
tree, so the current `.analysis/` is approximately **7.8 GiB**, down from
roughly 14 GiB before cleanup.

The remaining `.analysis/` is still large because referenced complete cold
proof trees, the required Wine toolchain and large original-target diagnostic
JSON data are **not** equivalent to stale build caches. Do not blindly delete
these to make disk usage smaller. If more space is needed, first examine
live ledger/docs/JSON dependencies and explicitly update retention proof
contracts before any guarded second pass.

Run the **dry run** after further source or documentation edits; it makes no
changes without `--apply`. If an active experimental run has no recorded
ledger/doc reference yet, pin it explicitly:

    python3 -B scripts/clean_generated.py --prune-unreferenced-receipts --keep-analysis .analysis/ACTIVE_RUN

The receipt and tests, not filesystem timestamps, determine what can go.

## Historical cleanup checkpoints

The **2026-10-06 closeout** removed 32,600 obsolete files / 450,320,719
bytes (429.5 MiB) under its own earlier guard policy. It is recorded in
[the historical closeout](../CLOSEOUT.md) and the preserved receipts at
`.analysis/closeout/sol-closeout-20261006/receipt.json` and
`.analysis/closeout/sol-closeout-post-ci-20261007/receipt.json`.
Other earlier shared PI, music, CDG, input and terminal-source cleanup
experiments are retained in historical Git and bounded subsystem reviews;
they do **not** supply the live 2026-10-08 source/Oracle denominator.

## Post-cleanup source/Oracle integrity check

No accepted source, manifest, exact-function/extent ledger, pinned original
byte file or previously accepted physical owner was replaced by cleanup.
The first and follow-up cleanup audits together verified the live files and
12 protected SHA-256 invariants across both passes. The current exact Oracle
was then replayed against the real post-cleanup worktree:

    python3 -B scripts/replay_th03_main_exact_units.py --run-id gpt-web-cleanup-maintenance-default-final-20261008

Result: **PASS**, two serial cold builds, 334 reviewed exact functions /
52,199 function bytes / 53,122 owned CODE bytes, original MAP, original
ordered MZ fixups, 20 build outputs, all 391 game OMF objects and DOS
behavior probes. Receipt:
`.analysis/th03-main-exact/gpt-web-cleanup-maintenance-default-final-20261008/receipt.json`.

A fresh complete CI attempt has **648 tests / 125 missing-Unicorn
import errors / 167 skips**; it does **not** pass on this host. The
remaining post-unittest gates were rerun separately and PASS, including
headless Ghidra/target/toolchain identity and the negative controls. Logs:
`.analysis/cleanup-20261008-followup/ci.log` and
`.analysis/cleanup-20261008-followup/postgates.log`.

The authenticated code reconstruction baseline stays unchanged by this
housekeeping work; the historical cleanup receipts and current cold
acceptance proof remain accessible and are not obsolete build caches.

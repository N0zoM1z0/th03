# Reconstruction workflow

1. Inspect Git state, the handoff, and run `scripts/preflight.py`.
2. Choose one artifact and bounded segment:offset ownership question.
3. Run `scripts/ghidra.py ARTIFACT check`. Distinguish packed storage and
   decoded code before interpreting function boundaries.
4. Review callers, exits, shared tails, data, relocations and near/far ABI.
   Record target observations separately from ReC98/TH04 hypotheses.
5. Recover natural source under the owning artifact and run pinned compiler
   probes. Do not replace unresolved code with target bytes or inert stubs.
6. Record source presence separately from structural, runtime and exact state.
   Exact promotion requires all `config/oracles.toml` gates over one extent.
7. Finish with focused checks, `scripts/ci.py`, whitespace checks and a concise
   handoff update. Preserve private receipts but keep conclusions replayable.

All tool use is headless. Serialize Borland writers and keep database exports
under `.analysis`. A reference build, function list or screenshot is not
proof of a reconstructed TH03 product.

## Local artifact retention

.analysis/ is an ignored replay/work directory, not source control. Keep the
specific receipt/review/log files referenced by tracked config or documentation,
plus the offline toolchain/runtime/Ghidra attestation trees required to replay
them. Protect *every concrete existing file named by tracked documentation or
configuration*, including standalone review JSON outside a receipt tree, as well
as transitive JSON input guards and ledger locations. The regular cache cleanup
must protect those concrete references as well as the optional aggressive
receipt-pruning step. A retained receipt run is kept as a complete proof tree, including its
frozen source/object/output/reference material; do not hollow out a receipt that
current evidence or documentation still names. Failed or duplicate receipt runs
that are no longer reachable from current evidence/docs may be removed as whole
runs. Build/cache directories such as build/, dist/, out/, .cache/, Python
__pycache__, pytest and mypy caches are disposable.

Use `python3 scripts/clean_generated.py` for a conservative dry run and add
`--apply` only after reviewing it. To include complete unreferenced receipt runs
in the cleanup, use `--prune-unreferenced-receipts`; this remains a dry run
unless `--apply` is also present. If an active experimental run is not yet
recorded in tracked evidence/docs, protect it explicitly with
`--keep-analysis .analysis/PATH` before applying aggressive pruning.

The owner-authorized guarded 2026-10-08 run and its path-by-path before/after
hash audit live in `.analysis/cleanup-20261008/receipt.json`; see
[analysis cleanup policy](reconstruction/ANALYSIS_CLEANUP.md). A cleanup
changes neither exact source credit nor prior binary comparison rules.

Do not delete _reference/, .tools/, ghidra-project/, the retained runtime
images, or the active toolchain merely to reduce disk usage. Protected
toolchain/runtime/Ghidra trees must be preserved as complete directory trees,
including empty Wine user directories and symlinks; deleting only their files
is not sufficient. If a tracked document intentionally shows an output path
for a command, that path need not already exist; do not rewrite historical
commands just to make every literal .analysis/ path resolve.

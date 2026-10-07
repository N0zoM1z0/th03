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
them. Once a receipt and replay command are retained, intermediate cold-build
copies (source/, obj/, bin/, reference.tar) and failed/duplicate probe runs may
be deleted. Build/cache directories such as build/, dist/, out/, .cache/,
Python __pycache__, pytest and mypy caches are disposable.

Do not delete _reference/, .tools/, ghidra-project/, the retained runtime
images, or the active toolchain merely to reduce disk usage. Protected
toolchain/runtime/Ghidra trees must be preserved as complete directory trees,
including empty Wine user directories and symlinks; deleting only their files
is not sufficient. If a tracked document intentionally shows an output path
for a command, that path need not already exist; do not rewrite historical
commands just to make every literal .analysis/ path resolve.

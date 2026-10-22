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

Keep source, canonical targets, the working toolchain/databases and evidence
needed to verify the current checkpoint. Remove caches and unused experiments
when no build is using them; remove discarded runs as whole directories.
Summarize useful conclusions before deleting an experiment. Historical notes
may refer to discarded outputs and do not imply those outputs are retained.

`scripts/clean_generated.py` provides an optional conservative dry run (`--apply`
performs its listed removals). A small, explicitly selected cleanup does not
require a repository-wide audit. Never delete shared tool state or another job's
files as part of routine cleanup.

### Serial cold-build wall allowance

The foreground MAIN serial adapter permits 300 seconds only for each of its
two exact, round/path/command-validated cold `build.bat` calls. The original
replay stays byte-identical; all other calls retain its 180-second limit.
The outer 900-second supervisor, one CPU, nice>=10, local Tup jobs1 and owned
process cleanup remain unchanged. Scheduling sidecars record original/effective
limits; inner build timeouts preserve captured partial stdout before failing.
The full game and research graph is still built, with all original acceptance
gates. No timeout, partial output or completed game products imply replay PASS.
A fresh run ID and fresh pinned plan are required after a failed run.

## Bounded replay staging and historical proof guards

Preserve historical proof trees in place and guard their bytes and modes before
and after a run. Materialize only the current build/import dependency closure
into a new runtime; do not recursively copy older frozen proof trees into each
new replay. Keep full historical guards and referenced evidence protected under
the existing retention rules. Per-run guard inventories remain ignored evidence,
not duplicated maintained runner frameworks or large committed manifests.

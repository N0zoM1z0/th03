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

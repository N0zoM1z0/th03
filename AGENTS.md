# TH03 reconstruction

Read `docs/RE_HANDOFF.md`, `docs/ARCHITECTURE.md`, `docs/RE_WORKFLOW.md` and
the local `th03-re` skill. Inspect Git and run `python3 scripts/preflight.py`.

- Use the Japanese targets pinned in `config/targets.toml`; never replace them
  with translated, patched or reference-game files. Provenance remains
  `candidate-local-attested`. Re-attest a Ghidra database before using it.
- Product source belongs in `src/main`, `src/op`, `src/mainl`, `src/zun` and
  proved `src/shared`. MAINL is the ending. Use local dependencies or explicit
  `compat/rec98` forwarding. `.c`/`.cpp`/`.asm` are TUs; `.inl` is a bounded include.
- Preserve 16-bit widths, ABI, segments, packing, x87 and compile/link order.
  Exact means complete raw-byte and ordered-relocation equality, reviewed
  ownership/layout, affected behavior and reproducible cold builds. No padding,
  target-byte arrays or object patches to manufacture equality.
- Keep useful findings in source, ledgers and the concise handoff. Generated
  analysis and decompiler output are provisional. Do not claim whole-game
  progress from reference builds or partial byte counts.
- Use local headless tools, with DISPLAY/WAYLAND_DISPLAY empty; no Factory MCP.
  Limit heavy work to one CPU at nice10. Serialize Borland/Wine writers and
  preserve the local prefix. Keep private tools/targets/assets out of Git.
- Keep one working build. Old verification, logs, experiments, caches, installer
  downloads and history documents can be deleted; references do not require
  retaining them. Regenerate checks when needed.

Finish with focused checks, `python3 scripts/ci.py` and `git diff --check`.
Commit format: `gpt-6-astra-medium: xxx ~`.

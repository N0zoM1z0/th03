# TH03 reconstruction

Prioritize natural source recovery and exact native output. Read the concise
`docs/RE_HANDOFF.md` and relevant parts of `docs/RE_WORKFLOW.md`,
`docs/ARCHITECTURE.md` and the local `th03-re` skill. Inspect Git; run preflight
when starting a session or when the environment/targets change.

- Use the Japanese targets pinned in `config/targets.toml`, with
  `candidate-local-attested` provenance. Never substitute translated, patched
  or reference-game binaries. Re-attest a Ghidra database before using it.
- Product source belongs in `src/main`, `src/op`, `src/mainl`, `src/zun` and
  proved `src/shared`. MAINL is the ending. Use local dependencies or explicit
  `compat/rec98` forwarding. `.c`/`.cpp`/`.asm` are TUs; `.inl` is a bounded include.
- Preserve 16-bit widths, ABI, segments, packing, x87 and compile/link order.
  Exact requires complete raw bytes, literal ordered relocations, reviewed
  ownership/layout and reproducible native output. No padding, target-byte
  arrays or object patches to manufacture equality.
- Tests serve a specific reconstruction question. Do not require allocation
  failures, null pointers, exhaustive input/flag matrices, full-memory emulator
  models or large instruction-mutation suites for each unit. Add a small
  targeted probe only when it resolves an actual source, ABI or codegen doubt.
  Preserve original unchecked behavior; do not add defensive product fixes.
- Rebuild/check the affected scope. Reuse and validate an unchanged cold pair;
  do not repeat full native cold replay or ancestor runtime chains every turn.
- Use direct local headless tools with DISPLAY/WAYLAND_DISPLAY empty. Limit
  heavy work to one CPU at nice10; serialize Borland/Wine writers and preserve
  the local prefix. Keep private tools/targets/assets out of Git.
- Keep useful findings in source, ledgers and the concise handoff. Do not turn
  diagnostic test counts or reference builds into source-exact progress.
  Keep one working build; obsolete verification, logs and experiments can be
  deleted. Preserve actual current build inputs, tools and fixed targets.

Finish with affected checks and `git diff --check`. Full `python3 scripts/ci.py`
is available for broad infrastructure changes; it is not a per-turn gate or a
requirement for ordinary source/ledger updates. Commit substantial progress
using `gpt-6.1-sol: xxx`.

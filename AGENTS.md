# TH03 reconstruction rules

Read `docs/RE_HANDOFF.md`, `docs/ARCHITECTURE.md`, `docs/RE_WORKFLOW.md`
and the relevant local skill before target-dependent work. Run
`python3 scripts/preflight.py` and inspect Git state first.

## Targets and evidence

- Use the Japanese YUMEZIKU targets pinned in `config/targets.toml`.
  Their canonical ignored paths are `.analysis/targets/th03/op.exe`,
  `main.exe`, `mainl.exe`, and `zun.com`. Never replace them with translated
  files, patched images, or ReC98 outputs.
- Provenance is `candidate-local-attested`; an independent pristine-dump
  attestation is still unknown.
- Re-attest the selected Ghidra database with `scripts/ghidra.py ARTIFACT check`
  before using its observations. Automatic functions and decompiler output
  are provisional, not independent Oracles or authored-source progress.
- Keep observed target facts, compiler observations, runtime observations,
  cross-game corroboration and inference distinct.
- Track units, evidence, hypotheses and knowledge in the CSV ledgers.
  Never inherit TH04 or ReC98 exactness claims.
- `exact` requires cold reproducible builds, complete raw byte equality,
  reviewed ownership, ABI/layout/relocations and the complete Oracle set.
  Do not manufacture equality with target-byte arrays, padding or fake ABI.

## Source and tool ownership

- Product source belongs to `src/main/`, `src/op/`, `src/mainl/`, `src/zun/`
  and proved shared code under `src/shared/`. MAINL is TH03's ending product.
  Do not create directories named `exact`, `partial` or `modules`.
- Treat `.c`, `.cpp` and `.asm` as translation units, `.inl` as bounded includes.
- Preserve 16-bit widths, near/far/Pascal ABIs, memory model, DGROUP,
  segment ownership, packing, x87 behavior and translation/link order.
- Reference source is untrusted candidate material. Product dependencies must
  be localized or explicitly forwarded through `compat/rec98/`; no direct
  product includes of reference-game or `libs/`/`platform/` paths.
- Use only headless tools. Clear DISPLAY and WAYLAND_DISPLAY; Ghidra uses
  `analyzeHeadless` with Java headless mode. Wine runs console tools only;
  if a virtual X server becomes necessary, use Xvfb without a visible desktop.
- Keep one Borland/Wine writer at a time and preserve the game-local prefix.
  Private tools belong under `.tools/` or `.analysis/toolchain/`; projects
  belong under ignored `ghidra-project/`, exports under `.analysis/`.
- Never commit targets, game assets, proprietary tools, archives or credentials.
- Factory is the shared MCP entry point. Register native command providers;
  do not create another game-specific HTTP MCP endpoint. Hot deployment must
  preserve existing service processes, public URL and tool metadata.

## Finish

Run focused verification, `python3 scripts/ci.py`, and `git diff --check`.
Update the concise handoff when verified facts or blockers change. Put durable
findings in ledgers, bounded notes or replayable scripts. Do not claim a whole
game build from a reference build or a compiler smoke result.

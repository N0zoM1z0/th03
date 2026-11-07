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
  Preserve the *entire active source-bound receipt DAG*, including both raw
  OBJ/LIB/EXE/MAP rounds and writer logs. Delete only audited superseded
  branches and disposable experiments, not files inferred "unused" from age.
  The last source-linked CRT-native-output deletion audit is the historical
  after520 guard (258 stages / 5,760 protected files); it is NOT a current
  after596/after587 DAG prune authorization. The after597 maintenance retired
  only three externally unreferenced, exploratory BOSS compiler trees
  (5,331 files / 78,938,112 allocated bytes), preserving their original
  receipts, logs and per-file SHA-256 manifest. See
  docs/STORAGE_HANDOFF_CURRENT.md and
  scripts/cleanup_after597_handoff_storage.py --verify for the present
  restricted policy. The later after710 handoff retired only six
  unreferenced failed source-verifier tool-config stages (12 small
  trial trees / 93 files / 1,847,296 allocated bytes) and regenerable
  Python caches; it did NOT prune any completed native source proof.
  Use docs/STORAGE_HANDOFF_AFTER710.md and its strict, one-time
  script/manifest to audit that bounded action.
  Never apply old after439/388/319/511-source cleanup
  tools to this checkout. A generic generated-file preview does not prove
  that native source-review dependency trees can be discarded.
  Preserve tools/targets.

Finish with affected checks and `git diff --check`. Full `python3 scripts/ci.py`
is available for broad infrastructure changes; it is not a per-turn gate or a
requirement for ordinary source/ledger updates. Commit substantial progress
using `gpt-web: xxx` (current user-required format).

# TH03 reconstruction

## Highest priority: lightweight exact reconstruction and useful knowledge

These are the user's current workflow requirements. They override older
instructions that mandate broad CI, repeated preflights, document/source-pin
refreshes, per-checkpoint audits or extra workflow machinery. Preserve the
actual exactness, target identity, natural-source and state-isolation rules.

- Prioritize exact reconstruction and reusable knowledge. Use the shortest
  useful loop: inspect relevant state, analyze/edit, compile and compare the
  affected scope, retain useful learning, and create a coherent checkpoint.
- Use existing repository scripts and composable Bash. Add only the smallest
  change needed for an observed problem. Do not introduce a framework, schema,
  registry, state machine, generalized validator, test family or reporting
  process merely to make a local reconstruction task look more engineered.
- Documentation, knowledge and handoff edits require no compiler, analyzer,
  full CI, cold replay or receipt refresh. Inspect the diff. Check syntax only
  for machine-readable inputs actually changed.
- Source changes need the complete affected exact comparison, including its
  owned extents and relocations. Recheck known consumers of changed shared
  inputs. Tool changes need relevant positive/negative cases and a bounded
  real smoke. Run a broad suite only for an explicit request or a demonstrated
  impact that cannot be narrowed; state that reason first.
- Do not add tests or live freshness gates for prose hashes, prompt wording,
  progress totals, handoff source-SHA tables or ordinary source spelling.
  Bind exact evidence to executable inputs and relevant verification settings.
  Keep Git metadata as provenance. A document genuinely consumed by a build
  remains a build input. Never edit historical receipts to manufacture a pass.
- Plain Markdown is sufficient for knowledge: record the finding, applicable
  target/compiler/scope, evidence links, useful failed attempts and open
  questions. No mandatory JSON conversion, promotion workflow or test per note.
  Search relevant sections; do not read an entire large knowledge journal.
- Write documentation and knowledge in natural, fluent English. Lead with the
  concrete finding and connect the evidence and next action clearly. Remove
  filler, circular restatements, repeated conclusions and unnecessary jargon.
  Do not add defensive-claim boilerplate. State a real uncertainty or scope
  limit once when it changes a decision; do not repeat disclaimers about what
  a note does not prove, certify or authorize. Prefer a small useful note over
  an exhaustive report that is difficult to read.
- Keep handoff focused on current work, evidence references, blockers and the
  next useful action. Generate progress from canonical ledgers; avoid manual
  duplicate counts, recurring full reports and unrelated documentation chores.
- Preserve dirty/untracked work, targets, useful evidence, game-specific Wine
  prefixes and analyzer projects. Exactness still requires a complete strict
  comparison; knowledge and successful commands alone confer no exact credit.


Prioritize natural source recovery and exact native output. Read the short
`docs/RE_HANDOFF.md`, relevant parts of `docs/RE_WORKFLOW.md` and
`docs/ARCHITECTURE.md`, and the local `th03-re` skill. Inspect Git; run
preflight before target-dependent reconstruction or after target/runtime
changes. Documentation and CI edits do not need private-tool preflight.

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
  Keep necessary original inputs, installed tools, Ghidra projects, maintained
  source and exact ledgers, reproducible build/complete-compare scripts, and
  concise useful findings. Build outputs are regenerable; keep only the
  working inputs current scripts still require. Historical archives,
  duplicate evidence, old trials and cleanup reports need no permanent
  retention, and documentation references are not a reason to keep them.
  Retain a special compiler context only when an unresolved problem actually
  needs it and it is difficult to rebuild; explain that need briefly.
  Do not create new audits, manifests, archives or reports merely to delete
  old ones. Remove obsolete references with the files. Factory supplies
  shared executable code; this game's mutable runtime state stays isolated.
  See docs/STORAGE_HANDOFF_CURRENT.md for the short retention guidance.

Finish with affected checks and `git diff --check`. `python3 scripts/ci.py`
is a fast, standard-library-only syntax/whitespace check, not a full test or
native-verification gate. It need not be repeated after every commit.
Documentation-only changes need only diff inspection and whitespace checking.
Run relevant tests or native comparisons explicitly when the change needs them.
Commit substantial progress using `gpt-web: xxx` (current user-required format).

## Shared Factory runtime

Follow [the shared tools instructions](docs/SHARED_TOOLS.md). Ghidra/JDK and
Wine executables are shared through Factory; repository scripts also work
without MCP. Use `scripts/shared_runtime.py` and the existing compiler/analysis
frontends. Keep this game's prefix, analyzer project, Java home/cache, target
and compiler profile isolated. Do not install duplicate tools or inherit
another game's `WINEPREFIX`. This shared-runtime procedure supersedes older
per-repository installation instructions; pinned versions/hashes still apply.

# TH03 reconstruction workflow

## Start a bounded unit

1. Read `AGENTS.md`, the [handoff](RE_HANDOFF.md), [architecture](ARCHITECTURE.md)
   and local `th03-re` skill. Inspect Git and run preflight.
2. Select a complete source/ownership question. Re-attest the chosen database
   before using Ghidra observations; inferred boundaries remain hypotheses.
3. Recover natural source using the fixed Japanese targets. Keep 16-bit widths,
   segments, near/far/Pascal/cdecl ABI, packing, x87 and compile/link order.
4. Prove complete raw bytes, literal ordered relocations, ownership/MAP/layout,
   affected behavior and independent cold reproducibility. All gates are in
   `config/oracles.toml`; compiler success and partial byte counts are insufficient.
5. Record findings in source, ledgers and the concise handoff. Run focused checks,
   full CI and whitespace checks, then commit and push an English checkpoint.

Use Factory MCP with the registered TH03 live repository, as authorized by the
user on 2026-10-26. Execute the existing headless tools through the repository
shell; preserve target attestation and every acceptance gate. Serialize Borland/Wine writers and
preserve the game-local prefix. Use `.venv/bin/python` for Capstone/Unicorn.

## Resource limits

The following shell helper applies the current machine's one-CPU/nice10 policy
and bounded Java settings to every Python command in this page:

```sh
th03_cpu=16  # choose an allowed CPU on another host
th03_run() {
  taskset -c "$th03_cpu" nice -n 10 env DISPLAY= WAYLAND_DISPLAY= \
    _JAVA_OPTIONS='-Xmx768m -XX:ActiveProcessorCount=1' .venv/bin/python "$@"
}
th03_run scripts/preflight.py
th03_run scripts/ghidra.py th03-mainl check
```

## Fresh complete chains

Run only the product chain affected by source/recipe changes. These recreate
native inputs and run the prerequisite review stages in order:

```sh
th03_run scripts/replay_th03_main_native.py
th03_run scripts/review_th03_op_music_state_work.py
th03_run scripts/review_th03_mainl_staff_roll_work.py
th03_run scripts/review_th03_zun_ongchk_work.py
```

OP/MAINL/ZUN complete-file equality includes DIET storage. It does not imply
whole-product source ownership. MAIN retains one CODE alignment byte and its MZ header gap; all literal
relocations match. Its VS module is explicitly prebuilt vendor context, freshly
extracted during each otherwise source-rebuilt game graph.

After new OP or MAINL cold pairs, refresh their joint input/ending-wait witness:

```sh
th03_run scripts/review_th03_shared_input_work.py
```

Where supported, `--current-cold` revalidates the **entire existing**
source/SDK/recipe/output graph and reruns the selected stage. Use it when native
inputs are unchanged. It does not repair stale prerequisite reports; replay
changed stages in dependency order or use the default complete chain. Stage
`INPUTS`, `witness()` and `current_scope()` definitions are authoritative.

OP main-menu context migration compares all eight complete prior scope
observations against Git checkpoint `d118c46`. Fresh decoded/stored outputs must
match; native phase-log hashes need not. Current cold source/tool/SDK/output
bindings still pass their own gates. Startup additionally preserves the complete main-menu observation at `dbf8a52`.
The separate DATA review preserves the complete startup observation at `9402601`.
The historical 33-owner cohort is immutable
and separate from current refined source scopes.

## Publication and final checks

Refresh affected publications after review or shared-verifier changes, then
regenerate progress. Shared helpers can invalidate more than one product:

```sh
th03_run scripts/publish_th03_op_work_scopes.py
th03_run scripts/publish_th03_mainl_work_scopes.py
th03_run scripts/publish_th03_zun_work_scopes.py
th03_run scripts/progress.py
th03_run scripts/ci.py
git diff --check
```

Current reports/publications bind live source, recipes, installed tools and
complete outputs. Historical private replay receipts are not current proof.
Current builders are source-only; keep only required inputs and one working
build per product. See the handoff for paths, including the required reference tar.

The frozen ReC98 candidate index retains historical `python3 scripts/replay_*`
unit commands and evidence unions. During source migration, preserve this
diagnostic namespace; record the current review command in its new evidence
row and scoped publication. Candidate-index source/exact flags stay separate.

## Behavior and ownership boundaries

- Execute actual owned nested helpers. Preserve caller frames and static state
  when composing contracts; OP's physical contexts provide an existing example.
- Check stated registers/high halves/segments, defined flags, ordered stores and
  complete memory. Declare private stack windows and external reply assumptions.
  Preserve unchecked indices, aliasing and the unsanitized fourth cfg byte.
- Separate instructions, inline switch storage, initialized DATA, BSS, linker
  gaps and proved unreachable bytes. Callback selection alone does not own a
  callback body. Source/ABI controls must not manufacture output equality.
- Prove a closed polling/retry CFG and its live invariant before reporting a
  nonterminal prefix. Instruction-budget exhaustion is not such proof. Keep
  ordinary entry and explicit continuation cases separate.
- Counter/device/file/graphics replies are bounded interfaces. They do not prove
  elapsed frames, physical IRQ/audio/pixels or successful executable replacement.
- Explicit NOPs, target-byte arrays, object patches and isolated alignment
  controls cannot substitute for natural producer/layout proof. Preserve current
  open padding/storage questions rather than promoting them accidentally.

## Disposable output

Preview `scripts/clean_generated.py --prune-unreferenced-receipts`, inspect the
selection, then add `--apply`. Use `--keep-analysis PATH` for an active input.
References alone do not require keeping obsolete runs. Actual current build
inputs, fixed private targets, the Wine prefix and attested tool trees remain.

After CI, `clean_generated.py --caches-only --apply` removes standard cache/build
output while leaving all `.analysis` state alone. Read-only status checks can use
`PYTHONDONTWRITEBYTECODE=1`; full CI deliberately recompiles Python caches.

# TH03 reconstruction workflow

## Recover and compare

1. Inspect Git and the concise [handoff](RE_HANDOFF.md). Run preflight at session
   start or after environment/target changes. Read architecture where relevant;
   attest a database before using Ghidra observations.
2. Select a complete function or source/ownership question. Recover natural
   source from the fixed Japanese target. TH04 and ReC98 are references;
   decompiler boundaries and earlier notes remain hypotheses.
3. Preserve 16-bit widths, segments, near/far/Pascal/cdecl ABI, packing, x87,
   translation-unit boundaries and compile/link order.
4. Compare the complete affected raw extent, literal ordered relocations and
   native OMF/MAP ownership/layout. Keep CODE, inline tables, DATA, BSS and
   linker gaps distinct. Compiler success alone is insufficient; padding,
   embedded target bytes and object patches cannot manufacture exactness.
5. Check reproducibility for changed native inputs. Reuse and validate a current
   cold pair when source/recipe inputs are unchanged. Rebuild affected units;
   a complete native chain is needed when changed shared inputs actually affect
   that chain, not at every turn.
6. Record useful findings and exactness limits, run affected checks plus
   `git diff --check`, and commit substantial progress locally with
   `gpt-web: xxx`. Do not push without authorization.

## Keep verification proportional

`config/oracles.toml` defines exact requirements. Runtime traces and semantic
probes are supporting evidence. Use a small probe when native output or ABI
analysis leaves a specific question unresolved.

Allocation failures, null pointers, artificial aliasing, exhaustive input/flag
matrices, large mutation suites, complete-memory emulator specifications and
closed-loop proofs are **not routine acceptance requirements**. Preserve the
original unchecked code; reconstruction is not a product-hardening task.
Do not infer successful execution from a stopped emulator or count supporting
test cases as source-exact progress.

Existing historical runtime receipts are records of earlier observations. They
do not require preserving or rerunning their diagnostic harnesses. Keep the
original receipts honest; do not refresh their hashes to imply a new replay.

Full `scripts/ci.py` is appropriate for changes to shared build, verifier or
tracking infrastructure. A bounded source change normally needs its native
comparison and directly relevant checks, rather than every product's runtime
suite and database check.

## Local tools and commands

Use direct local tools, as explicitly authorized by the user. Empty displays,
one CPU at nice10 and serialized Borland/Wine writers remain the resource policy:

```sh
th03_cpu=16  # choose an allowed CPU on another host
th03_run() {
  taskset -c "$th03_cpu" nice -n 10 env DISPLAY= WAYLAND_DISPLAY= \
    _JAVA_OPTIONS='-Xmx768m -XX:ActiveProcessorCount=1' .venv/bin/python "$@"
}
th03_run scripts/preflight.py
th03_run scripts/ghidra.py th03-op check  # when using this database
th03_run scripts/review_th03_op_music_menu_work.py
```

The Music Room check compares its complete 14-procedure native carrier and
ordered relocations; it does not run an emulator matrix or rebuild unchanged
native inputs. `--check` also compares the saved native receipt.

Existing product builders are `build_th03_main_work.py`, `build_th03_op_work.py`,
`build_th03_mainl_work.py` and `build_th03_zun_work.py`. Use the affected review's
`--current-cold` route where available. A stale native source/recipe binding
requires rebuilding its affected dependency chain, not editing receipt hashes.

When an accepted source scope changes, update its publication and regenerate
progress with `scripts/progress.py`. Source presence and accepted ownership are
separate; complete executable equality can still contain unowned vendor context.
OP/MAINL/ZUN also compare canonical DIET storage. MAIN retains its documented
CODE alignment/header differences.

## Working files and retention

The [current storage audit](STORAGE_HANDOFF_CURRENT.md) is the active
source-bound cleanup authority. As of `after388`, preserve **all 126 MAINL
receipt stages**, including the source/driver/parent receipts, writer logs
and both full native OBJ/LIB/EXE/MAP vectors. Do not delete a historical
`after*-round*` file merely because its name is old. Preserve all legal
original targets, installed Wine/Borland and Ghidra/JDK tool trees, the
accepted ledgers, runtime/cold inputs and the old-named `reference.tar`.

The general `scripts/clean_generated.py` preview is **not** a complete
native-proof dependency graph; it can select live dynamically referenced
files. Never blanket-apply it on this checkout. The scoped
`cleanup_mainl_after388_handoff.py` is **dry-run by default**, walks the
live builder DAG, and deletes only checked superseded alternate-mode
vectors and regenerable uncited disassemblies when explicitly applied. It
fails closed when a newer source builder/receipt appears. Regenerable Python
caches can be cleaned separately using `clean_generated.py --caches-only
--apply`. Always rerun the affected review and tests after cleanup.

The older [319-source cleanup report](STORAGE_HANDOFF_2026-11-05.md) and
[November 3 report](STORAGE_HANDOFF_2026-11-03.md) remain historical
snapshots; their paths and numerical totals must not be copied into a
current handoff.

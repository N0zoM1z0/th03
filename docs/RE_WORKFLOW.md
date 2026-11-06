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

## Latest protected-storage policy

The last applied native-deletion audit covers the after520 CRT prefix:
**258-stage, 5,760-file active native proof graph**. Use
[the current storage policy](STORAGE_HANDOFF_CURRENT.md)
and the pinned `cleanup_mainl_after520_handoff.py` for
dry-run-first, SHA-verified retired-output cleanup. It fails
closed on after521+ source stages. Older after439/after388
cleanup tools are historical; never bypass their guards
or infer disposability from a generic cleanup preview.
Cache-only cleanup is separate and does not touch `.analysis`.

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
th03_cpu="$(python3 -c 'import os; print(min(os.sched_getaffinity(0)))')"
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

The [latest applied after520 deletion audit](STORAGE_HANDOFF_CURRENT.md)
protects its historical prefix of **258 stages / 5,760 uniquely referenced receipt,
writer-log and native output files**, with both full raw
OBJ/LIB/EXE/MAP rounds retained. The older after439 audit
(177 stages / 4,464 files) is
[historical](STORAGE_HANDOFF_AFTER439.md), not the latest.
Never discard an old after-stage file based solely on age,
and preserve original Japanese targets, Wine/Borland and
Ghidra/JDK tool identities, source/acceptance ledgers,
runtime/cold evidence and the original reference.tar.

The general scripts/clean_generated.py preview is NOT a
complete native proof dependency graph; do not blanket-apply
it or use unreferenced-receipt pruning. The pinned
scripts/cleanup_mainl_after520_handoff.py used the then-current source DAG
and deleted15 completed superseded alternative-mode artifacts. It now rejects
this after554 checkout; the historical zero-candidate result is not a current
cleanup authorization. The after439/after388 cleanup scripts are
frozen historical controls. New after521+ source stages require
another independently audited active DAG and guard. Cache-only
cleanup is separately available for fully regenerable Python
bytecode, without touching .analysis state.
Always rerun the scoped review after any actual cleanup.

The older [319-source cleanup report](STORAGE_HANDOFF_2026-11-05.md) and
[November 3 report](STORAGE_HANDOFF_2026-11-03.md) remain historical
snapshots; their paths and numerical totals must not be copied into a
current handoff.

# TH03 reconstruction workflow

> Current workflow: follow the **Highest priority** section in `AGENTS.md`.
> Prefer affected exact comparisons and useful Markdown knowledge. Ordinary
> notes do not require full CI, native replay or document-hash/pin refreshes.
> Older broad validation instructions apply only when their impact is relevant.


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

## Scoped current-source native check (MAIN)

Use the original Turbo C++ 4.02 and complete normal TLINK response. The
current source-bound stages are listed in [generated progress](PROGRESS.md);
`status.py` checks them with the read-only native reviewer. Select the affected
owners from that current list rather than copying historical stage numbers.

Select **only the original physical TUs whose maintained C++ or actually
consumed implementation .inl files changed**. Use a new unused DOS-safe
stage, two independent original compiler rounds and two complete normal
MAIN links:

    STAGE=afNNNx  # choose an actually unused stage
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage "$STAGE" --units ba_koto,hitcirc
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage "$STAGE"

Compare complete CODE, literal ordered FIXUPPs, PUBLICs, source/header/.inl
bindings, segment geometry, full normal MAIN and ordered MZ relocations.
Do not infer canonical Factory acceptance from a target-equal normal link.

A composite report is current only while every input it compiled still
matches. Reuse unchanged native inputs; do not repeat a full cold chain for
an ordinary source edit.

## Scoped current-source native check (MAINL)

The current Staff/root route uses `build_th03_mainl_current.py`. It recompiles
both complete physical owners in a new `afNNNm` stage, compares complete
CODE/DATA/ordered FIXUPP/PUBLIC/segment geometry and repeats the full normal
link. The unchanged cold ancestor remains in place. Current publication selects
`af1055m`; see the [focused review](MAINL_CURRENT_SOURCE_REFRESH_AFTER1055_REVIEW.md).

    .venv/bin/python scripts/build_th03_mainl_current.py --stage afNNNm --build
    .venv/bin/python scripts/publish_th03_mainl_work_scopes.py --stage afNNNm
    .venv/bin/python scripts/progress.py

Omit `--build` to review an existing stage without native execution. The
publisher checks the specified stage against current source before adoption.
Changes outside these two producers need their affected native scope handled
explicitly; do not run the old cold builder in place over protected evidence.

## Storage

Keep necessary inputs and current build/compare working context. Remove
obsolete trial output, archives and cleanup reports; a documentation reference
does not make them necessary. Record useful findings briefly and use the
[short storage guidance](STORAGE_HANDOFF_CURRENT.md).

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

`scripts/ci.py` checks changed machine-input syntax and Git whitespace.
`scripts/ci.py --full` explicitly selects the broad suite for infrastructure
work. Historical private tests can require their recorded source snapshots;
the [script index](../scripts/README.md) lists current entry points.
A bounded source change needs its native comparison and directly relevant
checks rather than every product's runtime suite and database check.

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

When an accepted source scope changes, revalidate its affected evidence before
updating publication and regenerating `scripts/progress.py`. Current physical
owner reviews remain visible independently of a pending broad publication.
Status and progress use the same source-native reviewers; neither rebuilds native
inputs. Source presence and accepted ownership are separate; complete executable
equality can still contain unowned vendor context.
OP/MAINL/ZUN also compare canonical DIET storage. MAIN retains its documented
CODE alignment/header differences.

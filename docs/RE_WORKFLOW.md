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

The preferred bounded MAIN source verification uses the original
Turbo C++ 4.02 plus the complete normal TLINK response. The latest
source-bound integration is `af1053k`: both shared BOSS providers, all nine
character BOSS owners and the complete HitCircle owner (12 physical TUs,
18,845 CODE bytes, 2,570 ordered native fields and 97 PUBLICs). It passed two
independent original TC4 rounds and both normal Japanese MAIN links. The old
`af1024e`, `af1024d`, `af1024c`, `af1024b` and `af1021*` checkpoints are
historical for owners changed since those stages; do not cite them as current
source bindings. See the [active handoff](RE_HANDOFF.md) for the report hash,
latest owner-level work and next targets.

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

**Historical composite-stage correction:** af927a is no longer a current
whole-stage review because its ba_chiyu source hash differs from the
maintained Chiyuri source. Its entry, effects, cs_chiyu and b_chiyu source
hashes still match, but the stage-wide reviewer correctly rejects the
stale ba_chiyu member. Likewise af935a is historical for ba_maris.
Do not list either composite stage as a current all-owner source proof.
Use af1053k for the current twelve-owner BOSS/collision set. The active
handoff and its after1053 archive distinguish the latest source-bound proof
from historical stage snapshots.

The historical after596 MAIN and after587 MAINL pairs are separate
retained ancestors, **not** reasons to run full cold replay per edit.

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

## Latest protected-storage policy

The latest applied cleanup is the [after1024 safe storage audit]
(STORAGE_HANDOFF_AFTER1024.md): it removed only 448 regenerable Python
bytecode files and repacked Git with no pruning. All 21,319 Git object
IDs/types/sizes, refs, reflog files and fsck output remained identical.
No .analysis proof file, native receipt tree, target or toolchain file
was deleted. A 2026-11-09 cache-only preview found 0.0 MiB eligible and no
cleanup was applied. The earlier [after928 audit](STORAGE_HANDOFF_AFTER928.md)
is historical.

The after710 cleanup removed only six externally unreferenced incomplete
verifier-configuration stage pairs; after597 retired three explicitly
audited exploratory BOSS trees. The after520 source-linked CRT proof-output
audit covers only its historical prefix. These bounded historical actions
do not authorize further source-proof deletion.

Use [the current storage policy](STORAGE_HANDOFF_CURRENT.md). The old
cleanup_mainl_after520_handoff.py explicitly rejects newer source stages.
Older after439/after388 cleanup tools are historical; never bypass their
guards or infer disposability from an unrelated cleanup preview. Only the
official cache-only cleaner is a routine deletion route. Do not use
unreferenced-receipt pruning or bulk-delete .analysis.


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
the [script index](../scripts/README.md) records the current audit limits.
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

## Working files and retention

The [historical after520 deletion audit](STORAGE_HANDOFF_CURRENT.md)
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

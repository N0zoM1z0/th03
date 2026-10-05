# TH03 current handoff

## Current state

MAIN has thirteen maintained exact source owners represented by fourteen
reviewed CODE extents. They contain forty complete functions and 6210 exact
owned CODE bytes: 6103 function-body bytes plus 107 classified producer-owned
switch-table/alignment bytes. The owner set is vector-far, exit, polar,
frame-delay, input-sense, snd-se, snd-kaja, initmain, pi-load, input-modes,
explosion-collision, fireballs, and the two CODE contributions of the complete
`bullet.cpp` source owner.

These are repository-local exact results for bounded reviewed extents. They do
not imply a complete maintained MAIN build, whole-game closure, or Factory
Truth Kernel acceptance. `config/build.toml` still records an open product
graph. `docs/PROGRESS.md` and `config/th03_main_exact_units.toml` are the
authoritative current counts and replay scope.

The four required Japanese YUMEZIKU artifacts remain hash-pinned in
`config/targets.toml` with `candidate-local-attested` provenance. The pinned
TC4J/TASM/TLINK toolchain and Ghidra/JDK setup pass headless attestation. ReC98
revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` is only the frozen link/build
scaffold; it grants no TH03 exactness by itself. The older all-game
dependency-normalized OMF calibration mismatch remains isolated and unresolved;
do not rewrite its imported hashes to fit a current build.

## Local state and cleanup

`.analysis/` contains both required private state and disposable reconstruction
output. Preserve the imported targets/runtime image, Borland Wine prefix,
Ghidra state, and the small evidence files referenced by `config/evidence.csv`.
Cold reference builds, replay work trees, development probes, logs and Python
caches are disposable.

Use:

```sh
python3 scripts/clean_generated.py          # dry run
python3 scripts/clean_generated.py --apply  # prune disposable output
```

The cleanup script derives protected evidence paths from the ledger, so an old
replay directory can be reduced to its referenced receipt/review file instead
of retaining complete cold-build trees.

## Validation

Run Borland/Wine work serially.

```sh
python3 scripts/preflight.py
python3 scripts/ghidra.py th03-main check
python3 scripts/replay_th03_main_exact_units.py --run-id NEW_UNIQUE_ID
python3 scripts/ci.py
git diff --check
```

The maintained replay performs two independent source materializations, rebuilds
all game objects, validates OMF, checks deterministic configured products/game
objects, and verifies every reviewed owner/function byte, MAP contribution and
ordered relocation site. At the current frontier the deterministic vector is
20 configured products, 351 game objects and 417 generated OMF objects. Nine
Research benchmark objects with `__DATE__/__TIME__` LEDATA remain diagnostic
and outside the declared game-object vector.

Factory repository-shell execution can run this checked-in Oracle, but native
TH03 Truth Kernel replay is not registered. Repository-shell success and local
exact ledgers therefore remain distinct from Factory-accepted receipts.

## Next bounded work

Continue MAIN and include large owners, not only leaves. The next useful target
is the `e_enemy.cpp` gameplay owner, whose multiple code contributions total
more than 3 KiB. Rebuild its TH03 segment/data dependency map and function
boundaries from the original target first; use TH04/ReC98 only to propose
semantics, then recover the complete owner rather than cherry-picking easy
functions.

After that, continue through timing/state update and two-player/game-object
logic. For OP, MAINL and ZUN, establish stored-code versus decoded-code mapping
before treating storage inventories as source functions. Keep the OMF
calibration drift investigation separate from source reconstruction and replay
the complete existing MAIN aggregate after every new owner.

# TH03 current handoff

## Current state

MAIN has twenty-six maintained exact source owners represented by thirty
reviewed CODE extents: seventy-nine complete functions and 10329 owned bytes,
comprising 10199 function-body bytes and 130 classified producer-owned
switch-table/alignment bytes. `config/th03_main_exact_units.toml`,
`config/units.csv` and `docs/PROGRESS.md` define the current scope and counts.

The complete enemy owner remains a structural candidate: three CODE extents,
nineteen functions and 3325 bytes in `config/th03_main_enemy_candidate.toml`.
The two-round `sol-enemy-candidate-20261005` replay reproduced all candidate
bytes, MAP contributions and configured deterministic vectors, but failed
ordered relocations in ENEMY_2_TEXT. No enemy function or extent is exact.
Moving declarations/definitions did not resolve the ordering; the original
OMF producer record partition is still unknown. See
`docs/reconstruction/MAIN_ENEMY_REVIEW.md`.

These are repository-local exact results for bounded reviewed extents, not a
complete maintained MAIN/game build or Factory Truth Kernel acceptance.
`config/build.toml` records the open product graph. OP, MAINL and ZUN have no
maintained exact owner yet. The four Japanese YUMEZIKU artifacts remain pinned
with `candidate-local-attested` provenance; independent pristine-dump
attestation is unknown. The pinned TC4J/TASM/TLINK and Ghidra/JDK setups pass
headless attestation. ReC98 revision
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` is a frozen build/link scaffold,
not an independent exactness Oracle. The older all-game dependency-normalized
OMF calibration mismatch remains isolated; never rewrite its imported hashes.

## Validation

Run Borland/Wine work serially and keep all tools headless.

```sh
python3 scripts/preflight.py
python3 scripts/ghidra.py th03-main check
python3 scripts/replay_th03_main_exact_units.py --run-id NEW_UNIQUE_ID
python3 scripts/ci.py
git diff --check
```

The replay materializes two independent source trees, rebuilds every game
object, validates OMF and deterministic vectors, and checks every accepted
owner/function byte, MAP contribution and original ordered relocation site.
Its current vector is 20 configured products, 351 game objects and 417 OMF
objects. Nine Research objects with `__DATE__/__TIME__` LEDATA remain diagnostic
and outside the game-object vector. Inputs are frozen during each replay;
do not mutate source/config/ledgers until its process exits.

The latest final accepted-state receipt is
`sol-mrs-final-20261006`, covering the full 26-owner / 30-extent / 79-function /
10329-byte aggregate in both cold rounds. All prior accepted owners remain in
the replay. The enemy candidate keeps its separate failed receipt and manifest.
See `docs/reconstruction/MAIN_MRS_REVIEW.md` for this complete owner's evidence.
Factory repository-shell success remains distinct from Factory-accepted
receipts: native TH03 Truth Kernel replay is not registered.

## Next bounded work

Continue the complete ReC98 intake queue. Remaining directly linked MAIN roots
include shared sound/hardware, collision-map and reversal-table assembly, and
`th03_main.asm`. Review the latter's original code, data, resources and generated
scaffold separately. Do not count the reference build as authored progress.
For OP, MAINL and ZUN, establish stored-code versus decoded-code mappings before
accepting storage inventories as source functions. Keep other-artifact,
header/dependency and data acceptance separate from MAIN CODE decisions.

Player state preserves its collision algorithm in symbolic inline assembly
with compiler-owned locals/prologue; its companions retain C++. Hit circles
use symbolic XOR to preserve the observed encoding. Complete playfield,
sprite16 and MRS owners use symbolic TASM with genuine alignment in place of
codestring NOPs and opaque codegen emissions. MRS naturally reproduces the
ascending target relocation order, resolving its stock C++ reverse ordering.
Their bounded reviews live under `docs/reconstruction/`. This does not resolve
the separate enemy relocation failure.

The frozen intake has a replayable 504-file conservative queue in
`config/rec98_th03_inventory.csv`; fifty-one paths now have scoped CODE review
in `config/rec98_th03_reviews.csv`. Remaining file/artifact review is open.
See `docs/REC98_TH03_REVIEW.md`. Re-run the complete MAIN aggregate after every
new owner and keep observed facts, compiler output, inference and acceptance
separate in the ledgers.

## Local state and cleanup

Preserve targets/runtime images, the game-local Wine prefix, Ghidra state and
private evidence paths referenced by `config/evidence.csv`. Cold-build trees,
probes, logs and caches are disposable. Use:

```sh
python3 scripts/clean_generated.py          # dry run
python3 scripts/clean_generated.py --apply  # prune disposable output
```

Cleanup derives protected paths from the ledger and can reduce old replay trees
to referenced receipts/reviews. Do not run it against an active replay.

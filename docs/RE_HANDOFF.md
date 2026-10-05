# TH03 current handoff

## Current state

MAIN has twenty-two maintained exact source owners represented by twenty-six
reviewed CODE extents. They contain sixty complete functions and 8880 exact
owned CODE bytes: 8758 function-body bytes plus 122 classified producer-owned
switch-table/alignment bytes. The owner set is vector-far, exit, polar,
frame-delay, input-sense, snd-se, snd-kaja, initmain, pi-load, input-modes,
explosion-collision, fireballs, and the two CODE contributions of the complete
`bullet.cpp` source owner, hitbox, the four combo contributions, gauge, player movement, ordinary shots, player state, resident pointer,
extra-attack wrapper and hit circles.

The complete enemy owner is also maintained as a structural candidate: three
reviewed CODE extents, nineteen functions and 3325 bytes. Its separate manifest
is `config/th03_main_enemy_candidate.toml`. The two-round
`sol-enemy-candidate-20261005` replay reproduced every candidate byte, all MAP
contributions and the configured deterministic vectors, but failed ordered
relocations in ENEMY_2_TEXT. The remaining accepted owners passed their checks.
No enemy extent or function is exact. See
`docs/reconstruction/MAIN_ENEMY_REVIEW.md` for the bounded evidence and probes.

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

Continue the complete ReC98 intake queue. Investigate the enemy owner's single
ordered relocation failure without rewriting its MZ entries or weakening the
Oracle. The original OMF producer record partition remains unknown; moving
declarations or function definitions did not change the candidate's ordering.
Hitbox, combo, gauge, player movement, ordinary shots and player state have
passed the complete cold replay. The player-state owner now uses a reviewed
symbolic inline-assembly collision routine with natural compiler-owned locals
and prologue/epilogue; the damage and story-skill routines retain C++ bodies.
This resolves the stock source's 34 register-opcode encoding differences.
See `docs/reconstruction/MAIN_PLAYER_STATE_REVIEW.md`. The separate enemy
ordered-relocation question remains open.

Next, review the remaining directly linked MAIN candidates: static HUD,
playfield, sprite16, MRS, shared config/sound/hardware and original assembly.
The playfield, sprite16 and MRS upstream use explicit `codestring` NOPs; review
those producer bytes before deciding on a natural accepted source. MRS has a
preliminary ordered-relocation mismatch despite equal raw owner bytes; this
is a diagnostic intake question, not accepted source progress. The hit-circle
XOR direction difference is resolved with symbolic inline assembly. Then
continue original assembly, timing/state and two-player logic.
For OP, MAINL and ZUN, establish stored-code versus decoded-code mapping
before treating storage inventories as source functions. Keep the OMF
calibration drift investigation separate from source reconstruction and replay
the complete existing MAIN aggregate after every new owner.

The frozen ReC98 intake now has a replayable 504-file conservative review queue
in `config/rec98_th03_inventory.csv`, including dedicated/unlinked TH03 files,
the four product source roots and transitive includes. Scoped existing MAIN
CODE decisions are in `config/rec98_th03_reviews.csv`; the remaining review is
open. See `docs/REC98_TH03_REVIEW.md`. The thirteen existing owners passed the
fresh two-round `sol-rec98-baseline-20261005` replay. The enemy wrapper and
implementation have a scoped boundary-review decision; all remaining intake
review is still open.

Recent final accepted-state aggregate receipts all passed two cold rounds:

- `sol-hitbox-combo-gauge-final-20261005-b`: hitbox/combo/gauge;
  see `docs/reconstruction/MAIN_COLLISION_COMBO_GAUGE_REVIEW.md`.
- `sol-player-move-shots-final-20261005`: movement and ordinary shots;
  see `docs/reconstruction/MAIN_PLAYER_MOVE_SHOTS_REVIEW.md`.
- `sol-player-state-final-20261005`: collision, damage and skill;
  see `docs/reconstruction/MAIN_PLAYER_STATE_REVIEW.md`.

- `sol-cfg-exatt-hitcircle-final-20261005`: resident configuration pointer,
  extra-attack wrapper and hit circles; see
  `docs/reconstruction/MAIN_CFG_EXATT_HITCIRCLE_REVIEW.md`.

The last receipt covers the current full twenty-two-owner / twenty-six-extent
/ sixty-function / 8880-byte aggregate and complete configured
product/game-object deterministic vector. The enemy candidate retains its
separate manifest and recorded failure.

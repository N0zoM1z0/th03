# MAIN enemy owner review

The complete th03/e_enemy.cpp intake is maintained in
src/main/enemy/enemy.cpp with its public declarations in enemy.hpp. It is now a
normal owner in config/th03_main_exact_units.toml: three complete CODE extents,
nineteen functions, and 3325 owned bytes. The accepted replay uses two
consecutive physical OMF producers for this single semantic source owner. That
producer model is independently checked against TH03 target bytes, MAP ownership,
and ordered relocations; it does not claim the unavailable historical source
filenames.

## Observed Japanese target boundaries

Target SHA-256:
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
The Ghidra database was re-attested before the queries. The semantic names below
come from upstream and the candidate link map; instruction boundaries and
relocations are independently observed in the target.

| CODE segment in MAIN_04 | Relative segment:offset | Bytes | Functions |
| --- | --- | ---: | ---: |
| ENEMY_2_TEXT | 139D:024E | 1714 | 11 |
| E_ENEMY_TEXT | 139D:250B | 602 | 5 |
| ENEMY_PUT | 139D:278D | 1009 | 3 |

The owner contains 3260 function bytes, one producer alignment byte, and a
64-byte sparse-switch table. It does not own the intervening character,
hitbox, combo, gauge, or other CODE contributions. The candidate MAP has
zero-byte DATA and BSS contributions at 1D56:0BEC and 1D56:8DF8; externally
defined game state remains part of the open product scaffold.

`enemy_run` occupies 055C..08BE and returns with near `RET`. Its dispatch loads
CX=16 and BX=08C0, searches sixteen word keys, then jumps through CS:[BX+20].
08BF is alignment; 08C0..08DF contains the keys and 08E0..08FF their word
destinations. All destinations lie in the reviewed function body. Ghidra's
automatic function body reports only 154 of 867 bytes and is insufficient
for ownership. The raw review script decodes all function bytes and verifies
the sparse table independently:

```sh
python3 scripts/review_th03_main_enemy.py \
  --output .analysis/th03-main-exact/sol-enemy-target-review/raw-review.json
```

The target uses a 48-byte enemy stride and a 128-byte player stride. Enemy
script fields include word IP at +0A, word operation frame at +0C, and a near
script-base pointer at +0E; the interpreter loads ES from the external
`enedat_2` segment handle. The current compatibility boundary preserves the
upstream layout verification and 16-bit types; declarations and data outside
this owner have not received independent acceptance.

`enemies_add` is far Pascal with `RETF 6`. Formation spawn is near Pascal with
`RET 6`; per-player formation update and chain-pellet speed use `RET 2`.
The other helper returns are near `RET`; public update/render/load/free/RNG
functions return with `RETF`. The velocity helper saves ES around its far
Pascal vector call. Collision and update trampolines retain the target's
symbolic NOP/PUSH CS/near CALL sequence to a far-return callee; these are real
instructions with the target ABI, not target-byte arrays.

The interpreter retains the target's signed shifts/divisions, horizontal
mirroring, clip flags, sixteen operation cases, duration scaling, and broken
loop branches. `enemy_formations_randomize` reads its previous-formation byte
before initialization. Upstream's assertion that the first value is always
0x5E, and its claims about unused operations in ENEDAT.DAT, have not been
verified with runtime or asset observations here. Those source annotations
remain upstream hypotheses; no corrective initialization or script bug fix
has been applied.

## Compiler observations, historical failure, and exact resolution

The 2026-10-05 one-object compiler model was intentionally not accepted even
though it reproduced all 3325 raw CODE bytes. Its ENEMY_2_TEXT relocation
multiset matched but the ordered list did not:

    target:           512 503 494 485 431 394 282 277 257 246 235 224 216 204 686
    one-object model: 686 512 503 494 485 431 394 282 277 257 246 235 224 216 204

Site 686 is the segment relocation for the far vector call. Moving declarations,
assigning the known SHARED declaration segment, and source-order experiments did
not repair the ordering. Those failures remain in config/evidence.csv; no
ordered-relocation gate was weakened or replaced by a sorted/multiset check.

The successful maintained model splits physical production immediately before
enemy_velocity_set_from_angle_and_speed() while retaining one natural semantic
source file. The first generated wrapper, e_ena, contributes 650 bytes to
ENEMY_2_TEXT and 451 bytes to E_ENEMY_TEXT. The second, e_enb, contributes
1064 bytes to ENEMY_2_TEXT, 151 bytes to E_ENEMY_TEXT, and all 1009 bytes of
ENEMY_PUT. Explicit codeseg declarations keep the real contributions in MAIN_04;
the wrappers' zero-length default text segments stay ungrouped so they do not
perturb later logical groups.

This layout does not alter the target CODE bytes. It changes which physical OMF
producer owns the fixups, causing TLINK to emit the target relocation order
naturally. Both fresh accepted rounds now produce exactly:

    target: 512 503 494 485 431 394 282 277 257 246 235 224 216 204 686
    round1: 512 503 494 485 431 394 282 277 257 246 235 224 216 204 686
    round2: 512 503 494 485 431 394 282 277 257 246 235 224 216 204 686

At the enemy-owner promotion checkpoint, the default maintained replay passed
120 functions, 14747 function bytes, and 14953 owned bytes, including the enemy
owner's 19 functions / 3260 function bytes plus its one alignment byte and
64-byte sparse switch table. That checkpoint recorded 20 products, 355
deterministic game objects, and 421 valid generated OMF objects. The current
aggregate has since advanced to 127 functions / 18066 owned bytes through the
separately reviewed MAIN_05_TEXT bomb owner; the enemy evidence remains unchanged.
The raw target review independently checks all nineteen function boundaries and
the sparse dispatch table.

The split is therefore accepted as the maintained reconstruction producer model.
It is strong compiler/linker evidence for the physical boundary needed to
reproduce this target, but the original object names and historical source
filenames are unavailable and are not asserted.

Replay the complete accepted MAIN frontier with:

    python3 scripts/replay_th03_main_exact_units.py --run-id NEW_UNIQUE_ID

Review the enemy target boundaries independently with:

    python3 scripts/review_th03_main_enemy.py --output .analysis/th03-main-exact/NEW_ENEMY_REVIEW.json

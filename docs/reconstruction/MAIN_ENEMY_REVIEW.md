# MAIN enemy owner review

The complete `th03/e_enemy.cpp` intake is maintained in
`src/main/enemy/enemy.cpp` with its public declarations in `enemy.hpp`.
`config/th03_main_enemy_candidate.toml` adds this owner to the complete accepted
MAIN aggregate through `--candidate-manifest`. It cannot replace the target,
accepted units, functions, or gate policy. The three extents and nineteen
functions stay structural / boundary-reviewed until every owner gate passes.

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

## Compiler observations and failed acceptance dimension

The pinned TC4J/TLINK diagnostic probe reproduces all 3325 raw CODE bytes.
The complete `sol-enemy-candidate-20261005` replay confirms this in two
independent source materializations: 20 products, 351 game objects and all 417
generated OMF objects have the required integrity; the declared product and
game-object deterministic vectors pass. All 59 configured function checks and
all 17 CODE extent byte checks pass. The overall verdict correctly remains
FAIL because the formation extent fails ordered relocation comparison.
The ENEMY_2_TEXT relocation multiset matches, but ordered relocations differ:

```text
target:    512 503 494 485 431 394 282 277 257 246 235 224 216 204 686
candidate: 686 512 503 494 485 431 394 282 277 257 246 235 224 216 204
```

Site 686 is the vector call. The other fourteen relocated words contain
segment zero; this word contains SHARED's segment 0E8F. The other two CODE
extents have equal bytes and equal ordered relocations. This does not grant
them independent exact credit while the complete source owner is unresolved.

The candidate OMF emits ENEMY_2_TEXT LEDATA records of 1024 and 690 bytes.
Moving the vector declaration after library declarations, assigning its
known SHARED declaration segment, and moving `enemies_update` between the
formation and motion definitions did not change the failed ordering. These
experiments were private probes and are absent from maintained source.
The original object's record partition/order is unknown; it cannot be
recovered from a hypothetical historical source claim alone.

The next investigation should determine which natural producer input explains
the target ordering. Do not rewrite the relocation table, fabricate padding,
copy opcodes, or weaken ordered relocation comparison to accept this owner.
The full owner is replayable with:

```sh
python3 scripts/replay_th03_main_exact_units.py \
  --candidate-manifest config/th03_main_enemy_candidate.toml \
  --run-id NEW_UNIQUE_ID
```

# TH03 MAIN after935 — seven modified original physical owners linked together

The active source now expresses Marisa's distinct BOSS overlay sprites and
ring threshold, both HitCircle spawn placements as direct typed C++ stores,
enemy chain-ring initialization directly in the large `enemy_hittest` body,
and the Bullet engine's pellet Y-hitbox arithmetic without an alias macro.
These are four edited maintained source files, but **seven original physical
project objects**: `enemy.cpp` compiles separately as `eforna`, `efornb`,
`eupda` and `eupdb`. The other three are `ba_maris`, `hitcirc` and `bullet`.
All four enemy objects must be rebuilt to establish current source binding,
even though the new chain lifecycle statements execute only in `eupdb`.

The genuine original compiler/linker experiment is:

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af935a \
  --units ba_maris,hitcirc,eforna,efornb,eupda,eupdb,bullet
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af935a
```

Two independent original Turbo C++ 4.02 compiler rounds each rebuilt the
**entire seven original physical objects** and checked their source/header
OMF dependencies, exact segment geometry, all **7,886 original CODE bytes,
647 literal ordered OMF FIXUPP fields and 52 PUBLIC symbols/offsets**. Each
round genuinely linked the complete original 99-game-object normal MAIN
response, reusing **92 other unchanged original game objects and the original
Borland CRT**. Both normal MAIN EXE/MAP outputs match the original Japanese
**124,642-byte loaded program and all 1,553 ordered MZ relocations**. No
full cold replay or original OBJ, target, CRT or linker input modification.
Preserved report and real writer artifacts:
`.analysis/work/exatt-layout-af935a/report.json`, SHA-256
`924fdd7943c428064b1a26d9a3a4b4b99303d4204f7c4d7bfd682965d35c3620`.

The narrower `af934a` trial independently established that the four objects
containing changed executed code could link together (5,721 original CODE
bytes, 528 FIXUPPs and 37 PUBLICs), but omitted the three other physical
consumers of `enemy.cpp`. `af935a` replaces it as the complete changed-source
physical scope. The older genuine `af921a`, `af903a`, `af896a`, `af883a` and
`af881i` experiments remain retained as historical proof of their respective
source snapshots; they no longer bind to today's HitCircle, Bullet, Enemy or
Marisa source SHA-256. The independent `af927a`, `af915a`, `af909a`,
`af889a`, `af880h` and `af882e` reports were separately rechecked and remain
source-current. Do not infer one simultaneous 99-original-source build by
summing separate experiments.

Failed native C++ substitutions were investigated, not silently adopted:
register-local enum arithmetic in Marisa changed CODE, an extracted enemy
chain helper changed its physical ABI/codegen, a HitCircle method extraction
changed the stack prologue, and apparently equivalent Bullet byte predicates
changed branch instructions. Their trial artifacts remain available under
the respective unique `af930*`, `af931*` and `af933*` stage names.

This is a **current maintained-source native normal-link result**, not a
claim of newly distinct original CODE bytes (these owners were historically
source-covered), vendor packet-identical OMF, historically identical TLINK
MZ-header serialization or canonical packed-product Factory acceptance.

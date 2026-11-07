# TH03 MAIN after843: full Enemy formation loader and script-VM native recovery

The 1,049-line `src/main/enemy/enemy.cpp` has **four original physical
Turbo C++ 4.02 owners**: `eforna` (formation loader/creator), `efornb`
(the full approximately 867-byte ENEDAT movement/opcode interpreter),
`eupda` (spawn/explosion/update helpers), and `eupdb` (large enemy chain,
collision, renderer and global update). All four must stay in their
historical original CODE sections, linker slots and calling ABIs.

## Genuine natural C++ source improvements

The formation-file loader now has a natural `for(;;)` with the original
**zero `uint16_t` enemy-count sentinel**, tested as `if(!enemy_count)`.
It still consumes original script sizes and offsets in the same order,
does not add ENEDAT bounds checks, and preserves original near pointers.
The per-enemy formation spawning loop also uses a natural C++ `for`,
with the **global byte formation index and signed script offset both
incremented after each original `enemies_add` call**. These changes were
recompiled as the *whole original Enemy physical source*, including its
full VM and collision units, not only standalone leaf functions.

The original uninitialized formation RNG `prev` remains deliberately
uninitialized: changing it would affect the original first draw. The
original interpreter's broken absolute/relative loop semantics and
segmented ES script pointer are also preserved instead of 'fixed'.

## Actual native compiler experiments, including rejected alternatives

- `af843a` restored the formation-loader `for(;;)` and passed both real
  TC4/TLINK rounds across all four original physical objects.
- `af843b` additionally used a C++ `for` for formation-spawning with
  both increments in the continuation expression: still **complete
  original CODE exact** in two rounds.
- `af843c` challenged the large script VM's `EO_MOVE` branch with an
  apparently simpler early return. Genuine original TC4 emitted
  **different efornb CODE**. The target's original branch layout stays.
- `af843d` challenged the formation RNG `do/while` with a `for(;;)` and
  explicit break: `eforna` grew to **732** from **729** CODE bytes.
  Rejected without reordering RNG draws.
- `af843e` proved the natural `!enemy_count` termination in the real
  source with both full original native rounds.
- `af843f` independently challenged `enemy_move_and_clip`'s common
  `goto clip` exit with duplicated early returns. Original `eforna`
  CODE differed (even where initialized byte length did not change),
  so the shared original `clip` epilogue remains.
- Final `af843g` compiled the restored **entire maintained source** with
  precise inline comments and all accepted natural C++ forms twice,
  using genuine original TC4 and complete normal TLINK.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af843g --units eforna,efornb,eupda,eupdb
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af843g
```

Both independent original native compiler/full normal linker rounds match
**all 3,325 original CODE bytes** (`729+1064+372+1160`), **222 literal
ordered native OMF FIXUPP fields** (`58+37+24+103`), **19 PUBLICs**,
original segment/source ABI, complete original MAIN EXE/MAP, all
**124,642 Japanese loaded program bytes and 1,553 ordered MZ
relocations**. Independent standard MZ serialization recreates all
**130,882 original Japanese MAIN.EXE bytes**. The **95 other unchanged
original game objects and CRT were reused**, no full-project cold replay
or target-byte padding. Protected current-source proof and both native
writer rounds: `.analysis/work/exatt-layout-af843g/report.json`, SHA-256
`8c476989384c1289d6c13bf224c5d656ff61d8e9de64c19ec2467fd16b6ecf4c`.

These original physical source owners had historical native CODE coverage;
this improves maintained source/codegen fidelity, **not new distinct
coverage, vendor raw OMF identity or canonical Factory packed-game
acceptance**. The important negative results are retained as original
compiler trials, not offered as accepted matches.

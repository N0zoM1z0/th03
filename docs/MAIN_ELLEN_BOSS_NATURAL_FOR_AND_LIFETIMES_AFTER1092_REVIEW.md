# TH03 MAIN Ellen BOSS: natural attack loops and render-local lifetimes (af1092j)

This pass reworks the complete nine-function, 1,675-byte `ba_ellen` physical
BOSS. It is not a one-leaf compile: both attack-family controllers, the full
update/collision dispatcher, the strip renderer, main renderer, intro radial
renderer and top-level render dispatcher are rebuilt together with the
original Borland Turbo C++ 4.02 compiler.

## Spread attack: eight-shot volley

The eight-projectile spread burst now uses a natural `for` header and scopes
the register index to that loop:

```cpp
for(register int i = 0; i < ELLEN_SPREAD_VOLLEY_COUNT; ++i) {
    bullets_add();
    ellen_spread_angle = ellen_spread_angle + ELLEN_SPREAD_ANGLE_STEP;
    bullet_template.angle = ellen_spread_angle;
}
```

The bullet spawn, byte-angle assignment and template-angle update retain the
same order. The old function-entry `register int i` and manual increment are
gone.

## Radial Extra Attack bursts

Both `ELLEN_EXTRA_FIRST_BURST` and `ELLEN_EXTRA_LAST_BURST` now own separate
first-use locals and natural `for` loops:

```cpp
register int i = 0;
unsigned char angle = randring_far_next16();
for(; i < ellen_extra_count; ++i,
    angle = angle + (ELLEN_EXTRA_FULL_TURN_UNITS / ellen_extra_count)) {
    ellen_extra_add(boss_center_x, boss_center_y, angle, mode);
}
```

The iteration expression preserves the original post-spawn sequence exactly:
first the integer count increments, then the byte angle advances by the
original signed-width `256 / ellen_extra_count` quotient. The two bursts still
draw independent RNG angles and retain their different signed mode arguments.
The function-entry index and angle locals are eliminated; each burst has its
own declaration.

## Main and intro renderers

- `ellen_render_strip()` initializes its register index and sprite offset at
their declarations. The attempted narrowing of its left/top coordinate
scratch changed CODE and was reverted.
- `ellen_render_main()` initializes its PID at declaration. The register
sprite-offset local is declared at the original first assignment after the
coordinate setup, and the register strip index is declared at its first use
after the main sprite draw.
- `ellen_render_intro()` initializes its PID and strip index at declaration.
The register left coordinate and ordinary sprite offset are declared only
after the flicker early-return guard. Its four-by-eight radial sprite nest is
now two natural `for` loops, with the inner index declared in the inner loop
header. The byte-angle steps and sprite-offset decrement remain after the
same sprite spawns and in the same order.
- `gba_boss_update_ellen()` initializes the opponent PID after the
inactive-owner return, leaving the four level-derived parameter stores before
the guard and the collision/HP tail after the full mode switch.
- `gba_boss_render_ellen()` initializes its opponent PID after the
inactive-owner return and before clip setup / INTRO / normal / explosion
dispatch.

## Rejected alternatives

These were independently tried and not retained because the complete original
CODE changed:

- Moving `ellen_pattern_extra()`'s warning PID into only the warning branch
  (`af1091w`).
- Moving `ellen_pattern_spread()`'s PID into separate warning branches and
  recomputing it for the bullet template (`af1091y`).
- Replacing `boss_render_frame++` with prefix increment or explicit additive
  assignment in the update controller (`af1091t`, `af1091u`).
- Moving the intro left coordinate after the flicker return (`af1092e`) or
  moving the intro top coordinate after that return (`af1092f`).
- Moving both `ellen_render_strip()` coordinate declarations to their first
  assignments (`af1092g`), or only its left coordinate (`af1092h`).
- Moving `ellen_render_intro()`'s opponent PID after the flicker return
  (`af1092l`).
- Recomputing `ellen_render_main()`'s opponent PID inline at its only use
  (`af1092m`).
- Narrowing `gba_boss_update_ellen()`'s PID lifetime to the collision/hitbox
  tail after the mode switch (`af1092n`).

The accepted source keeps the original branch-entry PID in the two attack
leaves and the original postfix render-frame increment. The failed coordinate
experiments are negative controls, not accepted source variants.

## Complete original-owner verification

Stage `af1092j` rebuilt the complete Ellen BOSS in two independent original
Turbo C++ 4.02 rounds. All 1,675 CODE bytes, 213 ordered native fields and
nine PUBLIC offsets match. Both normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations. The source overlay checks
the maintained `ellen.cpp` producer and its actual wrapper/header inputs.

Report: `.analysis/work/exatt-layout-af1092j/report.json`

SHA-256: `380e6f08c9e07365534c88af16785b2113df831588e170858017434f27fd9daf`

Maintained source SHA-256: `d95567333bb2da4e4ea80ac5b44ad6ddc363f98b26e2dd710b0c733ad339beeb`.

## Twelve-owner integration

The current-source `af1092k` integration rebuilt 12 physical owners in two
independent TC4 rounds: 19,741 CODE bytes, 2,359 ordered native fields and 112
PUBLIC offsets. It includes the exact Ellen source hash above. Both normal
Japanese MAIN links reproduce the original loaded image and ordered MZ
relocations.

Report: `.analysis/work/exatt-layout-af1092k/report.json`

SHA-256: `063763924bc64038dbb7a11ca7ef234ab4907e28701b8b14a4b12a05820cf597`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

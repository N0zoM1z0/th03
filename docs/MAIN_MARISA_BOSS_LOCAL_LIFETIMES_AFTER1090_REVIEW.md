# TH03 MAIN Marisa BOSS: natural PID lifetimes in update and render paths (af1090j)

This pass revisits the complete nine-function, 1,431-byte `ba_maris` BOSS.
It narrows the opponent PID local in the full update controller, the main
renderer, the split renderer and the top-level renderer. Each declaration
move was compiled with original Turbo C++ 4.02 against the complete physical
owner; the attack leaves that did not tolerate narrower PID lifetimes remain
unchanged.

## Full update controller

`gba_boss_update_marisa()` keeps its six level-derived parameter stores before
the launched-player guard. The opponent PID is now declared and initialized
only after the inactive-owner return:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}

pid_t pid_other = (1 - pid_current);
boss_target_update();
++boss_frame;
```

The INTRO, SELECT, Spread, Wide, Ring, Narrow, DESCEND and EXPLODE dispatch,
collision-map setup, hitbox test, HP subtraction and hittest cleanup retain
their original order. No parameter initialization was moved across the guard.

## Main, split and top-level renderers

`marisa_render_main()` initializes `pid_other` after its two register-qualified
screen-coordinate locals:

```cpp
sprite16_offset_t sprite_offset;
register screen_x_t left;
register screen_y_t top;
pid_t pid_other = (1 - pid_current);
```

`marisa_render_split()` likewise initializes its PID after the two register
locals that intentionally allocate SI and DI:

```cpp
screen_y_t top;
register screen_x_t signed_offset = offset;
register screen_x_t left;
pid_t pid_other = (1 - pid_current);
```

The original split-sprite masks and SI/DI allocation order remain unchanged.
`gba_boss_render_marisa()` initializes the PID after the inactive-player
return, before clipping and the INTRO / normal / explosion dispatch:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
pid_t pid_other = (1 - pid_current);
sprite16_clip_set_for_pid(pid_other);
```

## Rejected column-attack lifetime changes

Both `marisa_pattern_columns_wide()` and `marisa_pattern_columns_narrow()`
retain their original function-entry `pid_other` initialization. Moving it
after the warmup return changed complete CODE (`af1090c`, `af1090d`). Moving
it after the render-mode store also changed CODE (`af1090e`), as did wrapping
the post-guard attack chain in a narrower block (`af1090h`). The accepted
source therefore narrows the four update/render locals above without
normalizing the two attack-leaf locals.

## Complete original-owner verification

Stage `af1090i` rebuilt the complete Marisa BOSS in two independent original
Turbo C++ 4.02 rounds. All 1,431 CODE bytes, 199 ordered native fields and
nine PUBLIC offsets match. Both normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations. The source overlay checked
the maintained `marisa.cpp` producer.

Report: `.analysis/work/exatt-layout-af1090i/report.json`

SHA-256: `f2da4f21209a373204e9492eb0ed77bc412a8039ab13cc9f04fe90053f2239f8`

Current `marisa.cpp` SHA-256:
`6ccefcb6b069fac99d1dc0913d08b6be3fd471a0cdf3bcab590d2974e34ec25a`

## Eleven-owner integration

Stage `af1090j` rebuilt the current Marisa owner together with `bullet`,
`e_fireb`, `ba_mima`, `ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`,
`ex_reup` and `hitcirc` in two independent original TC4 rounds: 18,066 CODE
bytes, 2,146 ordered native fields and 103 PUBLIC offsets match. Both normal
Japanese MAIN links reproduce the original loaded image and ordered MZ
relocations.

Report: `.analysis/work/exatt-layout-af1090j/report.json`

SHA-256: `7397a4101bc767b7126defdf63395b963720610475e53ee00b5b717f88f0f6da`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

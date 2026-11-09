# TH03 MAIN Mima BOSS: natural local lifetimes in attack, update and render (af1088p)

This pass revisits the complete nine-function, 1,922-byte `ba_mima` physical
BOSS, not an isolated helper. It narrows locals in the random-bomb attack,
BOSS update controller, split renderer and top-level render dispatcher while
keeping the original TC4 allocation and complete object exact.

## Random-bomb attack: coordinates after the early return

`mima_pattern_bomb_random()` previously reserved `x` and `y` at function
entry, although the `MIMA_RANDOM_BOMB_FIRE_BEGIN > boss_frame` path returns
before either coordinate is used. The locals now begin at their first actual
use, after the warning-state update / early-return guard:

```cpp
if(MIMA_RANDOM_BOMB_WARN == boss_frame) {
    boss_render_mode = MIMA_RMODE_TRAIL;
} else if(MIMA_RANDOM_BOMB_FIRE_BEGIN > boss_frame) {
    return;
}

int x = (boss_center_x + MIMA_BOMB_ORIGIN_X_OFFSET);
int y = (boss_center_y + MIMA_BOMB_ORIGIN_Y_OFFSET);
```

Both ordinary `int` declarations (without `register`) preserve the original
complete object. The three warning-frame comparisons, `bomb_center_add()`
return, bullet/pellet spawn order, ring event, four-frame firing clock and
sound timing remain unchanged.

## BOSS update: opponent PID after the inactive-owner guard

`gba_boss_update_mima()` now declares and initializes its opponent PID at the
first point after the inactive-player return:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}

pid_t pid_other = (1 - pid_current);
boss_target_update();
```

The local no longer exists across `boss_update_start()` or the inactive-owner
path. Crucially, `bullet_template.pid` still recomputes `(1 - pid_current)`
after `boss_target_update()`; it does not reuse `pid_other`. That distinction
was an independently measured negative control (`af749c`) and remains
intentional. The accepted form also removes the unnecessary `register` hint.

## Split and top-level renderers

`mima_render_split()` initializes `pid_other` at its declaration after the
parameter-derived split distance and the local coordinate declarations:

```cpp
register int split_distance = distance;
register screen_x_t left;
pid_t pid_other = (1 - pid_current);
```

`gba_boss_render_mima()` scopes its opponent PID to the active-owner branch:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_t pid_other = (1 - pid_current);
    sprite16_clip_set_for_pid(pid_other);
    // Intro split, normal render, or explosion render.
}
```

The intro split call, normal main renderer and explosion renderer preserve
their original dispatch order. The split-distance and left-coordinate
`register` hints are retained: removing either changed the complete object
(`af1088j`, `af1088k`).

## Rejected alternatives

- Moving `mima_pattern_bomb_random()`'s `pid_other` below the early return
  changed CODE (`af1088d`).
- Replacing its single `pid_other` local with an inline `(1 - pid_current)`
  argument changed CODE (`af1088e`).
- Removing `register` from the split renderer's `split_distance` or `left`
  changed CODE (`af1088j`, `af1088k`).

These failures are why the accepted source keeps the original bomb PID
lifetime and split-renderer register hints, even though the other local
lifetimes can be expressed more naturally.

## Complete original-owner verification

Stage `af1088o` rebuilt the entire Mima BOSS in two independent original
Turbo C++ 4.02 rounds. All 1,922 CODE bytes, 277 ordered native fields and
nine PUBLIC offsets match; both normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations. The source overlay checked
the maintained `mima.cpp` producer.

Report: `.analysis/work/exatt-layout-af1088o/report.json`

SHA-256: `8dc11f646fb85d26e4d7075e47463315b9668014e608afe5be0f1cee9c81fe21`

Current `mima.cpp` SHA-256:
`47f582b8ddb44b6aab621a506f458aeb6d130553dacc814f629e859ac9f59b7f`

## Ten-owner integration

Stage `af1088p` rebuilt the current Mima owner together with `bullet`,
`e_fireb`, `ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`, `ex_reup`
and `hitcirc` in two independent original TC4 rounds: 16,635 CODE bytes,
1,947 ordered native fields and 94 PUBLIC offsets match. Both normal Japanese
MAIN links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1088p/report.json`

SHA-256: `babb2696f9416f9b3f760c70c7689b3cd55d2564b309cba459c6d55180e33304`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

## Later current-source integration refresh

The Mima source binding remains `af1088o` (source SHA-256
`47f582b8ddb44b6aab621a506f458aeb6d130553dacc814f629e859ac9f59b7f`). Its
current eleven-owner integration was refreshed at `af1090j` after the Marisa
BOSS PID-lifetime recovery; report SHA-256
`7397a4101bc767b7126defdf63395b963720610475e53ee00b5b717f88f0f6da`.

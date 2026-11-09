# TH03 MAIN Reimu Extra Attack Update: scoped state and eight-slot iteration (af1075w)

This pass attacks the full 281-byte `exatt_update_reimu()` function inside the
separate original `ex_reup` physical object. The update now uses a local
register entity pointer whose lifetime is restricted to the eight-slot loop,
a `for`-initializer index, a byte-angle scratch restricted to the successful
flight-initialization branch, and natural variable-first state/geometry tests.
The paired 50-byte `exatt_render_reimu()` body is unchanged.

## Eight-slot iteration and pointer lifetime

```cpp
{
    register exatt_entity_t near *p = exatt_entities[pid_current];
    for(int i = 0; i < 8; ++i, ++p) {
        // free / active / flying / appearing-state dispatch
    }
}
```

The ordinary signed index is declared in the loop initializer. The entity
pointer remains register-qualified (removing `register` changes the complete
physical owner), but is initialized only after the shared hitbox setup and
scoped to the loop that uses it. Array decay
`exatt_entities[pid_current]` is equivalent to
`&exatt_entities[pid_current][0]` in this original TC4 build. Prefix `++p` in
the comma-separated loop increment matches the original; `i != 8` does not,
so the maintained loop keeps the original `< 8` termination test.

## State-specific local angle and transition logic

The random angle is now declared only where it is used:

```cpp
} else if(REIMU_UPDATE_FLYING == p->state) {
    exatt_entity_p = p;
    if(exatt_fly_update()) {
        unsigned char angle;
        angle = randring_far_next16_and(0x1F);
        angle = ((randring_far_next16_and(1) * 0x60) + angle + 0x80);
        vector2(
            p->velocity_x, p->velocity_y,
            angle, ((round_speed / 8) + 0x32)
        );
    }
}
```

The angle is not needed when a flying entity does not initialize its
trajectory, nor in the active and appearing paths. Narrowing its lifetime all
the way into the successful `exatt_fly_update()` branch still reproduces the
original 331-byte physical owner.

The state tests now name the FREE, ACTIVE, FLYING and APPEARING values. The
APPEARING comparison is variable-first:
`REIMU_UPDATE_APPEARING_END >= p->state`. FREE uses an explicit equality test
instead of Boolean negation. The branch order and early `continue` paths are
unchanged.

## Active flight bounds and acceleration

The active entity still advances X and Y before applying the original
reflections and playfield cutoff. The equivalent variable-first forms are:

```cpp
if((0 >= p->x) || (TO_SP(PLAYFIELD_W) <= p->x)) { ... }
if(TO_SP(-24) > p->y) { ... }
if(TO_SP(PLAYFIELD_H) <= p->y) { ... }
```

Both compound signed reflections `p->velocity_x *= -1` and
`p->velocity_y *= -1` remain intact. Direct assignment from unary negation was
independently rejected for both fields in the earlier native experiments and
was not reintroduced here.

The vertical acceleration is maintained as `p->velocity_y += 1`. Prefix
`++p->velocity_y` also matched; explicit `p->velocity_y = p->velocity_y + 1`
did not. The appearing-state increment remains postfix `p->state++`; changing
it to prefix `++p->state` changed CODE.

## Additional negative controls

- Removing `register` from the entity pointer changes CODE; retain the
  register-qualified near pointer.
- A `switch(p->state)` rewrite of the free/active/flying/appearing state
  machine changes CODE; retain the ordered `if` / `else if` chain.
- `i != 8` changes CODE; retain `i < 8`.
- Prefix `++p->state` changes CODE; retain postfix state advancement.
- Explicit self-addition for vertical velocity changes CODE; retain `+= 1`.
- Both direct unary-negation replacements for the signed velocity reflections
  remain rejected; retain compound `*= -1`.

## Complete original-owner verification

Stage `af1075w` rebuilt the complete `ex_reup` physical owner in two
independent original Turbo C++ 4.02 rounds. All 331 CODE bytes, 22 ordered
native fields and two PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The source
overlay independently checks the live `exatt_reimu_update.inl` include and
its actual compiler dependency record.

Report: `.analysis/work/exatt-layout-af1075w/report.json`

SHA-256: `ca6e69073359d59980eae20c8cefa8d9fe1b49421238e161ed4caf7d27426da4`

Current update include SHA-256:
`dd8c6122dbb7c4e44a2bc29d834a7d42de8131719495ae56565ec671897601af`

## Joint Reimu BOSS and Extra Attack integration

Stage `af1075y` rebuilt all three relevant original physical units together:
`ba_reimu`, `ex_rfly` and `ex_reup`. Two independent original TC4 rounds match
3,176 CODE bytes, 343 ordered native fields and 19 PUBLIC offsets. Both normal
Japanese MAIN links reproduce the original loaded image and ordered MZ
relocations.

Report: `.analysis/work/exatt-layout-af1075y/report.json`

SHA-256: `cdf398fdb3e7aa4888da861a7b3a77e52f3cf4d290295187a8697081f8996dc3`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

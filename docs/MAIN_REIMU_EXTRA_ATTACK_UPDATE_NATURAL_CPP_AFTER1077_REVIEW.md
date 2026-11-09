# TH03 MAIN Reimu Extra Attack Update: natural loop, state and angle lifetimes (af1077d)

This pass continues the complete 281-byte `exatt_update_reimu()` function in
the separate original `ex_reup` physical object. It revisits several earlier
assumptions with isolated native experiments. In particular, removing
`register` from the entity pointer is accepted when tested alone; the earlier
negative conclusion in the af1075w review was confounded by a larger combined
edit and must not be carried forward.

## Entity pointer and eight-slot loop

The maintained loop now starts after hitbox setup and uses ordinary C++ locals:

```cpp
hitbox_hittest_skip_explosions = true;
hitbox.radius.x.v = TO_SP(16);
hitbox.radius.y.v = TO_SP(16);
hitbox.pid = 1 - pid_current;
exatt_entity_t near *p = exatt_entities[pid_current];
for(int i = 0; i < 8; ++i, ++p) {
    // entity state machine
}
```

The pointer no longer needs `register`, and no extra nested block is needed.
The `for` initializer owns the signed slot index; prefix `++p` advances the
near entity pointer. Array decay `exatt_entities[pid_current]` is exact in this
TC4 build and avoids the redundant `[0]` or explicit address-of spelling.
`i != 8` was independently tested and changes CODE, so the loop retains
`i < 8`.

The earlier af1075w report's statement that removing `register` changes CODE
was too broad: the original experiment also moved declarations and changed
other expressions. Isolated stage `af1076a` removes only `register` from the
loop-local pointer and reproduces the complete original owner. Stage `af1076c`
then removes the temporary pointer scope block while retaining the natural
loop-local index and reproduces the same owner.

## State tests and control flow

All three named state equality tests are now variable-first:

```cpp
if(p->state == REIMU_UPDATE_FREE) {
    continue;
}
if(p->state == REIMU_UPDATE_ACTIVE) {
    // movement, reflection, collision and culling
} else if(p->state == REIMU_UPDATE_FLYING) {
    // flight handoff and optional trajectory initialization
} else if(REIMU_UPDATE_APPEARING_END >= p->state) {
    p->state++;
} else {
    p->state = REIMU_UPDATE_ACTIVE;
}
```

Isolated changes at `af1076b`, `af1076h`, `af1076i` and `af1076j` confirm the
FREE, ACTIVE and FLYING variable-first forms. The APPEARING range remains
variable-first as before. The branch order and early `continue` paths remain
unchanged. A `switch(p->state)` rewrite changes CODE and was rejected.

The byte-state advance remains postfix `p->state++`. Isolated `++p->state`
and `p->state += 1` experiments change CODE; do not infer that the velocity
increment has the same preferred spelling as the state-byte increment.

## Active movement, boundaries and collision

The active entity still advances X and Y before the original reflections and
playfield cutoff. Variable-first bounds remain exact:

```cpp
if((0 >= p->x) || (TO_SP(PLAYFIELD_W) <= p->x)) {
    p->velocity_x *= -1;
    p->x += p->velocity_x;
}
p->y += p->velocity_y;
if(TO_SP(-24) > p->y) {
    p->velocity_y *= -1;
    p->y = TO_SP(-24);
}
if(TO_SP(PLAYFIELD_H) <= p->y) {
    p->state = REIMU_UPDATE_FREE;
    continue;
}
p->velocity_y += 1;
```

The signed compound reflections `p->velocity_x *= -1` and
`p->velocity_y *= -1` must remain. Their apparently equivalent direct unary
negation assignments were separately rejected for horizontal and vertical
velocity in af765e and af765f. The vertical velocity increment accepts
`p->velocity_y += 1` and `++p->velocity_y`; explicit self-addition does not.
Collision origin updates, `hitbox_hittest()`, `exatt_collmap_set()` and the
final reset of `hitbox_hittest_skip_explosions` retain their original order.

## Flight angle lifetime and expression

The byte angle now exists only inside the successful flight-initialization
branch, and its first RNG draw is the initializer. The second draw contributes
through compound addition:

```cpp
} else if(p->state == REIMU_UPDATE_FLYING) {
    exatt_entity_p = p;
    if(exatt_fly_update()) {
        unsigned char angle = randring_far_next16_and(0x1F);
        angle += ((randring_far_next16_and(1) * 0x60) + 0x80);
        vector2(
            p->velocity_x, p->velocity_y,
            angle, ((round_speed / 8) + 0x32)
        );
    }
}
```

The angle is not needed when a flying entity does not initialize its
trajectory, nor in the active or appearing paths. Both the declaration
initializer and the `+=` form passed independently: `af1076f` accepted the
initializer, `af1076g` accepted compound angle addition, and `af1077d`
recompiled the complete current source with both forms together.

## Other rejected transformations

- `i != 8` in place of `i < 8` changes CODE.
- `switch(p->state)` changes CODE.
- Prefix `++p->state` changes CODE.
- `p->state += 1` changes CODE.
- The original signed velocity reflections must not be rewritten as direct
  unary negation assignments.
- The 50-byte `exatt_render_reimu()` function is unchanged in this pass.

## Complete original-owner verification

Stage `af1077d` rebuilt the complete `ex_reup` physical owner in two
independent original Turbo C++ 4.02 rounds. All 331 CODE bytes, 22 ordered
native fields and two PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The source
overlay independently checked the live `exatt_reimu_update.inl` include and
its actual compiler dependency record.

Report: `.analysis/work/exatt-layout-af1077d/report.json`

SHA-256: `405e6eaa5ad650f0e97a85f51e0a2a2a6516eb170b81ff2e709b0a3aa1ec0c3f`

Root producer source SHA-256: `52fb85cf1fc3c53c9e904d5b6717a1276190b56e236f7fceb3b81c74d3ed25a1`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

## Current five-owner Reimu / Yumemi / Chiyuri integration

Stage `af1077k` also rebuilt the current `ba_reimu`, `ba_yumem`, `ba_chiyu`,
`ex_rfly` and `ex_reup` owners together in two independent original TC4
rounds: 8,188 CODE bytes, 1,067 ordered native fields and 40 PUBLIC offsets
match. Both normal Japanese MAIN links reproduce the original loaded image
and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1077k/report.json`

SHA-256: `ac71f4eff35a78362537d81d8d01b1d306c8a86d4dfa137830c0775de65742b8`

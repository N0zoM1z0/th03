# TH03 MAIN HitCircle spawn: pointer arithmetic and coordinate expressions

The two spawn paths in the complete `hitcirc` physical owner now use natural
pointer arithmetic for their selected records, and the enemy random-center
path uses base-first arithmetic.

## Enemy slot selection

```cpp
HitCircle near& p = *(hitcircles + last_id);
```

This replaces the array-subscript reference while retaining the same near
record address and reference lifetime. The byte `last_id++` and the named
capacity wrap guard remain unchanged.

## Player slot selection

```cpp
HitCircle near& p = *(hitcircles + HITCIRCLE_ENEMY_COUNT);
```

The single player hit circle remains the thirteenth record after the twelve
enemy slots. The named enemy count still determines the same address.

## Random center arithmetic

Both enemy-center calculations put the RNG displacement first and the
hitbox origin second:

```cpp
randring_far_next16_mod(2 * hitbox.radius.x) +
    hitbox.origin.topleft.x.v
randring_far_next16_mod(2 * hitbox.radius.y) +
    hitbox.origin.topleft.y.v
```

The radius scale is constant-first. Each RNG call still occurs once and X
is still drawn before Y. The flag that suppresses random recentering and the
near-record coordinate stores remain in their original order.

## Spawn-to-screen coordinate arithmetic

Both enemy and player spawn paths use these exact groupings:

```cpp
(-(HITCIRCLE_W / 2)) + playfield_fg_x_to_screen(center_x, pid)
(PLAYFIELD_TOP - (HITCIRCLE_H / 2)) + TO_PIXEL(center_y)
```

The horizontal screen conversion remains a single call per spawn; the
vertical pixel conversion and top/half-height adjustment retain the same
integer result.

## Negative control

A natural-looking attempt to split the cel's initial age subtraction:

```cpp
_BX = age;
_BX--;
```

changed the complete `hitcirc` CODE. Keep `_BX = (age - 1);` and the
existing BX/AX division/multiply/add sequence. Earlier complete-owner
reviews document the register-local, shift, multiply and return-expression
alternatives that also changed the original code.

## Complete-owner verification

Stage `af1039f` rebuilt the complete `hitcirc` physical owner in two
independent original Turbo C++ 4.02 rounds. All 445 CODE bytes, 30 ordered
native fields and four PUBLIC offsets match. The object still has zero
private DATA/BSS. Both normal Japanese MAIN links reproduce the original
loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1039f/report.json`

SHA-256: `04592562692c98a3ca0d5df449f03cc8e6dfe598a231dbeaac68371b1e1f6750`


## Current-source spawn lifetime revalidation (af1068n)

Both spawn sites now express the two record-state writes directly in their
natural source order:

```cpp
p.age = 1;
p.pid = pid;
```

The previous `HitCircle::spawn(const pid2&)` member only performed those two
stores. After replacing both calls with the direct assignments, the now-unused
member was removed. This leaves the record's state transition visible at each
spawn site without changing the near-record reference, random-center path,
coordinate calculation, or store order.

Stage `af1068n` rebuilt the complete `hitcirc` physical owner in two
independent original TC4 4.02 rounds: all 445 CODE bytes, 30 ordered native
fields and four PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered relocations.

Current-source report: `.analysis/work/exatt-layout-af1068n/report.json`

SHA-256: `3c88d02174b30f1f9acbe4511f3494e8a4ce2f3b907e5d983717e7cd637464fd`


## Superseding current-source form (af1068s)

The af1068n direct spawn stores and removal of the now-unused `spawn()` member
remain in the current source. Two later lifetime changes were then re-tested
together: `hitcircles_update()` now uses a declaration-initialized signed-index
`while` loop with index-before-pointer increments, and `hitcircles_render()`
shares one `sprite16_offset_t so` between the enemy and player draw paths.

Stage `af1068s` rebuilt the complete `hitcirc` owner in two independent
original TC4 4.02 rounds: 445 CODE bytes, 30 ordered native fields and four
PUBLIC offsets match. Both normal Japanese MAIN links reproduce the original
loaded image and ordered relocations.

Current report: `.analysis/work/exatt-layout-af1068s/report.json`

SHA-256: `af14a3b0d2de5b3b25d324d7725caf693c5363b12bd4b9c98be1e565af35e50b`

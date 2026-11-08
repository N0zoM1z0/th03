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

# TH03 MAIN Bullet add: allocator pointer initialized after bounds guard (af1085x)

This pass revisits the complete 562-byte far-cdecl `bullets_add()` producer.
The function validates the template center, selects the bullet flag and
acceleration mode, clamps template speed, searches for the first free physical
slot, initializes the bullet/trail state, computes transfer-pellet targeting
or delegates velocity generation to the group dispatcher, then restores the
original template speed.

## Accepted pointer lifetime

The bullet record pointer is now initialized at the first point where the
allocator needs it, after the four center bounds have been checked:

```cpp
if(
    (bullet_template.center.y.v <= CENTER_MIN) ||
    (bullet_template.center.y.v >= CENTER_Y_MAX) ||
    (bullet_template.center.x.v <= CENTER_MIN) ||
    (bullet_template.center.x.v >= CENTER_X_MAX)
) {
    return;
}

bullet_t near *p = bullets;
switch(bullet_template.type) {
    // Select type, flag and acceleration.
}
```

The original pointer assignment instruction remains at the same control-flow
point. Only the C++ declaration/lifetime is narrowed past the early bounds
return. The first-free-slot `for` / `continue` / `break` allocator, the signed
index and near-pointer progression, trail-ring postfix byte mutation,
transfer-pellet branch and `group_velocity_set()` call ordering remain intact.

## Other allocator-scope experiments

Several other natural lifetime changes were compiled and rejected against
the complete physical Bullet owner:

- Moving `bullet_i` into the allocator `for` header changed CODE (`af1085k`).
- Moving `trail_i` into the trail block changed CODE (`af1085l`).
- Moving `group_i` down to the allocator loop changed CODE (`af1085m`).
- Moving the transfer-only speed scratch or origin X scratch into the
  transfer branch changed CODE (`af1085n`, `af1085o`).
- Moving the target-center union into the transfer branch changed CODE
  (`af1085p`).
- Moving the group completion flag into the velocity branch changed CODE
  (`af1085q`).

The successful pointer declaration is deliberately kept separate from those
rejected changes; it does not imply that every local can be moved to a
narrower block without changing TC4 register allocation.

## Complete original-owner verification

Stage `af1085w` rebuilt the complete Bullet physical owner in two independent
original Turbo C++ 4.02 rounds: all 2,685 CODE bytes, 196 ordered native
fields, 20 PUBLIC offsets and the original 9,500-byte BSS extent match. Both
normal Japanese MAIN links reproduce the original loaded image and ordered
MZ relocations. This source also includes the previously accepted
`++ring_remaining` update in the ordinary and aimed ring-count paths.

Report: `.analysis/work/exatt-layout-af1085w/report.json`

SHA-256: `340af6d938b01be5342a8fc0aace3cb044fad6ab2da02fb213ffe33baaa9bc6a`

Current `bullet.cpp` SHA-256:
`87c48268237fb4e75677bd3ce4e47b02a7762fb7f5f356022c09966304dba6c6`

## Eight-owner integration

Stage `af1085x` rebuilt `bullet`, `ba_koto`, `ba_reimu`, `ba_yumem`,
`ba_chiyu`, `ex_rfly`, `ex_reup` and `hitcirc` in two independent original
TC4 rounds: 13,158 CODE bytes, 1,555 ordered native fields and 75 PUBLIC
offsets match. Both normal Japanese MAIN links reproduce the original loaded
image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1085x/report.json`

SHA-256: `8e5883fb880311c5d785ccc16243c496309387ce5b81b6f1aef5eae2bdc249b7`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

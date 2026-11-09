# TH03 MAIN Bullet add/update/render: natural C++ loop lifetimes (af1086v)

This pass reworks several real control-flow regions across the complete
2,685-byte Bullet physical object, including the 562-byte `bullets_add()`,
438-byte `bullets_update()` and 477-byte `bullets_render()`. The goal is not
to rewrite register-sensitive operations indiscriminately: each natural loop
form was tested with original Turbo C++ 4.02 against the complete physical
object.

## Accepted `bullets_add()` loops and index progression

The per-bullet trail-history initializer now uses a natural `for` header,
retaining the original signed index and two independent XY stores:

```cpp
for(trail_i = 0; trail_i < TRAIL_POINT_COUNT; ++trail_i) {
    p->trail->center_x.v[trail_i] = bullet_template.center.x;
    p->trail->center_y.v[trail_i] = bullet_template.center.y;
}
```

The group velocity index advances with `group_i++`. Both prefix and postfix
forms are valid C++, but the postfix spelling is the current accepted source
form and was tested together with the complete owner. The original first-free
bullet allocator retains its `for` / `continue` / `break` shape; changing it
to `while` or narrowing its loop index still changes CODE.

## Large `bullets_update()` controller

The 438-byte update controller now uses `for(;;)` rather than `while(true)`.
The AX counter carrier is combined with the natural zero test:

```cpp
for(;;) {
    p++;
    if(!(_AX = --i)) {
        break;
    }
    // Full original update, collision, transfer and clipping body.
}
```

This preserves the critical order: advance the near bullet pointer, decrement
the signed remaining count into AX, then exit before processing the terminal
slot. All existing `continue` paths return to this same pointer/count sequence.
The compiler-sensitive AX/FLAGS and inline-assembly carriers inside the body
remain intact.

The apparently simpler `if(--i == 0)` form changes CODE. Removing the unused
`alive` byte counter, prefix-incrementing it, prefix-incrementing the byte age,
or replacing the age update with `+= 1` also changes CODE. These were tested
against the full object and rejected; the original `alive++` and `p->age++`
remain. The byte age update is therefore not being normalized based only on
source-level equivalence.

## Full-color, cloud and trail rendering

Both full-color 16×16 bullet traversal and the separate 32×32 monochrome cloud
pass now use natural `for` headers. The signed index and near pointer advance
in the loop expression after the sprite/cloud decision:

```cpp
for(bullet_i = 0; bullet_i < BULLET_COUNT; (bullet_i++, ++bullet_p)) {
    // Full-color bullet/trail pass, or cloud marker discovery.
}

if(need_cloud_pass) {
    bullet_p = bullets;
    for(bullet_i = 0; bullet_i < BULLET_COUNT; (bullet_i++, ++bullet_p)) {
        // Separate mono cloud sprite pass.
    }
}
```

The reverse trail-sprite walk also uses a `for` header. Its index and sprite
cel move only after `sprite16_put_noclip()` completes, in the original order:

```cpp
for(
    trail_i = (TRAIL_POINT_COUNT - 1);
    trail_i > 0;
    (trail_i -= TRAIL_POINTS_PER_SPRITE,
     so -= (BULLET16_W / BYTE_DOTS))
) {
    // Position and draw the current trail sample.
    sprite16_put_noclip(topleft.x, topleft.y, so);
}
```

The low-level 8×8 pellet renderer's bottom-tested `do/while` remains unchanged;
changing it to a top-tested `while` previously grew the original CODE extent.
The GRCG hardware operations, transfer-pellet semantics, trail-ring side
effects, and the two distinct rendering passes are unchanged.

## Rejected local-scope alternatives

- Removing `alive`, prefix-incrementing `alive`, prefix-incrementing `p->age`
  or replacing the age update with `+= 1` changed CODE (`af1086a`–`af1086d`).
- Register-qualifying the allocator's signed bullet index changed CODE
  (`af1086e`).
- Replacing the AX exit carrier with `if(--i == 0)` changed CODE (`af1086h`).
- Moving the pointer/count updates into the `for` condition changed CODE
  (`af1086l`).
- Moving the trail index or render index declarations into their `for`
  headers changed CODE (`af1086o`, `af1086s`, `af1086t`).

The accepted scope is intentionally narrow. A loop-header index does not
justify moving every scratch variable into that header.

## Complete original-owner verification

Stage `af1086y` rebuilt the complete Bullet physical owner in two independent
original Turbo C++ 4.02 rounds. All 2,685 CODE bytes, 196 ordered native fields
and 20 PUBLIC offsets match. The original 9,500-byte BSS extent is preserved,
and both normal Japanese MAIN links reproduce the original loaded image and
ordered MZ relocations. The source overlay independently checked the current
maintained `bullet.cpp` producer.

Report: `.analysis/work/exatt-layout-af1086y/report.json`

SHA-256: `432b76c60dfcfcecb86fc1127ed97e4460eb71de4c8d5c1bafa2addbc3fbb433`

Current `bullet.cpp` SHA-256:
`18e1c0293dca14b2de64f1c8d0e92164383c2ab9df5acd8e33a5ff234913dd5f`

## Eight-owner integration

Stage `af1086z` rebuilt the current Bullet owner together with `ba_koto`,
`ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`, `ex_reup` and `hitcirc` in two
independent original TC4 rounds: 13,158 CODE bytes, 1,555 ordered native
fields and 75 PUBLIC offsets match. Both normal Japanese MAIN links reproduce
the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1086z/report.json`

SHA-256: `ffee5155082a891c3ef83553341cc609d014b160e70faf40dcd75820c8736f0d`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

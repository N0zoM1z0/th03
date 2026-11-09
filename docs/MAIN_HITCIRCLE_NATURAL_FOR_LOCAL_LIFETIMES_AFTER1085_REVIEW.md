# TH03 MAIN HitCircle update/render: for-header and draw-local lifetimes (af1085f)

This pass takes the current four-function, 445-byte `hitcirc` physical owner
beyond the earlier cel arithmetic change. It narrows the signed loop-index
and cel-offset scratch lifetimes while retaining the near-record pointer's
original register role.

## Thirteen-record update

`hitcircles_update()` walks all thirteen records in ascending order. The
signed index advances before the near pointer in the comma-expression, just
as in the original loop body:

```cpp
register HitCircle near* p = hitcircles;
for(register int i = 0; i < HITCIRCLE_COUNT; (++i, ++p)) {
    if(p->age) {
        p->age++;
        if(HITCIRCLE_FRAMES < p->age) {
            p->age = 0;
        }
    }
}
```

This is a natural `for` representation of the original thirteen-record walk.
It preserves the byte postfix age update and the index-first / near-pointer-
second progression. The current form was not assumed from an old note: the
whole physical owner was rebuilt after the source change.

## Enemy and player rendering

The enemy pass renders twelve records. Its signed index is declared in the
`for` header, while the cel offset is declared only in the active-record
branch:

```cpp
for(register int i = 0; i < HITCIRCLE_ENEMY_COUNT; (++i, ++p)) {
    if(p->age) {
        sprite16_clip_set_for_pid(p->pid);
        sprite16_offset_t so = p->cel();
        sprite16_put(p->topleft.x, p->topleft.y, so);
    }
}

// The thirteenth record is the separately colored player circle.
if(p->age) {
    sprite16_clip_set_for_pid(p->pid);
    sprite16_offset_t so = p->cel();
    sprite16_put(p->topleft.x, p->topleft.y, so);
}
```

The enemy and player cel temporaries now have disjoint lifetimes instead of
sharing a function-scope `so`. The `HitCircle` near pointer remains live across
the enemy loop and points at the thirteenth record for the player draw. The
monochrome color setup, clip selection, `sprite16_put()` ordering and final
hardware interrupt sequence are unchanged.

## Cel arithmetic carried forward

The `HitCircle::cel()` member keeps the compiler-sensitive BX intermediate
and uses the natural compound assignment `_BX /= HITCIRCLE_FRAMES_PER_CEL`.
The following named VRAM stride multiply and three BX additions remain
unchanged. This compound division was independently verified at `af1084n`
and is included in the current `af1085e` / `af1085f` source bindings.

## Complete original-owner verification

Stage `af1085e` rebuilt the complete `hitcirc` owner in two independent
original Turbo C++ 4.02 rounds: all 445 CODE bytes, 30 ordered native fields
and four PUBLIC offsets match. Both normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations. The source overlay checked
the maintained `hitcircle.cpp` producer.

Report: `.analysis/work/exatt-layout-af1085e/report.json`

SHA-256: `51120b41a145c2d3222ac49d5c2afd11eb10c2fe6bdbcee3e45b856c9079ada5`

Current `hitcircle.cpp` SHA-256:
`74d7f7936070ad3c96137fe8dd0c6079cb7cd39ea5679cac27848d7508686c24`

## Seven-owner integration

Stage `af1085f` rebuilt the current `hitcirc` owner together with
`ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly` and `ex_reup` in two
independent original TC4 rounds: 10,473 CODE bytes, 1,359 ordered native
fields and 55 PUBLIC offsets match. Both normal Japanese MAIN links reproduce
the original loaded image and ordered MZ relocations. All seven maintained
source hashes are recorded in the report.

Report: `.analysis/work/exatt-layout-af1085f/report.json`

SHA-256: `072f2f02aad253e656f4f821f53bb483492f43362dc6f370ae4209624b1a27fe`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

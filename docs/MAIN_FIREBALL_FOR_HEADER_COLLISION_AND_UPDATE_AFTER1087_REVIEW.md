# TH03 MAIN Fireball: natural `for` headers for update, reverse hit scan and render (af1087f)

This pass changes three substantial original fireball control paths in the
complete 1,555-byte `e_fireb` physical object. It targets the 276-byte
`fireballs_update()`, 441-byte `fireballs_hittest()` and 69-byte
`fireballs_hittest_and_render()` functions. The update and hit-test changes
centralize the signed index and near-pointer progression in natural C++
`for` headers while preserving the original `continue` and `goto` behavior.

## 24-fireball forward update

`fireballs_update()` now advances the original signed index and near pointer
in one loop expression:

```cpp
for(i = 0; i < FIREBALL_COUNT; (++i, p++)) {
    if(!p->flag) {
        continue;
    }
    // Fall, transfer, explosion and collision-map updates.
}
```

The inactive, clipped/free, and transfer-to-fall branches all reach the same
loop expression through `continue`. The original `free_and_continue` and
`switch_to_fall` labels remain at their authentic points, and their state
mutations happen before the shared index/pointer progression. The byte frame
increment remains postfix: the earlier original-TC4 control `af891d` showed
that prefix increment changes CODE. The current session independently
repeated the negative control at `af1087g`: `++p->frame` changed the complete
`e_fireb` CODE payload and was restored to `p->frame++`.

## Reverse 24-entity fireball hit scan

`fireballs_hittest()` now has a single reverse scan expression:

```cpp
for(
    i = (EFE_COUNT - 1);
    i >= (EFE_COUNT - FIREBALL_COUNT);
    (--i, p--)
) {
    if(p->flag != FF_FALL) {
        continue;
    }
    // Hitbox, chain charge, transfer and explosion behavior.
}
```

The non-falling skip and no-hit skip now share the same post-body decrement
as the successful collision path. The original `chain_slot` is deliberately
still uninitialized. Its rare stack-dependent out-of-bounds behavior is a
historical gameplay landmine, not an invitation to initialize or repair it
as part of a control-flow reconstruction.

## Hit-test and render dispatcher

The 69-byte `fireballs_hittest_and_render()` uses a natural loop-header index
and near-pointer advance. Inactive slots still skip both drawing calls, while
active falling fireballs and explosion states retain their separate renderer
calls and original ordering.

## Complete original-owner verification

Stage `af1087e` rebuilt the entire Fireball physical owner in two independent
original Turbo C++ 4.02 rounds. All 1,555 CODE bytes, 115 ordered native fields
and ten PUBLIC offsets match. The original one-byte DATA and one-byte BSS
carriers are preserved, and both normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations. The source overlay checked
the maintained `fireball.cpp` producer.

Report: `.analysis/work/exatt-layout-af1087e/report.json`

SHA-256: `eef6db8073c533d8d449c8afaff22f32ab6e93a30febfe8c8bf3c920d22694cb`

Current `fireball.cpp` SHA-256:
`cccda5680a4f93648d15de6d599c14e799e2e3273751fde0b9ba8855760453cb`

## Nine-owner integration

Stage `af1087f` rebuilt the current Fireball owner together with `bullet`,
`ba_koto`, `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`, `ex_reup` and
`hitcirc` in two independent original TC4 rounds: 14,713 CODE bytes, 1,670
ordered native fields and 85 PUBLIC offsets match. Both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1087f/report.json`

SHA-256: `e1983561ed4dedbea01c2c9a395929bf69ff76d44ca2b05e461306dc09cd4c8f`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.

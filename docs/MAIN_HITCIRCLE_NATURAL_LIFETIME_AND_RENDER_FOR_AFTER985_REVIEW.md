# TH03 MAIN HitCircle: natural lifetime and renderer for headers

Both HitCircle traversal loops now use complete C++ `for` headers with
prefix updates of the signed index and near record pointer:

    for(i = 0; i < HITCIRCLE_COUNT; (++i, ++p))
    for(i = 0; i < HITCIRCLE_ENEMY_COUNT; (++i, ++p))

The loop-local index initialization moved into each header without changing
TC4 output. The lifetime loop still advances all thirteen physical records
(12 enemy and 1 player) after each age update. The renderer still draws only
the twelve enemy slots in order and leaves `p` pointing at the separate
player record for the later white monochrome draw.

The comma-expression order is significant. Reversing it to `(++p, ++i)`
changes the complete physical object. Keep index-before-pointer order.
The byte age postfix increment, age expiry check, separate player draw and
original sprite16 hardware-register calls remain unchanged.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af985b --units hitcirc
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af985b

Two independent original Turbo C++ 4.02 rounds recompiled the complete
445-byte `hitcirc` physical object, preserving all 30 ordered OMF FIXUPP
fields and four PUBLIC offsets. Both normal MAIN links reproduce the
124,642-byte Japanese loaded image and all 1,553 ordered MZ relocations.
The other 98 original game objects and Borland CRT were reused.

Protected current-source report:
`.analysis/work/exatt-layout-af985b/report.json`, SHA-256
`000fc1edb8af9c71f4daa3c91f14a9c64825f8fb4b06e89c1b25853d804641a1`.


## Current-source age walk and shared cel temporary (af1068s)

The current `hitcircles_update()` now uses a natural pre-tested `while` loop
with the signed index initialized at its declaration. The index and near
record pointer advance in the original order after each record's age update:

```cpp
register int i = 0;
while(i < HITCIRCLE_COUNT) {
    if(p->age) {
        p->age++;
        if(HITCIRCLE_FRAMES < p->age) {
            p->age = 0;
        }
    }
    ++i;
    ++p;
}
```

The original `for` header form and this natural `while` form both preserve the
complete current owner. The age postfix and expiry comparison remain unchanged.

`hitcircles_render()` now declares one `sprite16_offset_t so` before the enemy
loop and reuses it for both the twelve enemy draws and the separate player
circle draw. This shortens the source duplication without changing the
compiler's stack slot, `cel()` inlining, sprite call order, monochrome palette
transition or final hardware reset.

Stage `af1068s` rebuilt the complete 445-byte `hitcirc` owner in two original
TC4 4.02 rounds: 30 ordered native fields and four PUBLICs match, and both
normal Japanese MAIN links reproduce the original loaded image and ordered
relocations.

Report: `.analysis/work/exatt-layout-af1068s/report.json`

SHA-256: `af14a3b0d2de5b3b25d324d7725caf693c5363b12bd4b9c98be1e565af35e50b`

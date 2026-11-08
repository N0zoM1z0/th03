# TH03 MAIN HitCircle renderer: positive active-slot guard

The twelve-enemy rendering pass now keeps all work for a live record inside a
positive age guard:

```cpp
for(i = 0; i < HITCIRCLE_ENEMY_COUNT; (++i, ++p)) {
    if(p->age) {
        sprite16_clip_set_for_pid(p->pid);
        sprite16_offset_t so = p->cel();
        sprite16_put(p->topleft.x, p->topleft.y, so);
    }
}
```

This replaces the zero-age `continue` with the direct active-record condition.
The register cursor/counter remain SI/DI, the loop still visits exactly twelve
enemy slots, and the thirteenth player slot retains its separate white
monochrome pass. Sprite clipping, cel selection and draw ordering are
unchanged.

Stage `af1028d` rebuilt the complete `hitcirc` physical owner in two
independent original Turbo C++ 4.02 rounds. All 445 CODE bytes, 30 ordered
native fields and four PUBLIC offsets match. Both normal MAIN links reproduce
the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1028d/report.json`

SHA-256: `49d512c4b0870838be78bb1546b653b60e826c1464271adb8c7f142c467cda40`

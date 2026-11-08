# TH03 MAIN Chiyuri update: nonzero render-mode guard

The update controller now uses the byte-valued render-mode field directly as
a truth test:

```cpp
if(boss_render_mode) {
    boss_render_mode--;
}
```

`CHIYURI_RENDER_MODE_NORMAL` is zero, so this is the same non-normal guard
without repeating the enum name in a comparison. The decrement remains
postfix because the compiler-sensitive byte update is intentionally retained.

Stage `af1030d` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030d/report.json`

SHA-256: `bad47a358ec63b5c0f8fb5b1846cb5e98652c39a123e4ac5d4e1413f8bb65b2c`

# TH03 MAIN HitCircle renderer: explicit SI/DI traversal locals

`hitcircles_render()` now records the original two-register traversal directly
in its declarations:

```cpp
register const HitCircle near* p = hitcircles;
...
register int i;
```

The original renderer disassembly starts the record cursor in SI and the
signed enemy-slot counter in DI. Its twelve-slot pass increments DI and adds
six to SI together, then leaves SI pointing at the thirteenth player slot for
the separate monochrome draw. These declarations make the original register
roles explicit without changing the twelve-enemy/one-player split, clip calls,
cel calculation, sprite order, or final mask restore.

Stage `af1028c` rebuilt the complete `hitcirc` physical owner in two
independent original Turbo C++ 4.02 rounds. All 445 CODE bytes, 30 ordered
native fields and four PUBLIC offsets match. Both normal MAIN links reproduce
the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1028c/report.json`

SHA-256: `1d1de27f75bf83b17ef438918712f6629ef3b37587a28992fa269127ca5cdfff`

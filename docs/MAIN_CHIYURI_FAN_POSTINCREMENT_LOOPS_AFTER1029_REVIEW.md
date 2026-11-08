# TH03 MAIN Chiyuri fan generator: postfix loop increments

All four fan passes now use the ordinary postfix loop increment:

```cpp
for(i = 0; i < chiyuri_fan_count; i++) {
    // original fan coordinate, angle, projectile and speed work
}
```

The returned old value of built-in `int` is unused, so the source remains a
straightforward traversal while the compiler emits the target's `INC SI` at
the end of each pass iteration. This applies to both horizontal speed sweeps
and both vertical speed sweeps; the four loops, projectile ordering, speed
updates and byte-angle assignments remain separate and unchanged.

Stage `af1029j` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1029j/report.json`

SHA-256: `69d0cec573550a3ca5df9c4848932055fddde651a845428c00450b4315efcf1c`

# TH03 MAIN Chiyuri intro: mutually exclusive frame phases

`gba_boss_update_chiyuri()` now expresses the two distinct intro-frame tests
as one `if`/`else if` chain:

```cpp
if(boss_frame == CHIYURI_INTRO_DONE_FRAME) {
    // complete intro, enter selection and initialize the palette cycle
    break;
} else if(boss_frame == CHIYURI_INTRO_CROSS_EFFECT_FRAME) {
    // emit the four intro cross-effect bombs
    break;
}
// ordinary intro frame: enable animation and return
```

The two frame constants select mutually exclusive actions. The completion
frame still resets the clock and changes mode before leaving the switch; the
cross-effect frame still emits four bombs in left, right, upper, lower order;
all other intro frames still enable animation and return. The shared collision
and hitbox tail remains reached only after the same cases as before.

Stage `af1026h` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1026h/report.json`

SHA-256: `ca3aa1804cd72fa4ad038bc1d819dc7812387db66058b7467a7a2a7f23a00a80`

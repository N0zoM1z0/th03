# TH03 MAIN Mima update: explicit intro success branch

The INTRO case in the 298-byte `gba_boss_update_mima()` controller now makes
both outcomes explicit:

```cpp
case MIMA_MODE_INTRO:
    if(boss_frame == MIMA_BOSS_INTRO_END) {
        boss_frame = 0;
        boss_mode = MIMA_MODE_SELECT;
        break;
    } else {
        return;
    }
```

The completion frame resets the timer and enters SELECT before reaching the
shared collision tail; every other INTRO frame returns immediately. This is
the positive-form branch for the same mutually exclusive frame outcomes.

Stage `af1030f` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030f/report.json`

SHA-256: `f475c51e08e98e93fd1149dad11f62f28cde27bd20c366ead35397732d95dd59`

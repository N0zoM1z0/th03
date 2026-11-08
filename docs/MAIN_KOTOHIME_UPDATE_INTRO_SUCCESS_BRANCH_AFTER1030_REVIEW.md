# TH03 MAIN Kotohime update: explicit INTRO success branch

The 332-byte `gba_boss_update_kotohime()` controller now expresses the INTRO
completion path positively:

```cpp
case KOTOHIME_MODE_INTRO:
    if(boss_frame == KOTOHIME_INTRO_FINISH_FRAME) {
        boss_frame = 0;
        boss_mode = KOTOHIME_MODE_SELECT;
        break;
    } else {
        return;
    }
```

The completion frame resets the timer and enters SELECT before reaching the
shared collision tail. Every other INTRO frame returns without reaching that
tail. The positive branch retains the original switch exit and timing.

Stage `af1030m` rebuilt the complete `ba_koto` physical owner in two
independent original TC4 rounds. All 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030m/report.json`

SHA-256: `351fe11755f7cea6011d8a2d8bd0cd805a1e8d8965548a90f2b08aeeb9d05001`

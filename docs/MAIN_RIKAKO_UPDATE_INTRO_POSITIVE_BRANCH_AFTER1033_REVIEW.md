# TH03 MAIN Rikako Update: positive INTRO completion branch

The INTRO case in the complete Rikako update controller now expresses
completion as the positive equality branch:

```cpp
case RIKAKO_MODE_INTRO:
    if(boss_frame == RIKAKO_INTRO_FINISH_FRAME) {
        boss_frame = 0;
        boss_mode = RIKAKO_MODE_SELECT;
    } else {
        return;
    }
    break;
```

Non-completion frames still return immediately. Completion still resets the
frame, selects the next pattern mode and exits the switch before the existing
signed-byte spin compound update and collision/hitbox tail.

Stage `af1033n` rebuilt the complete `ba_rikak` physical owner in two
independent original TC4 4.02 rounds. All 1,677 CODE bytes, 215 ordered native
fields and eight PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033n/report.json`

SHA-256: `bb6703f499aeff7c0e76f1e441dec1252b5d58fbab4906ca34dd77e7aebc5726`

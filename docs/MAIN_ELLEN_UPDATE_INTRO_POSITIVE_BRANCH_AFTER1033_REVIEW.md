# TH03 MAIN Ellen Update: positive INTRO completion branch

The INTRO case in the complete Ellen update controller now spells its
completion path as a positive equality branch:

```cpp
case ELLEN_MODE_INTRO:
    if(boss_frame == ELLEN_INTRO_FINISH_FRAME) {
        boss_frame = 0;
        boss_mode = ELLEN_MODE_SELECT;
    } else {
        return;
    }
    break;
```

The non-completion frame still returns immediately. On the completion frame,
the 16-bit clock is reset and SELECT is entered before the switch exits.
The render-frame postfix increment remains before the BOSS frame increment;
the remaining attack dispatch and collision/hitbox work is unchanged.

Stage `af1033m` rebuilt the complete `ba_ellen` physical owner in two
independent original TC4 4.02 rounds. All 1,675 CODE bytes, 213 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033m/report.json`

SHA-256: `6492ea8471350aecc7e5298f66d5577c09d7fded4f06e41a10fc7dfdb47f1368`

# TH03 MAIN Marisa Update: positive INTRO completion branch

The INTRO case in the 269-byte `gba_boss_update_marisa()` controller now
expresses completion as the positive equality branch:

```cpp
case MARISA_MODE_INTRO:
    if(boss_frame == MARISA_BOSS_INTRO_END) {
        boss_frame = 0;
        boss_mode = MARISA_MODE_SELECT;
    } else {
        return;
    }
    break;
```

Previously the same case returned when the frame did not equal the completion
constant and otherwise fell through to the reset/SELECT assignments. The
positive branch makes the completion path explicit while retaining the
non-completion early return, frame reset, mode assignment and switch exit.

Stage `af1033g` rebuilt the complete `ba_maris` physical owner in two
independent original TC4 4.02 rounds. All 1,431 CODE bytes, 199 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033g/report.json`

SHA-256: `827d40dbab29d0346285cfe562a4590c06b5ef05f5f698a50c3e8f087ef3ea44`

# TH03 MAIN Kana Update: positive INTRO completion branch

The INTRO case in the complete Kana update controller now expresses
completion as the positive equality branch:

```cpp
case KANA_MODE_INTRO:
    if(boss_frame == KANA_INTRO_COMPLETE_FRAME) {
        boss_frame = 0;
        boss_mode = KANA_MODE_SELECT;
    } else {
        return;
    }
    break;
```

A non-completion frame still returns immediately. On the completion frame,
the clock is reset and SELECT is entered before the switch exits. The
following controller behavior, including render-frame postfix increment and
the collision/hitbox tail, remains unchanged.

Stage `af1033k` rebuilt the complete `ba_kana` physical owner in two
independent original TC4 4.02 rounds. All 1,874 CODE bytes, 274 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1033k/report.json`

SHA-256: `95a6678957ecb95978c671257b867823a1c671ffb9768fbc9cc8252306714ab5`

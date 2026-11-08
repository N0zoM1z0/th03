# TH03 MAIN Kotohime update: natural intro completion guard

`gba_boss_update_kotohime()` now expresses the intro case as an early return
for every frame except the completion frame:

```cpp
case KOTOHIME_MODE_INTRO:
    if(boss_frame != KOTOHIME_INTRO_FINISH_FRAME) {
        return;
    }
    boss_frame = 0;
    boss_mode = KOTOHIME_MODE_SELECT;
    break;
```

This removes the nested `if/else` while retaining the same state transition:
the intro continues to return until its exact terminal frame, then resets the
clock, switches to selection mode and resumes the common controller tail.
The remaining mode dispatch, collision update and hitbox sequence are
unchanged.

The complete `ba_koto` physical object is source-bound to `af1025c`. Two
independent original Turbo C++ 4.02 rounds reproduce all 1,840 CODE bytes,
262 ordered native fields and eleven PUBLIC offsets. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

A separate experiment hoisted the repeated `gba_boss_level / 2` expression
into a `const int` local for the seven difficulty parameters. That changed the
complete `ba_koto` CODE and was reverted; the original independent expressions
remain until a native-exact natural form is found.

Protected report: `.analysis/work/exatt-layout-af1025c/report.json`

SHA-256: `024db141ba0924a156d377b8efb9dd2c122e0664daa9e2b470e5ac08af8a18ce`

## Outer launched-player guard recovery

The same 332-byte `gba_boss_update_kotohime()` controller now uses the direct
inactive-player return before its main update body:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}

pid_other = (1 - pid_current);
```

This removes the outer `if(equal) { ... } else { return; }` nesting without
changing the one active player's update sequence, the mode switch, the shared
collision-map setup, or the final boss hit test. It is deliberately a guard
at the controller boundary, before target tracking, frame advancement and
bullet-template PID assignment.

Stage `af1026a` rebuilt the complete `ba_koto` owner in two independent
original Turbo C++ 4.02 rounds. All 1,840 CODE bytes, 262 ordered native
fields and eleven PUBLIC offsets match, and both normal MAIN links reproduce
the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1026a/report.json`

SHA-256: `316468b7dcc6a3a8ba02aeccb7803633356553e450bda55e812a9a2bfb948079`

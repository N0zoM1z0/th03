# TH03 MAIN Chiyuri Cardinal: positive cadence guard

The 352-byte `chiyuri_pattern_cardinal()` leaf now places the full attack
body under its firing-frame condition:

```cpp
if((boss_frame % chiyuri_cardinal_interval) == 1) {
    // first-frame cross bombs, finish transition, four cardinal shots
}
```

The previous form returned immediately when the remainder was not one. The
positive form makes the firing condition the scope of the entire body while
leaving the first-frame setup, end-frame transition, angle reversal and
four-shot emission order unchanged.

Stage `af1030h` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030h/report.json`

SHA-256: `fce1c5dbc9924c617068b13d11416154e74d7cb639ab5f45f7a2745d211e9d04`

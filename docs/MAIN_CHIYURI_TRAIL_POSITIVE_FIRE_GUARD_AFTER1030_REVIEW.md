# TH03 MAIN Chiyuri Trail: positive fire-frame guard

The 115-byte `chiyuri_pattern_trail_ring()` leaf now scopes the release
sequence under its positive fire-frame condition:

```cpp
if(CHIYURI_TRAIL_FIRE_FRAME == boss_frame) {
    // initialize the 48-shot trailing ring and return to SELECT
}
```

The periodic warning-bomb check remains before this condition, so every
eight-frame warning still occurs independently of the final release frame.
Only the inverse early return around the one-time ring emission was changed.

Stage `af1030j` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1030j/report.json`

SHA-256: `fd9c5fe013c15f66c7856864071e39eb38f006377697c2510d42c4d5d7162d36`

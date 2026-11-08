# TH03 MAIN Chiyuri Update: explicit paired-center index scaling

The 613-byte `gba_boss_update_chiyuri()` SELECT path now expresses its
paired-center word-array index with a natural left shift:

```cpp
random_i = (randring_far_next16_mod(5) << 1);
boss_center_x = chiyuri_boss_x_words[random_i];
boss_center_y = chiyuri_boss_y_words[random_i];
```

The random helper still returns one of five center pairs, and shifting by one
converts that pair number into the even word index used by both arrays. The
random call is still evaluated once, and X/Y still use the same index in the
same order. TC4 lowers this spelling to the same byte arithmetic and the
complete original owner remains exact.

A separate attempt to cache `gba_boss_level` in a local `unsigned char level`
for the seven initialization formulas changed the complete `ba_chiyu` CODE
and was reverted. The original repeated direct reads remain in place.

Stage `af1032b` rebuilt the complete `ba_chiyu` physical owner in two
independent original TC4 4.02 rounds. All 2,654 CODE bytes, 381 ordered native
fields and eleven PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1032b/report.json`

SHA-256: `b96327fc1e286853766e0d069c35031b0d87bfb56ce8fa0473cfd093f50b2d9e`

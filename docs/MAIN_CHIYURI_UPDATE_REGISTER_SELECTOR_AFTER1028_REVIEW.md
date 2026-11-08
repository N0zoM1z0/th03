# TH03 MAIN Chiyuri update controller: register-qualified selector

The `random_i` local in the 613-byte `gba_boss_update_chiyuri()` controller is
now declared as a register-qualified byte:

```cpp
register unsigned char random_i;
```

It carries the even index produced by `randring_far_next16_mod(5) * 2` while
SELECT chooses the paired boss-center X/Y entries. The selector width and
random-call order are unchanged; this is a source-level register intent for a
value used only within that selection path.

Stage `af1028f` rebuilt the complete `ba_chiyu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLIC offsets match. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1028f/report.json`

SHA-256: `df3b264833e129071b0213278160a90eb20b2d8d9731aa46a4df6f30647a41ef`

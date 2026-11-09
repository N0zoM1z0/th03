# TH03 MAIN Yumemi Aimed Random: natural period-mask firing cadence (af1070a)

The 266-byte `yumemi_pattern_aimed_random()` leaf now expresses its period-two
firing gate as a natural word mask with a variable-first zero comparison:

```cpp
if((boss_frame & (YUMEMI_AIMED_FIRE_PERIOD - 1)) == 0) {
    // sound, aimed projectile template, RNG draws and bullets_add()
}
```

`YUMEMI_AIMED_FIRE_PERIOD` remains the named period value (2); subtracting one
forms the corresponding low-bit mask. This recovers the target's even-frame
cadence without hard-coding an unrelated literal or changing the sequence of
sound, speed RNG, type RNG, group RNG and projectile emission.

## Independent natural-expression trials

All three forms below were tested against the complete `ba_yumem` physical
owner in two original TC4 rounds and all matched:

```cpp
if(0 == (boss_frame % YUMEMI_AIMED_FIRE_PERIOD))
if(0 == (boss_frame & (YUMEMI_AIMED_FIRE_PERIOD - 1)))
if(!(boss_frame & (YUMEMI_AIMED_FIRE_PERIOD - 1)))
```

The maintained source chooses the variable-first explicit mask comparison;
it is direct, readable and follows the source's existing variable-first
frame predicates. The older modulo form also remains a valid exact source
spelling, but is no longer needed for this firing gate.

## Original-owner verification

The individual trial at `af1069z` rebuilt all 2,358 CODE bytes, 343 ordered
native fields and ten PUBLIC offsets in two independent original TC4 4.02
rounds. Both normal Japanese MAIN links reproduce the original loaded image
and ordered MZ relocations.

The final joint current-source integration `af1070a` rebuilt Yumemi and
Chiyuri together in two independent rounds: 5,012 CODE bytes, 724 ordered
native fields and 21 PUBLIC offsets match, as do both complete normal MAIN
links and ordered relocations.

Integration report: `.analysis/work/exatt-layout-af1070a/report.json`

SHA-256: `efb3df5395b7952a6652ce13920de53c65a4edfeeba5b5b305c1cbdec34884e3`

Current Yumemi source SHA-256: `e93146d2915798e5de6ff7214fdf6e8bc9ef78889e61c26603925e89aca2d8b3`

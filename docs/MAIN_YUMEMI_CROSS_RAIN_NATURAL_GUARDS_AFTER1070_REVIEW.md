# TH03 MAIN Yumemi Cross Rings and Rain: natural cadence and finish guards (af1070h)

This pass reopens two additional attack leaves after the Aimed Random and Rain
index work: `yumemi_pattern_cross_rings()` and `yumemi_pattern_rain()`.

## Cross Rings

The variable interval firing gate now uses an explicit zero remainder test:

```cpp
if(0 == (boss_frame % yumemi_cross_interval)) {
    // four independent RNG angle draws and four ring projectiles
}
```

The finish guard is written with the frame on the left:

```cpp
if(boss_frame >= YUMEMI_CROSS_FINISH_AT) {
    boss_mode = YUMEMI_MODE_SELECT;
    boss_frame = 0;
}
```

The four random-angle draws, paired horizontal/vertical displacement stores,
ring group/speed/type setup and `bullets_add()` order remain unchanged.

## Rain

The variable-word rain interval uses the same explicit zero remainder form.
The finish guard now uses `boss_frame >= YUMEMI_RAIN_FINISH_AT`. The loop's
signed index remains declared in its sole `for` initializer, and all twelve
independent random X draws and twelve byte-angle draws remain separate:

```cpp
for(register int i = 0; i < YUMEMI_RAIN_DROPS_PER_WAVE; ++i) {
    // one X RNG draw, one byte-angle RNG draw, one bullets_add()
}
```

The interval is dynamic and remains modulo; only the constant period-two
Aimed Random gate uses a low-bit mask. No variable interval was replaced by a
mask.

## Original-owner verification

The Cross Rings and Rain predicate/lifetime experiments each rebuilt the
complete `ba_yumem` owner in two original TC4 rounds. The final joint stage
`af1070h` rebuilt Yumemi and Chiyuri together: 5,012 CODE bytes, 724 ordered
native fields and 21 PUBLIC offsets match. Both complete normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1070h/report.json`

SHA-256: `878048b4f927d4afa219d30ecf5c8a1660cfa8395fc7b4865bd7b9fceb3a68f4`

Yumemi source SHA-256: `da4d7feab5930a50c5816c35b5bf018de3a8a360b6e8969e50ea26847fccba62`

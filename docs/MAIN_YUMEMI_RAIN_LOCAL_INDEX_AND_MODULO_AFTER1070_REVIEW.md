# TH03 MAIN Yumemi Rain: loop-local index and explicit interval zero test (af1070d)

The 238-byte `yumemi_pattern_rain()` function now gives its twelve-drop signed
index the narrowest natural lifetime: the `register int i` declaration lives
in the only `for` header that uses it.

```cpp
for(register int i = 0; i < YUMEMI_RAIN_DROPS_PER_WAVE; ++i) {
    bullet_template.center.x.v =
        randring_far_next16_mod(TO_SP(PLAYFIELD_W));
    bullet_template.angle = (
        YUMEMI_RAIN_RANDOM_ANGLE_BIAS +
        randring_far_next16_and(YUMEMI_RAIN_RANDOM_ANGLE_MASK)
    );
    bullets_add();
}
```

The variable-word rain interval gate now uses an explicit zero remainder test:

```cpp
if(0 == (boss_frame % yumemi_rain_interval)) {
```

The variable interval remains a real modulo operation; unlike the period-two
Aimed Random cadence, it cannot be replaced by a fixed low-bit mask. The sine
movement, spread warning shots, rain group/speed setup, twelve independent RNG
X draws, twelve independent byte-angle draws, one `bullets_add()` per drop and
finish transition remain in their original order.

## Original-owner verification

Stage `af1070d` rebuilt the complete `ba_yumem` owner in two independent
original Turbo C++ 4.02 rounds: all 2,358 CODE bytes, 343 ordered native fields
and ten PUBLIC offsets match. Both normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations.

The same stage jointly rebuilt Yumemi and Chiyuri: 5,012 CODE bytes, 724
ordered native fields and 21 PUBLIC offsets match in both rounds, as do both
normal MAIN links and ordered relocations.

Report: `.analysis/work/exatt-layout-af1070d/report.json`

SHA-256: `355f608a6951c8cb462495e3b42b7c237f80b418e1808d0ba58931f39ea9b60d`

Yumemi source SHA-256: `438b08e5765e2737a35667a1772ab85b3ff7df35fe2841a7b81d42f0cbdf6da9`

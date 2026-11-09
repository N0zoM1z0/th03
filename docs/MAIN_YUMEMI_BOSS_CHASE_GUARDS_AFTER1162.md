# Yumemi BOSS: exact chase phase and attack guards

The complete `ba_yumem` physical owner now uses natural C++ phase and
frame comparisons throughout the chase controller, the player-side render
clip and the ring/rain/aimed warning stages. The aimed-shot RNG masks are
named without changing the order of the speed, type and group draws.

The actual original TC4/TLINK probe `af1162c` independently compiled and
linked the entire 2,358-byte CODE owner twice. Both rounds reproduced all
343 ordered native fields, ten PUBLICs, the Japanese MAIN loaded image and
all ordered MZ relocations.

A separate `af1162b` experiment reversed the chase seek-range predicate
and consolidated its two exits. Although its movement state transitions
looked equivalent, TC4 emitted different CODE; the original positive
short-circuit range test is therefore retained. Follow up by studying
that transition's register/control-flow geometry, not by assuming a
logical simplification is a native match.

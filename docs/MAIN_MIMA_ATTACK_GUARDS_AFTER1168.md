# Mima BOSS: native warmup and barrage-phase exits

The full `ba_mima` owner now handles inactive spread frames with an early
return before the two-frame bullet and six-frame pellet logic. The random
Bomb pattern also exits after its warning markers but before its later
four-frame volleys, ring burst, sound and finish checks. These are meaningful
control-flow changes in two attack state machines, not extracted leaf patches.

Original TC4/TLINK stages `af1168a` and `af1168b` each matched all 1,922
CODE bytes, 277 ordered native fields, nine PUBLICs, the Japanese MAIN image
and MZ relocations in two compiler/link rounds. Preserve the original
warning-phase `else if`: a separate earlier trial showed it is codegen-
sensitive even when the numeric conditions look equivalent.

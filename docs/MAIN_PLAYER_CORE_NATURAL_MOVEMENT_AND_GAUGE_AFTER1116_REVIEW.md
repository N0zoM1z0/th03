# TH03 MAIN — complete player core: natural retry, CPU fire and gauge thresholds (af1116g)

The original `core` Turbo C++ 4.02 object physically includes movement,
Hyper, player state update, player render/overlay/knockback/bomb handling and
shot sprite preparation. Its 1,106-byte `player_state_update` is a substantial
live state machine inside the **3,135-byte** original physical owner, not a
standalone extracted leaf. Its nested human movement retry now uses natural
`while(1)` without changing how the original invalid-movement retry, last
movement, or position clamp work. Its periodic CPU auto-shot checks now use a
natural unsigned-word `if(!remainder)`; every shot, enemy marker, gauge and
RNG observation remains in its original order.

Named native 16-bit charge-spend/minimum and invincibility constants express
the three distinct Gauge Attack branches and Hyper drain. Named shot hold,
charge, fire and release thresholds replace overlapping untyped literals.
The human movement `first_attempt` Boolean now initializes at its actual
first use, inside the human movement branch. The original persistent
`movement` scratch retains its wider lifetime, which is TC4 codegen-visible.

The original compiler experiment sequence was `af1116a` (retry), `af1116d`
(gauge constants), `af1116e` (shot/fire/invincibility constants), `af1116f`
(CPU cadence), and final `af1116g` (first-use Boolean). Every accepted trial
recompiled the **complete** original `core` owner in two independent TC4 and
normal MAIN TLINK rounds, matching all 3,135 CODE bytes, 260 ordered original
native fields, 21 PUBLICs, the full Japanese MAIN loaded image and all 1,553
ordered MZ relocations. Final retained proof:
`.analysis/work/exatt-layout-af1116g/report.json`.

Independent failures: `af1116b` narrowed the main `player` register-pointer
lifetime, `af1116c` narrowed both human movement locals, and `af1116h`
isolated the actual culprit to the `movement` local alone. All changed the
original CODE and were rolled back. The already-successful narrowed
`first_attempt` Boolean remains. This is local source-native recovery, not
canonical Factory packed-game credit.

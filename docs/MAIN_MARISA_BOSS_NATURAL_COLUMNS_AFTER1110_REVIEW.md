# TH03 MAIN — Marisa BOSS column phases and native word clocks (af1110d)

The complete original `ba_maris` physical Turbo C++ 4.02 owner now expresses its
unsigned 16-bit spread, ring and main-render flicker clocks using `%4`, `%32`
and `%4`. Both wide and narrow Extra Attack column controllers use separate
natural `if` branches after their original early returns; emission coordinates,
original warning frames and the terminal update remain unchanged. The hit
sprite renderer uses natural byte truthiness rather than `!= 0`.

Each change was checked in its full native owner, not just as a leaf:
`af1110a` for word clocks, `af1110b` for the two long column state machines,
and final `af1110d` for the sprite-hit condition. All pass two original
TC4/TLINK rounds, including 1,431 original CODE bytes, 199 ordered native
fields, nine PUBLICs, full Japanese MAIN image and all 1,553 ordered MZ
relocations. The final current source-bound receipt is
`.analysis/work/exatt-layout-af1110d/report.json`.

At `af1110c` an independent experiment changed the attack renderer's
register-visible literal coordinate steps to enum-valued compound assignments;
TC4 changed CODE, so those particular expressions were restored. Keep the
character's exact call/RNG sequence and signed speed division. No new
canonical Factory claim or whole-game coverage credit follows from this
source-level improvement.

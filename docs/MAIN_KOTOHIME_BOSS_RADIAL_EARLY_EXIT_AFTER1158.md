# Kotohime BOSS: radial burst and sprite mode early exits

The full `ba_koto` owner now expresses its radial burst release as a natural
`return` while its warning frame has not elapsed. The nested ring-center and
per-center bullet loops still execute only after this guard and retain all
signed angular divisions, byte speed assignments and projectile call order.
The main renderer likewise exits before ring drawing when no ring mode is
active, and the renderer's signed radius initializes at first use. The
pellet-arc finish comparison is expressed with the original constant first.

Two original TC4/TLINK rounds at `af1158e` matched all 1,840 CODE bytes,
262 ordered native fields, 11 PUBLICs, and the complete Japanese MAIN image
and relocations. A separate `af1158a` test inverted the expanding-ring
branch and moved its `boss_move_sine()` path to an early return; TC4 produced
different code, so that expansion branch remains in its original order.

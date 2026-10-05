# MAIN hitbox, combo and gauge review

The maintained owners are `src/main/collision/hitbox.cpp`,
`src/main/player/combo.cpp` and `src/main/player/gauge.cpp`. Their complete
CODE contributions are declared in `config/th03_main_exact_units.toml`.
The frozen upstream wrappers and implementations are intake candidates;
the Japanese target and pinned compiler replay determine local acceptance.

Target SHA-256:
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
The MAIN Ghidra database was re-attested before the queries. The independent
raw export verifies the complete function/producer byte partition, target
digest, decode coverage, RET boundaries and relocation edges:

```sh
python3 scripts/review_th03_main_code.py \
  --owner th03-main-hitbox --owner th03-main-combo --owner th03-main-gauge \
  --output .analysis/th03-main-exact/sol-collision-combo-target-review/raw-review.json
```

Semantic names below are proposed by upstream and the candidate MAP; offsets,
instructions and relocations are observed from the pinned target.

| Owner | CODE segment in MAIN_04 | 139D offset | Bytes |
| --- | --- | --- | ---: |
| hitbox | HITBOX_TEXT | 1F25 | 266 |
| combo | P_COMBO_TEXT | 22E9 | 491 |
| combo | E_ENEMY_TEXT | 2765 | 40 |
| combo | ENEMY_PUT | 2B7E | 103 |
| combo | E_EXPL_TEXT | 2BE5 | 344 |
| gauge | P_GAUGE_TEXT | 24D4 | 55 |

These six contributions contain seven complete functions and 1299 bytes.
There are no switch tables, shared tails or padding bytes in these extents.
The intervening original assembly and enemy functions are separate owners.
Each of the three candidate MAP owners has zero-byte DATA/BSS contributions
at 1D56:0BEC / 1D56:8DF8. Shared state, glyph data and callback implementations
remain outside their source acceptance scope and are forwarded explicitly
through `compat/rec98/` where declarations have not been localized.

## Hitbox target observations

`hitbox_hittest` is far cdecl, has no arguments, returns damage in AL, and
ends in RETF. It rejects negative hitbox Y or defeat flag 2, then destructively
converts center/radius into top-left/right/bottom coordinates. It clears
`ef_onehit` and uses exactly 32 shot-pair records at a 14-byte stride. A pair
must have alive byte 1 and the matching player byte at +0C. Each intersecting
pair is removed, adds two damage, and invokes the far hit-circle routine.
The horizontal edges and the Y center comparisons preserve inclusive bounds.

If the explosion-skip byte is zero, the target's NOP/PUSH CS/near CALL enters
the far-return explosion function. The two charge-shot callbacks are indirect
far calls through four-byte DGROUP pointers at 2D3C and 2D40. Bomb damage adds
one on even round/result frames. Damage additions retain the unsigned byte
wrap behavior. The sole owned MZ relocation is at owner-relative site 181,
in the direct far hit-circle call.

## Combo target observations

P_COMBO_TEXT contains `combo_add_raw` (154 bytes, far Pascal, RETF 6) and
`combos_update_and_render` (337 bytes, far cdecl, RETF). The near `combo_add`
wrapper (RET 6), fireball-charge helper (RET 4), and point-based boss/panic
helper (RET 4) own the other three contributions. All byte arguments occupy
16-bit Pascal stack slots. No argument width or near/far ABI has been changed
to manufacture code equality.

The raw addition widens the new bonus and existing total to 32 bits, clamps
at 65535, and records the player's full hit count and bonus maximum before
clamping visible hits to 99. Player fields are observed at +70 for the bonus
word and +72 for the hit byte, with a 128-byte player stride. Combo records
have a four-byte stride: timer, highest-hit byte, and total word. Hits below
two return the current total without changing it. Timer values 80 and 32,
and the 65535 exception to timer refresh, remain as observed.

The update/render loop handles both players. It decrements the timer before
the frame-phase color condition, retains the bitwise boolean AND, and adds
the bonus to score only when the timer reaches zero. Text strings and glyph
constants are external dependencies; their resource ownership is still open.
P_COMBO_TEXT owns ordered relocation sites 209, 227, 272, 306, 334, 408, 436,
451 and 466. The other three contributions own no relocations.

The fireball helper uses the existing collision chain slot, clears charge
at the `12 - round_speed/16` threshold, saves/restores the global EFE pointer,
and retains the symbolic NOP/PUSH CS/near CALL to the far-return fireball
function. The boss/panic helper preserves warning and active-attack guards,
clears the three chain fields, adds 5120 to the unsigned word threshold,
caps boss/gauge levels at 16, and preserves the separate fired/reversed/panic
counter paths and the 30000 panic threshold. These are static target
observations, not independently recorded gameplay runtime traces.

## Gauge target observations

`gauge_avail_add` is near Pascal with RET 4. It indexes a 128-byte player
record, rejects a nonzero hyper byte at +1E or an available gauge word at +1A
already at least 4080, adds the zero-extended byte charge, and clamps at 4080.
The compared maximum and unsigned branches match the maintained declaration.
It owns no direct calls or relocation sites.

## Acceptance

The initial frozen-scaffold comparison matched every byte and ordered
relocation. `sol-hitbox-combo-gauge-probe-20261005` then passed two full cold
builds with all maintained source: 47 functions, 20 CODE extents, 7509 owned
bytes, every MAP contribution and ordered relocation, and the deterministic
20-product / 351-game-object vector. All 417 generated OMF objects were
validated. The three owners are locally exact in the unit/evidence ledgers.
`sol-hitbox-combo-gauge-final-20261005-b` repeated the complete replay with the
new exact states and their scoped evidence frozen at build start; it passed.
Automatic
Ghidra types, upstream exactness, and that preliminary comparison do not
grant acceptance themselves. Whole-product ownership remains open.

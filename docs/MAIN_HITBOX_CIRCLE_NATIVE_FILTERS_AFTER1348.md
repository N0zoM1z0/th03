# Hitbox and HitCircle: original collision short circuit and near-record state

The physical `hitbox` and `hitcirc` modules now express the original
collision/no-hit guards and animation state with explicit C++ conditions.
In `hitbox_hittest()`, a negative hitbox center or an active defeat banner
short-circuits to the same early return. The individually owned shotpair
records remain protected by the original **two separate** alive and PID
tests, followed by the original four-way AABB rejection condition.
Only a clear explosion-skip flag enters the original near-call carrier;
original per-player far charged-shot callbacks retain their distinct
paths. Bomb contact now states the two required tests together: the
selected player's bomb must be active **and** the unsigned frame clock
must be on the even phase before incrementing the 8-bit damage counter.

In `hitcircle`, both enemy and player spawn paths now use actual
`HitCircle near *` pointers into the original DGROUP array rather than
references. This keeps the single reserved thirteenth player hit slot,
round-robin twelve enemy slots, exact RNG sampling and near-record
position writes. The ring index wraps under an explicit `>=` bound.
The thirteen-slot age update and twelve-slot enemy renderer use positive
nonzero activity tests. Inactive enemy hit circles do not call the sprite
clip/angle/render routines, while the near pointer advances on *every*
slot. The original 16-frame expiration and original byte postincrements
remain unchanged.

Original TC4 4.02/TLINK staged trials `af1348b` (enemy draw gate),
`af1348c` (ring wrap and thirteen-slot age), `af1348d` (explicit RNG
centering and player draw), `af1348e` and `af1348f` (DGROUP near pointers)
all matched full `hitcirc` CODE. Stages `af1348g`, `af1348h` and
`af1348i` proved the complete Hitbox's combined initial guard, explosion
skip and active-bomb/even-frame gate. Final current-source `af1348j`
recompiled both physical owners: **711 CODE bytes, 63 ordered native
fixup fields and five PUBLICs**, exact in both independent normal links.
Dependent `af1348k` recompiled these with the complete Chiyuri BOSS,
Bullet and both shared BOSS owners: **6,999 CODE bytes, 746 ordered
fields, 44 PUBLICs**; both complete original Japanese MAIN images,
normalized MAPs and ordered MZ relocations matched. No cold replay.

A rejected `af1348a` trial separated the four combined shotpair AABB
rejection conditions into four individual `continue` statements. This
was logically short-circuited but produced **269 instead of 266 CODE
bytes** under original TC4; the combined condition was restored. The
legacy `explosions_hittest` near-call carrier also remains unchanged.
No new hitbox logic, target patching, padding or canonical Factory
packed-file credit is claimed.

Read-only current-source evidence:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1348j af1348k
```

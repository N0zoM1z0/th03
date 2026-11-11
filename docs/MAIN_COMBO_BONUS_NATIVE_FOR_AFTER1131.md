# Combo bonus display: shared native for-loop progression

The complete Combo bonus/HUD dispatcher now uses a natural `for` header to
advance both the player index and the near combo pointer, including the
inactive-combo `continue`. The time decrement, digit rendering, flashing,
score payout and two-player layout preserve their original order.

Original TC4/TLINK `af1131a` matched both `p_combo` and `p_cmbhl` physical
objects: 978 CODE bytes, 57 ordered native fields and the Japanese MAIN
image/relocations across two independent rounds. `af1131b` additionally
moved the signed player index declaration into the `for` header; that changed
original `p_combo` CODE, so its earlier declaration remains.

## 2026-11-11: charged-fireball helper uses an exact early exit

`explosion_collision_chain_slot_fire_charged_fireball()` now returns
immediately when the current chain slot's fireball charge is below the
original round-speed-dependent threshold. The successful path still
zeros the charge *before* spawning, temporarily replaces the near
`efe_p.efe` cursor, issues the original `NOP; PUSH CS; CALL near`
fireball carrier, then restores that cursor. The saved cursor is now a
`near * const` local, making its non-reassignment explicit without
changing TC4's live register/stack lifetime. The original threshold
division and segmented same-group call remain unchanged.

Native `af1360m` established the early-exit form; `af1360n` additionally
confirmed the fixed pointer. Current `af1360o` compiled **both** original
Combo objects in two original TC4 rounds: **978 CODE bytes, 57 ordered
fields, 5 PUBLICs**, with complete normal Japanese MAIN images and
ordered MZ relocations exact. The consumer `af1360p` recompiled both
Combo objects, Fireball, Explosion collision, Ellen BOSS and Extra
Attack, Bullet, both shared BOSS objects, Gauge and shared Extra Attack:
**9,697 CODE bytes, 818 ordered fields and 61 PUBLICs** original-exact.

Owner proof: `.analysis/work/exatt-layout-af1360o/report.json`, SHA-256
`fff1b376f450c982e51daa2fde8ed83b0e9f0f5a4248b39723fcff57faf4eeaf`.
Joint proof: `.analysis/work/exatt-layout-af1360p/report.json`, SHA-256
`dd8c7d0d46cf52b2bde868fa838a5edb731a841c6c40e85be01f51e007c38192`.

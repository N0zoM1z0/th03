# TH03 MAIN nine-BOSS update controllers: positive launched-player scopes

All nine character-specific `gba_boss_update_*()` controllers now express
the active launched-player path as a positive scope rather than an early
return on PID mismatch:

| BOSS | Complete update CODE | Source stage |
| --- | ---: | --- |
| Chiyuri | 2,654 | af1032l |
| Kana | 1,874 | af1033c |
| Kotohime | 1,840 | af1032p |
| Ellen | 1,675 | af1032z |
| Rikako | 1,677 | af1033e |
| Yumemi | 2,358 | af1032x |
| Mima | 1,922 | af1032o |
| Reimu | 2,020 | af1032r |
| Marisa | 1,431 | af1032v |
| **Total** | **17,451** | |

The changes retain each character's specific pre-switch setup and ordering:

- Chiyuri keeps the SELECT center-pair selection, 20-mode switch, render and
  palette countdowns, and collision/hitbox tail inside the active-player
  scope.
- Yumemi keeps the bullet PID assignment before `boss_target_update()`, then
  computes both origin coordinates before dispatch; effect/render countdowns
  and collision remain inside the scope.
- Mima retains its deliberate recomputation of `bullet_template.pid` after
  `boss_target_update()`.
- Ellen retains render-frame postfix increment before BOSS frame increment.
- Kana retains bullet PID setup before target update and render-frame postfix
  increment after the switch.
- Rikako retains bullet PID setup before target update and the signed-byte
  `boss_render_frame += boss_spin_delta` after the switch.
- Reimu retains pre-switch SELECT handling; Marisa, Kotohime and the other
  controllers retain their own INTRO/EXPLODE early returns and dispatch order.

Stage `af1033f` rebuilt all nine complete physical owners simultaneously in
two independent original TC4 4.02 rounds:

- 17,451 CODE bytes
- 2,434 ordered native fields
- 85 PUBLIC offsets
- complete original Japanese MAIN loaded image and ordered MZ relocations

The probe rebuilt only these nine physical BOSS objects and reused unaffected
original objects and CRT.

Protected report: `.analysis/work/exatt-layout-af1033f/report.json`

SHA-256: `8bbb10d812d66fc6c2bfdcc4c0586cc49bb72419f5926fcf0bdea2325e8d4801`

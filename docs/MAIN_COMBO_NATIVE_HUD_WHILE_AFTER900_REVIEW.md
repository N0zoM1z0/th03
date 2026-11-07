# TH03 MAIN after900 — full Combo HUD control and BOSS/Panic helper ABI

The maintained single `src/main/player/combo.cpp` is **two distinct
historical original physical Turbo C++ 4.02 objects**. `p_combo` owns
the signed/unsigned-32-bit-saturated Combo accumulation and the full
two-player HUD bonus/score/label renderer. `p_cmbhl` contains near/far
charged-fireball transfer and full BOSS-launch versus Panic logic. They
remain in their original project linker positions; this was a **real
two-object native compile**, not a synthetic merged translation unit.

The entire substantial `combos_update_and_render()` now uses a natural
C++ `while(pid < PLAYER_COUNT)` with its original near combo pointer
initialized *before* the loop. The expired/inactive Combo path explicitly
increments the signed player ID and the original near pointer **before
continuing**, and the active path increments both **after** all original
TRAM glyph, 32-bit bonus, dynamic score and exact score-add work.
The original bitwise `&` on the flash/expiry Boolean expressions remains
bitwise rather than an invented short-circuiting `&&`. The true 80-frame
Combo display, 32-frame flash expiry, two-digit HUD and 32-bit 65,535
bonus clamp are all unchanged. The second physical helper's original
near fireball-call carrier, 5,120/30,000-point BOSS/Panic thresholds,
byte BOSS level cap and far/near ABI remain authentic.

## Genuine independent original compiler variants

- `af900a`: original complete two-player Combo HUD `for/continue` changed
  to ordinary `while` with explicit original index and pointer advances;
  **both `p_combo` and `p_cmbhl` plus full MAIN** matched in two genuine
  TC4/normal TLINK rounds.
- `af900b`: mathematically reversed original **32-bit** `total > CAP`
  comparison as `CAP < total`, original machine CODE remained exact.
  The final code keeps the clearer original `total > CAP` expression.
- `af900c`: changed the HUD expiry/flash source's **bitwise `&`** to
  logical `&&`; genuine original TC4 produced only **471 p_combo CODE
  bytes** versus its target **491**, first diff CODE segment 1 offset
  169. Original bitwise truth evaluation retained.
- `af900d`: prefix `++gba_boss_level` instead of original byte postfix
  generated **491 p_cmbhl CODE bytes** instead of original **487**.
  Postfix restored, including original cap timing.
- `af900e`: reversed original BOSS-launch threshold comparison from
  `points >= threshold` to `threshold <= points` changed `p_cmbhl`
  CODE at segment 6 offset 10, even though byte count remained 487.
  Original operand order retained.
- Final `af900f`: current complete source with real BOSS/HUD comments
  recompiles **both original physical objects in two independent
  genuine original TC4 4.02/complete normal MAIN TLINK rounds**, exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af900f --units p_combo,p_cmbhl
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af900f
```

| Original physical owner | CODE bytes | Ordered literal OMF FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: |
| `p_combo` | 491 | 17 | 2 |
| `p_cmbhl` | 487 | 40 | 3 |
| **Both real project objects in each native round** | **978** | **57** | **5** |

Both complete original normal TLINK rounds matched the full original
MAIN EXE and normalized MAP, **all 124,642 Japanese loaded program
bytes, all 1,553 original MZ relocation entries**, and independently
checked standard DOS MZ serialization reproduces **all 130,882 pinned
Japanese MAIN.EXE bytes**. The latter does not prove historical vendor
linker header-byte serialization. **97 other unchanged original game
objects and original CRT reused**, no whole-project cold replay,
patched CODE/OBJ, synthetic buffers or fake NOPs.

Protected original compiler/source/OBJ/EXE/MAP native writer proof:
`.analysis/work/exatt-layout-af900f/report.json`, SHA-256
`b27cbc694c46b0cb11e262f4a347499b6743bd17009ceaaa8c983d88c55217db`.
These were previously source-owned original CODE bytes, **not new
distinct game CODE or canonical Factory packed-file accepted credit**.

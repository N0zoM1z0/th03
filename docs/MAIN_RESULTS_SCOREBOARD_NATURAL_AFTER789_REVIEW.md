# TH03 MAIN after789: natural complete round scoreboard, decimal rendering and long bonus math

The complete original `results` physical TC4 source contains the round
object/counter reset, **three-digit Japanese score formatter** and the
large **match-result renderer including all five score categories, story
lives, 32-bit bonus calculation, frame-by-frame score amortization and HUD
rendering**. Its code is maintained across `src/main/round/results.cpp` and
both actual implementation includes `objects_reset.inl` and `results.inl`.
The native overlay enforces both current inline file identities and actual
original TC4 OMF dependency records; no stale Wine source copies or emitted
binary byte patches participate.

## Recovered natural C++ semantics

- The once-every-eight-frame score display, at frame index one, now uses
  **natural unsigned `(round_or_result_frame % RESULTS_DISPLAY_PERIOD)
  == RESULTS_FIRST_FRAME`** in place of an anonymous `& 7` mask. The
  first-frame statistics snapshot and story-clear stage remain separate,
  explicitly named conditions. The original TC4 turns the natural `%8`
  into the **same original 16-bit machine instructions**.
- Named compile-time original score rewards for combo hits, gauge attacks,
  BOSS launches, reversals and panics preserve **1,000 / 10,000 / 15,000 /
  20,000 / 30,000** point multipliers. The per-life story-clear bonus
  intentionally retains its literal **100000L** and the original explicit
  `(long)` casts: neither 16-bit overflow nor source-level 16-bit enum
  promotion is permitted to replace the original 32-bit arithmetic.
- The original **192-frame bonus-payoff divisor**, high/low **10,000-
  point base**, and signed two/three-digit formatter divisors **10/100**
  are now semantic constants used consistently in all matching calculation
  and HUD display expressions. All original truncations, sign checks,
  score-add calls, and the `65535U` incremental cap remain unchanged.
- Two original `!= 0` guards can be natural C++ truth tests
  `if(winner)` / `if(result_bonus_low)` without altering codegen. The
  renderer intentionally continues to call `hud_dynamic_5_digit_points_put`
  for the same original five-line score label and clear-stage display.

All changes were actually compiled and checked on the **complete original
physical result object** incrementally: `af789a` recovered `%8` alone,
`af789b` added clock/bonus/decimal-group names, `af789c` proved natural
Boolean tests, and final **`af789d`** names all reward display multipliers
and integer decimal formatter bases. Each stage passed both independent
original Turbo C++ 4.02 and full normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af789d --units results
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af789d
```

The final complete original object matches **all 1,060 original CODE bytes,
89 literal ordered OMF FIXUPP fields, three PUBLICs**, original segment
geometry, full normal MAIN EXE/MAP, **124,642 Japanese loaded bytes and
1,553 ordered MZ relocations**. The independent standard DOS MZ serializer
recreates all 130,882 bytes of the original Japanese MAIN.EXE. Other 98
original project objects and CRT reused: no full cold replay. Protected
report `.analysis/work/exatt-layout-af789d/report.json`, SHA-256
`7ce8a925084695d2dc051c3d677150e505b1d7f8ea8a5b8477f33a699b99aa4f`.
`results` was a previously covered original source owner, so this is a
significant **native-verified source readability/semantic recovery**, not
additional unique CODE byte credit or canonical packed-game acceptance.

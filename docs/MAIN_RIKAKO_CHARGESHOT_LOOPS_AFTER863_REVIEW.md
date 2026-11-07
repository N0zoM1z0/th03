# TH03 MAIN after863: complete Rikako Chargeshot/Gauge orbit controller

The genuine original physical `cs_rika` owns **eleven original Turbo
C++ 4.02 functions**: four 6-byte orbit projectiles per player,
initializer, two modes, four-part orbit update, enemy hitbox traversal,
sprite renderer and the complete Gauge warning/bullet pattern. The
maintained source now expresses the **four-shot allocation**, **four-shot
polar update** and **four-shot render** traversals as natural C++
`while` loops with original post-call pointer and index updates.

The four-projectile initial signed angle schedule `i<<6 + 0x20`,
original signed 8-bit clockwise/counterclockwise angle increments
±8, 0x80 startup radius, 0x20 subpixel upward movement, exact
12-pixel hit margin, sprite dimensions and active Gauge entrypoint
truth checks are named C++ semantics. The signed **`register int i`**
in orbit-update parity is **explicitly promoted to `unsigned int`
before `%2`**. This is original TC4's exact low-bit instruction form,
not an assumption that signed remainder lowers equivalently.

## Original compiler experiments and actual rejected alternatives

- `af863a`: allocation and rendering loops changed from `for` to
  natural signed `while`; whole physical original CODE exact twice.
- `af863b`: the core **four-projectile orbit polar update** likewise
  uses `while` with original signed index/near-pointer mutations;
  complete original CODE/fixups and normal MAIN still exact.
- `af863c`: two Gauge entrypoint flags use native-exact truth tests;
  original radius, signed movement, four hit margins and sprite size
  named, two real compiler/link rounds passed.
- `af863d`: replacing the original signed `i & 1` with **signed**
  `i % 2` in the live byte-angle update **failed** original CODE:
  **1,287** initialized candidate bytes versus **1,280** target.
  This is independent of the BOSS renderer's earlier signedness trial.
- `af863e`: explicit `static_cast<unsigned int>(i) % 2` with the
  same C++ conditional **passed** full original CODE and normal MAIN
  in both original compiler rounds. This is the actual accepted form.
- `af863f`: original initial angle step/bias and signed +8/-8
  rotation values named; still full original-native exact twice.
- `af863g`: converting original byte `rikako_frame[pid_current]++`
  to prefix increment **failed** native CODE, candidate **1,294**
  vs original **1,280** initialized bytes. Postfix restored.
- Final `af863h`: fresh final current source and explanatory comments
  compiled in two genuine original TC4/complete normal TLINK rounds,
  including the original Gauge/polar/hitbox functions together.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af863h --units cs_rika
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af863h
```

Both original compiler/complete normal MAIN linker rounds reproduce
**all 1,280 initialized CODE bytes, 137 literal ordered native OMF
FIXUPP fields, 11 PUBLIC offsets**, original source/segment ABI,
complete normal MAIN EXE/MAP, **124,642 original Japanese loaded bytes
and all 1,553 ordered MZ relocations**. Independent verified standard
DOS MZ serialization produces the original **130,882-byte Japanese
MAIN.EXE**. The other **98 unchanged original project objects and CRT
were reused**, no full cold replay, patched object bytes, fake CODE
buffer or NOP padding.

Protected source-bound real native compiler/writer proof:
`.analysis/work/exatt-layout-af863h/report.json`, SHA-256
`bacc50a5816dc83115526685e6676cdcf84c056b480f3fe529fc2deda67c7a96`.
This source had historical native coverage. This is new **current native
C++ fidelity**, not 1,280 additional distinct owned original bytes,
historic vendor OMF packet identity or canonical Factory packed-game
acceptance.

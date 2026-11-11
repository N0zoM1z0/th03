# Player gauge: original near-pointer access and saturation gate

The earlier Gauge source obtained the 128-byte player record via an actual
`player_stuff_t near *` rather than a C++ reference and expressed Hyper-active
or already-full rejection with an ordered short-circuit OR. Both conditions
skipped charging before any memory write.
After passing the gate, the unsigned 16-bit charge is still added with
the original compound memory operation and clamped only when it exceeds
`GAUGE_MAX` (0xFF0); changing the addition or the saturation comparison
can alter Turbo C++'s native code.

The actual original compiler matched the entire **55-byte physical
`p_gauge` CODE**, its ordered native fixup and PUBLIC in two rounds at
`af1324c`. Joint `af1324e` also compiled the original shared Extra
Attack helper: **96 CODE bytes, three ordered fields and two PUBLICs**.
The current Gauge consumer test `af1324d` combined the Gauge, Explosion
collision, enemy hit-test update and Kana BOSS objects, reproducing **3,719
CODE bytes, 427 ordered fixup fields and 15 PUBLICs**. Both native rounds
of every scope matched the original normal MAIN loaded image, MAP layout
and ordered MZ relocations; only the selected objects were compiled.

Recheck the live Gauge / shared Extra Attack scope:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1324e
```

## Positive charging gate and fixed DGROUP cursor (2026-11-11)

`gauge_avail_add()` now uses `player_stuff_t near * const p`, explicitly
retaining the original near record cursor without permitting source-level
pointer reassignment. Its positive short-circuit gate accepts charge only
when Hyper is inactive and the unsigned word is below `GAUGE_MAX`.
The compound memory addition and separate strictly-greater saturation
are unchanged; old Turbo C++ is sensitive to combining these operations.

Whole-owner `af1356h` validated the positive gate; `af1356k` separately
validated the fixed near cursor. Current `af1356l` compiles Gauge and
shared Extra Attack together: **96 CODE bytes, 3 ordered native fields,
2 PUBLICs**, both independent original TC4 rounds and normal MAIN links
exact. Joint `af1356m` additionally compiles the original Q8 Polar,
Marisa BOSS and Bullet owners: **4,238 CODE bytes, 398 ordered fields,
32 PUBLICs** and ordered MZ relocations exact.

Current proof: `.analysis/work/exatt-layout-af1356l/report.json`, SHA-256
`35f6d1c756f2b3e6ab0a83e0756fa94d7b216fe9b20658a40208f9042ac17792`.
Joint proof: `.analysis/work/exatt-layout-af1356m/report.json`, SHA-256
`56e85f778f3430043111870e2dcaf3cf902d16efc16f4ce20184aa8a25fd7a63`.

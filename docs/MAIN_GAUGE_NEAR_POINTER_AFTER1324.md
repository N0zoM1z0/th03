# Player gauge: original near-pointer access and saturation gate

`gauge_avail_add()` now obtains the current 128-byte player record as a
`player_stuff_t near *` rather than a C++ reference, and expresses the
original two early rejection conditions with one short-circuit OR. Both
Hyper-active and already-full gauges refuse extra charge, in that order.
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

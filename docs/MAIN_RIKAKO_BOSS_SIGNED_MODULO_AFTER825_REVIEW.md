# TH03 MAIN after825: signed vs unsigned sprite cadence in the full Rikako BOSS

The **complete physical `ba_rikak` original** owns Rikako's BOSS template,
orbital ring spread, entity/pellet releases, alternating volleys, update,
hitbox collision, eight-sprite orbital renderer and 16-sprite arrival renderer.
This is a genuine full-module C++ codegen experiment, not a one-leaf
simulation or a change to target bytes.

## Recovered C++ and a newly reproduced negative control

- The unsigned 16-bit `round_or_result_frame & 1` entrance-flicker gate
  now uses **natural `% RIKAKO_INTRO_BLINK_PERIOD`**; original TC4 4.02
  generates the original mask. Stage `af825a` proved this in the entire
  original 1,677-byte BOSS code.
- `i` is a signed 16-bit `register int` in the eight-sprite orbital
  renderer. Simply changing the two original `i & 3` expressions to
  **signed `i % 4`** is **not** byte exact. An actual original TC4 compile
  of stage `af825b` produced **1,684 initialized CODE bytes** vs the
  original **1,677**; the first divergence is CODE offset 1263. The
  syntactically natural signed remainder is a **rejected** hypothesis,
  even though the actual runtime loop visits indices 0..7.
- Both expressions instead use ordinary C++ **`static_cast<unsigned
  int>(i) % RIKAKO_RING_ANIM_PERIOD`**. This makes the 16-bit unsigned
  intent explicit and generates the **exact** target instructions in
  the *entire* BOSS. Stage `af825c` independently passed both rounds.
- The complete two-phase warning/entity pattern's **256-step signed
  multiplication before division**, four-way renderer cycle, 48-pixel
  orbital radius, and separately paced 2-frame intro blink have
  explicit original semantic constants, without changing RNG draws,
  byte-angle truncation, sprite offsets or update sequence. Stage
  `af825d` verified this combined maintained source twice.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af825d --units ba_rikak
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af825d
```

Both independent actual original Turbo C++ 4.02 and normal TLINK
rounds match **every 1,677 original CODE byte, all 215 literal ordered
OMF FIXUPP fields and eight PUBLIC offsets**, original source/segment
layout and the complete original normal MAIN EXE/MAP. The loaded
Japanese original game equals all 124,642 bytes; all **1,553 literal
ordered MZ relocations** match. The separately validated standard MZ
serialization recreates all 130,882 original Japanese MAIN.EXE bytes.
The 98 other original project objects and Borland CRT were reused,
not cold-replayed. No fake padding or object-byte changes occurred.

Current-source report `.analysis/work/exatt-layout-af825d/report.json`
(SHA-256 `d0539e4b5545c049dead985bcfbbc0a49a8507c65d7fc50f7fd62784f0969bc7`)
and all native compiler/TLINK round receipts are retained under the
original ignored evidence DAG. The BOSS was a previously covered physical
source owner, so this is **not** additional distinct target CODE byte
ownership, raw original vendor OMF metadata identity, or canonical
packed-game Factory acceptance.

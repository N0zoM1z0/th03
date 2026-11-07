# Yumemi target selection, charged-shot ring renderer and eight Gauge volleys (after647)

This native recovery extends the v2 actually-consumed-source compiler
scope to the full original `cs_yume` owner, **outside** the older 28
gameplay/BOSS modules. It is one physical Turbo C++ 4.02 translation
unit containing ten complete original functions: acquiring the closest
active enemy formation, initializing/updating charged shots, the
rectangle hit tests, long multi-ring sprite renderer, and the
triangle-based eight-volley Gauge Attack dispatcher.

The genuine original physical producer wrapper is
`src/main/player/producers/yumemi_chargeshot_native.cpp`. The scoped
driver now replaces its original after596 physical TLINK slot, forces
the **modified current** C++ source path in both independent compile
rounds, and validates the emitted native OMF COMENT source dependency
to prevent historical v1 stale-source false positives.

Source-level recovery and negative controls:

- Charged-shot rendering's alternating frame sprite uses
  `(static_cast<unsigned int>(frame) % 2) != 0`, replacing the
  previous bitwise parity test. Original byte-for-byte code is
  generated (`af647b`).
- The long ring renderer's exact 8/16/24/32/40/48/56/64 sprite
  phases, plus the 24-frame effect sound threshold and 64-frame
  projectile limit, are explicitly named as compiler-time
  constants. Their original code generation remains identical
  (`af647e`).
- The Gauge projectile's original **eight switch cases at
  0/8/16/24/32/40/48/56 frames**, which form two interleaved
  triangles, now have named volley phases. No manual jump-table
  bytes or hand-crafted optimizer constraints are introduced:
  Turbo C++ still generates the whole **original** switch
  jump/value table (`af647f`). The unusual x/y local
  assignments and first/last volley behavior are preserved.
- The target-scanning helper now names the actual per-player
  formation-index sentinels: boss=254, none=255, earliest normal
  formation=0. The original first-formation early break and
  enemy coordinates remain intact (`af647g`).

An attempted `flag_expected += GBAF_PELLET_TO_BULLET` in the
Gauge init path was **rejected**: TC4 generated original-unequal
CODE (`af647c`). The original expression
`flag_expected = flag_expected + GBAF_PELLET_TO_BULLET` was
restored, and `af647d` provided the positive source-bound control.
Matching source semantics alone are never elevated to native equality.

Final two-round original Turbo C++ 4.02/TLINK source-proven proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af647g --units cs_yume
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af647g

Both rebuilt complete objects match **all 1,645 original CODE bytes,
133 literal ordered native FIXUPP fields, ten PUBLIC offsets**, and
all original OMF segment definitions. Both complete normal MAIN EXEs
and path-normalized MAPs equal the retained after596 original
source-native parent. Both original Japanese program images and the
**1,553 literal ordered original MZ relocations** match, and the
independent standard DOS MZ serializer reproduces every byte of
the 130,882-byte original Japanese MAIN.EXE.

Retained proof:
`.analysis/work/exatt-layout-af647g/report.json`
SHA-256 `ee97b7462e5cfc7b3409110e68749ae27261d6aebca5bb077608e290acb01107`.
The actual native compiler/linker logs, per-round source inputs,
raw OBJ/EXE/MAP outputs, and both response files are retained.
Only the affected object was newly compiled in each round; the
other 98 original project objects and startup/CRT libraries were
reused, **not** a full game cold replay.

These already tracked original CODE bytes are improved in natural
source and compiler exactness, but are not newly accepted canonical
packed-game Factory credit. Historical raw vendor OMF packet
identity and real PC-98 runtime behavior remain independent questions.

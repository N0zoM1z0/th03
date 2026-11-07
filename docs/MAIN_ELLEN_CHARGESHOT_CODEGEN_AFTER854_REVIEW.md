# TH03 MAIN after854: complete Ellen Chargeshot/Gauge byte and branch ownership

The entire **ten-function, 1,530-CODE-byte physical `cs_ellen`** was
compiled against the pinned original Turbo C++ 4.02, not a single
small renderer leaf. It contains the real 64 × 12-byte charged projectile
lifecycle, 32-per-player scans, spread activation, homing motion/target
selection, collision, the private sprite renderer and Gauge paired
emissions. The maintained source now names the exact **-110-subpixel
tracking target offset**, **-8-subpixel clip margin**, sprite angle
bias 0x10 and two **distinct** byte cel shifts (5 then 1). Natural
truth predicates in both Gauge entrypoints preserve native codegen.

## Actual original compiler experiments, including rejected C++

- `af854a` collapsed the sprite's `unsigned char cel` initialization,
  `cel >>= 5; cel <<= 1` into one expression. It changed TC4 instructions
  and lost the original intermediate byte truncation near 0xFF:
  candidate **1,528** vs original **1,530** initialized CODE bytes.
- `af854b` attempted natural `for/break` and a final slot-count check
  instead of the charged-shot updater's `goto active` search. The
  complete physical source changed to **1,534** CODE bytes. Original
  first-live-slot flow remains intact.
- `af854c` split `if((--p->state) == 1)` into a separate postfix
  decrement plus test. TC4 produced **1,527** bytes. Retained the
  original one-expression byte predecrement and branch.
- `af854d` replaced two trivial Gauge entrypoint checks with
  `if(gba_flag_active[pid_current])` and passed both genuine native
  compiler/complete normal linker rounds.
- `af854e` named the original signed target/clip geometry and two
  separately evaluated sprite cel shifts; all 1,530 original CODE
  bytes remained identical in two native rounds.
- `af854f` inverted the Chargeshot render loop's inactive `continue`
  into an active-only `if`. It changed the original CODE to **1,526**
  bytes. Its original branch layout remains.
- Final `af854g` restores all these tested native-sensitive forms,
  documents their physical purpose and compiles the **whole current
  maintained source** in two independent original TC4/normal MAIN
  TLINK rounds. No old-stage source snapshot is silently reused.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af854g --units cs_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af854g
```

Both original compiler and complete normal TLINK rounds reproduce **all
1,530 initialized CODE bytes, 169 literal ordered native OMF FIXUPP
fields and ten PUBLIC offsets**, the original source/segment ABI,
complete original normal MAIN EXE and normalized MAP, all **124,642
Japanese loaded program bytes and 1,553 ordered MZ relocations**.
Independent standard MZ serialization matches every byte of the pinned
130,882-byte Japanese MAIN.EXE. The **98 other original game objects
and Borland CRT were reused unchanged**, without a full cold replay,
target substitution, byte padding, code array or patched OBJ.

Protected compiler-source-bound native proof and both genuine writer
rounds: `.analysis/work/exatt-layout-af854g/report.json`, SHA-256
`b182241110a62b9669002235900d30342b536b6fb4574e3fadc0b5087eda4e80`.
This is *current-source recovery for an already historically covered
original physical object*: no incremental distinct CODE byte credit,
packet-identical historical vendor OMF, whole-project historical source
identity or canonical packed-game Factory acceptance is claimed.

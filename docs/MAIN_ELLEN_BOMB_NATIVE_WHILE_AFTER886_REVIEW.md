# TH03 MAIN after886 — complete Ellen Bomb eight-particle lifecycle and native C++ loops

This source is the complete original physical `b_ellen` Turbo C++ 4.02
translation unit, not an isolated sprite leaf. Its three functions own
the 8-particle-per-player reset/creation, full motion/clip/respawn
controller, eight-particle sprite renderer, 64/128-frame palette/quake
Bomb scheduler and four-frame explosion emitter. The 132-byte real DGROUP
Bomb state remains in its original physical carrier; no extra runtime
storage is introduced here.

The original eight-slot creation, **entire position/velocity/respawn
update with a native `goto` and two independent `continue` paths**, and
the sprite renderer's two sentinel-skip branches now use natural C++
`while` loops. Both early-continue paths advance the same original
signed index and near particle pointer in the exact original order.
The preserved goto-respawn path performs a single RNG call before its
velocity and pointer advancement; no RNG draw has been moved or added.

Meaningful source constants now identify the -32-pixel clip margin,
(144,184)-pixel particle origin, 224 subpixel flight speed, 64×64
sprite, original 0x29C sprite offset and two screen clipping margins.
The explosion clock can be written as `if(!(frame % 4))`, while the
*different* byte-valued `frame &3` screen-shake gate and the unsigned
promotion before the byte `%2` palette flash must remain as the
original. The word-valued `ellen_bomb_particle_spawn_count` does admit a
natural prefix increment in this original native source.

## Actually compiled original TC4 alternatives

- `af886a`: original eight-slot initializer and two-continue render
  dispatcher become natural `while` loops, exact whole object twice.
- `af886b`: full original update/respawn `for` with `goto` and two
  continue exits becomes native-exact `while`, both full MAIN rounds.
- `af886c`: removing the explicit `unsigned int` promotion from the
  **byte** palette frame `%2` changed original CODE to **1,032** vs
  the target's **1,023** bytes. Original promotion restored.
- `af886d`: replacing the byte shake-mask `frame &3` with `%4`
  generated **1,026** candidate CODE bytes instead of **1,023**.
  Original bit test restored.
- `af886e`: genuine natural `if(!(byte_frame %4))` explosion cadence,
  distinct from the shake mask, remained whole-source native-exact.
- `af886f`: original clip/particle/sprite/explosion physical geometry
  named, no native CODE or fixup changes.
- `af886g`: word-valued spawn counter `count++` became natural
  `++count`, still identical original bytecode in both rounds.
- Final `af886h`: all current maintained source and semantics recompiled
  in two independent original TC4 4.02 plus complete normal TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af886h --units b_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af886h
```

Both genuine original compiler/full normal linker rounds reproduce
**all 1,023 CODE bytes, 116 literal ordered native OMF FIXUPP fields
and three PUBLIC offsets**, exact original segment/source/DGROUP ABI,
normal MAIN EXE and normalized MAP, **124,642 Japanese loaded bytes
and 1,553 ordered MZ relocations**. Independently verified standard
DOS MZ serialization reproduces all **130,882 original Japanese
MAIN.EXE bytes**, not proof of historical vendor header serializer
identity. **98 other game project objects and CRT reused**, no full
cold replay, synthesized CODE buffer, patched object/target or NOPs.

Protected native source/TC4/OBJ/EXE/MAP evidence:
`.analysis/work/exatt-layout-af886h/report.json` SHA-256
`a6600df458e801271d7d2457a4d7a1efe520941000a154941aeb4cada4cc5a13`.
The owner already had historical source coverage: native maintainability
improvement is **not newly distinct original CODE, raw vendor OMF
packet identity or canonical Factory packed-unit accepted credit**.

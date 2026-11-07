# TH03 MAIN after873 — complete Ellen Extra Attack history and spiral

The complete original **six-function** Turbo C++ 4.02 physical `ex_ellen`
owner implements twelve paired 30-byte history slots, two creation paths,
seven-point spiral history, 4-sprite tail rendering, the full entity
update/collision/arrival state machine and twelve-slot dispatch renderer.
The original 32-byte projectile entities and 30-byte per-slot history
live in separate unchanged DGROUP carriers; no additional DATA/BSS is
allocated here.

The real paired twelve-slot initializer, reverse sparse 6/4/2/0 spiral
renderer, reverse **6..1** history shift, **0..6** landing history fill and
twelve-entity render dispatcher now use ordinary C++ `while` with original
signed index and near-pointer mutation order. These changes preserved all
original CODE bytes in independently compiled actual original TC4 and
normal MAIN TLINK rounds. The two character allocation loops with their
compiler-sensitive `continue` remain original `for`, not generalized.
Original random X/Y range and biases, 0x46 flight speed, 32×32 sprite,
24-pixel negative clip and 16-pixel hit margin are named as actual
original compile-time C++ geometry, preserving all original RNG calls.

## Real original compiler-positive and negative tests

- `af873a`: replaced the two twelve-slot initializer and render dispatch
  loops with natural `while`; complete original physical source and
  full normal MAIN remain exact in both independent native rounds.
- `af873b`: replacing both Extra Attack **allocator** loops with `while`
  and explicit pointer/index stepping before `continue` compiled to
  **1,133 CODE bytes** rather than the original **1,129**. Those source
  loops were restored, including their original `continue` shape.
- `af873c`: the sparse four-sprite spiral `for` became a natural `while`;
  all actual original TC4/MAIN CODE and fixups again exact twice.
- `af873d`: both large history update/landing loops became `while`;
  all 1,129 original CODE bytes and full normal MAIN remain exact.
- `af873e`: named the exact random target, speed, clip, hit radius and
  sprite geometry; both genuine original compiler/link rounds pass.
- `af873f`: independent attempt to replace the mutable byte
  `slot->entity->frame++` with prefix increment generated **1,134**
  initialized CODE bytes instead of 1,129. Original byte postfix restored.
- Final `af873g`: all current source and comments recompiles the complete
  original physical owner in two independent TC4/normal full TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af873g --units ex_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af873g
```

Both genuine original Turbo C++ 4.02 and normal MAIN TLINK rounds match
**all 1,129 original CODE bytes, 79 literal ordered OMF FIXUPP fields and
6 PUBLIC names/offsets**, original source dependency and physical ABI,
complete original normal MAIN EXE/MAP, **124,642 Japanese loaded program
bytes and all 1,553 original MZ relocations**. The separately reviewed
standard MZ serializer recreates the entire **130,882-byte Japanese
MAIN.EXE**; this is not vendor header byte identity. The 98 other original
project objects and Borland CRT are reused, **no all-project cold replay**,
byte buffer substitution, object patch, target padding or receipt repin.

Retained real original two-round compiler/source/OBJ/EXE/MAP evidence:
`.analysis/work/exatt-layout-af873g/report.json`, SHA-256
`16af3dabb8bce7d492fc815151a8e2fa9278d593756f972b78fa5036b91eed38`.
These were **previously source-owned** game bytes; the new C++ fidelity
is not new distinct original CODE credit, vendor raw OMF packet identity
or canonical Factory packed-game acceptance.

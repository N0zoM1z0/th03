# TH03 MAIN after873 — complete Ellen Extra Attack history and spiral

The complete original **six-function** Turbo C++ 4.02 physical `ex_ellen`
owner implements twelve paired 30-byte history slots, two creation paths,
seven-point spiral history, 4-sprite tail rendering, the full entity
update/collision/arrival state machine and twelve-slot dispatch renderer.
The original 32-byte projectile entities and 30-byte per-slot history
live in separate unchanged DGROUP carriers; no additional DATA/BSS is
allocated here.

## Current source refresh: af1094e

The maintained six-function `ex_ellen` source now expresses every loop as a
natural C++ `for`; `src/main/player/exatt_ellen.cpp` contains no `while` loops.
The current source keeps the original compiler-sensitive allocator loops and
`continue` paths, while recovering these five additional `for` forms:

- Paired 12-slot initialization: `++i`, `p0++` and `p1++` live in the loop
  iteration expression, after both entity links are stored.
- Active spiral rendering: the signed history index walks 6, 4, 2, 0 in the
  `for` header; each sprite is drawn before the index/offset advance.
- Active-history shifting: the reverse 6..1 copy is a `for` with prefix
  decrement in its iteration expression.
- Arrival history initialization: all seven 0..6 samples use a natural `for`.
- Twelve-slot rendering dispatch: the index and near slot pointer advance in
  the `for` iteration expression after each conditional render call.

Two further local lifetimes are source-native exact: `exatt_update_ellen()`
initializes `pid_other` at its declaration after the slot pointer, and
`ellen_exatt_render_one()` declares/initializes the spiral `sprite_offset`
inside the active-state branch. The render-dispatch index is also scoped to
its `for` header. The update controller deliberately retains its function-
scope outer index and history index, and its slot pointer remains function-
scope; seemingly narrower variants changed original CODE.

The current-source report is `.analysis/work/exatt-layout-af1094e/report.json`,
SHA-256 `f7042dd9db9bfef65d83588b33259c9cebdf30f0319a158bb9c15cd492398164`.
Maintained source SHA-256: `3fc814ac81ead438185051c26f2838c0e8a39462b2c7ca1ebc550caf52473dad`.
Two independent original TC4 rounds match all 1,129 CODE bytes, 79 ordered
native fields and six PUBLIC offsets; both normal Japanese MAIN images and
ordered MZ relocations match. The source overlay reports one complete original
unit and full Japanese MAIN equality. Raw OMF packet identity and Factory
Oracle acceptance are separate claims and are not asserted here.

At historical stage `af873g`, the paired twelve-slot initializer, reverse
sparse 6/4/2/0 spiral renderer, reverse **6..1** history shift, **0..6**
landing history fill and twelve-entity render dispatcher used ordinary C++
`while` with original signed index and near-pointer mutation order. That
while-based variant was native exact; the current `af1094e` refresh above
re-expresses those same operations as `for`. The two character allocation
loops with their compiler-sensitive `continue` remain natural `for`, not
generalized.
Original random X/Y range and biases, 0x46 flight speed, 32×32 sprite,
24-pixel negative clip and 16-pixel hit margin are named as actual
original compile-time C++ geometry, preserving all original RNG calls.

## Historical af873 compiler-positive and negative tests

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

## Additional af1093/af1094 lifetime experiments

- `af1093a` was an initial probe-script attempt that exposed a missing support
  dependency: the isolated producer script copied `exatt_ellen.cpp` but omitted
  its direct `src/main/player/exatt_entity.hpp` include. The support list now
  includes that header; baseline `af1093b` then passed the 1,129-byte,
  six-function producer-shape probe.
- `af1093c`/`af1093d` verified the paired-slot `for` form in two full native
  rounds. `af1093e`/`af1093f` added the signed 6/4/2/0 spiral `for`.
- `af1093g` checked the reverse history-shift `for`; `af1093i` added the
  seven-sample arrival-history `for`, and `af1093j` proved both together in
  the complete owner. `af1093k`/`af1093l` added and fully proved the
  twelve-slot render-dispatch `for`.
- `af1093o`/`af1093v` established that initializing `pid_other` at its
  declaration is exact. Moving the update outer index into the `for` header
  (`af1093q`, `af1093t`) or declaring it at first use (`af1093w`, `af1093z`)
  changed original CODE in full-owner checks (`af1093t`, `af1094a`).
- `af1093m` showed that scoping both history indices separately in their
  `for` headers changes the update CODE. `af1094f` showed the same for moving
  the update slot pointer into the loop header.
- `af1093r` checked the active-branch sprite-offset declaration; `af1093u`
  fully proved it, and `af1093v` then added the update PID initializer while
  preserving the original update-index lifetime. `af1094d`/`af1094e`
  established and fully proved the render-dispatch index in the `for` header.
- `af1094b`/`af1094c` tried initializing all random allocator locals directly
  at declaration; the full physical CODE differed, so the original declaration
  and RNG assignment sequence was restored.

The current producer-shape helper was corrected to include the actual
`exatt_entity.hpp` compiler dependency. Its producer-shape receipt is useful
for quick iteration, but full-owner acceptance still requires the separate
two-round original MAIN object/link/source-overlay proof above.

Retained real original two-round compiler/source/OBJ/EXE/MAP evidence:
`.analysis/work/exatt-layout-af873g/report.json`, SHA-256
`16af3dabb8bce7d492fc815151a8e2fa9278d593756f972b78fa5036b91eed38`.
These were **previously source-owned** game bytes; the new C++ fidelity
is not new distinct original CODE credit, vendor raw OMF packet identity
or canonical Factory packed-game acceptance.

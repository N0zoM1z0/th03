# TH03 MAIN after899 — entire original Bullet engine, native render, trail and update loops

The entire original **20-PUBLIC `bullet` Turbo C++ 4.02 physical source**
is recompiled, including its 386 low-level fastcall GRCG pellet blitter,
full group velocity dispatcher, complex bullet transfer/create, all
accelerated/player/terrain/collmap update modes, multicolored sprite and
mono cloud passes, and the register-sensitive 8×8 pellet writer.
The original physical bullet **BSS of 9,500 bytes** remains in the
original object and is compared. This work did not replace it with a
new data carrier or a standalone mock renderer.

## Actually recovered natural C++ control

- The original `bullets_reset()` full bullet-flag loop is now an ordinary
  signed-index `while`, preserving every original flag store and the
  subsequent physical trail-ring reset.
- The **per-projectile trail history initializer** uses natural `while`,
  retaining separate original X/Y assignments for every real sample.
- The **full-color 16×16 sprite pass** and its separate **mono 32×32
  cloud pass** use natural signed-index and near-pointer `while`,
  retaining original pass order and GRCG/sprite palette state.
- The original reverse **sprite trail per-sample traversal** also
  naturally uses `while`, updating both trail index and sprite cel
  *after* each original `sprite16_put_noclip` call.
- The large register-sensitive `bullets_update()` machine-code loop
  now uses natural `while(true)` without changing the original `_AX`,
  FLAGS, near-call, clipping, transfer or collision behavior. This is
  not a replacement for its historical inline x86 register carriers.

## Genuine independent Turbo C++ 4.02 experiments

- `af899a`: changed full bullet reset and trail-point initialization
  loops to `while`; both genuine original TC4/full normal MAIN TLINK
  rounds matched all original machine-code bytes, FIXUPPs and PUBLICs.
- `af899b`: converted **both complete full-color and mono-cloud sprite
  passes** to native `while`, preserving the original near-pointer and
  signed index updates; entire original 2,685 CODE bytes still exact.
- `af899c`: independently challenged the **first-free-slot allocator**
  inside substantial `bullets_add()` with natural while and explicit
  post-skip index/pointer increments. Real original TC4 generated
  **different CODE at segment 1 offset 964**, despite the same 2,685
  initialized byte count. Rejected; original for/continue/break stays.
- `af899d`: changed full bullet state update's `while(1)` to natural
  `while(true)`; both original compiler/linker rounds exact.
- `af899e`: converted the full original per-sprite trail-render
  `for` to natural `while` with two authentic post-call mutations;
  complete original CODE again exact twice.
- `af899f`: changed the actual low-level **8×8 pellet writer** from
  historical bottom-tested `do/while` to top-tested `while`. Original
  TC4 generated **2,687** initialized CODE bytes rather than 2,685,
  first difference segment 1 offset 2541. The original bottom test
  and hardware write order were restored.
- Final `af899g`: complete current C++ source plus true original
  DATA/BSS/OMF and genuine register-effect comments recompiled in
  **two independent original TC4/full normal MAIN TLINK rounds**.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af899g --units bullet
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af899g
```

Both independent genuine original compiler/full normal linker rounds
match **all 2,685 original CODE bytes, 196 literal ordered OMF FIXUPP
fields, 20 PUBLIC offsets and original 9,500-byte BSS extent**,
original segment/source/16-bit ABI, complete original normal MAIN EXE
and normalized MAP, **124,642 Japanese loaded program bytes and all
1,553 ordered MZ relocations**. Independent standard MZ serialization
reproduces all 130,882 original Japanese MAIN.EXE bytes; it does not
establish historical vendor header-byte serialization. **98 other
original game objects and CRT reused**, no full cold replay, patched
original target/OBJ, synthetic CODE or NOP padding.

Protected actual native compiler/source/OBJ/EXE/MAP writer evidence:
`.analysis/work/exatt-layout-af899g/report.json`, SHA-256
`8b2e133173ec4ce29e1671cccd35d075a60a5ca81bfd5e9a7249cdabd113dd84`.
Historical source ownership of these original CODE bytes already existed.
These natural C++ improvements are **not 2,685 newly distinct game bytes,
raw vendor OMF packet identity or canonical Factory packed acceptance**.

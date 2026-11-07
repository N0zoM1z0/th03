# TH03 MAIN after891 — full fireball transfer, collision and render control

This rebuilds the **entire physical `e_fireb` original Turbo C++ 4.02
project object**, including all ten functions and its original one-byte
DATA and one-byte BSS state. The real original source owns 24 independent
fireballs and their transfer/fall physics, explosion hit/scoring,
red/blue chain generation and full sprite renderer. The global variant
and previous generation bytes must retain their original ownership and
side effects; no substitute DATA/BSS is invented.

## Recovered natural C++ for substantial full functions

The full **24-fireball movement/transfer/fall update**, the **reverse
24-slot chain/collision scan**, and the complete sprite render dispatcher
now use natural C++ `while` instead of `for`. These are not isolated
helper stubs. The movement loop has three materially different early
`continue` exits: inactive projectile, clipped/free projectile (including
a `goto free_and_continue`), and the transfer-to-fall transition (including
`goto switch_to_fall`). Each explicitly advances the original signed
index and near pointer *after* the original state/velocity mutations.
Both real historical labels remain, retaining their original compound
16-bit velocity, position checks, collision and audio side effects.

The backward collision scan retains separate skip branches for non-falling
fireballs and no-hit decisions, both with their original decreasing
signed index and near pointer. The **uninitialized `chain_slot`** passed
through the collision/Extra Attack system is original historical behavior
and is not zero-initialized, bounded or reinterpreted as a safe value.
The 24-sprite render pass retains its original free-entity skip and
forward index/pointer updates.

## Original TC4 codegen trials

- `af891a`: full 24-slot reverse hit/collision and render loops naturally
  rewritten as `while`; two real original TC4/full normal TLINK rounds
  matched the entire `e_fireb` CODE and state carrier.
- `af891b`: the substantial whole `fireballs_update()` with both goto
  destinations and early-continue paths also became natural `while`;
  the full 1,555 original CODE bytes remained exact twice.
- `af891c`: attempting the same natural rewrite on the **first-free-slot
  fireballs_add()** allocator changed original CODE (first difference
  segment 1, offset 36). Original `for/continue/return` shape restored.
- `af891d`: attempting to replace the update's mutable byte `p->frame++`
  with `++p->frame` changed original CODE (first mismatch segment 1,
  offset 709). The original byte postfix remains.
- Final `af891e`: all current maintained original C++ and comments,
  authentic existing DATA/BSS, and both independent original TC4 4.02
  compiler/complete normal MAIN TLINK rounds remain exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af891e --units e_fireb
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af891e
```

Both independent original compiler/complete normal MAIN linker rounds
match all **1,555 original CODE bytes, 115 literal ordered native OMF
FIXUPP fields, 10 PUBLIC offsets, and the original one-byte DATA and BSS
carriers**, original source/segment ABI, complete original normal MAIN
EXE/MAP, **124,642 Japanese loaded program bytes and all 1,553 original
MZ relocations**. Independently checked standard DOS MZ serialization
reproduces all **130,882 bytes of the original Japanese MAIN.EXE**; raw
historical vendor MZ-header identity is not established. The other
**98 unchanged original game objects and Borland CRT were reused**,
not cold rebuilt, patched or padded.

Protected actual original source/compiler/TLINK/OBJ/EXE/MAP proof:
`.analysis/work/exatt-layout-af891e/report.json`, SHA-256
`1b2a13408eafbdf0002bc58724ae4821f0cfbbbe4ff76d44c79190a4d6fd8717`.
This historical source-owned object gains native C++ fidelity,
**not additional unique original CODE or canonical packed Factory credit**.

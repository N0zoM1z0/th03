# Marisa BOSS and Fireball: exact native attack and removal control

Marisa's BOSS renderer now uses a positive attack-mode branch after its
separate hit-sprite return. The two alternating sprite/VRAM strips retain
the original four-frame flicker and display order. The narrow-column
attack returns to pattern selection only on its final emission frame;
the wide-column's fourth emission and intro split radius use named
frame/value expressions. High-level rings still emit a dense ring before
the cloud ring; lower levels emit only the cloud. The two speed layers
of the four-frame spread and their byte-angle advance remain unchanged.

In the 24-slot Fireball update, falling fireballs now test the bomb-active
flag, left bound and right bound separately. All three paths reach the
same original `free_and_continue` label, preserving fall-frame updates,
Y clipping and distinct cross-field transfer behavior. The update and
render loops explicitly compare flags to `EFF_FREE`; transfer toward
player zero is explicitly tested with `pid == 0`. The uninitialized
`chain_slot` in the collision routine is intentionally untouched.

Original TC4/TLINK source-bound stages `af1325h` (whole 1,431-byte
Marisa BOSS, 199 native fields and 9 PUBLICs) and `af1325i` (whole
1,555-byte Fireball, 115 native fields and 10 PUBLICs) match two
independent compiler rounds apiece. The combined `af1325g` source
recompiled both complete owners, yielding **2,986 CODE bytes, 314
ordered native fields and 19 PUBLICs**, with two complete normal
Japanese MAIN links, full MAP and ordered MZ relocations equal.
Only these original physical owners were recompiled.

The native negative trial `af1325a` reversed the low/high ring level
comparison and block order. TC4 changed a `JAE` to `JB` and the original
branch destinations despite equal CODE length and field counts. The
original low-level-first decision was restored. The more natural
positive rendering branch was independently accepted (`af1325d`).

Recheck the current source-bound owners without cold replay:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1325h af1325i
```

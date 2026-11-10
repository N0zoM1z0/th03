# Bullet engine: native spawn, movement and collision gates

The complete 2,685-byte original `bullet` physical translation unit now
expresses multiple independent control requirements directly in the
maintained `src/main/bullet/bullet.cpp`, without changing the original
processor instructions, callbacks or hardware behavior.

`bullets_add()` rejects each out-of-bounds spawn in its original order:
top, bottom, left and right, using the original inclusive subpixel
boundaries. These are four explicit early exits rather than a compound
OR expression. The slot iterator, group dispatch, speed limiter, trail
ring allocation and RNG consumption remain unchanged.

`bullets_update()` now separately skips free and invalid bullet flags;
no age update, trail move, transfer or collision is performed for either
class. In the normal X movement path, either original left/right border
now independently sends the bullet to `remove_x`, without affecting the
special clamped trail path or transfer movement. Finally, collision-map
updates require a non-transfer bullet **and** its `is_collidable` flag.
Those two guards are nested, preserving their original short-circuit
order and original near `collmap_set_vline` call carrier. The unchecked
register and FLAGS handling elsewhere in the bullet engine is untouched.

The real original TC4/TLINK source trials passed incrementally at `af1318a`
(slot flags), `af1318b` (X clipping), `af1318c` (collision eligibility) and
`af1318d` (four spawn boundaries). Final current-source stage `af1318f`
compiled the entire owner in two independent original rounds, matching
**2,685 CODE bytes, 196 literal ordered native fixup fields, 20 PUBLICs**,
complete segments and MAP, the full Japanese MAIN program and all ordered
MZ relocations. The separate joint `af1318g` trial recompiled both `bullet`
and its updated Mima BOSS consumer: **4,607 CODE bytes, 473 ordered native
fields and 29 PUBLICs** were exact in both normal MAIN links. No full cold
replay or target-byte patches were involved.

A negative `af1318e` trial flattened the special trail clamp into left
and right early-out tests. This left the owner length and fixup count
unchanged but reversed the sense/order of the second Jcc at CODE offset
approximately `0x72D`, changing three raw bytes. The original positive
nested clamp comparisons were restored. A superficially equivalent
control-flow rewrite therefore cannot replace the native branch layout.

Read-only revalidation of the current bullet owner:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1318f
```

This establishes current source-bound physical-object and normal-link
exactness, not newly gained whole-product or Factory packed-file acceptance.

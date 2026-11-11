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

## 2026-11-11: current-source short-circuit spawn and frame update

The original four `bullets_add()` bounds checks now form one ordered
short-circuit OR: Y minimum, Y maximum, X minimum, X maximum. No out-of-
bounds template can reach the allocator. The large register-sensitive
`bullets_update()` loop similarly combines the free-slot and invalid-tag
skips into one ordered OR and combines the non-transfer/collidable gates
around the near collision-map call into one ordered AND. These predicates
preserve the original invalid-tag semantics, register/FLAGS carriers,
physical update phases, random draws, clipping and transfer behavior.

Trials `af1351h` (collision-map gate), `af1351i` (active slot filter), and
`af1351j` (spawn bounds) each rebuilt the entire **2,685-byte `bullet`
object** in two original TC4 rounds. Current source-bound `af1351j`
reproduces **196 ordered native fields, 20 PUBLICs**, the complete normal
Japanese MAIN image and ordered MZ relocations. A negative test `af1351k`
replaced the acceleration-type branch with a ternary assignment. Original
TC4 emitted 2,683 rather than 2,685 CODE bytes, so that change was rejected.

The four-object integration stage `af1351l` rebuilt the complete bullet,
Mima and both shared BOSS owners: **5,556 CODE bytes, 579 ordered native
fields, 37 PUBLICs** and both normal MAIN links match. No full cold replay
or generated padding was used.

Current proof: `.analysis/work/exatt-layout-af1351j/report.json`, SHA-256
`60ad59b02966f070f5f8bc408f1543e0df2a3c4fcd9d5c75b8a6e73af0882b67`.
Joint proof: `.analysis/work/exatt-layout-af1351l/report.json`, SHA-256
`0ede9a1f9e0910ed75419b60277f9b3bb3cc2ea3b43499dada9e29e2f8718970`.

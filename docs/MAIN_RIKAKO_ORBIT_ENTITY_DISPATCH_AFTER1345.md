# Rikako BOSS: mutually exclusive orbit and entity release phases

The full `ba_rikak` native owner now spells its orbit warning, radial
fire and terminal selection as one **mutually exclusive `if/else if`**
chain, without early returns between those branches. The signed-byte
spin acceleration still advances on its original eight-frame cadence
*before* the phase dispatch. The 0x28 ring uses the same single RNG word
for signed rotation choice, original 256-unit signed angular divisions,
`polar()` centers, bullet spawn ordering and closing sound effect.

The entity family likewise branches exclusively between the 0x10
warning, 0x28 Extra Attack ring, 0x40 four-volley pellet ring and the
post-0x50 terminal state. Its apparently overwritten random angle draw
at 0x28 is **still consumed**, before the signed entity-angle iteration;
all four pellet RNG draws and speed increments remain after their
respective setup, as in the physical original. The alternating burst's
mode reset now occurs under a positive post-0x80 frame condition, after
the original 1/5/9/13 shot phase. No new safety check or gameplay fix
was added.

Original TC4/TLINK `af1345a` first proved all three positive terminal
gates; `af1345b` proved the orbit mutually-exclusive branches; and
`af1345c` proved the entity phases. After final source comments and
formatting, `af1345e` reconstructed the complete physical **1,677
CODE bytes, 215 ordered native fields and eight PUBLICs**, with two
independent normal Japanese MAIN links and ordered MZ relocations exact.
Joint `af1345f` compiled Rikako, Bullet, both shared BOSS objects and
Rikako Extra Attack: **6,013 CODE bytes, 563 ordered fields and 41
PUBLICs**, also with both complete original normal links equal.

Negative `af1345d` inverted Rikako's final far renderer to an
explosion-first if/else. It retained total CODE length and field counts
but changed the terminal `JE` to `JNE` and swapped its two original
near-call destinations. That tempting source rewrite was reverted,
leaving the original exact renderer/ABI intact.

This is improved source structure for an existing original physical
owner, not 1,677 newly recovered game bytes and not canonical Factory
packed-file or full cold-build acceptance.

Read-only current-source verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1345e af1345f
```

## Pre-tested attack and renderer loops (2026-11-11)

The maintained Rikako BOSS now spells five originally equivalent loop
bodies as pre-tested `while` statements: orbit-spread bullets, entity
Extra Attack spawns, four independently randomized pellet volleys,
the orbiting sprites in the main renderer, and the sixteen-sprite
intro. Each retains its original register-qualified signed index,
which advances only **after** the `bullets_add()`, `rikako_extra_add()`
or `sprite16_put()` call. Both render loops then advance the mutable
byte angle, retaining original wraparound. The orbit/entity ring angle
still multiplies the signed index by 256 *before* integer division.
The otherwise overwritten RNG draw before entity spawning and the
main renderer's unsigned `%4` promotion are unchanged.

Stages `af1361a` through `af1361e` tested the five source edits
independently. Final current-source `af1361f` rebuilds the complete
**1,677 CODE bytes, 215 ordered native fields, 8 PUBLICs** with two
independent original TC4 rounds and normal Japanese MAIN links.
Consumer stage `af1361g` recompiles Rikako, Bullet, both shared BOSS
objects, Rikako Extra Attack, Polar and SE service: **6,159 CODE
bytes, 581 fields, 44 PUBLICs**, full normal MAIN image and ordered
MZ relocations original-exact. Only these physical objects were
recompiled; previously source-owned bytes are not counted again.

Current proof: `.analysis/work/exatt-layout-af1361f/report.json`, SHA-256
`0f4a7e12f7e7f735cdd4fb94c96891cd5b269d2a43ffc8191673193f9a7d901c`.
Joint proof: `.analysis/work/exatt-layout-af1361g/report.json`, SHA-256
`81708170e883acc21bbd5b7d5da02f25316c10e734ec19064ee5647dc955cadd`.

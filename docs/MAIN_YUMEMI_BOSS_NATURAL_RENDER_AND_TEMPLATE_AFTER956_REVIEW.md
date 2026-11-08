# TH03 MAIN Yumemi BOSS: named render protocol, raster geometry and template C++

The complete original ten-function `ba_yumem` physical BOSS remains one
maintained natural C++ source. This current-source pass extends the existing
large attack/rain reconstruction through its renderer and template leaf:

- The shared BOSS template's center, velocity, HP, sprite offset and
  player-two sprite adjustment are now named compile-time values.
- The render-mode protocol distinguishes none, primary effect and alternate
  effect. Every original transition in the ring, aimed, chase and intro
  paths now uses the named state values; the mode-2 sprite selection uses
  the same name.
- The full boss sprite size, placement margins, effect/hit sprite sizes and
  offsets, player-specific clip rectangles, effect color and effect-origin
  scale/bias are named at the large `yumemi_render_main()` owner.
- Intro sound, ring/explosion and aimed-shot effects have named IDs. The
  twelve-pellet rain's initial angle and spread speed, chase render-frame
  selector, aimed initial render frame and per-frame effect-radius decay are
  named separately from the similarly valued attack-clock constants.
- The two state predicates in the renderer now use explicit comparisons
  (`render_mode != NONE`, `render_frame == 0`), and the large update uses
  explicit nonzero tests before the effect-radius and render-frame updates.

The complete BOSS retains all four large pattern controllers, the 12-pellet
RNG/call loop, four native modulo clocks, collision scheduler, full effect
renderer and four-phase arrival raster renderer. The arrival's two signed
scale stages, four separate typed `while` traversals, GRCG/EGC ordering,
original byte postfix decrement and all RNG ordering remain unchanged.

## Re-tested natural C++ versus hardware-specific assembly

A new attempt replaced the arrival leaf's `asm { xor dx, dx }` with natural
`_DX = 0`. It was not equivalent: the candidate's one original CODE byte
was **33 D2**, while the Japanese source requires **31 D2** at original CODE
segment offset 1,886. The maintained source keeps the one-instruction
hardware register expression explicit. The earlier `_DX ^= _DX` attempt
also remains a documented negative control. This is why the original
operand-specific assembly is not replaced merely to remove inline assembly.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af956a --units ba_yumem
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af956a
```

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
**entire 2,358-byte original Yumemi BOSS** and linked each object through
the complete normal MAIN response. Both reproduce all **343 literal
ordered OMF FIXUPP fields and ten PUBLIC offsets**, the full original
Japanese MAIN loaded image (**124,642 bytes**) and all **1,553 ordered MZ
relocations**. The other **98 original game objects and original Borland
CRT** were reused; no full cold replay, target patch, original OBJ patch,
synthetic byte buffer or NOP padding.

Protected source-current report:
`.analysis/work/exatt-layout-af956a/report.json`, SHA-256
`418f24c6cf9c7aa8b2bb5480ef4b7fb808642da2b46ff37e052157c614b35c7a`.
The physical BOSS was historically source-covered; this improves current
natural C++ semantics and source provenance, not distinct original CODE
ownership, raw vendor OMF packet identity or canonical Factory acceptance.

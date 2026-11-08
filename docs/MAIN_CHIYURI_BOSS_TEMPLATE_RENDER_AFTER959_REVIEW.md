# TH03 MAIN Chiyuri BOSS: template, render-state and sprite-placement semantics

The complete original 11-function `ba_chiyu` BOSS remains a single natural
C++ physical source. This current-source pass extends the existing cardinal,
ring, trail and four fan-pattern reconstruction through the template leaf,
attack completion states and main renderer:

- `boss_chiyuri_template_init()` now names the original center, velocity,
  HP, sprite offset and player-two sprite adjustment.
- The attack controllers and intro now return to the named
  `CHIYURI_MODE_SELECT` state; the pattern limit uses the named descend mode.
  The post-attack palette/render state is named at all original completion
  points.
- `chiyuri_render_main()` now names the main-sprite half-width/top offset,
  hit-sprite placement and the animation period. Its normal-render state is
  explicit and named, as is the complementary non-normal render-state test.

The complete 2,654-byte BOSS still includes the large cardinal/fan/ring
controllers, four signed fan loops, 16-sprite polar ring, mono GRCG renderer,
full intro and collision scheduler. The original byte render mask, byte
postfix operations, AL-carried palette/intro updates, signed 16-bit polar
arithmetic and draw-before-angle-increment order are preserved.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af959b --units ba_chiyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af959b
```

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
**entire 2,654-byte original Chiyuri BOSS** and linked each object through
the complete normal MAIN response. Both reproduce all **381 literal
ordered OMF FIXUPP fields and eleven PUBLIC offsets**, the complete original
Japanese MAIN loaded image (**124,642 bytes**) and all **1,553 ordered MZ
relocations**. The other **98 original game objects and original Borland
CRT** were reused; no full cold replay, target patch, original OBJ patch,
synthetic byte buffer or NOP padding.

Protected source-current report:
`.analysis/work/exatt-layout-af959b/report.json`, SHA-256
`2a3f864b74ed5c01b6b0217833ce46ecb04ea8930cd8af301503658329baba69`.
The BOSS had historical source coverage already; this advances current
natural C++ semantics and native-source provenance, not distinct original
CODE ownership, raw vendor OMF packet identity or canonical Factory
packed-file acceptance.

# TH03 MAIN Chiyuri BOSS: natural lifecycle and render predicates

The complete eleven-function Chiyuri BOSS now expresses four byte-state
checks and its initial scheduler state with the existing named C++ values:

- The template starts in CHIYURI_MODE_INTRO instead of a raw zero.
- The hit byte is tested explicitly as nonzero.
- The animation-frame byte uses an explicit zero comparison.
- Both movement-phase byte gates use explicit nonzero comparisons.

These changes cover the complete BOSS lifecycle, not isolated leaf builds:
the intro/template, four attack families, update/collision scheduler,
sixteen-sprite ring renderer, main/hit renderer, monochrome GRCG transitions
and the multi-phase intro renderer are all recompiled together.

The source retains the original postfix byte decrement, byte &= 3 renderer
mask, signed 16-bit polar coordinate conversion, separate GRCG palette
phases, and the original render-state countdown. Those operations have
specific TC4 codegen history and were not rewritten speculatively.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af972a --units ba_chiyu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af972a

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire eleven-function, 2,654-byte original Chiyuri BOSS. Both preserve
all 381 literal ordered OMF FIXUPP fields and eleven PUBLIC offsets;
both complete normal MAIN links reproduce the 124,642-byte Japanese
loaded image and all 1,553 ordered MZ relocations. The other 98 original
game objects and Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af972a/report.json, SHA-256
50c59b33f2dcbe40a5a3b9422fbd87f3980f29596c29549135249e54580594ce.

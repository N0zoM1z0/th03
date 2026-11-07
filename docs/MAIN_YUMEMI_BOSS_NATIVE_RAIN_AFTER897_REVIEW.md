# TH03 MAIN after897 — Yumemi major BOSS natural C++ rain and phase control

The **entire 10-function original `ba_yumem` Turbo C++ 4.02 physical
source** is rebuilt in all native trials. This is the complete BOSS:
expanding ring, RNG aimed volley, four-cross ring, two-stage chasing
Extra Attack, twelve-pellet rain, full mode/collision scheduler, sprite/
GRCG renderer and four 8-pixel-step arrival raster phases. Shared BOSS
helper and historical DGROUP state ownership remain in their original
separate physical slots.

## What is actually recovered

The rain pattern's **twelve separately randomized pellets** now use
natural signed-index `while`, with *two original RNG draws and one
`bullets_add()` per pellet* preserved in order. Four independent unsigned
16-bit attack clocks — ring, aimed, cross and rain — now use natural
`if(!(boss_frame % period))`. The full GRCG circle/line renderer's
absence-of-effects predicate uses explicit
`if(!boss_effect_radius && !boss_render_frame)`, byte-identical to the
original code. The two ring-angle delta choices ±3, original 0x100
intro/warning radius, byte speed step +8, 56-pixel collision tiles,
32-pixel hit margin and random rain angle/velocity are now source-named
original constants. Nothing changes original RNG, target coordinates,
collision side effects or signed/unsigned 16-bit arithmetic.

## Actual TC4 compiler trial sequence

- `af897a`: twelve-rain-pellet `for` -> ordinary typed `while`, entire
  2,358-byte BOSS original-exact in both native compiler/link rounds.
- `af897b`: four distinct unsigned-word frame `%period==0` conditions
  -> natural `if(!remainder)`; entire original BOSS and normal MAIN exact.
- `af897c`: changing the byte `yumemi_angle += signed_delta` to
  `yumemi_angle = yumemi_angle + signed_delta` changed the real original
  CODE to **2,362** vs target **2,358** bytes, first difference original
  CODE segment 4 offset 181. Original compound byte update restored.
- `af897d`: native-exact named initial radius, signed two-way angle
  increment and byte speed step; entire scope unchanged.
- `af897e`: natural explicit conjunction for the large GRCG effect
  renderer accepted, full original CODE exact in two actual rounds.
- `af897f`: original collision and twelve-pellet random-angle geometry
  named; full CODE/fixups/MAIN unchanged.
- `af897g`: attempted to combine arrival-coordinate `<<3` then `<<4`
  into one `<<(3+4)`. Actual TC4 generated **2,355** instead of
  **2,358** CODE bytes, first difference segment 4 offset 1921; restored
  both original signed 16-bit scaling stages.
- `af897h`: replacing the original byte `boss_render_frame--` with
  prefix `--boss_render_frame` emitted **2,362** initialized CODE bytes;
  postfix retained.
- Final `af897i`: all current C++ and explanatory comments recompiled
  in *two independent genuine original TC4 4.02 + full normal MAIN
  TLINK rounds*, byte-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af897i --units ba_yumem
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af897i
```

Both genuine original compiler/full normal linker rounds reproduce
**all 2,358 CODE bytes, 343 literal ordered native OMF FIXUPP fields
and 10 PUBLIC offsets**, original source/segment ABI and dependencies,
complete normal MAIN EXE/MAP, all **124,642 Japanese loaded bytes and
1,553 ordered MZ relocations**. Independently checked standard DOS MZ
serialization reproduces all 130,882 original Japanese MAIN.EXE bytes,
not independently proving historical vendor TLINK header serialization.
**98 other original project objects and CRT reused**, no full cold replay,
source substitution, altered original OBJ or target, synthetic bytecode
array or NOP padding.

Protected original compiler/OBJ/EXE/MAP/source-bound native receipt:
`.analysis/work/exatt-layout-af897i/report.json`, SHA-256
`2285e65fb6ab652755668787bca91390caac393b86744f5a250e60b78cc6fb72`.
These original bytes already had historical source coverage; this
improves current maintained native C++ fidelity, **not distinct original
CODE ownership or canonical Factory packed-file accepted credit**.

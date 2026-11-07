# TH03 MAIN: complete Explosion collision/chain arbitration C++ after747

The original `e_expl` physical Turbo C++ owner consists of one **substantial
630-byte `explosions_hittest()` routine**, not a small wrapper. It scans the
entire EFE pool, clips hitboxes against a growing explosion rectangle,
updates the original per-player chain, bonus, gauge, fireball and Extra
Attack charges, and starts charged projectiles. Its original physical
OMF contains **49 literal ordered native FIXUPP fields**, one PUBLIC,
correct `E_EXPL_TEXT` CODE, and zero initialized DATA/BSS. No original
slot, signed arithmetic, random draw or collision transition was altered.

The source now names the original **four-frame explosion hit cadence**,
three separate chain-charge thresholds **4 / 10 / 20** and the bonus
speed divisions at **48 / 96**. It tests the four-frame hit mask using
natural `if(expl_p->frame & (EXPLOSION_HIT_PERIOD - 1))`, and advances the
signed EFE-loop local via `++i` and the unsigned 16-bit collision-count
local via `++collision_count`. The explosion-pointer `expl_p++`, the
mutable memory `expl_p->flag++`, `hits++` and original independent signed
bonus arithmetic/charge slots remain unchanged. The peculiar repeated
`against2` byte encoding and saturation behavior are preserved.

## Actually executed native TC4 experiments

- `af747a`: initial full original source recompile with named gates,
  Boolean frame mask and signed loop-local `++i` matched original CODE,
  literal OMF fields, PUBLIC and complete MAIN link twice.
- `af747b`: further recovered natural `++collision_count` and passed both
  native rounds without removing the final return value or changing the
  original unsigned counter width.
- `af747c`: tried apparently equivalent signed bonus doubling
  `bonus <<= 1` instead of original `bonus += bonus`. TC4 CODE changed;
  that expression is **not** accepted and the original addition was
  restored. The failed compiler source/OBJ remains in its native stage.
- `af747e`: a final **live maintained source** recompile with the explicit
  original double-bonus addition and explanatory codegen comment passed
  both native compiler/full normal linker rounds.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af747e --units e_expl
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af747e

Both independent real original TC4 4.02 compiler rounds match **all 630
original CODE bytes, all 49 ordered native OMF FIXUPPs, the one PUBLIC,
segments and compiler-emitted current-source dependencies**. Each full
99-object normal MAIN TLINK EXE/MAP matches the original source-native
parent; the Japanese 124,642-byte loaded program and all 1,553 ordered
MZ relocations are exact. The separately verified normal MZ serializer
reproduces all original 130,882-byte Japanese MAIN.EXE file bytes. Only
the affected `e_expl` was rebuilt, with the other 98 original project
objects and CRT **reused**, no full cold replay.

Primary source-bound proof `.analysis/work/exatt-layout-af747e/report.json`
SHA-256 `56412f98555d46b804476c28c43b8c66b0a868000ae60245724991dfca9f772a`.
Original native compiler/linker output, exact OMF dependencies, negative
trial and all full binary products remain retained. These original CODE
bytes were already owned; this establishes natural source-codegen
fidelity, **not** newly accepted canonical Factory packed-file units,
historical vendor raw-OMF packet identity or whole-product closure.

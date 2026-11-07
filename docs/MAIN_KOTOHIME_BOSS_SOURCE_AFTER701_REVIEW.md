# Kotohime full BOSS: native ring and radial-attack C++ source after701

This is a genuine full-object original Turbo C++ 4.02 compiler/TLINK
source proof for the **complete eleven-function Kotohime BOSS
translation unit**, not an isolated render leaf. It owns the large
BOSS update dispatcher, random/aimed ring attack generators, pellet
arcs, the nested radial burst and the normal/introduction ring
renderers: **1,840 original CODE bytes, 262 literal ordered FIXUPPs,
eleven PUBLIC offsets**.

The complete `kotohime_ring_emit` now uses natural
`if(randomize_angle)` instead of an explicit comparison to
zero. It consumes exactly the same original per-pellet random word
in the randomized ring and none in the aimed rings (native control
`af701b`). Four independent complete attack/renderer loops now
use ordinary C++ prefix increments: the optional-angle
ring emitter, the radial burst's center loop, its nested pellet
loop, and the shared ring renderer. Turbo C++ emits every
original machine instruction and fixup from this source
(`af701c`).

Both normal BOSS renderer state tests
`if(boss_render_mode)` and `if(boss_hit)` now use natural
byte-field truthiness, with exact original-compiler output
(`af701d`). Their sprite/render order, collision side effects,
signed 16-bit pixel conversion and current packed BOSS template
are unchanged.

**Concrete negative experiment:** Both random and aimed ring
branches previously used a distinct AL load, add 2 and store
for the original 8-bit `boss_move_phase`. Even a typed
natural `boss_move_phase = static_cast<unsigned char>(
boss_move_phase + 2)` changes the original native CODE
(`af701a`). The compiler-visible AL path is therefore
preserved, not inaccurately called an equivalent replacement.
The original signed integer full-circle angle division
and prior natural `i * 256`/ `i * 128` improvements remain.

Final source/packed-header OMF-COMENT-attested native pair:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af701e --units ba_koto
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af701e

Both actual current-source native compiler rounds reproduce **all
1,840 CODE bytes, 262 ordered literal native FIXUPP fields and
eleven PUBLICs**, original full OMF segments, normal complete MAIN
EXE and path-normalized complete MAP, Japanese loaded program,
all 1,553 ordered MZ relocations and independent byte-exact
130,882-byte original Japanese MAIN.EXE serialization.

Preserved original source, objects and compiler/linker writer evidence:
`.analysis/work/exatt-layout-af701e/report.json`,
SHA-256 `59dc84e0ddc0336e2371dff7b2685b28340cb441d9100056e57e88bac2d42c8f`.
Only this one affected complete original BOSS source was compiled
twice; the other 98 original project objects and CRT libraries
were reused. No full game cold replay, target-byte patch or newly
accepted canonical Factory packed-game CODE bytes are claimed.

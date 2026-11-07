# TH03 MAIN original combo HUD and BOSS/Panic controller — after751

The single maintained `src/main/player/combo.cpp` is compiled into **two
original physical TC4 source owners**, not one artificial object:
`p_combo` (491 CODE bytes / 17 ordered native OMF fixups / 2 PUBLICs)
contains the large 16-bit combo score accumulator and full HUD update,
while `p_cmbhl` (487 CODE / 40 fixups / 3 PUBLICs) owns the BOSS-launch,
charged fireball and panic threshold controller. They are linked at
original distinct positions and **both** were actually compiled together
in each native round.

## Source recovery and experiments

The source now names the two-hit chain-continuation threshold, the
**unsigned 16-bit four-frame HUD blink** and first-two-frame brightness
window. Within the large combo HUD routine, the blink interval uses
natural `(round_or_result_frame & 3) < 2`, retaining the original
**bitwise `&` between the two distinct render conditions** (substituting
logical `&&` is a documented original-codegen failure). The two-player
clip/score location uses natural `if(!pid)` rather than explicit `== 0`.
Original chain score saturation at 65535, hit count cap 99, 80-frame
combo display, 32-frame hit reset, boss score increments of 5120 and
panic route 30000 remain intact. In particular, the actual 16-bit
source-ABI-visible `player.combo_hits_max` is updated before capping
the displayed hit count, and `p->time--` is still original postfix.

`af751b` passed these natural C++ changes simultaneously in two genuine
Turbo C++ 4.02 compiler/full MAIN TLINK rounds. An additional `af751c`
experiment combined the original `uint32_t bonus_total_new = bonus;`
and `bonus_total_new += combo.bonus_total` into a single arithmetic
initializer. The compiler-generated original CODE changed, so the
separate widening/add instruction sequence was **restored**, not called
native-exact. `af751d` again rebuilt the **final current product source**
with an explanatory comment and formatted original bitwise blink:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af751d --units p_combo,p_cmbhl
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af751d

Both real rounds match **all 978 original CODE bytes, all 57 literal
ordered native OMF relocation fields, all 5 PUBLIC offsets**, complete
DATA/BSS and segment/group metadata, native source COMENT dependencies,
full normal MAIN EXE/MAP, original Japanese 124,642-byte loaded program
and all **1,553 ordered MZ relocations**. Independent standard MZ
serialization reproduces every byte of the original **130,882-byte
Japanese MAIN.EXE**. The other 97 original project objects and CRT were
reused; no full cold replay, original-target substitution or CODE patch.

Current-source receipt `.analysis/work/exatt-layout-af751d/report.json`
SHA-256 `b53f3465face515591de22cc226de1c8159ea4acd8fc195421d6f39b1ecd10ba`.
The failed `af751c` original compiler artifacts remain as an actual
negative control. The full two-round source-rooted proof establishes
more natural maintained C++ for existing source-owned original bytes;
not additional canonical Factory packed credit, historical vendor OMF
packet identity or whole-product source ownership.

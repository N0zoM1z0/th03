# TH03 full Combo scoring and BOSS/panic helper, original-native after698

The single maintained `src/main/player/combo.cpp` is partitioned into
**two separate original physical Turbo C++ translation units**:
`p_combo` (491 CODE bytes / 17 ordered native fixups / two PUBLICs)
contains `combo_add_raw` and the substantial
`combos_update_and_render` HUD update; `p_cmbhl` (487 CODE bytes /
40 fixups / three PUBLICs) contains the near wrapper,
charged-fireball chain helper and the large score-dependent
BOSS/panic launch controller. The original linker places
these physical objects in separate sections and orders them
independently. The v2 source binder now uses distinct
`TH03_COMBO_MAIN_ONLY` / `TH03_COMBO_HELPERS_ONLY` wrappers,
and independently checks all six native MAP rows per owner.
The `af696b` unchanged-source dual TC4/TLINK control verified
the original split before source modifications.

## Real C++ recovery in the HUD and scoring source

The two-player render/update loop uses
`for(pid=0;pid<PLAYER_COUNT;++pid,++p)`, the current/last-frame
activity gates use natural `if(!p->time)`, the visible hit
digit uses `hit_val_rem = hit_val_rem % 10` and the four-frame
blink predicate uses `round_or_result_frame % 4 < 2`.
These are genuine changed-source original-byte-equal native
compiler results (`af696c`, `af696e`, `af697a`, `af697c`).

Three negative checks are important to original fidelity:
a natural prefix `--p->time` in the HUD update changes
TC4's native opcode form (`af696d`); converting the
two independent blink predicates' bitwise boolean `&`
into short-circuit `&&` changes original branch CODE
(`af696f`); removing the apparently redundant
`combo_hits_max` local and comparing the field directly
changes original bytecode (`af697b`). The maintained
source retains all three original-native forms.

## Full BOSS/panic trigger and fireball-chain helper

The physically original chained-fireball base value 12,
BOSS score threshold increment 5120, defending-player
panic trigger at 30000 and three-unit panic Gauge gain
now have explicit compiler-time C++ names in the
helper-only physical producer. The original 16-bit
fireball position/round-speed calculation, chain slot
clearing order, BOSS reversal accounting and warning
creation are unchanged (`af697d`, `af698b`).

The warning-state and Gauge/BOSS-active zero checks use
natural nonzero C++ expressions. Real original TC4
emits byte-for-byte identical CODE (`af697e`,
`af697f`, `af698a`). The highly specific
`_asm { nop; push cs; call near ptr fireballs_add; }`
still preserves the original near/far segment ABI and
was **not** replaced with an unproved ordinary call.
This is an ABI boundary rather than evidence that
the source was originally written as inline assembly.

## Source-bound native proof

Both new complete original Turbo C++ 4.02 and full normal
MAIN TLINK rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af698c --units p_combo,p_cmbhl
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af698c

reproduce every one of **978 original CODE bytes, 57
literal ordered FIXUPP fields, five PUBLIC offsets**,
all original OMF segment/BSS metadata, the complete normal
MAIN EXE/path-normalized MAP, the Japanese loaded program,
all 1,553 ordered MZ relocations and the independently
serialized exact 130,882-byte original Japanese MAIN.EXE.
The original Borland OMF COMENT dependency records prove
both compiler processes actually consumed the current
modified `combo.cpp` in its corresponding partition.

Native actual-source/OBJ/EXE/MAP writer evidence:
`.analysis/work/exatt-layout-af698c/report.json`,
SHA-256 `fb89db83073eaac096c687a5f308d8e82a66969e41c0fd63e6e9785e66137554`.
Only two selected physical original objects were rebuilt
in two compiler rounds; other 97 originals, startup and
CRT libraries were reused. No cold replay or target
object patching was used. The original CODE was
already source-owned; this is not newly accepted
canonical Factory packed-game byte credit.

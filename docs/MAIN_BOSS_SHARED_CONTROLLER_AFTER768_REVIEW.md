# TH03 MAIN shared major-BOSS state and attack controller: original-native after768

The original `src/main/boss/shared.cpp` is divided into **two distinct
physical Turbo C++ source objects**. `ba_sring` contains the large
24-sprite explosion ring (348 original CODE bytes, 22 ordered FIXUPPs,
1 PUBLIC). `ba_srest` contains the seven shared functions for BOSS
movement, descending, template activation, hit/lifecycle and random
attack-mode selection (601 CODE bytes, 84 ordered fixups, 7 PUBLICs).
Both are source-bound in the original 99-object MAIN linker order.

## Source recovery in the entire major controller

The long real `boss_update_start` / `boss_pattern_next` paths now have
explicit compile-time C++ names for original 16-bit and byte mode gates:
`BOSS_EXPLODE_MODE=0xFF`, `BOSS_DESCEND_MODE=0x80`, the 16-choice
random attack mask `0x0F`, the 2-step mode offset, the 2-step
anti-repeat radius and original 8-choice pattern-count mask. The exact
nearby-pattern rejection uses two separate signed/unsigned comparisons
and **does not change original RNG consumption or do/while order**.
The hit/descend/launch transition states are not merged: the source
preserves the original 32-byte BOSS template record and the order in
which the player attack is launched and palette restored.

## Original compiler trials that **failed** and were rejected

`boss_update_start` contains a real fixed-32-byte template copy that
uses original `_SI`, `_DI`, the current DS copied to ES, `_CX=16` and
`asm { rep movsw }`. We challenged that historical register sequence
with two actual original TC4 4.02 compiler experiments:

- `af768a` used natural C++ `boss_state = boss_character_template[pid_current]`.
  It emitted a **597-byte `ba_srest` CODE** instead of the original
  601 bytes, changed OMF fixups and later PUBLIC offsets.
- `af768b` used a `register boss_state_t near *source`, selected player
  0/1 explicitly and then wrote `boss_state = *source`. That also
  changed original CODE. Neither aggregate-copy form is accepted.

The exact original `REP MOVSW` template copy therefore remains explicit.
Two independent original `ba_sring` experiments were also rejected:
`af768d` changed signed `length *= 8` to `length <<= 3` and generated
non-original CODE; `af768e` changed `(0 - (unsigned char)length)` to
unary `-static_cast<unsigned char>(length)`, likewise changing original
CODE. The sixteen-plus-eight-sprite ring's original angular arithmetic,
near Pascal ABI and status return were retained.

`af768c` proved the substantial shared BOSS controller's named gates
native exact in two genuine original compiler/full MAIN link rounds;
`af768f` independently recompiled the **final current maintained source**
with original copy/multiply/angle code and explanatory comments:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af768f --units ba_sring,ba_srest
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af768f

Both genuine original TC4 4.02 and normal TLINK rounds reproduce **all
949 original CODE bytes, all 106 ordered literal original native OMF
FIXUPPs, all 8 PUBLIC offsets**, segment/ABI and compiler source-COMENT
metadata, complete normal MAIN EXE/normalized MAP, Japanese 124,642-byte
loaded program and all 1,553 original MZ relocation words. Independent
standard MZ serialization reproduces every byte of the original
130,882-byte Japanese MAIN.EXE. The other 97 project objects and CRT
were reused, **not cold-replayed**. No patched objects, inserted NOPs
or target-byte arrays were used to obtain a match.

Current original source-bound proof:
`.analysis/work/exatt-layout-af768f/report.json`, SHA-256
`42ba07b82b299aa73892124842a193fed02f1627014739fe3e5aea2c28fc3525`.
The four negative compiler trials remain available under their native
stages, not promoted to exactness. This demonstrates natural source
progress and a real compiler/ABI limit, **not** new Factory canonical
packed-file acceptance, vendor raw OMF packet equality or whole-product
99-object source ownership.

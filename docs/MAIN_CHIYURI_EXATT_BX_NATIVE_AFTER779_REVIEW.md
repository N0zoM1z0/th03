# TH03 MAIN Chiyuri Extra Attack: natural BX comparison and full beam update — after779

The complete original `ex_chyu` Turbo C++ physical source owns **four
functions** including paired projectile creation, a roughly 518-byte
GRCG beam renderer, a roughly 298-byte paired-entity update state machine
and the shared renderer dispatcher. The original OMF contains **978 CODE
bytes, 55 literal ordered FIXUPP fields and 4 PUBLICs**. We rebuilt
this actual physical original 16-bit translation unit, not an isolated
invented hitbox leaf.

## Genuine original register-source recovery

The original `exatt_update_chiyuri()` loop contained a handwritten
assembler sequence which loaded the global `exatt_entity_p` pointer into
BX, compared byte `[BX]` against zero and conditionally branched to
`chiyuri_first_done`. **The maintained game now contains normal C++**:

    if(!exatt_entity_p->state) {
        goto chiyuri_first_done;
    }

The real original Turbo C++ 4.02 compiler naturally emits the **identical
original BX/memory comparison and conditional jump** for that expression,
without manually scripting the original instructions. The important
`chiyuri_first_done` label, `exatt_entity_p++` side effect and every
paired top/bottom entity update remain exactly ordered. In the complete
beam renderer and update controller, active/flying state names, hit-
warning/flying-result Boolean tests and the two paired-entity render
loops are also ordinary native-exact C++ while preserving all original
GRCG trapezoid, collision-map, sound and palette calls.

## Real compiler experiments / source-exactness constraints

- `af779a`: first complete modified physical source trial, with natural
  state names and two paired-entity controllers, matched every original
  CODE byte, OMF relocation field and full MAIN link in both rounds.
- `af779b`: independently replaced the handwritten BX/CMP/branch with
  the natural C++ condition above, and **both original native compiler
  rounds still matched the entire complete physical original object**.
- `af779c`: attempted to remove the late beam-radius AX/DX stack dance
  and use `_AX = (CHIYURI_BEAM_FINISH - phase)` in the 518-byte renderer.
  TC4 generated different original CODE, so the original register/stack
  sequence in this **different** branch remains intact. Rejected.
- `af779d`: restored the native-exact late-beam instructions, added a
  comment explaining the C++-generated BX comparison and recompiled the
  **final live maintained game source** in two genuine original TC4 4.02
  rounds and full normal MAIN TLINK links. Both passed byte-for-byte.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=s .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af779d --units ex_chyu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af779d

Both compiler rounds exactly reproduce all **978 original CODE bytes,
55 literal ordered OMF FIXUPP fields, 4 PUBLIC offsets**, original
segment and compiler-emitted source COMENT declarations. The full
normal 99-project-object MAIN EXE and normalized MAP, Japanese
**124,642-byte loaded game and all 1,553 ordered MZ relocations** match;
independent standard MZ serialization reproduces every byte of the
original **130,882-byte Japanese MAIN.EXE**. Only `ex_chyu` was rebuilt;
98 original project objects and CRT were reused without a cold replay.

Proof `.analysis/work/exatt-layout-af779d/report.json`, SHA-256
`e974c5f24919c739c566e7337702c0bcb6188245ff623f0bf35424bc3de20542`.
This is a real elimination of previously handwritten original CPU
instructions from a **large** original controller, with a separately
retained negative control. The game bytes were previously source-owned;
no new canonical Factory packed-unit accepted credit, vendor-raw OMF
identity or whole-program source ownership is claimed.

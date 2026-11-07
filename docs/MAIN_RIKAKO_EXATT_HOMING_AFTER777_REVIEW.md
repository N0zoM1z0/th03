# TH03 MAIN Rikako Extra Attack: full homing/collision 14-slot controller after777

The original `ex_rika` 16-bit Turbo C++ physical source owns **five
complete functions**: eight-slot normal creation, fourteen-slot special
creation, aimed sprite render, the substantial fourteen-slot homing /
clip/hitbox/collision update loop and active-entity renderer. Its
original complete source/OMF has **702 initialized CODE bytes, 46
ordered literal FIXUPP fields, 5 PUBLICs** and original segments.

The maintained C++ now uses natural signed local `++i` in all four
creation/update/render loops while retaining original pointer postfix,
original 32-byte entity pool layout, target-player selection, random
draws and homing movement. Explicit byte-valued inactive (0), active (1)
and flying (2) states are named; simple inactive/active checks, the
homing-disabled flag and the two-frame sprite palette selection use
native-exact Boolean expressions. In the sprite render leaf, the
original unsigned-byte `% 2` is naturally an `if(frame & 1)` because
TC4 generates precisely the original sprite offset instructions here.

Two deeper homing state machine expressions were **actually challenged
against genuine compiler output, not assumed**:

- `af777b` rewrote the original signed-char `angle_delta /= 8` as
  `angle_delta >>= 3`. The full object differed, and negative angular
  deltas also expose distinct signed truncation semantics. Rejected.
- `af777c` replaced the mutable byte memory `p->speed++` with
  `++p->speed`. Real original CODE differed. Original postfix retained.

`af777a` first established full source-native equality for the broader
changed state machine. The final source with preserved original signed
division and byte postfix and comments was independently rebuilt in
**two real original Turbo C++ 4.02 compiler/full normal TLINK rounds**:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af777d --units ex_rika
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af777d

Both rounds reproduce **all 702 original CODE bytes, all 46 literal
ordered OMF FIXUPP fields, all 5 PUBLIC offsets**, original segments
and current-source compiler COMENT dependencies, complete normal MAIN
EXE/normalized MAP, Japanese **124,642-byte loaded program** and all
**1,553 ordered MZ relocations**. Independent standard MZ serialization
matches the complete original **130,882-byte Japanese MAIN.EXE**. Only
this original physical TU was rebuilt; the other 98 game project
objects and Borland CRT were reused unchanged. No cold replay, target
patching, CODE padding or fabricated OMF was used.

Current source receipt `.analysis/work/exatt-layout-af777d/report.json`
SHA-256 `5169597a110760a9e8877f8751a6450189bed7f9ea0487e4a9c7aec0d5b1eb09`.
Both native negative experiments and all writer logs remain retained.
This demonstrates natural current C++ codegen fidelity for **already
owned original game bytes**, not new canonical Factory packed-file
acceptance, historical vendor raw OMF packet identity or whole-product
99-object source ownership.

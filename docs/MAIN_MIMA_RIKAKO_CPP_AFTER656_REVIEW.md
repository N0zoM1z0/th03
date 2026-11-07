# Mima and Rikako complete BOSS native C++ improvements (after656)

This source-bound original Turbo C++ 4.02 / TLINK proof covers the
two complete large character BOSS sources together, including their
actual attack schedulers, entire pattern generators and renderers.

Mima's full BOSS update computes the other player's bullet PID after
calling the shared BOSS target helper. The old AL load/one-minus/store
sequence now uses ordinary C++ direct assignment:

    bullet_template.pid = (1 - pid_current);

The calculation is intentionally repeated after the helper, not
incorrectly replaced with the earlier pid_other local. The real
TC4 source-bound independent negative/positive check af656b proves
exact original code generation over the entire 1,922-byte Mima TU.

Rikako's large entity-and-pellet BOSS pattern also emits original
instructions using a natural byte-field operation:

    bullet_template.speed.v += 8;

The original AL intermediary is gone; complete 1,677-byte native
CODE equality was proved independently in af656a. Conversely,
changing the signed renderer's original AX += -8 to AX -= 8
changes the actual 16-bit register opcode (af656c). The
original register form is therefore retained with an explanation
rather than claiming semantic arithmetic alone proves exactness.

The full simultaneous two-round compiler/link evidence is:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af656d --units ba_mima,ba_rikak
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af656d

Both original TC4/TLINK rounds preserve every byte of the combined
3,599 native CODE bytes, 492 literal ordered FIXUPP fields, 17
PUBLIC offsets and all original OMF segments. Their full normal
MAIN executable and path-normalized complete MAP match the
historical source-native parent. The original Japanese loaded
program, all 1,553 literal MZ relocations and independently
serialized 130,882-byte Japanese MAIN.EXE also match.

The compiler actually consumed the current modified BOSS source
paths, as evidenced by native OMF COMENT dependencies in both
rounds. Proof archive:
.analysis/work/exatt-layout-af656d/report.json
SHA-256 2f437fa71668cd525413068b3bb810a4999ac444edd92175fe612eadc9b86da8.
Only two selected physical BOSS objects were recompiled;
the other 97 original game objects and startup/CRT libraries
were reused, not cold replayed.

The work improves original-byte-exact maintainable C++ inside
already tracked CODE. Raw historical vendor OBJ packet identity,
new canonical packed-game Factory credit, and real PC-98
hardware behavior are not implied.

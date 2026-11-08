# TH03 MAIN Kotohime BOSS: natural volatile phase reload

The random-ring attack's second phase increment is now a C++ volatile-byte
read feeding the original AL register expression:

    _AL = *(volatile unsigned char near *)&boss_move_phase;
    _AL += 2;
    boss_move_phase = _AL;

This removes the direct memory-to-register pseudo-assignment while preserving
the original explicit byte reload. It matters because the preceding
boss_move_phase += 4 leaves the new phase in AL. Without an observable
reload, Turbo C++ reuses that AL value and omits the original second memory
read. The volatile dereference forces the original MOV AL,[boss_move_phase]
before ADD AL,2 and the store.

## Compiler experiments

- af965c: direct boss_move_phase += 2 generated **1,838 CODE bytes and
  261 FIXUPPs**, rather than the original **1,840 / 262**.
- af965d: a nonvolatile local-byte temporary also failed the full object.
- af967c: boss_move_phase = static_cast<unsigned char>(boss_move_phase + 2)
  reused AL from the preceding +4, omitting the reload.
- af967e: a single volatile C++ assignment expression still did not
  preserve the original instruction sequence.
- af967f and af968a: ordinary and register-local byte temporaries also
  failed complete CODE equality.
- af967d: a volatile dereference assigned to AL, followed by the
  original byte increment/store, matched both full native rounds.
- Final af968c: the same current source with an explanatory codegen
  comment was rebuilt and reviewed again in two independent rounds.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af968c --units ba_koto
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af968c

Both genuine original Turbo C++ 4.02 rounds recompiled the entire
1,840-byte, eleven-function Kotohime BOSS, preserving all 262 literal
ordered OMF FIXUPP fields and eleven PUBLIC offsets. Both complete normal
MAIN links reproduce the 124,642-byte Japanese loaded image and all
1,553 ordered MZ relocations. The other 98 original game objects and
original Borland CRT were reused; no full cold replay.

Protected current-source report:
.analysis/work/exatt-layout-af968c/report.json, SHA-256
4e85046a9c0d4a959b28e736d339392fda2732e25a086bfa0abecaee0834a598.

# Reimu BOSS: source-recovered scheduler and four full attack timelines

Reimu's complete physical BOSS translation unit has nine functions,
including the large `gba_boss_update_reimu` dispatch and its four full
attacks: orbiting cloud, two-stage spreads, expanding/releasing orbit
and mirrored spreads. Unlike other characters, its real update first
processes intro and pattern-selection **before** the separate attack
`switch`, so an apparently equivalent generic single-switch
refactoring could change when a newly selected pattern runs. The
maintained C++ intentionally preserves this observed behavior.

The dispatch now names every shared scheduler value 2..17 according to
its actual Reimu-specific attack family, and names the 0x80 fall and
0xFF explosion states. Real frame phases are also explicit as
compile-time typed enums: the cloud's initialization and 0x80 finish,
narrow/medium spreads switching at 0x40/0x64, orbit expansion through
0x18 and Extra Attack release at 0x50, and mirrored spread finish at
0x80. The original global 16-frame synchronization and independent
RNG calls are left intact; no extra DATA, bounds check or gameplay
correction is introduced.

A negative control `af631a` found that the tempting
`angle = -angle` is **not** codegen-identical to the original
`angle = (0 - angle)` under this compiler and register allocation.
The original eight-bit expression is retained. After named scheduler
modes (`af631b`) and four timing sets (`af631c`) were added,
both complete real native Turbo C++ 4.02 compiler/linker rounds passed:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af631c --units ba_reimu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af631c

Each rebuilt object must bind its emitted Borland OMF COMENT
dependencies to the actual changed C++ source. The entire **2,020
original CODE bytes, 270 literal ordered native FIXUPP fields,
nine PUBLICs** and segment metadata match exactly. Both full
normal MAIN EXEs and complete path-normalized MAPs equal the
historical source-native link; all 1,553 Japanese MZ relocations,
loaded program bytes and the independently serialized original
130,882-byte Japanese MAIN.EXE match.

Native receipt:
`.analysis/work/exatt-layout-af631c/report.json`,
SHA-256 `be81ac69e6d1cd2700ce2f947e1b4f13244e8e4eccba2757bd00ff4854dbfdc8`.
All actual compiler/linker phase logs, emitted objects and the
complete response, EXE and MAP evidence are retained; only this one
source TU was recompiled. No canonical packed-file Factory credit,
historical raw vendor OMF packet identity or physical hardware
behavior proof is claimed.

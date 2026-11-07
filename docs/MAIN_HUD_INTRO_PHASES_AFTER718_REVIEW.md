# TH03 MAIN large original HUD intro/particle state machine — after718

`intro` is a **single complete original physical TC4 source TU** with
1,478 original initialized CODE bytes and four PUBLIC functions. It spans
three maintained implementation includes: `start_anim.inl` (long particle
initialization, slide, banner and 128-particle update), `start_render.inl`
(frame-by-frame HUD intro drawing) and `start_lowlevel.inl` (real-mode
VRAM hardware strip/pixel output). The after595 native success was
historical; prior scoped source verification could not independently bind
later modifications in these three nested live `.inl` bodies.

The scoped compiler now supports `intro`, its actual original after595
full-MAIN linker slot, all three separate current implementation files,
per-round SHA input identities and mandatory **native OMF COMENT source
dependencies** for the root and every `.inl`. It is not satisfied by stale
WORK copies. Source-wrapper, original object and normal MAP identities are
checked against the unchanged after596 parent.

## Real natural C++ progress and negative controls

The **long HUD update and rendering state machines** now share explicit
four-stage C++ phase names: slide, banner, star initialization and star
motion. The reset/running/stopped flag protocol, separately initialized
16 slide strips and two 64-star banks (128 total), and the original RNG
draws in each bank remain distinct. Six original update/render loops
now use natural prefix `++i` for the signed register index without
changing the original global particle-pointer mutations or codegen. The
three low-level video functions' original hardware semantics remain intact.

We also challenged a real limitation, rather than assuming all apparent
C++ simplification is exact. `af718b` attempted direct natural
`hud_start_particle_p->field` in place of a manual `mov bx` and `_BX`
field accesses in the slide update; the original CODE differed and
shifted the full function length. `af718c` tried a `register` near
particle pointer; it also changed CODE. **Both are rejected** and their
failure stages retained. The exact original manual-BX operation remains
where TC4 has not yet naturally reproduced its register/lifetime.

`af718a` established an unchanged source-bound control. The current
**modified-source** verification `af718d` rebuilt only the original
`intro` object in two genuine TC4 4.02 / full original TLINK rounds:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af718d --units intro
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af718d

Both rounds match **all 1,478 original CODE bytes, 145 ordered native OMF
FIXUPP fields, all 4 PUBLIC offsets and the complete original segment
layout**. Entire original normal source-native TLINK MAIN and MAP match;
the Japanese 124,642-byte program, all 1,553 MZ relocations and the
independent original 130,882-byte full-file MZ serialization also match.
The other 98 original game objects and the original CRT were reused.

Receipt: `.analysis/work/exatt-layout-af718d/report.json`, SHA-256
`084f24c906bea93b15a8987eef6bd13014749abb905b87f732e59165ceeb348a`.
It retains the actual current-source and three `.inl` snapshots, all
writer logs, two complete compiler/linker rounds and full OBJ/EXE/MAP.
This is real C++ and source-binding progress, **not new canonical Factory
packed-unit acceptance or proof of original vendor raw OMF packet identity**.

# TH03 MAIN Mima Extra Attack: native six-slot bounce/acceleration controller after770

The original 16-bit `ex_mima` Turbo C++ physical owner includes **four
complete functions**: six-slot entity creation, projectile sprite
state rendering, the large bouncing movement/collision/acceleration
controller and the active-entity renderer. Its original physical module
has **727 initialized CODE bytes, 44 literal ordered native OMF FIXUPP
fields and 4 PUBLICs**. The source recompiled the whole original TU,
not a small invented standalone snippet.

Natural C++ source changes now name the distinct original inactive (0)
and active (1) 8-bit entity states, preserve flying state 2 and the
appearing/collision timing, and use signed local prefix `++i` in all
three six-entity loops. Original pointer postincrements and frame,
state and speed byte-memory mutations remain unchanged. The original
hitbox and arrival predicates now use natural zero/nonzero Boolean
checks; the two different 8-bit bounce frame conditions are likewise
expressed by `if(!p->frame)` and `if(p->frame)`.

The physically important **16-bit duration parity** that controls
acceleration between the original 0x10 and 0x20 transition frames is
now written as ordinary `duration & 1` rather than an explicit
`static_cast<unsigned int>(duration) % 2`. The complete original
codegen matches despite the shorter source expression. The original
signed x/y reflection and unusual no-bounds-check projectile behavior
are deliberately preserved.

## Executed original-native compiler experiments

- `af770a`: natural six-slot local loops, state names and original hit
  Boolean results compiled exact in two genuine original TC4 rounds.
- `af770b`: the narrower `duration & 1` acceleration parity also
  compiled exact in both real original compiler/full MAIN linker rounds.
- `af770c`: a separately compiled attempt to replace original direct
  signed `p->velocity_x = -p->velocity_x` with `*= -1` failed original
  CODE exactness. The direct signed negation was restored.
- `af770d`: natural byte-frame truth checks passed again.
- `af770e`: explanatory compiler-source comments were added, and the
  final maintained complete TU was genuinely compiled and full-linked
  in two fresh original Turbo C++ 4.02/TLINK rounds, both byte exact.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af770e --units ex_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af770e

All **727 original CODE bytes, 44 ordered literal native FIXUPP fields,
4 PUBLIC offsets, original segments and native current-source dependency
COMENT records** match. Both complete 99-project-object normal MAIN
EXE/MAP links reproduce the original Japanese **124,642-byte loaded
program** and all **1,553 ordered MZ relocations**. The independent
standard MZ serializer matches all **130,882 bytes** of original
Japanese MAIN.EXE. The other 98 project objects and original CRT were
reused without any full cold replay or byte patching.

Current-source report `.analysis/work/exatt-layout-af770e/report.json`
SHA-256 `cc0a154da930677bd99414f3cb5768aa26d8742660469519a8c5b7f7ccbd8ade`.
The failed `af770c` original compiler writer is retained separately.
This is newly demonstrated natural C++ exactness for already source-owned
original bytes, **not** additional canonical Factory packed-file accepted
credit, historical vendor raw OMF packet identity or whole-game closure.

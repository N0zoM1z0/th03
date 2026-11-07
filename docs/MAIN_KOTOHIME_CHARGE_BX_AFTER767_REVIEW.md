# TH03 MAIN Kotohime Chargeshot: natural source / historical BX near-pointer ABI (after767)

The complete original `cs_koto` Turbo C++ physical object owns **nine
functions** (690 initialized CODE bytes, 79 literal ordered OMF FIXUPP
fields and 9 PUBLICs): the original 8-byte projectile creation/update,
charge/hit collision, sprite renderer and full Gauge pellet/bullet
attack controller. We challenged its machine-register collision setup
while retaining exact native output as the acceptance criterion.

## Actual native experiments, including rejected alternative C++

The hit test's historical `_BX = (unsigned int)kotohime_chargeshot_p` and
`#define p (*(kotohime_chargeshot_t near *)_BX)` are not automatically
reproduced by obvious C++ equivalents. We separately compiled the
**entire nine-function physical source** with:

- `af767a`: a `register kotohime_chargeshot_t near *` replacing the BX
  macro, giving 692 CODE bytes instead of original **690**, and moving
  later original PUBLIC offsets. Not accepted.
- `af767b`: a `register unsigned int address` plus a casted near lvalue,
  also producing non-original CODE. Not accepted.
- `af767d`: an ordinary `kotohime_chargeshot_t near&` reference, again
  changing CODE. Not accepted.

The old raw BX code is **retained only where experimentally necessary**;
we did not inject a fake original instruction stream, change physical
record layout, or claim these failed variants exact. The real compiler
logs/objects for all three native negative controls are preserved.

## Accepted natural C++ source changes

The complete Chargeshot creator now accesses the original 16-bit
subpixel fields naturally and directly:

    kotohime_chargeshot_p->center.x.v = center_x.v;
    kotohime_chargeshot_p->center.y.v = center_y.v;

The two Gauge active-flag entry helpers use native-exact Boolean tests,
while the main gauge frame's first-frame guard uses `if(!frame)` rather
than an explicit equality check. The original separate Gauge state
reload, RNG bit, side-effect ordering, original 0x80 exit, and
16-bit near/far-Pascal ABI remain intact. These modified expressions
passed in actual `af767c` and final **current-source** `af767e` native
compiler and complete normal MAIN linker rounds.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af767e --units cs_koto
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af767e

Both actual original TC4 4.02 compiler/TLINK rounds reproduce all
**690 original CODE bytes, 79 ordered literal native OMF FIXUPP fields,
9 PUBLIC offsets**, complete source-dependency/segment metadata, normal
full 99-object MAIN EXE/MAP, Japanese 124,642-byte loaded program,
1,553 ordered relocations and separately serialized original Japanese
130,882-byte MAIN.EXE. The **other 98 project objects and Borland CRT
were reused**, not cold-recompiled.

Source-bound protected receipt:
`.analysis/work/exatt-layout-af767e/report.json`, SHA-256
`221944be28f6bcb615d45ef463f8f0df267931f9b995f8c38d9b7b39c8da0c29`.
This is current original-source/codegen fidelity for existing physical
bytes, not new Factory canonical packed-file credit, historical
raw-vendor OMF packet identity or completed game-source ownership.

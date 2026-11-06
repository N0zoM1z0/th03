# MAINL CDG 386 blitters: real shared TASM source and CODE EVEN

The original CDG drawing objects cdg_put.obj and cdg_p_na.obj are
three complete symbolic 386 far routines operating on PC-98 VRAM:
CDG_PUT_8 (alpha + colors), CDG_PUT_HFLIP_8 (mirrored pixels),
and CDG_PUT_NOALPHA_8 (plane-based drawing). They share original
maintained macro source under src/shared/formats/ rather than
introducing an opcode-byte array or invented draw algorithm.

New bounded MAINL forwarding translation units:
src/mainl/formats/cdg_put_native.asm and
src/mainl/formats/cdg_noalpha_native.asm reuse precisely those
natural shared TASM sources. Their native TASM5 code contains 382 + 114
original initialized CODE bytes, 19 ordered OMF FIXUPP entries, and
all three PUBLIC function addresses. In particular, natural TASM
EVEN produces the verified original 90h at CODE+179 and CODE+381
in cdg_put and at CODE+113 in cdg_p_na. All complete original
object CODE bytes, ordered native fields and segment definitions match,
not merely the last alignment byte.

Two native TASM/TLINK rounds then replaced *both* objects simultaneously
in the after575 large Staff/Cutscene source-native MAINL build. Both
reproduce the entire 67,372-byte Japanese decoded MAINL EXE,
all 677 ordered MZ relocations and original complete MAP geometry.
Only assembler module filenames differ in MAP text.

A first after576 proof attempt also passed all native compiles/links but
incorrectly demanded raw cross-round MAP identity despite upstream
Cutscene/Staff source files using distinct r1 and r2 diagnostic names.
Its native objects, logs and unfinished report are preserved. A fresh
after577 stage verifies the real original per-round MAP coordinates and
normalizes only these two proven source-name differences before comparing
the two entire output vectors. No target or source object patch occurred.

Original and shared 386 source was already maintained, so this is an
additional reproducible source-link integration and natural CODE alignment
proof; it is not new source ownership credit for the original three
functions, historical tool/packet identity or canonical Factory acceptance.

Run affected native review without any cold replay:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_cdg_after577_work.py

Native build: scripts/build_th03_mainl_cdg_after577_work.py
Report: .analysis/work/mainl-cdg-after577-native-build.json
Review: .analysis/work/mainl-cdg-after577-native-review.json
Both OMF/EXE/MAP rounds, native writer logs and source/recipe inputs are retained.

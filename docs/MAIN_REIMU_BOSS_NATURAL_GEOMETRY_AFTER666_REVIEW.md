# Reimu major BOSS: exact two-stage orbit scale and native render arithmetic (after666)

The full original Reimu BOSS translation unit owns nine complete
functions, 2,020 original CODE bytes, and the substantial attack
and update controllers. This recovery covers its huge expanding
orbit/Extra Attack pattern, the cloud attack tick clock, the other
orbit ring cadence, and the two independent sprite renderers.

## Recovered natural C++ and meaningful negative control

Two original masked frame checks now use ordinary unsigned C++:
`boss_frame % 2 == 0` for orbit-cloud speed acceleration and
`boss_frame % 16 != 0` in the expanding orbit's emission clock.
Actual modified-source TC4 `af666a` compiled **all original
bytes** across the complete physical BOSS object.

The expanding orbit originally had two distinct arithmetic operations:
`((boss_frame << 4) * 2)`. A tempting single multiply
`boss_frame * 32` was *not* native-equal (`af666b`), even though
the mathematical radius is the same. Preserving the actual two
integer calculation stages via **natural C++ multiplication**
`((boss_frame * 16) * 2)` reproduces the entire original
16-bit CODE and fixups (`af666c`). The source documents this
real Borland instruction-scheduling constraint, rather than
silently changing the radius representation.

Both small sprite renderer leaf functions now express their
four-frame animation clocks as `anim = boss_frame / 4`
instead of `boss_frame >> 2`. Since `boss_frame` is
unsigned, Turbo C++ lowers this exact power-of-two division
to the original shift instructions (`af666d`). Render order,
original sprite ABI and signed pixel conversions are unchanged.

Final original-source/OMF-dependency-attested two native rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af666e --units ba_reimu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af666e

The original Turbo C++ 4.02 compiler/TLINK pair reproduces
**every one of 2,020 original CODE bytes, 270 literal ordered
OMF FIXUPP fields, 9 PUBLIC offsets** and complete original
segment/ABI metadata. The linked normal complete MAIN EXEs
and path-normalized MAPs equal the retained after596 parent,
as do the loaded Japanese program image, 1,553 ordered
MZ relocations and independent exact 130,882-byte original
Japanese MAIN.EXE serialization.

Retained genuine compiler source and binary evidence:
`.analysis/work/exatt-layout-af666e/report.json`
SHA-256 `46befdf97161e696689382812bce2a18ea53cddfd52a2bf5dbe23bdb5c2cd032`.
Only the affected full Reimu BOSS object recompiled twice; all
other 98 project objects and startup/CRT libraries were reused.

These 2,020 CODE bytes were previously tracked original source
bytes. They are not new canonical packed-game Factory credit,
historical raw vendor OMF packet identity or PC-98 runtime proof.

# Chiyuri Extra Attack: paired beam renderer and update states (after649)

The complete original 978-CODE-byte Chiyuri Extra Attack physical
producer contains four functions: paired projectile creation, the
**518-byte GRCG trapezoid/line beam renderer**, the **298-byte
two-ended update/collision state machine**, and batch rendering.
The beam is not 16 independent shots: its 32-byte entity slots
are handled in eight **even/odd pairs**, one for each beam endpoint.

The maintained source now identifies the physical pair stride,
all sixteen owned entity slots and the true beam timeline:

- Phase below 0x10 draws the narrow line; 0x10..0x27 draws a
  growing two-color trapezoid before the final white center line.
- Phase 0x28..0x6F draws the full three-color trapezoid;
  0x70..0x87 shrinks it; at/after 0x88 no beam remains.
- The pair updater issues the first warning at frame 4, plays
  its sound at frame 0x10, writes the sloped collision map
  on 0x29..0x6F, frees the pair after frame 0x88, and preserves
  the independent first/second endpoint flight-arrival flags.

These physical slot counts and true *frame* phase boundaries are
compiler-time C++ enums. The original **near ASM skip branch**
for an empty first entity, the line/trapezoid join labels, the
separate `exatt_entity_p` pair-pointer choreography, and the
late-beam original AL/AX/DX stack/register sequence are preserved.

A concrete negative source experiment (`af649a`) attempted to
replace the late-beam register/stack sequence with the natural,
typed `_AX = 0x88 - phase`; it **changed** the full original
native CODE. The exact original register sequence is therefore
retained, with an explanatory comment, rather than pretending the
semantic rewrite was byte-identical.

The accepted final current-source/OMF-header-attested two-round
original Turbo C++ 4.02/TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af649b --units ex_chyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af649b

Both complete original CODE objects match **978 bytes, 55 literal
ordered native FIXUPP fields, four PUBLIC offsets** and all original
16-bit OMF segments. Both complete normal MAIN links and normalized
MAPs match the retained source-native original. The Japanese loaded
program, 1,553 literal ordered original MZ relocations and independent
standard DOS MZ serialization of the original 130,882-byte Japanese
MAIN.EXE remain unchanged.

Native proof:
`.analysis/work/exatt-layout-af649b/report.json`,
SHA-256 `9064fefe7a61ade2605a155bffc5b3670a5e45d8d6eb2c1691e7f52a23fe0e4d`.
Actual per-round modified source and shared entity-header OMF dependency
records, compiler/linker logs, binary outputs and response files
are retained. Only this complete four-function physical producer
was rebuilt, with the remaining original project objects reused.

This establishes accurate source-visible behavior and full
compiler-exact codegen for already owned bytes. It does not
establish original historical vendor packet-byte identity,
new canonical packed-file Factory credit or real PC-98 runtime proof.

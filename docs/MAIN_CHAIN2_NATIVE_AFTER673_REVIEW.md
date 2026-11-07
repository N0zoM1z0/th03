# TH03 Chain 2 background initializers and both large native renderers (after673)

The original physical `chain2` object owns three complete native
functions: its 50-particle initializer and two substantial
accelerating/periodic background particle draw/update controllers.
The original object is `obj/chain2.obj`, and its historical
module in the complete MAIN MAP is
`src/main/background/chain2.cpp`, both verified through the
source-rooted v2 compiler/linker and independent read-only review.

The maintained initializer now uses the meaningful original
subpixel-scale C++ for its two RNG coordinates:

    particle->x = irand() % TO_SP(640);
    particle->y = irand() % TO_SP(400);

Both original Turbo C++ 4.02 rounds compile the code to exactly the
same original instructions, preserving RNG order and full signed
16-bit remainder semantics (`af673c`). Compiler-time constants
explicitly identify the 50 visible 16-byte particle slots, the first
40 randomized sprite/velocity slots, initial angle 64 and
original initial velocities and speed (`af673b`).

The historical initializer has two separate sprite-assignment
branches for particle indices 0..39 and 40..49. A semantically
equal ternary instead emitted different original CODE (`af673a`),
and was rejected. Similarly, the large accelerating controller's
`round_frame > 144UL` cannot be rewritten as
`round_frame >= 145UL` without changing original native code
(`af673d`). Both original source forms are intentionally retained,
rather than silently considering identical numerical values proof
of original TC4 lowering.

Both original TC4.02/TLINK rounds used the **current physical
source** and **current shared phase.inl**, with actual OMF COMENT
dependency checks and no stale TH03WORK include. The period
transition logic remains precisely as restored in after672, with its
original unsigned %4096/%8/%4 clocks and original uninitialized
`changed` path; none was adjusted by the Chain 2 refactor.

Final full physical object native proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af673e --units chain2
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af673e

Both rounds reproduce **all 550 original CODE bytes, 43 literal
ordered FIXUPP fields, three PUBLIC offsets** and complete OMF
segment definitions, plus the full linked normal MAIN
EXE/MAP, original Japanese loaded program, all 1,553 literal
MZ relocations and independently serialized exact
130,882-byte Japanese MAIN.EXE.

Preserved native proof:
`.analysis/work/exatt-layout-af673e/report.json`,
SHA-256 `3457c4b88a2b82d82623f00086e6b3bc77955fd35e3c057805626ca1e2429871`.
Only this affected original TU was rebuilt twice; 98 other
project objects and startup/CRT were reused, not cold replayed.
Original CODE bytes were already tracked; this is not new
canonical Factory packed-game byte credit, historic raw
vendor OMF packet equality or real PC-98 runtime proof.

# TH03 Chain 1 background: original native C++ and real linker ownership (after671)

The original Chain 1 background `chain1` object has **695 CODE
bytes, 43 ordered native FIXUPP fields and six PUBLIC offsets**.
This complete six-function physical producer includes initialization
of particle positions, sprite choice and velocity, a near
screen-pixel helper, the near position-wrapping helper and
two large acceleration/periodic background state-machine
functions. The shared background array uses 16-byte records.

The previous scoped script assumed that all physical originals
were stored in `obj/th03`. The actual original 99-object
TLINK response uses `obj/chain1.obj` and `obj/chain2.obj`
instead. The source-rooted v2 compiler and independent reviewer
now read those exact original objects, retain the original
`src/main/background/chain1.cpp`/chain2 MAP module names,
and bind the full maintained `src/main/background/phase.inl`
periodic code **from the current source** (rather than a stale
TH03WORK include).

The compiler OMF COMENT dependency records must attest BOTH
the changed Chain source and the staged phase include in each
independent native round. The reviewer additionally compares
the complete staged phase header bytes and source/report SHA.
Failed `af671a`/ `af671b` attempts, which discovered
original physical path versus DOS TLINK path differences,
were not misreported as source mismatches and remain retained.

Meaningful natural C++ change in Chain 1's real initializer:
the original sprite-choice `irand() & 1` now uses
`static_cast<unsigned int>(irand()) % 2 != 0`.
This preserves the original single random draw, byte
selection and machine code, proved in `af671d`.
The 48 physically initialized particles, angle 64, Y
velocity 16 and initial speed 32 have compiler-time
names rather than extra runtime state (`af671e`).
The real register/ES:DI drawing and position-wrapping
hardware helper contracts are retained; no unsafe
rewrite of DS/ES setup or intentionally indeterminate
periodic local state is claimed.

Final complete modified-source original native proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af671f --units chain1
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af671f

Both actual Turbo C++ 4.02/TLINK rounds reproduce all
**695 original CODE bytes, 43 literal ordered FIXUPP
fields, six PUBLIC offsets and original segment metadata**,
the full normal MAIN EXE and path-normalized MAP, Japanese
loaded program and all 1,553 ordered MZ relocations,
plus independently serialized exact original
130,882-byte Japanese MAIN.EXE.

Retained source, writer and binary evidence:
`.analysis/work/exatt-layout-af671f/report.json`,
SHA-256 `0ea22b6e9f6a95bfde390e4035110ea79502be6b51a7f59e5406eeafd044ddd5`.
Only this one complete physical producer was rebuilt in
two rounds. Other 98 original project objects and CRT
inputs were reused without a full project cold replay.

This improves maintainable natural source over previously
tracked original CODE, not new canonical Factory
packed-game byte credit, historical vendor raw OMF
packet identity or PC-98 runtime proof.

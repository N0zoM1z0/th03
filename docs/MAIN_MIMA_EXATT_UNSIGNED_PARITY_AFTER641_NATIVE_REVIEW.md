# Mima Extra Attack: signed-duration parity and full bounce state machine (after641)

The maintained `exatt_mima.cpp` is one complete original 727-CODE-byte
physical Turbo C++ producer. Its six player slots participate in flight,
rebound, speed-up, hitbox collision, collmap writes and a phase-driven
renderer. The central `exatt_update_mima` is a substantial gameplay
function, not just a single helper expression.

The historical acceleration path uses `duration & 1` from a **signed
16-bit `int` local**. Replacing that with `duration % 2` changed the
compiler output (`af641a`) because signed remainder has a different
codegen/negative-operand contract. The following truly natural, typed
C++ expression compiles to the original bit-extraction instruction:

    p->speed += (static_cast<unsigned int>(duration) % 2);

This correctly identifies the original unsigned-bit parity semantics
without assuming the entire duration field is declared unsigned or
changing its other comparisons. Two native rounds `af641b`
proved that one change in isolation.

The complete maintained code now also names the six physical slots,
the original flight/appearance state, the frame 0x10 start of speed
acceleration, the 0x20 parity-phase end and the 0x50 final speed
adjustment threshold. The existing X-before-Y boundary handling,
signed velocity negation and zero-frame expiration retain their
original paths. No newly initialized DATA/BSS or defensive behavior
was added.

Final source/header OMF-COMENT-attested dual 16-bit Turbo C++ 4.02
compiler/TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af641c --units ex_mima
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af641c

Both native rounds match the complete **727 original CODE bytes,
44 literal ordered FIXUPP fields, four PUBLIC offsets**, all OMF
segment definitions, full original normal MAIN EXE and normalized
MAP. The Japanese program image, its 1,553 ordered MZ relocations
and the separately serialized original 130,882-byte Japanese MAIN.EXE
remain identical.

Retained native proof:
`.analysis/work/exatt-layout-af641c/report.json`,
SHA-256 `09daf97435306af1561f2f4e20075ec49b02fe85e3d84d7a06c43de51b63258c`.
The rejected `af641a` signed-remainder candidate is kept in
ignored work; the accepted current source was compiled rather
than replaced by an old TH03WORK source snapshot.

This recovers accurate natural C++ behavior over already owned CODE.
Historic Borland raw OMF packet identity, original packed-game
provenance, canonical Factory credit and PC-98 runtime execution
are different unproven requirements.

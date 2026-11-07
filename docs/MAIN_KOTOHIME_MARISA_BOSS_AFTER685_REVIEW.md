# Kotohime and Marisa complete BOSS: original-native C++ angular geometry (after685)

The full original Kotohime BOSS owns eleven complete functions:
the large mode dispatcher, four distinct attack families,
ring and radial burst emission, sprite rendering and template
initialization. The complete Kotohime object contributes
1,840 CODE bytes, 262 ordered native FIXUPPs and eleven PUBLICs.
Marisa's complete BOSS contributes another 1,431 CODE
bytes, 199 native fixups and nine PUBLICs, including its
substantial attack dispatcher and its animated sprite renderer.

In **four independently compiled locations** of Kotohime's
ring emitter, nested radial burst and rotating ring renderer,
the original authored left shifts:
    (i << 8) / count
    (center_i << 8) / kotohime_orbit_count
    (bullet_i << 7) / kotohime_burst_count

now use natural C++:
    (i * 256) / count
    (center_i * 256) / kotohime_orbit_count
    (bullet_i * 128) / kotohime_burst_count

The actual 16-bit multiplication precedes integer division,
preserving the original type, wrap and integer rounding.
Changed-source OMF-attested original Turbo C++ 4.02
native control `af685a` proves the whole original
Kotohime object and its full MAIN link are byte-equal.
Original AL-mediated +2 and -4 updates, already proven
native-unequal when directly abbreviated, remain unchanged.

In Marisa's full BOSS sprite renderer, the four-frame
flicker test `(round_or_result_frame & 3) < 2` now
uses natural `(round_or_result_frame % 4) < 2`.
The original global frame is an unsigned 16-bit input,
so the real TC4 compiler lowers this exact branch to
the original masked instruction sequence. The independent
two-round `af685b` native control proved full
Marisa BOSS original equality.

Final simultaneous physical source/OMF-dependency-attested
original compiler/full normal MAIN TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af685c --units ba_koto,ba_maris
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af685c

Both independent full original TC4/TLINK rounds match **all
3,271 original CODE bytes, 461 literal ordered native
FIXUPP fields, twenty PUBLIC offsets**, OMF segments,
the original normal full MAIN EXE and path-normalized MAP,
the Japanese loaded program and its 1,553 ordered
MZ relocations. Independently serialized exact original
130,882-byte Japanese MAIN.EXE also agrees.

Native writer/OMF proof:
`.analysis/work/exatt-layout-af685c/report.json`,
SHA-256 `b976dcee4766f102b1979fead71ab81b294c8634a45980d175310ce7dcffdde1`.
Both modified source and packed BOSS template headers
were explicitly bound and emitted as OMF COMENT source
dependencies in two compiler rounds. Only the two
affected original complete BOSS TUs were rebuilt;
other 97 original objects and startup/CRT libraries
were reused with no whole cold replay.

These are natural maintained C++ changes in previously
tracked original CODE bytes. They do not add canonical
Factory packed-game byte credit, prove historical
raw vendor OMF packet-byte equality or actual PC-98
hardware runtime correctness.

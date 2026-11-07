# Ellen complete BOSS: original-native signed Extra volley and C++ attack timing (after678)

The real complete original Ellen major BOSS object contains nine
functions, including a substantial multi-branch spread state machine,
two full Extra Attack burst emission loops, timed pellet patterns
and two animated sprite renderers. The physical unit contains
**1,675 CODE bytes, 213 literal ordered FIXUPP fields and
nine PUBLIC offsets**.

Actual original Turbo C++ 4.02 codegen was tested for the
entire changed source, not one extracted leaf. The two
`boss_frame & 1` gates in `ellen_pattern_spread` now
express real unsigned timer parity as `boss_frame % 2`,
preserving the original BOSS firing and jump paths
(`af678a`). The original `goto fire_single`/`done`
state control is kept; branch or cadence equivalence
alone does not prove identical original machine bytes.

In the full Extra Attack emitter, the last volley
argument formerly spelled as byte `0xFE` now reads
naturally as **signed `-2`**, with the identical
underlying unsigned-byte Pascal argument and same
native caller instructions (`af678e`). The RNG call,
radial angular increment and original volley timing
remain exactly positioned.

The eight-shot spread emission and full intro renderer
now use standard preincrement `++i` / `++j` loops.
The original register and CODE payload match in
two native controls `af678c` and `af678d`.
A proposed collapse of four separate `i--;`
followed by `if(i<0)` checks into `if(--i<0)`
instead changed native TC4 CODE (`af678b`).
This negative codegen result was rejected; all four
original decrement/test sequences were restored.

Final original-current-source OMF-dependency-attested
two-round original TC4/TLINK proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af678f --units ba_ellen
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af678f

Both compiler rounds reproduce **all 1,675 original CODE
bytes, 213 ordered native fixups, nine original PUBLICs**,
OMF segments, the complete normal MAIN executable and
path-normalized MAP, the exact Japanese loaded program
and all 1,553 ordered MZ relocations. Independently
serialized complete 130,882-byte original Japanese
MAIN.EXE also matches both rounds.

Native proof: `.analysis/work/exatt-layout-af678f/report.json`,
SHA-256 `c77181f5a3dbeb630575c269d81bfc7c4dbcad73e3e13cf65b187cfe973c50bb`.
Actual modified source and packed BOSS state header are
attested by real emitted OMF COMENT dependencies. Only this
affected original physical object was recompiled twice;
all 98 other original project objects and startup/CRT
inputs were reused, with no full cold replay.

These original CODE bytes were already tracked; the
recovery improves exact maintained C++ and does **not**
add canonical Factory packed-game acceptance bytes,
prove historic vendor raw OMF packet-byte identity,
or certify real PC-98 runtime behavior.

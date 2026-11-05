# Original six streambuf/istream/ostream operations, complete native source

Six original Japanese Borland CL.LIB members are recovered as full 16-bit
symbolic 8086 source, not wrappers or binary target-code arrays. They retain
the original far C++ calling conventions, original streambuf/ios members,
get/put area cursor and position calculation, output-stream tie management,
whitespace mode flags, and the original failure/EOF handling.

| Original CL.LIB slot | CODE | Exported original C++ method |
| --- | ---: | --- |
| `stbsgetn` (866) | 117 | `@streambuf@sgetn$qnci` — bulk buffer get |
| `stbsputn` (869) | 113 | `@streambuf@sputn$qnxci` — bulk buffer put |
| `isttellg` (787) | 120 | `@istream@tellg$qv` — input position and state |
| `osttellp` (822) | 123 | `@ostream@tellp$qv` — output position and state |
| `sttie` (887) | 104 | `@ios@tie$qn7ostream` — flush/tie association |
| `istws` (697) | 96 | `@ws$qm7istream` — skip whitespace with mode setup |

Every original CODE byte, `_TEXTA`/DATA/BSS segment geometry, one original
far public per member, and imported far function interface matches the
actual Japanese CL.LIB. Together the six members cover **673 CODE bytes**,
zero DATA/BSS and **eight original OMF imported far-call fixups**. Five have
one FIXUPP each. `istws` uses three original references at CODE+77,+59,+45,
which require descending source emission at genuine instruction boundaries
to reproduce the **original literal FIXUPP order**. All eight relocation
fields match literally in site, width, frame, target and addend; the whole
original Borland OMF record-program serialization remains distinct from
TASM metadata, so no whole-OBJ record equality is claimed.

`scripts/build_th03_mainl_after362_work.py streambuf-io-leaves` extends the
SHA-bound **421-member** parent (including full diagnostic `checks` boss),
rebuilds only these six changed original members, then reconstructs the
original 893-slot CRT library and native Japanese MAINL link in **two
independent TASM/TLIB/TLINK rounds**. Both rounds reproduce the complete
original **67,372-byte Japanese EXE and MAP byte-for-byte**, including all
**677 original ordered DOS MZ relocations**. The working CRT reaches **427
source-backed original-equal members**, **466 unchanged contextual original
members**, and **136,181 source-compiled original-equal CODE bytes** (+673).
Every raw original and source-produced OBJ/LIB/EXE/MAP vector, writer logs,
source hashes and parent receipt bindings are retained under
`.analysis/work/after362-*`, with scope reviewer and independent tests in
`scripts/review_th03_mainl_after362_work.py` and
`tests/test_mainl_after362_work.py`.

This is working CRT source proof, not a formal Factory accepted decoded
extent, packed-product credit or whole-game source-exactness claim.
No full cold replay was performed.

# Native overlay source binding correction (after615)

The earlier after598–610 compiler overlays used a copied source in
`probe/afNNN/rX/src/...`, but their compiler wrappers retained a literal
`#include "src/..."`. Turbo C++ resolved that source under the main
TH03WORK tree instead. The old receipt's source SHA and OBJ equality did
**not** demonstrate that the edited source was compiled. This was detected
by a field-name typo in `src/main/enemy/expl.cpp`: the old probe reported
success despite a nonexistent `chains.hitsue` field. It is a confirmed
source-binding false positive, not a theoretical possibility.

The corrected v2 probe now rewrites the actual compiler wrapper to include
`probe/<stage>/rN/src/...` explicitly. When the source includes the shared
Extra Attack entity header, its include is also explicitly rewritten to the
per-round header. The original source and wrapper in the checkout are not
overwritten. The *emitted OMF COMENT dependencies* must name the forced
source and, if applicable, the forced header. These constraints are checked
during the native compile **and** by the read-only reviewer, which rejects
v1 receipts rather than certifying them retrospectively. It compares the
complete original CODE/DATA initializer payloads, literal ordered FIXUPPs,
PUBLIC offsets and segment definitions, full MAIN EXE/MAP and 1,553 ordered
MZ relocations, and separate complete original MZ serialization.

A negative proof with the deliberate `chains.hitsue` typo, `af611a`,
produced the original compiler error on the **forced** source file. The
corrected spelling compiled in `af611b` but failed exactness on 634 vs
630 CODE bytes; independent source changes must therefore be probed. A
control rebuild of unmodified explosion source, `af611c`, generated exact
630 CODE bytes in both rounds. No target-byte patching or full cold replay
was used to obtain these results.

The obsolete source claims in the after598–610 review docs are retained as
historical records but cannot be cited as current native proofs. In
particular, the old Bullet `_DX=0` and `_BX=0` forms produced 33 D2 and
33 DB where original instructions encode 31 D2 and 31 DB. The suggested
`_AX <<= 1` emitted ADD AX,AX (03 C0) in place of SHL AX,1 (D1 E0).
The corrected Bullet source retains the necessary inline assembly and its
v2 proof is `af612d`.

Extra Attack shared `exatt_entity_t` originally used one-byte fields and
a 32-byte stride. Adding nested unions under `#pragma option -a2`
introduced non-original padding. A local `-a1` struct definition,
restoring `-a2` afterward, is required for correct original offsets.
The large Chiyuri Extra Attack compiler TU also needs its original
assembly jump and beam phase sequence (natural alternatives were only
successful in the v1 false-positive probe). The corrected full family
v2 receipt is `af614a`: 10 original TUs, 8,781 CODE bytes, 563 fixup
fields, 52 PUBLIC symbols, exact full normal MAIN link and original file
in both rounds, with verified OMF dependency paths.

This is a correction to evidence provenance; it does not establish
original Borland vendor OBJ packet-byte identity, device behavior, or
canonical packed-file Factory credit.

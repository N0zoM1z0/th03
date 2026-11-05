# Two complete Borland string insertion/replacement bosses and exception runtime

The recovered original Japanese CRT `insert1` boss was used as a **layout
comparison**, not as a blind proof that the related C++ overloads were
identical. The actual original `CL.LIB` members were independently parsed
and disassembled for each distinct path:

| Original member | Export | `_TEXT` CODE | `_TEXTC` CODE | DATA | Relocation fields |
| --- | --- | ---: | ---: | ---: | ---: |
| 408: `insert2` | `@string@insert$quimx6stringuiui` | 365 B | 671 B | 30 B | 43 |
| 422: `replace` | `@string@replace$quiuimx6stringuiui` | 365 B | 711 B | 30 B | 43 |

Each has one extra zero-sized BSS section, the original group bytes
`0aff02ff03`, one far method public at `_TEXTC+0`, twelve far
imports and the entire 365-byte exception helper/descriptor section
of the original. Both objects include the original null-terminated
`String reference out of range` message in initialized DATA and the
typed class hierarchy for `xmsg`, `string`, lengtherror, xalloc and
outofrange, including original Borland alignment.

## Distinct control flow reconstructed, not assumed

The full `src/mainl/crt/insert2.asm` algorithm constrains the source
start against source length, then clips the count against the remaining
substring before invoking `TStringRef::splice`. Its additional 76
executable bytes over `insert1` are genuine control-flow, not NOP filler.

The full `src/mainl/crt/replace.asm` has the same bounded source-substring
logic with different far argument positions and independently clips the
**destination removal** count to the destination's remaining length. The
additional 40 bytes over the ranged insertion method are real comparison
and pointer-selection code. Both methods preserve the far Borland
exception-context setup, thrown out-of-range path, clone-on-write and
complete destructor/RTTI metadata.

For each member, independent TASM compilation produces exact original
CODE bytes in **both CODE segments**, the original 30 DATA bytes,
the original section/public/extern/group metadata and all **43 of 43**
original relocation fields **including site, kind, target, frame and
addend**. TASM and the original Borland compiler serialize their
FIXUPP records in a different literal order; consequently neither
original OMF program-record equality nor formal source acceptance is
claimed.

## Incremental native product validation

The bounded insertion was established first by
scripts/build_th03_mainl_after325_work.py (mode: string-insert-range),
which reached 330 source CRT member programs. Only then does
scripts/build_th03_mainl_after326_work.py (mode: string-replace-boss)
consume the unchanged 330-source parent and rebuild the entire replacement
method. **Two real native TASM/TLIB/TLINK rounds for each scoped step**
produce the original decoded Japanese MAINL EXE and MAP byte-for-byte,
including all 677 ordered MZ relocations, without replaying any older
full cold builds.

The final working CRT carries **331 source members**, **562 contextual
original vendor members** and **109,886 original-equal CRT CODE bytes**.
Both separate receipts check the original library object and source hashes,
relocations, saved OBJ/LIB/EXE/MAP bytes and native phase-log digests:
review_th03_mainl_after325_work.py plus tests.test_mainl_after325_work
for insertion, and review_th03_mainl_after326_work.py plus
tests.test_mainl_after326_work for replacement.

This is real source-bound reconstruction and linked-product parity,
not literal Borland OMF record equality, a Factory-accepted ownership
receipt or a whole-game exact-source claim.

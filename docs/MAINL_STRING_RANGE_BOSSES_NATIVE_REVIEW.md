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

Two successive incremental builds preserve the full source-bound receipt
DAG while compiling **only the newly selected members**, rather than
rerunning a cold replay:

1. `scripts/build_th03_mainl_after325_work.py string-insert-range` consumes
   the 329-source parent, rebuilds member 408, and links 330-source MAINL.
2. `scripts/build_th03_mainl_after326_work.py string-replace-boss` consumes
   that source-bound 330-member product, rebuilds member 422, and links
   331-source MAINL.

Each build performs **two independent** native TASM/TLIB/TLINK rounds,
reconstructing the original **Japanese decoded MAINL EXE and MAP
byte-for-byte**, including **677 ordered MZ relocations**. All previously
recovered members remain source-bound, and every other contextual CRT member
remains the original program.

The result is **331 native-source CRT members** out of 893, **562
contextual original vendor members** and **109,886 original-equal CRT
CODE bytes**. The round-by-round proof reads original library member
records and raw OBJ/LIB/EXE/MAP bytes, phase-log digests and source
hashes, using both `scripts/review_th03_mainl_after325_work.py` and
`scripts/review_th03_mainl_after326_work.py`, plus
`tests.test_mainl_after325_work` and `tests.test_mainl_after326_work`.

This is real working-source reconstruction and linked-product parity,
**not** a promoted Factory acceptance fact, a bit-identical original
Borland OMF record program or a complete original packed game.

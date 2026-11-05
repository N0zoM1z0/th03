# Five original native 8086 CRT leaves — source-bound Japanese MAINL

Five complete, separately authored real 8086 routines have been recovered
from the original Japanese Borland CRT objects, rather than inserted as opaque
CODE bytes or bypassed because they are short:

| Original library member | Full CODE | Original ABI and operation |
| --- | ---: | --- |
| `crotl` (13) | 15 bytes | `__crotl`: far char rotate-left with 16-bit count, clear AH |
| `crotr` (14) | 15 bytes | `__crotr`: far char rotate-right with 16-bit count, clear AH |
| `n_lxmul` (94) | 23 bytes | `N_LXMUL@`: near unsigned 32-bit multiply returning low DX:AX, with original short-circuit limbs |
| `n_scopy` (96) | 28 bytes | `N_SCOPY@`: near-call, callee-pop8 far-pointer block copy in CX bytes, preserving odd-length tail |
| `f_scopy` (52) | 28 bytes | `F_SCOPY@` and `SCOPY@`: far-call block-copy sibling with two original public aliases |

Each complete source resides at `src/mainl/crt/<member>.asm`. All five have
the original `_TEXT` CODE and zero-byte `_DATA` DATA segments, original
`DGROUP` definition (`06ff02`), complete original PUBDEF entries, no
imports and **zero logical relocation fields**. Native direct standalone
TASM builds reproduced every original CODE byte and the original member
segment/public group identities before construction of the carrier.

`scripts/build_th03_mainl_after324_work.py assembler-leaves` consumes the
complete, source/receipt-bound 324-member carrier. Two native TASM/TLIB/TLINK
producer rounds independently reconstruct the original complete Japanese
MAINL EXE and MAP (including **677** ordered DOS MZ relocations), with the
five members replaced by source objects and all previously recovered members
revalidated. The library now has **329/893** complete source members, **564**
unchanged contextual vendor members, and **107,774 original-equal CRT CODE
bytes**, an increase of **109**. The native OBJ/LIB/EXE/MAP rounds and writer
logs are retained under `.analysis/work/after324-*`, along with a SHA-bound
incremental receipt and `scripts/review_th03_mainl_after324_work.py`.

`tests/test_mainl_after324_work.py` separately verifies all five original
OBJs, both independently compiled full CODE payloads, the empty original and
new FIXUPP inventories, the complete original ABI and all source-bound link
outputs. Here literal FIXUPP equality means *both have no relocations*; it
does not imply byte-identical OMF record serialization. No new Factory
accepted extent or packed-file unit credit follows from this working-source
reconstruction. No full cold replay was run.

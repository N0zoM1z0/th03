# Ten original near/far Japanese MBCS compare, span-pointer and set routines

Ten previously unowned Japanese Borland CL.LIB members now have complete
symbolic 8086 source, including actual lead/trail byte handling, near/far
buffer access and original DBCS character classification at `__mbctype+1`.
These are complete independent programs, not exported forwarding stubs or
serialized target-CODE arrays.

| Original CL.LIB member | CODE | Original public API |
| --- | ---: | --- |
| `MBSNBCMP` (613) | 198 | `__mbsnbcmp` |
| `FMBSNBCM` (669) | 198 | `__fmbsnbcmp` |
| `MBSSPNP` (631) | 204 | `__mbsspnp` |
| `FMBSSPNP` (687) | 204 | `__fmbsspnp` |
| `MBSNSET` (625) | 178 | `__mbsnset` |
| `FMBSNSET` (681) | 178 | `__fmbsnset` |
| `MBCCMP` (581) | 151 | `__mbccmp` |
| `FMBCCMP` (654) | 151 | `__fmbccmp` |
| `MBSDEC` (605) | 132 | `__mbsdec` |
| `FMBSDEC` (661) | 132 | `__fmbsdec` |

The ten natural `.asm` files reproduce all **1,726 original CODE bytes**,
all original single far public entry names, no initialized DATA/BSS, each
original `_TEXT` segment and group `08ff02ff03`. Their total **20 original
OMF byte-table FIXUPP fields** match literally in site, group frame1, target
`__mbctype+1`, addend and original **descending record order**. The source
places genuine 8086 classification instructions at their original `ORG`
offsets without padding the code or modifying the produced binaries. The
full original Borland OBJ record metadata still differs from TASM's
serialization; full individual OBJ equality is not claimed.

`scripts/build_th03_mainl_after381_work.py japanese-mbcs-pointer-ops`
revalidates the entire **477-source** inherited Japanese CRT carrier and
replaces these ten full original members in a newly built **893-position
CL.LIB**, using two independent native TASM/TLIB/TLINK rounds. Both produce
the pinned **67,372-byte decoded Japanese MAINL EXE and full MAP**
byte-for-byte, including all **677 DOS MZ relocation entries in original
order**. The working CRT reaches **487 complete original-equal source
members**, **406 unchanged contextual original programs** and **154,282
original-equal logical CRT CODE bytes** (+1,726). Original/source OBJ/LIB/
EXE/MAP vectors, logs, parent/source/driver SHA hashes and independent OMF
review and tests are retained under `.analysis/work/after381-*`,
`scripts/review_th03_mainl_after381_work.py` and
`tests/test_mainl_after381_work.py`.

This is scoped working-source evidence, not new Factory-accepted decoded
ownership, packed-game unit credit or whole-game source completeness.
No full native cold replay was run.

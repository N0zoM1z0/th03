# Ten complete original Japanese MBCS character classification/conversion leaves

This source-bound increment reconstructs **ten actual 16-bit original Borland
CRT programs** rather than treating them as self-evident tiny stubs. Each
`src/mainl/crt/<member>.asm` preserves the original far calling convention,
character width, masking, named `__ctype` or `__mbctype` import, segment and
original bit-test behavior, including the original unchecked cases.

| Original CL.LIB member | CODE | Complete original exported far routine |
| --- | ---: | --- |
| `MBISALP` (586) | 32 | `__ismbcalpha` |
| `MBISDGT` (587) | 32 | `__ismbcdigit` |
| `MBISLWR` (594) | 32 | `__ismbclower` |
| `MBISSPC` (596) | 32 | `__ismbcspace` |
| `MBISUPR` (598) | 32 | `__ismbcupper` |
| `MBISL0` (590) | 44 | `__ismbcl0` — first original lead-byte class |
| `MBISL1` (591) | 44 | `__ismbcl1` — second original lead-byte class |
| `MBISLGL` (593) | 49 | `__ismbclegal` — original two-byte lead/trail test |
| `MBTOLWR` (637) | 29 | `__mbctolower` |
| `MBTOUPR` (639) | 29 | `__mbctoupper` |

Each complete original source-built CODE payload and original public/extern,
zero DATA/BSS, segment and DGROUP identities match the pinned Japanese
CL.LIB member. The ten members contain **11 original byte-table relocations
in total**, all group-framed to the original `__ctype+1` or `__mbctype+1`.
`MBISLGL` has two real fields at CODE+33 and CODE+20. A simple forward
assembly initially wrote these fields in ascending order; reordering the
two real instruction blocks at their original offsets using `ORG 31` and
`ORG 0` retains every opcode and logical reference while restoring their
**original ordered FIXUPP list `[33,20]`**, with no target-byte arrays or
binary/object patches. Both native rounds now have **literal complete
original FIXUPP fields and order** for all ten members. The full original
Borland OMF record serializations remain different from native TASM
non-semantic record metadata.

`scripts/build_th03_mainl_after346_work.py mbcs-classification-leaves`
revalidates the complete previous source-bound **379-member** carrier,
reassembles these ten members and reconstructs the full original 893-slot
CRT library with native TASM/TLIB/TLINK **twice**. Both rounds reproduce
the complete original Japanese decoded MAINL **67,372-byte EXE and MAP**,
including all **677 DOS MZ relocations in original order**. The current
working source-backed CRT reaches **389 original-equal members**, with
**504 unchanged contextual vendor members**, and **125,396 original-equal
CODE bytes** (an increase of **355**). Both full raw native OBJ/LIB/EXE/MAP
rounds, source/parent/driver hashes and writer logs remain retained under
`.analysis/work/after346-*`. Tests and scoped reviewer are
`tests.test_mainl_after346_work` and
`scripts/review_th03_mainl_after346_work.py`.

No full cold replay, whole-game source ownership, packed-unit credit or
new formal Factory acceptance is claimed.

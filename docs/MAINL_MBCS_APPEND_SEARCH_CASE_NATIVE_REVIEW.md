# Eight complete Japanese MBCS append, search, and case-conversion members

Eight original Japanese near/far Borland CL.LIB routines now have complete
symbolic 8086 implementations: multibyte append (`MBSNCAT`, `FMBSNCAT`),
byte-counted append (`MBSNBCAT`, `FMBSNBCA`), substring search (`MBSSTR`,
`FMBSSTR`) and far-pointer lowercase/uppercase (`FMBSLWR`, `FMBSUPR`). Each
uses its real original near/far segmented pointer ABI, Japanese DBCS
lead/trail classification, original character table and conditional loops,
not a forwarding wrapper or executable machine-code byte array.

| Original CL.LIB member | CODE | Original far public |
| --- | ---: | --- |
| `MBSNCAT` (618) | 187 | `__mbsncat` |
| `FMBSNCAT` (674) | 187 | `__fmbsncat` |
| `MBSNBCAT` (612) | 224 | `__mbsnbcat` |
| `FMBSNBCA` (668) | 224 | `__fmbsnbcat` |
| `MBSSTR` (632) | 199 | `__mbsstr` |
| `FMBSSTR` (688) | 199 | `__fmbsstr` |
| `FMBSLWR` (667) | 106 | `__fmbslwr` |
| `FMBSUPR` (690) | 106 | `__fmbsupr` |

All **1,432 original CODE bytes** and all **18 original FIXUPP fields**
match their actual pinned Japanese Borland members, including original
literal record order, site, frame, target, width and addend. The source
correctly distinguishes `__mbctype+1`/`__ctype+1` byte-table accesses from
the *real far calls* to `__mbsbtype`, `__fmbsbtype`, `_strlen` or `__fstrlen`.
All publics/imports, segment geometry, group `08ff02ff03`, and zero DATA/BSS
are original-equal. The full original Borland OBJ serialization remains
different in ancillary metadata, so byte-for-byte individual OBJ records
are not claimed identical. All executable instructions are natural 8086,
without binary target-code arrays, synthetic executable padding or patched
link products.

`scripts/build_th03_mainl_after387_work.py japanese-mbcs-append-search-case`
validates the **502-source** parent, reassembles only these eight complete
members, and rebuilds all original **893 CL.LIB positions** with native
TASM/TLIB/TLINK in **two independent rounds**. Both reproduce the pinned
**67,372-byte Japanese decoded MAINL EXE and full MAP byte-for-byte**,
including all **677 DOS MZ relocations in original order**. Source-backed
CRT now includes **510 complete members**, **383 unchanged contextual
original programs** and **158,551 source-compiled original-equal logical
CODE bytes**, an increase of 1,432. Entire original/source OBJ/LIB/EXE/MAP
pairs, writer logs, SHA-bound driver/source/parent receipts, scoped reviewer
and independent OMF/MZ tests are retained in `.analysis/work/after387-*`,
`scripts/review_th03_mainl_after387_work.py` and
`tests/test_mainl_after387_work.py`.

This is working CRT source evidence, not a new formal Factory accepted
source extent or canonical packed-file unit. No full cold replay ran.

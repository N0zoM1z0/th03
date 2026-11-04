# TH03 Japanese Borland CRT: C++ cast and sixteen complete DOS utilities

Sixteen genuinely selected original CRT programs now have complete symbolic
8086 sources in `src/mainl/crt/`, rather than wrappers, copied machine-code
byte arrays, artificial padding or altered generated objects:

| Original slot | Member | Original CODE | Native operation |
| ---: | --- | ---: | --- |
| 199 | `castmptr` | 182 | Full C++ far memory pointer cast/adjustment |
| 815 | `ostmanip` | 27 | `ostream` manipulator insertion |
| 782 | `istmanip` | 27 | `istream` manipulator extraction |
| 114 | `setdta` | 18 | DOS DTA set |
| 491 | `dosvsist` | 17 | DOS/V status update |
| 108 | `rotr` | 17 | 16-bit rotate right |
| 107 | `rotl` | 17 | 16-bit rotate left |
| 20 | `divt` | 16 | 16-bit division helper |
| 486 | `dosvgkid` | 14 | DOS/V keyboard ID |
| 485 | `dosvgist` | 14 | DOS/V input status |
| 59 | `getdta` | 13 | DOS DTA get |
| 487 | `dosvisck` | 12 | DOS/V shift check |
| 867 | `stbskoff` | 11 | `streambuf::seekoff` |
| 62 | `getpsp` | 11 | DOS PSP query |
| 489 | `dosvison` | 10 | DOS/V IAS shift on |
| 488 | `dosvisof` | 10 | DOS/V IAS shift off |

`castmptr` reconstructs a genuine **182-byte Borland C++ algorithm**, with
real pointer segment/arithmetic/conditional branches. The three `ostream`,
`istream`, and `streambuf` members preserve their original `_TEXTA` segment
and C++ far ABI; their original DGROUP group order is not replaced with the
near DOS members' ordering. The actual `ostmanip` and `istmanip` call through
stack-resident **far function pointers**; TASM needs explicit `call dword ptr
[bp+0Ah]` to generate original `FF 5E 0A` instead of a near `FF 56 0A`.

Every selected member assembles with native TASM 5.0 `/m /mx /kh32768 /t`
producing **all 416 original CODE bytes**, original public symbols and
per-member segment/group structure, with genuinely empty initialized DATA,
BSS, EXTDEF and **literal original empty FIXUPP inventories**. This is
raw native payload and field evidence, not a claim of identical unexamined
OMF record classes.

`build_th03_mainl_after283_work.py cpp-dos-utility-leaves` inherits the
source-bound original Japanese **283-source CRT**, rebuilding only 16 selected
original slots in **two independent normal TASM/TLIB/TLINK rounds**. Both
reproduce the complete original **67,372-byte decoded Japanese MAINL EXE
and MAP byte-for-byte**, preserving all **677 ordered MZ relocations**, with
**594 original contextual vendor member programs unchanged**. Working CRT
reaches **299 source-built members and 99,132 original-equal CODE bytes**.
No formal accepted-ledger credit is claimed; no cold replay was run.

Proofs: `review_th03_mainl_after283_work.py cpp-dos-utility-leaves`,
`tests.test_mainl_after283_work`, full source-hash-bound native OBJ/LIB/EXE/MAP
pair and actual TASM/TLIB/TLINK writer logs under `.analysis/work/after283-*`.

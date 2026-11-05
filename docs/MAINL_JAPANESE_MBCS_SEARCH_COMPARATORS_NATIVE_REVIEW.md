# Ten complete near/far Japanese MBCS string search and comparison routines

These ten original Japanese Borland CL.LIB members are reconstructed as
natural 16-bit 8086 source, including complete comparison, character-set
search, reverse search and bounded case-insensitive comparison logic.
Each near/far version retains its own original control flow, return ABI,
segmented pointers and true `__ctype+1` / `__mbctype+1` byte-table tests.
This is not a set of imported function stubs or embedded target machine code.

| Original member | CODE | Full original far public |
| --- | ---: | --- |
| `MBSCMP` (603) | 168 | `__mbscmp` |
| `FMBSCMP` (659) | 168 | `__fmbscmp` |
| `MBSPBRK` (626) | 195 | `__mbspbrk` |
| `FMBSPBRK` (682) | 195 | `__fmbspbrk` |
| `MBSRCHR` (627) | 162 | `__mbsrchr` |
| `FMBSRCHR` (683) | 162 | `__fmbsrchr` |
| `MBSNBICM` (616) | 228 | `__mbsnbicmp` |
| `FMBSNBIC` (672) | 228 | `__fmbsnbicmp` |
| `MBSNICMP` (623) | 210 | `__mbsnicmp` |
| `FMBSNICM` (679) | 210 | `__fmbsnicmp` |

All ten complete source-compiled CODE images reproduce the **1,926 original
CODE bytes** from actual pinned CL.LIB members. Every original public,
extern and segment/class/DGROUP ABI matches, along with **26 literal
original FIXUPPs**, including their original descending Borland record
order, width, frame, site and addend. The near/far source uses native
symbolic statements at their genuine instruction offsets, including the
two-byte table tests; it does not patch any output or encode executable
machine bytes as data. Full original Borland OMF record serialization still
differs in other metadata and is not claimed equal.

`scripts/build_th03_mainl_after375_work.py japanese-mbcs-search-comparators`
consumes the verified **460-member source CRT** and rebuilds all ten whole
new original members, then the full original **893-slot CL.LIB library**
and decoded MAINL native link in **two independent TASM/TLIB/TLINK rounds**.
Both reproduce the pinned original **67,372-byte Japanese EXE and complete
MAP byte-for-byte**, including all **677 ordered DOS MZ relocations**.
The working CRT reaches **470 complete original-equal source-backed
members**, **423 original contextual vendor members**, and **148,020
original-equal source CODE bytes** (+1,926). Raw original and produced
OBJ/LIB/EXE/MAP, writer logs, source/parent/driver SHA receipts and
independent reviewer/test are under `.analysis/work/after375-*`,
`scripts/review_th03_mainl_after375_work.py` and
`tests/test_mainl_after375_work.py`.

No full cold replay, new Factory-accepted decoded extent, canonical
packed-game credit or complete source-owned game is claimed.

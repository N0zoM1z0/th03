# First 500 complete original CRT members: eleven MBCS count/navigation leaves

The Japanese Borland CL.LIB now has **500 original-equal source-compiled
members** in the scoped MAINL working CRT. This increment fully reconstructs
11 original near/far PC-98 multibyte count, length, next-character,
advance, second lead-byte category, and character-copy programs as real 8086
source (not empty APIs or target-code arrays):

| Original member | CODE | Public original function |
| --- | ---: | --- |
| `MBSNCCNT` (619) | 70 | `__mbsnccnt` |
| `FMBSNCCN` (675) | 70 | `__fmbsnccnt` |
| `MBSLEN` (610) | 57 | `__mbslen` |
| `FMBSLEN` (666) | 57 | `__fmbslen` |
| `MBISL2` (592) | 56 | `__ismbcl2` |
| `MBSNEXTC` (622) | 56 | `__mbsnextc` |
| `FMBSNEXT` (678) | 56 | `__fmbsnextc` |
| `MBSINC` (607) | 50 | `__mbsinc` |
| `FMBSINC` (663) | 50 | `__fmbsinc` |
| `MBCCPY` (582) | 49 | `__mbccpy` |
| `FMBCCPY` (655) | 49 | `__fmbccpy` |

These complete routines add **620 original CODE bytes**, have zero original
DATA/BSS, preserve their far entry ABI and group `08ff02ff03`, and reproduce
**all 11 original literal FIXUPP fields** for the byte-table references to
`__mbctype+1`. Each field matches the original site, frame1/DGROUP, target,
width and addend. The real 8086 instructions match the pinned Japanese
CL.LIB without binary patches, original executable byte arrays or
artificial initialized padding. The full original Borland OBJ record
serialization remains different in ancillary metadata, and is not claimed
identical.

`scripts/build_th03_mainl_after384_work.py japanese-mbcs-count-navigation`
revalidates the **489-member** source/receipt-bound parent, assembles the
11 selected original programs and reconstructs all **893 CRT library
slots** through two actual serialized TASM/TLIB/TLINK rounds. Both produce
the pinned original **67,372-byte decoded Japanese MAINL EXE and complete
MAP byte-for-byte**, with **677 ordered DOS MZ relocations**. The working
CRT reaches **500 original-equal complete source members**, **393
unchanged original contextual programs** and **155,800 original-equal
source CODE bytes** (+620). Original/source OBJ/LIB/EXE/MAP pairs, logs,
SHA receipts, reviewer and independent OMF/MZ tests are retained in
`.analysis/work/after384-*`,
`scripts/review_th03_mainl_after384_work.py` and
`tests/test_mainl_after384_work.py`.

This is a reproducible scoped working-source milestone, not formal Factory
accepted decoded-file ownership, complete CRT source coverage or the packed
whole-game exactness claim. No full cold replay was executed.

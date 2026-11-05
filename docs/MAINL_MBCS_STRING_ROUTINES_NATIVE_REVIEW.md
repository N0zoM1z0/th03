# Eight original near/far Japanese MBCS string routines: complete native source

These eight complete Borland Japanese CL.LIB members are now reconstructed
in real 8086 source: `src/mainl/crt/{MBSISLE,MBSISTR,FMBSISLE,FMBSISTR,
MBSNBCNT,FMBSNBCN,MBSLWR,MBSUPR}.asm`. They preserve character-table
bit tests, lead/trail byte detection, multibyte character counts and original
in-place case conversions. All original near/far pointer and return ABI,
branch behavior, indexed `__mbctype+1` / `__ctype+1`, zero DATA/BSS,
original segment geometry and original public symbol names are maintained.

| Original member | CODE | Original exported API |
| --- | ---: | --- |
| `MBSISLE` (608) | 83 | `__ismbslead` |
| `MBSISTR` (609) | 83 | `__ismbstrail` |
| `FMBSISLE` (664) | 83 | `__fismbslead` |
| `FMBSISTR` (665) | 83 | `__fismbstrail` |
| `MBSNBCNT` (614) | 89 | `__mbsnbcnt` |
| `FMBSNBCN` (670) | 89 | `__fmbsnbcnt` |
| `MBSLWR` (611) | 106 | `__mbslwr` |
| `MBSUPR` (634) | 106 | `__mbsupr` |

The **722 original CODE bytes**, eight complete far entries and **ten
original relocation fields** match the pinned Japanese CL.LIB members.
All are original DGROUP frame1 with addend +1, for the real original
character classification tables. `MBSLWR` and `MBSUPR` require two
relocations in the original descending order **CODE+66, +34**, while each
other member has a single original field. The source emits real 8086
instructions, with the later referenced instruction block first using its
actual original offset; TASM now reproduces the **literal OMF FIXUPP frames,
sites, targets, addends and original record order** without a machine-code
array or binary patch. The entire original Borland OBJ record program still
differs in nonsemantic metadata and is not claimed byte-identical.

`scripts/build_th03_mainl_after360_work.py mbcs-string-routines` extends
the source/receipt-verified **412-member** carrier, compiles these eight
complete functions and rebuilds all **893 original CRT library programs**
with native TASM/TLIB/TLINK in **two independent rounds**. Both reproduce
the complete original decoded **67,372-byte Japanese MAINL EXE and MAP**,
including all **677 ordered MZ relocations**. The working CRT now contains
**420 source-backed original-equal members** and **473 contextual original
programs**, totaling **133,800 original-equal CODE bytes** (+722).
All raw original and source-produced OBJ/LIB/EXE/MAP pairs, phase logs,
source hashes and parent receipt references are retained under
`.analysis/work/after360-*`, independently checked by
`scripts/review_th03_mainl_after360_work.py` and
`tests/test_mainl_after360_work.py`.

This working CRT evidence does not assert formal Factory acceptance,
canonical packed-unit credit or whole-game exactness. No full cold replay.

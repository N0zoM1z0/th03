# Japanese MAINL native CRT: five far string comparison/transformation modules

The retained original Japanese 893-member CRT's selected member program records
were independently checked before source reconstruction. Five previously
unowned **complete** modules have now been rebuilt from genuine 8086 symbolic
assembly at their original library positions:

| Original slot | Source module | Native CODE | Imports | Original ordered fixups |
| ---: | --- | ---: | --- | --- |
| 299 | `stricmp` | 65 | none | none |
| 305 | `strnicmp` | 68 | none | none |
| 303 | `strncmp` | 56 | none | none |
| 130 | `strcoll` | 29 | `_strcmp` | 1 literal field exact |
| 129 | `strxfrm` | 66 | `_memcpy`, `_strlen` | 2 logical fields; order differs |

All modules emit **all original CODE bytes**, the original CODE public names at
original offsets, complete ordered EXTDEF imports, correct zero DATA/BSS, and
literal original OMF DGROUP order. The three compare routines preserve
16-bit string and case conversion assembly including the original far source
and destination pointer/segment behavior. `strcoll` is the native far call
through the actual C-locale comparison service. Public `_strxfrm` here is
**not** the separate full `_strxfrm` internals member index192: it is Borland's
66-byte C-locale transform wrapper with original size/count behavior.

`strxfrm` reproduces both original far `_strlen` and `_memcpy` relocation
**sites, targets and frame methods** but its native TASM object enumerates them
in ascending CODE-offset order, unlike the original vendor object. Thus
*original literal FIXUPP record order* is not claimed. No binary patches,
embedded CODE bytes, compiler-substituted semantics, or artificial padding were
used to make the linked bytes agree.

Actual original-source proof: `scripts/build_th03_mainl_after77_work.py
strings`, `scripts/review_th03_mainl_after77_work.py strings`, and
`tests.test_mainl_after77_work`. Two independent TASM/TLIB/TLINK native rounds
preserve all 811 unchanged vendor CRT records and **completely reproduce** the
original 67,372-byte decoded Japanese MAINL EXE and original MAP, including
all 677 ordered MZ relocations. The working-source CRT now contains
**82 members, 34,058 original-equal CODE bytes**. This is a source-only
native proof, **not** formal published source acceptance; no full cold replay
was run. Retained raw proof outputs and writer logs reside under
`.analysis/work/after77-strings-*` with source-hash-bound receipts.

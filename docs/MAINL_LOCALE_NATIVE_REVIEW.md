# Original Japanese MAINL locale lifecycle, full four-segment CRT boss

The actual selected original Borland large-model CRT `locale` is **member 244**
of 893, with **950 CODE / 22 initialized DATA / zero BSS / 6 EXITDATA** bytes.
It exports three far entry points at the original offsets:

| CODE offset | Export | Recovered behavior |
| ---: | --- | --- |
| 0 | `___initialize_locale` | Allocate and initialize the active locale, with original C-locale fallback |
| 181 | `___uninitialize_locale` | Free the original locale-owned far objects and restore C-locale state |
| 300 | `___set_c_locale` | Initialize locale tables and copy or format the seven category selections |

`src/mainl/crt/locale.asm` contains the original real 8086 instruction
sequence with symbolic external C-locale tables, ctype maps, allocation and
free routines, 7-label category dispatch table and one real DATA format string
`%s;%s;%s;%s;%s;%s;%s;`. The `EXITDATA` record is a Borland priority
`db 1,14h` followed by a symbolic four-byte pointer to the original
uninitialization entry, not a hardcoded executable/relocation blob.

The source preserves the original twelve imports (`_sprintf`, `_calloc`,
`_free`, `_memcpy`, `_strcmp`, `_strxfrm`, `__ctype`, `_localeconv`, `__Clocale`,
`__pLocale`, `__lower`, `__upper`) and complete active far-pointer ownership.
A particular reverse-engineering trap: ordinary TASM rewrites calls to
intra-segment *far* locale functions into shorter `PUSH CS` + near `CALL`.
Two **zero-byte** `ASSUME CS:NOTHING` scopes instead retain the genuine
original five-byte immediate far-call form and the original CODE offsets.
Another TASM quirk is the `DGROUP` member encoding: the source uses the
TASM order `_BSS,_DATA` to emit the original literal `0aff02ff03` group.
No original CODE arrays, object patching or size-forcing padding are used.

The original selected member's complete native comparison validates:

- **950/950 CODE**, **22/22 DATA**, and **6/6 EXITDATA** original-equal bytes;
- all three original CODE exports, 12 ordered imports, original segment names,
  sizes, classes and group membership;
- all **113/113** original literal relocation *sites, kinds, targets and frame
  methods*, including 112 CODE fields and one EXITDATA callback pointer.

**Limit:** the original compiler records these FIXUPPs in a different OMF
record sequence than TASM, although their site-sorted frames and targets are
identical. The whole original OMF object record stream is **not** claimed
equal; byte-exact CODE/data and target-equal link are separate evidence.

`scripts/build_th03_mainl_after73_work.py vprinter-collate-strxfrm-locale`
rebuilds this full locale boss with the previous three source members on the
retained original Japanese 73-member native source carrier. Two independent
TASM/TLIB/TLINK rounds reproduce the entire **67,372-byte decoded original
Japanese MAINL EXE** and byte-for-byte original **MAP**, preserving **all
677 MZ relocations**. The active working CRT now has **77 source-built
members** with **33,774 original-equal CODE bytes**; the other **816**
original vendor program records remain unchanged. This is verified working
source, not new formal accepted-ledger credit or whole-source ownership.

Raw native OBJ/LIB/EXE/MAP rounds and writer logs remain under
`.analysis/work/after73-vprinter-collate-strxfrm-locale-*`, with a separate
source-bound build/review JSON receipt. Verify with
`review_th03_mainl_after73_work.py` and `tests.test_mainl_after73_work`.
There was **no full cold replay**; the retained original cold pair is reused.

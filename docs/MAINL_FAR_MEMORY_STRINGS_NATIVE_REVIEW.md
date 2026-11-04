# Original Japanese MAINL: nine complete far-memory/string CRT sources

Nine distinct selected original 893-member Borland CRT programs were recovered
as genuine symbolic 8086 source units. Each has original large-model far
pointer arguments, segment-register restoration, exact instruction/branch
forms and complete function extents; these are **not** merely equivalent C
implementations or native CODE byte arrays.

| Original slot | Complete module | Original CODE | Original public entry |
| ---: | --- | ---: | --- |
| 258 | `memccpy` | 57 | `_memccpy` |
| 433 | `fmemccpy` | 57 | `__fmemccpy` |
| 443 | `fstrcpy` | 41 | `__fstrcpy` |
| 451 | `fstrncpy` | 49 | `__fstrncpy` |
| 442 | `fstrcmp` | 48 | `__fstrcmp` |
| 450 | `fstrncmp` | 56 | `__fstrncmp` |
| 441 | `fstrchr` | 63 | `__fstrchr` |
| 438 | `fmemset` | 72 | `__fsetmem` at +0, `__fmemset` at +38 |
| 436 | `fmemcpy` | 36 | `__fmemcpy` |

These modules preserve native `LES`/`LDS`, `REPNE SCASB`, `REPE CMPSB`,
`REP MOVSW`/`MOVSB`, `REP STOSW`/`STOSB`, odd-byte handling, returns and
original far pointer result registers. `fstrchr` searches word-aligned far
strings; `fmemset` owns two native public functions and a real local near
call. TASM's default orientation of `xchg bx,cx` encoded an equivalent but
**non-original** ModRM in `fstrncpy`; spelling the operands `xchg cx,bx`
reproduces the original native opcode without patching target bytes.

Each selected CRT member independently assembles under TASM 5.0
`/m /mx /kh32768 /t` with **all original 479/479 CODE bytes**, the original
PUBLIC offsets, no imports, empty DATA/BSS, and the literal original
`08ff03ff02` DGROUP. All nine have *zero* genuine OMF FIXUPPs, and native
TASM preserves this complete empty field inventory without frame concerns.
All nine are distinct actual original library slots; the original far-pointer
ABI, not file naming or a guessed library stand-in, establishes identity.

`scripts/build_th03_mainl_after119_work.py far-memory-leaves` inherits the
source-hash-bound 119-member Japanese CRT, assembles these nine at their
original positions, and performs **two independent full normal TASM/TLIB/
TLINK rounds**. The complete **67,372-byte original decoded Japanese MAINL
EXE** and original MAP agree byte-for-byte in both rounds, including all
**677 ordered DOS MZ relocations**. The **765 untouched vendor member
program records** are preserved; working CRT now has **128 source-built
members and 58,639 original-equal CODE bytes**. No formal accepted-ledger
credit is claimed; no full cold replay ran.

Provenance and tests: `review_th03_mainl_after119_work.py far-memory-leaves`,
`tests.test_mainl_after119_work`, raw OBJ/LIB/EXE/MAP rounds and writer logs
under `.analysis/work/after119-far-memory-leaves-*`, and source-hash-bound
receipts `.analysis/work/mainl-after119-*`.

# Japanese MAINL original CRT `lstrftim`: 1,831-byte long date-format boss

The selected original Japanese Borland large-model CRT member is **slot 213**
`lstrftim`, not a TH04 substitute or guessed standalone object. It exports
`__lstrftime` at CODE+0 and `__getordinal` at CODE+1730 and imports, in
original order, `__UTOA`, `__tzname`, `_strcpy`, `_strlen`, `_strncpy`,
and `__pLocale`. Its complete native segments are **1,831 CODE**, **23
initialized DATA**, and zero BSS, with the original `08ff02ff03` DGROUP.

`src/mainl/crt/lstrftim.asm` reconstructs the full original long date/time
formatting dispatcher and ordinal formatter with real symbolic 8086
instructions and pointers, not original CODE byte arrays or binary patches.
The format dispatch uses a **85-word relocatable CODE table** at offset +1560,
with actual `dw case_...` references to original handlers. The far ordinal
formatter begins at +1730. DATA contains the literal strings `00`,
`%m/%d/%y`, `%H:%M:%S`, and `%`, with native offsets 0, 3, 12 and 21.
The source preserves the original stack/near/far ABI, 16-bit size behavior,
locale and timezone references, and 13 far internal calls to
`__getordinal`. Source-scoped **zero-byte** `ASSUME CS:NOTHING` keeps those
original far-call instructions from being rewritten as `PUSH CS` plus near
calls by TASM.

Full original native TASM `/m /mx /kh32768 /t` output comparison proves:

- **1,831/1,831 original CODE bytes** and **23/23 original DATA bytes**;
- original two public entry offsets and all six ordered EXTDEFs;
- **128/128 OMF fixup sites, widths, targets, addends and relocation modes**;
  **85** belong to the genuine symbolic CODE jump table.

A precise remaining **OMF metadata gap** is retained: the original vendor
object serializes FIXUPPs in another order, and the near external `__UTOA`
call at CODE+1377 uses original **TARGET frame5** whereas TASM uses
**CODE frame0**. The other 127 site-paired fields agree including frames.
`ASSUME CS:NOTHING` for this *near* call was explicitly tested and rejected:
TASM reports a near-call-to-different-CS error. A `near ptr` spelling gives
the same CODE-frame record; no patch, forced target bytes, or false original
OBJ assertion was used.

Native integration: `build_th03_mainl_after86_work.py lstrftim` inherits the
retained source-bound 86-member original Japanese native CRT and replaces
**only the real member 213**. Two independent TASM/TLIB/TLINK rounds preserve
all other native library programs and reproduce the **entire 67,372-byte
decoded Japanese MAINL EXE and original MAP byte-for-byte**, including all
**677 MZ relocations**. Working CRT now has **87 source-compiled members**,
**36,137 original-equal CODE bytes** and **806 unchanged contextual vendor
member programs**. This is source-only working evidence, **not** newly
accepted formal ledger credit or complete original OMF identity.

Receipts, raw native OBJ/LIB/EXE/MAP rounds and real writer phase logs are
retained under `.analysis/work/mainl-after86-lstrftim-*` and
`.analysis/work/after86-lstrftim-*`. Reviewer:
`review_th03_mainl_after86_work.py lstrftim` plus
`tests.test_mainl_after86_work`. The existing original cold pair was reused;
**no full cold replay** occurred.

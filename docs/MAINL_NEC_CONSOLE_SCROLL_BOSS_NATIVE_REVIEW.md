# Original Japanese NEC text console scroll boss — after413

Original Borland Japanese `CL.LIB` member `cnecscrl` (index 545) has been
recovered into maintainable 8086 ASM at `src/mainl/crt/cnecscrl.asm`.
The entire **170 CODE bytes** implement the original near Pascal-cleanup
`__NEC_SCROLL` entry, with three actual NEC scroll/clear direction cases.
It adjusts the original byte-sized stack arguments and uses real
`__MOVETEXT` and `__NEC_ZAP_LINE` helpers to shift or clear rows. The
actual `ret 12`, full stack ABI and all original conditional branch
paths are preserved; the output is not patched OMF or literal target CODE
bytes.

Original `_TEXT`/`_DATA`/`_BSS` = 170/0/0, original DATA-first GROUP
`08ff02ff03`, exported public name at CODE+0 and original ordered
imports are exact. All **five logical OMF relocation fields** are
preserved with their true sites, target members, sizes and addends.
The original Borland program uses TARGET-frame method 5 for near imported
calls, while TASM generates CODE-frame method 0. This difference is
allowed **only** for the proven CODE site/target pairs
`34→__NEC_ZAP_LINE`, `79→__MOVETEXT`, `93→__NEC_ZAP_LINE`,
`136→__MOVETEXT`, `150→__NEC_ZAP_LINE` (ordered by site), and the
builder/reviewer guards every site/target/width and requires those
original-vs-TASM frame alternatives. Literal ordered original Borland
FIXUPP record equality and raw member-program serialization are explicitly
not claimed.

The after413 producer checks the unchanged after412 native carrier of
588 source members, then runs two actual fresh TASM/TLIB/TLINK native
rounds with full raw OBJ/LIB/EXE/MAP and writer logs retained. Both
complete Japanese decoded MAINL EXE/MAP match the originals byte-for-byte
(67,372-byte MZ EXE and 677 ordered DOS relocations). The working CRT
reaches **589/893** source-linked members and **166,254 original-equal CODE
bytes**, leaving **304** unchanged contextual vendor programs. No full
cold replay, canonical packed-file source credit or Factory acceptance
is asserted.

Focused verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after413_work.py nec-console-scroll-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after413_work -v
```

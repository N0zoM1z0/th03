# Original DOS date/time string formatting CRT member (after394)

Original Japanese Borland CL.LIB member `strdate` (index 295) contains a
**159-byte private near Pascal-cleanup formatter** plus two public far
entry points, `__strdate` at CODE+159 and `__strtime` at CODE+216. The
complete **272-byte original CODE** is reconstructed in natural 8086 assembly
at `src/mainl/crt/strdate.asm`, not as original machine-code data or patched
native artifacts. The near helper writes two digits for each of three fields,
retains the original separator and nine-byte NUL-terminated output, uses
signed `idiv`/`cwd` byte-generation instructions, returns a far pointer in
DX:AX, and cleans its 12 bytes of arguments with `ret 12`. The two public
methods make original `__dos_getdate` and `__dos_gettime` far calls using
near stack-local DOS date/time structures.

The exact original CODE bytes, full `_TEXT`/`_DATA`/`_BSS` 272/0/0 segments,
public offsets, ordered imports and both logical original OMF far-call
relocations (CODE sites 173 and 230, preserving site/width/frame/target) match.
TASM emits the two literal FIXUPP records in the opposite order from original
Borland; full literal OMF member-program equality remains explicitly unclaimed.

The source-bound after394 native builder validates and reuses the existing
**534-member after393 native receipt** without full cold replay. Both fresh
TASM/TLIB/TLINK rounds with complete OBJ/LIB/EXE/MAP and writer logs reproduce
the original Japanese decoded MAINL.EXE and MAP **byte-for-byte** (EXE 67,372
bytes with 677 ordered MZ relocations). The maintained CRT has **535/893**
original-equal source members, **358 unchanged vendor members** and **161,262
source CODE bytes**. These counts do not grant packed-member Factory ownership
or whole-game source acceptance.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after394_work.py dos-date-time-format-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after394_work -v
```

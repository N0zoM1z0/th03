# Eleven original Borland formatted I/O, scanner and conio leaves — after434

Eleven previously contextual Japanese `CL.LIB` members are now rebuilt
from natural 8086 ASM: `cprintf`, `vcprintf`, `vprintf`, `vfprintf`,
`fprintf`, `cscanf`, `vcscanf`, `clreol`, `insline`, `gotoxy`, `window`.
All **515 original CODE bytes** match the live original programs. These
are real Borland 16-bit near-callback/far-cdecl implementations: the
formatters invoke the native `__VPRINTER` with their true `FPUTN`/`CPUTN`
callbacks and stack-varargs pointers, scanners call `__scanner` with the
original `Ngetche`/`Nungetch` near callbacks, and the console functions
update real `__video` window fields, implement insert/delete line and
clreol via `__SCROLL`, validate cursor coordinates and call `__GOTOXY`.

Each source matches complete original segment sizes, public offsets,
ordered external symbols and original CODE. All **43 logical OMF
relocation locations/targets** have been checked, including the
`__streams+20` callback base pointer and each `__video` member offset.
Original Borland uses TARGET-frame method 5 for **15 specific near
external call sites**, whereas native TASM uses CODE-frame method 0.
Only the precise site-to-target pairs enumerated in
`scripts/build_th03_mainl_after434_work.py:NEAR_FRAME_GAPS` are
normalized, with strict method, width, target, addend and segment
assertions. Every other original relocation field remains exact.
All eleven source members have different literal FIXUPP record chronology
from Borland (even `gotoxy`, whose logical frames all match), and raw
original Borland OBJ serialization is not claimed. No executable CODE
arrays or patched OMF output were used.

After434 validates the unchanged 631-source after433 receipt and runs
two complete fresh native TASM/TLIB/TLINK producer rounds, retaining
source-bound OBJ/LIB/EXE/MAP and writer logs. Both entire original
decoded Japanese MAINL EXE and MAP are byte-for-byte equal (67,372-byte
EXE, 677 ordered DOS relocations). Working CRT becomes **642/893**
source-built members, **173,421 original-equal CODE bytes** and **251**
unchanged contextual vendor programs. No full cold replay, canonical
packed-file unit acceptance or Factory source credit is implied.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after434_work.py eleven-format-scan-console-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after434_work -v
```

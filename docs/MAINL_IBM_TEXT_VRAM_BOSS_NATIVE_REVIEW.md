# Original IBM text VRAM pointer, transfer and refresh boss — after410

The original Japanese Borland `CL.LIB` member **cibmvram** (index 533) is
recovered as readable 8086 assembly in `src/mainl/crt/cibmvram.asm`, with
all **201 CODE bytes** matching the original active target. Three original
near Pascal-cleanup APIs are retained: `__IBM_VPTR` at CODE+0 calculates
a far video-memory pointer from `__video` row-width, column, VRAM segment
and base; `__IBM_VRAM` at +36 transfers video WORDs with forward/reverse
`MOVSW` semantics and a special 03DAh retrace-synchronized path with
`CLI`/`STI`; `__IBM_REFRESH_VRAM` at +158 checks the active display page
and calls the original near `__IBM_VIDEOINTESDI` helper. The original
`ret 4`, `ret 10`, `ret 6` ABI cleanups and protected register behavior
are preserved without any target byte array or OBJ patch.

Original `_TEXT`/`_DATA`/`_BSS` = 201/0/0, BSS-first `08ff03ff02` GROUP,
all three native public offsets, ordered `__video`/`__IBM_VIDEOINTESDI`
imports, and **all seven original literal ordered FIXUPP fields**
(including their DGROUP and near CODE frame methods, offsets and addends)
are exactly source-reproduced. The active MAINL CL.LIB program was checked
against the installed vendor copy and proved identical for this member.
As usual, full original Borland-vs-TASM raw OMF member-program record
serialization is not claimed equal.

The after410 builder/reviewer inherits the validated 578-source after409
carrier and executes two fresh TASM/TLIB/TLINK native rounds preserving the
complete OBJ/LIB/EXE/MAP vectors and writer logs. Both full decoded Japanese
MAINL EXE and MAP match the original byte-for-byte (67,372-byte EXE and
677 ordered DOS MZ relocations). Source-linked CRT grows to **579/893**
members, **165,578 original-equal CODE bytes**, leaving **314** contextual
vendor programs. This does not establish whole-game source ownership or
Factory accepted-source status, and no full cold replay was performed.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after410_work.py ibm-text-vram-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after410_work -v
```

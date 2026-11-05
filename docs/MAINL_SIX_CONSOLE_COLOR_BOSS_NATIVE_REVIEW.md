# Original NEC/IBM six-way text-color dispatcher — after414

Japanese Borland `CL.LIB` member **ccomcolr** (original index 509) is now
maintained as natural 8086 source in `src/mainl/crt/ccomcolr.asm`. It has six
complete far public entries: `_textcolor` (CODE+0), `_textbackground` (+41),
`_textattr` (+82), `_highvideo` (+123), `_lowvideo` (+154) and `_normvideo`
(+185). These use the real `___conio_type` machine selector to dispatch to
the original six NEC or six IBM color/attribute handlers. The first three
preserve their 16-bit far-cdecl argument and `pop cx` cleanup; the final
three have no argument. Unknown-machine behavior and caller registers are
unchanged from the actual original program.

All **216 original CODE bytes**, full `_TEXT`/`_DATA`/`_BSS` sizes
(216/0/0), the DATA-first original GROUP `08ff02ff03`, public offsets
and all **13 ordered external imports** match. Every original logical OMF
relocation agrees at the actual 24 sites (12 group-frame `___conio_type`
reads and 12 far-call TARGET-frame references, with widths, frames,
targets and addends all intact). Original Borland and native TASM serialize
those FIXUPPs in different record chronology, so *literal ordered FIXUPP*
and original raw member-program serialization equality are not claimed.
There is no embedded target CODE data or patched OBJ.

`scripts/build_th03_mainl_after414_work.py six-console-color-boss` validates
the unchanged after413 source-bound parent and runs two independent actual
native TASM/TLIB/TLINK rounds retaining the complete OBJ/LIB/EXE/MAP and
writer logs. Both linked Japanese decoded MAINL EXE and MAP equal the original
byte-for-byte (67,372-byte EXE, 677 ordered DOS MZ relocations). The
working-source CRT grows to **590/893** members, **166,470 original-equal
CODE bytes**, leaving **303** unchanged contextual vendor programs.
No full cold replay was performed; the result is not packed-original unit
acceptance or Factory accepted-source credit.

Focused review and tests:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after414_work.py six-console-color-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after414_work -v
```

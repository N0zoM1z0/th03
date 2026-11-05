# Original istream_withassign() constructor, FAR thunk and RTTI — after428

The active Japanese Borland `CL.LIB` member `istctr4` (index 754), formerly
contextual in the 623-source working CRT, now has maintained, readable
16-bit ASM at `src/mainl/crt/istctr4.asm`. Its complete far
`@istream_withassign@$bctr$qv` entry allocates an original **46-byte**
object if necessary, constructs the `ios` base at `this+6`, calls the
actual `istream` base constructor, installs both original DATA-backed
vtable references and increments the far 32-bit destructor reference count.

The member includes **349 original CODE bytes**: the executable constructor,
the symbolic local FAR `this`-adjustor thunk at CODE+131 with actual
**-6** object displacement, and typed RTTI for `istream_withassign`, `ios`
and `istream`. Original DATA contains **20 initialized bytes**, including
the RTTI and destructor pointers, vtable displacement words and a real
pointer to the adjustment thunk. Source uses semantic instructions,
`dw`/`dd` fields and named class strings; no target CODE arrays or
post-assembly object modifications.

Native TASM reproduces the original `_TEXTA`/`_DATA`/`_BSS` sizes and
complete CODE/DATA payload, original public/import order, DATA-first
GROUP and **all 16 logical OMF FIXUPP fields** (sites, frames, targets,
widths and addends). The literal Borland-vs-TASM FIXUPP record chronology
still differs, so exact raw original member serialization is not claimed.

The after428 builder validates the unchanged after427 parent and performs
two new TASM/TLIB/TLINK native rounds, retaining source-bound raw
OBJ/LIB/EXE/MAP and writer logs. Both decoded Japanese MAINL EXE/MAP are
byte-for-byte original-equal (67,372-byte EXE, 677 ordered relocations).
The working CRT reaches **624/893** members, **171,327 original-equal CODE
bytes** and **269** unchanged contextual vendor members. There was no full
cold replay or new Factory accepted-source credit.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after428_work.py istream-withassign-default-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after428_work -v
```

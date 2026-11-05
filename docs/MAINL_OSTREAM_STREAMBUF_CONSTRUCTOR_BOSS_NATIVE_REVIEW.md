# Original `ostream(streambuf*)` constructor and RTTI — after422

Original Japanese Borland `CL.LIB` member `ostctr2` (index 807), previously
contextual in the 615-source working CRT, has complete readable 16-bit
ASM at `src/mainl/crt/ostctr2.asm`. Its actual far C++ constructor
conditionally allocates the 44-byte object, initializes the `ios` base,
installs original DATA-resident vtable pointers, calls the genuine far
`ios::init(streambuf*)` method, and increments the original 32-bit
reference destructor count. The source includes its **real local FAR
this-adjusting destructor thunk at CODE+134**, typed class RTTI at
CODE+146 (`ostream`) and CODE+212 (`ios`), and all original far destructor
and inheritance references. No binary CODE stuffing or post-assembly patch.

TASM reproduces **266/266 original CODE bytes and 20/20 DATA bytes**,
original `_TEXTA`/`_DATA`/`_BSS` layout, symbol/public/import ordering,
DATA-first group and **all 13 complete logical original OMF FIXUPP fields**.
Those fields include three true DATA relocations at +0, +8 and +16,
real CODE-resident inherited-class pointers, and far external destructor
references. Native TASM FIXUPP record *chronology* differs from original
Borland; literal ordered original FIXUPPs and original raw member-program
serialization are therefore **not** claimed exact.

The source-bound after422 builder validates the unchanged after421 native
parent and executes two fresh TASM/TLIB/TLINK rounds retaining entire
OBJ/LIB/EXE/MAP and writer logs. Both Japanese decoded MAINL EXE/MAP
remain byte-for-byte original-equal, including the 67,372-byte EXE and
677 original ordered DOS MZ relocations. Working CRT reaches **616/893**
source members, **169,506 original-equal CODE bytes**, with 277 contextual
vendor members. This is not a full cold replay or Factory acceptance.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after422_work.py ostream-streambuf-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after422_work -v
```

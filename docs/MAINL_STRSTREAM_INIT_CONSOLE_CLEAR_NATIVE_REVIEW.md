# Complete strstreambuf::init and DOS/PC-98 console clear — after429

The Japanese Borland `CL.LIB` members `srbinit` (index 843) and `clrscr`
(index 536) are now compiled from natural 16-bit ASM sources in
`src/mainl/crt/`. These were absent from the live 624-source CRT carrier.

`srbinit` is the full **227-CODE** `strstreambuf::init(char*,int,char*)`
implementation: real far string-length fallback, original maximum-growth
mode, near/far buffer extent calculations, three distinct calls to
`streambuf::setb`, `setp` and `setg`, and clearing the original stream
state. This is not a trivial wrapper. `clrscr` adds **45 original CODE
bytes** for the actual conio window-clear operation: `__video` window
fields, window-bottom inquiry, `__SCROLL`, and `__GOTOXY`.

Complete CODE, original segmentation, public/import symbol identities
and the complete logical OMF relocation population match the live original
members (**four plus eight fields**). `srbinit` differs from Borland only
in literal FIXUPP record chronology. On `clrscr` the sole OMF meaning
difference is the original near `__SCROLL` call at CODE+27: original
Borland TARGET frame 5 versus TASM CODE frame 0. The reviewer permits
*only this individually attested site/target/frame alternative* and checks
all seven other fields and the full original payload without normalization.
Literal ordered Borland records and full OBJ serialization are not claimed.

`scripts/build_th03_mainl_after429_work.py` consumes the unchanged after428
source-bound receipt and runs two fresh native TASM/TLIB/TLINK rounds,
retaining complete raw OBJ/LIB/EXE/MAP and writer logs. Both decoded
Japanese MAINL EXE/MAP remain byte-for-byte original-equal (67,372-byte
EXE and 677 ordered DOS relocations). Working CRT increases to **626/893**
original-source members, **171,599 original-equal CODE bytes** and
**267** unchanged contextual vendor programs. No full cold replay, Factory
accepted-source claim or packed-file unit credit.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after429_work.py strstreambuf-init-and-console-clear
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after429_work -v
```

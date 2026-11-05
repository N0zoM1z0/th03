# Full Borland `stdiostream(FILE*)` constructor and four RTTI types — after417

Original Japanese `CL.LIB` member **sdctr** (index 832) is now fully
recovered in readable 8086 source at `src/mainl/crt/sdctr.asm`. Its far
`@stdiostream@$bctr$qn4FILE` constructor (CODE+0) conditionally allocates
the 84-byte C++ object, calls `ios` construction, sets the real DATA-resident
vtable offset, constructs the embedded `stdiobuf` from the FILE far pointer,
initializes its `ios` streambuf base and updates the original 32-bit
reference destructor counter. The first **125 CODE bytes** are executable
instructions with the actual 16-bit compiler stack and far-pointer ABI.

The remaining CODE+125..382 is **not unowned padding** or an imported object:
it contains original typed Borland RTTI for `stdiostream` (CODE+125),
`stdiobuf` (+201), `ios` (+269) and `streambuf` (+323), including names,
field layout, inherited-type pointers and the actual far destructor
symbols. All are authored as semantically typed `dw`/`dd`/`db` fields and
real symbolic relocations, with no copied executable byte arrays. Original
DATA is 12 bytes: a far pointer to the actual `stdiostream` RTTI at CODE+125,
a reserved 4-byte field and the original far destructor pointer at DATA+8.

The entire **383 original CODE bytes + 12 initialized DATA bytes** agree
byte-for-byte, as do `_TEXTA`/`_DATA`/`_BSS` sizes (383/12/0), DATA-first
GROUP `08ff02ff03`, C++ mangled public and all **9 ordered imports**.
All **15 original logical OMF FIXUPPs**, including internal CODE RTTI
pointers and both DATA pointers, match exactly at their site, width, frame,
target and addend. The initial prototype matched the full 395 payload bytes
but had only 14 FIXUPPs: CODE+155 was erroneously written as a zero dword
instead of the genuine symbolic far destructor `@stdiostream@$bdtr$qv`.
Replacing the value with that *real semantic symbol* restored the 15th
original FIXUPP without changing a single CODE byte. Borland and TASM
serialize the 15 records in different literal order; raw member-program
serialization and literal ordered FIXUPP equality are **not** claimed.

`scripts/build_th03_mainl_after417_work.py` validates/reuses the unchanged
603-source after416 carrier and executes two fresh actual TASM/TLIB/TLINK
native rounds with full raw OBJ/LIB/EXE/MAP vectors and logs retained.
Both complete Japanese decoded MAINL.EXE and MAP are byte-for-byte original-
equal (67,372-byte EXE, 677 ordered DOS MZ relocations). The working CRT
reaches **604/893** source-linked original members, **167,706 original-
equal CODE bytes**, and **289** unchanged vendor-context members. No full
cold replay was run; canonical packed-file ownership and Factory accepted
source remain separately open.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after417_work.py stdiostream-file-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after417_work -v
```

# Complete original strstreambuf() default constructor and virtual table — after431

Original Japanese Borland `CL.LIB` member **srbctr1** (index 834) has
been reconstructed as natural 8086 ASM in `src/mainl/crt/srbctr1.asm`.
The real far `@strstreambuf@$bctr$qv` constructor conditionally allocates
50 bytes, constructs the base `streambuf`, installs the original DATA
vtable, clears the far-pointer and private buffer state at object offsets
+26h..+30h, sets the original active flag, and increments the 32-bit
Borland reference destructor counter. No original executable byte arrays
or binary object patches are involved.

The complete **250 CODE bytes** include genuine semantic RTTI for
`strstreambuf` at CODE+118 and its `streambuf` base at CODE+190. All
**52 initialized DATA bytes** contain the real RTTI pointer, original
reserved field and **11 virtual-function slots** with named external
symbols. Every one of the **19 original logical OMF FIXUPP fields**
(site, width, frame, target and addend) is reproduced exactly, including
DATA+28 `streambuf::do_sputn` and DATA+32 `strstreambuf::overflow`.
Original public, ordered imports, `_TEXTA`/`_DATA`/`_BSS` segments and
DATA-first GROUP also match. TASM and Borland serialize FIXUPP records
in different literal chronology, so complete Borland OBJ-record equality
is not asserted.

The after431 incremental producer validates/reuses the unchanged after430
628-member CRT and executes two actual fresh TASM/TLIB/TLINK rounds,
retaining full source-bound OBJ/LIB/EXE/MAP vectors and writer logs.
Both decoded Japanese MAINL EXE/MAP remain byte-for-byte original-equal
(67,372-byte EXE, 677 ordered MZ relocations). Working CRT is now
**629/893** source members with **172,332 original-equal CODE bytes**
and **264** contextual vendor members. Formal Factory acceptance and
canonical packed-file credit remain separately open; no cold replay.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after431_work.py strstreambuf-default-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after431_work -v
```

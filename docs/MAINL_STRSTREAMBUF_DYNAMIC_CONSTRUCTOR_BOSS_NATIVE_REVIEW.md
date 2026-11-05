# Complete strstreambuf(int) dynamic buffer constructor — after433

Previously contextual Japanese Borland `CL.LIB` member `srbctr3` (index
836) is now rebuilt entirely from natural source at `src/mainl/crt/srbctr3.asm`.
Its far C++ `@strstreambuf@$bctr$qi` constructor really allocates a 50-byte
`strstreambuf` object if needed, calls the base streambuf constructor,
installs the DATA vtable, enforces the original **minimum 16-byte buffer**,
allocates the character array through the real `@$bnwa$qui` near/far
operator, computes an original 16-bit far end pointer, passes the true
buffer span to `streambuf::setb`, null-terminates the allocated region,
sets the original internal mode flags, and increments the 32-bit
reference destructor count. Stack-local far pointer words and unchecked
Borland arithmetic are preserved; no synthesized executable byte arrays.

All **320 original CODE bytes and 52 initialized DATA bytes** match the
live original program. The last CODE region contains genuine `strstreambuf`
and `streambuf` RTTI at +188 and +260. DATA contains the typed RTTI pointer
and 11 genuine virtual method symbols (including distinct `do_sputn` and
`overflow` slots). All **21 original logical OMF FIXUPPs** are reproduced
site-for-site, including the CODE+72 `new[]` call, CODE+105 `setb` call,
internal inheritance pointers and all eleven DATA virtual-function slots.
The `_TEXTA`/`_DATA`/`_BSS` layout, DATA-first GROUP, mangled public and
17 ordered imports match. Borland/TASM literal FIXUPP record chronology
is different; full raw original OBJ record serialization is not claimed.

The after433 source-bound producer validates the unchanged after432
630-source CRT and runs two fresh actual TASM/TLIB/TLINK rounds retaining
OBJ/LIB/EXE/MAP, source hashes and native writer logs. Both complete
decoded Japanese MAINL EXE/MAP are byte-for-byte original-equal (EXE
67,372 bytes, 677 ordered DOS relocations). The working CRT reaches
**631/893** members, **172,906 original-equal CODE bytes**, and **262**
unchanged contextual vendor members. No full cold replay or new Factory
accepted-source credit was claimed.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after433_work.py strstreambuf-dynamic-buffer-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after433_work -v
```

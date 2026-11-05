# Original strstreambuf far-buffer constructor and complete vtable — after432

Original Japanese `CL.LIB` member **srbctr2** (index 835) has been
reconstructed as readable natural 16-bit ASM in `src/mainl/crt/srbctr2.asm`.
Its far C++ constructor `@strstreambuf@$bctr$qnql$nvnqnv$v` allocates the
real 50-byte object if necessary, constructs the `streambuf` base,
installs the original DATA virtual table, copies two *far pointers* from
stack arguments to the original object offsets +26h/+28h and +2Ah/+2Ch,
clears its other buffer state and increments the original 32-bit Borland
destructor reference count.

The native source reproduces the complete **254 CODE bytes and 52 DATA
bytes**. CODE includes the real typed Borland `strstreambuf` and
`streambuf` RTTI at CODE+122/+194; initialized DATA contains the actual
RTTI pointer, reserved fields, and eleven individually named far virtual
functions. All **19 original logical OMF FIXUPP fields** are reproduced
at exact sites with original widths, frames, targets and addends. DATA+28
is the true `streambuf::do_sputn` slot and DATA+32 is the distinct
`strstreambuf::overflow` slot, preventing the byte-equal-but-wrong target
error discovered in a previous overload. Segment layout, public ABI,
ordered imports and DATA-first group match the live original member.
Original Borland versus TASM literal FIXUPP record chronology remains
different; whole raw Borland OBJ serialization equality is not claimed.

The incremental after432 builder validates the complete unchanged after431
source-bound native receipt and executes two actual independent
TASM/TLIB/TLINK rounds, retaining complete OBJ/LIB/EXE/MAP vectors and
writer logs. Both whole decoded Japanese MAINL EXE/MAP match their original
bytes (67,372-byte MZ EXE, 677 ordered relocations). The working CRT
reaches **630/893** source-built original members, **172,586 original-equal
CODE bytes**, and **263** unchanged contextual vendor members. No full cold
replay, packed-file unit credit or Factory accepted-source claim is made.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after432_work.py strstreambuf-far-buffer-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after432_work -v
```

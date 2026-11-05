# Complete original filebuf(int,char*,int) constructor, RTTI and vtable — after437

Original Japanese Borland `CL.LIB` member **fsbctr3** (index 710) has
been reconstructed as ordinary 16-bit ASM at `src/mainl/crt/fsbctr3.asm`.
The actual far C++ constructor `@filebuf@$bctr$qinci` conditionally
allocates its 54-byte object, constructs the `streambuf` base, installs
its true DATA-backed vtable, stores the original file descriptor and
buffer ownership/status flags, and calls **the original virtual method
at vtable+4** to configure the buffer using its passed pointer/length.
It increments the original 32-bit reference destructor counter and
returns the complete original far object pointer.

All **259 CODE bytes and 52 initialized DATA bytes** are source-real
and byte-exact. The CODE+133 `filebuf` and CODE+199 `streambuf` class
records are typed C++ RTTI with names, inherited-type and destructor
references. DATA contains the true RTTI pointer, reserved field and 11
real symbolic virtual function slots; these are not anonymous zero
constants. All **19 original logical OMF FIXUPP fields** match exact
site, width, frame, target and addend, including CODE+50 -> DATA+8
vtable immediate and DATA+28 `streambuf::do_sputn` versus DATA+32
`filebuf::overflow`. The original `_TEXTA`/`_DATA`/`_BSS` segments,
public, 15 ordered imports and DATA-first GROUP also match. Borland/TASM
literal FIXUPP record chronology differs; complete original Borland OBJ
serialization is **not** claimed equal. No binary executable copying or
post-assembly patches were used.

The incremental after437 native producer validates the unchanged after436
source-bound parent and performs two fresh native TASM/TLIB/TLINK rounds,
retaining the complete OBJ/LIB/EXE/MAP outputs, source hashes and writer
logs. Both decoded Japanese MAINL EXE and MAP are byte-for-byte original-
equal (67,372-byte EXE, 677 ordered DOS MZ relocations). The working CRT
now contains **645/893** source-built original members, **174,207 original-
equal CODE bytes** and **248** unchanged contextual vendor programs.
Factory acceptance and packed-file source ownership remain separately
open; no full cold replay was run.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after437_work.py filebuf-virtual-setbuf-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after437_work -v
```

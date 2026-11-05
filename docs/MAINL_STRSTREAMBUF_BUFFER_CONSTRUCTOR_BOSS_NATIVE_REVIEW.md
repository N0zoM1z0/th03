# Original strstreambuf buffer constructor and full 52-byte vtable — after425

The Japanese Borland `CL.LIB` member **srbctr4** (original index 837) is
now reconstructed as readable natural 8086 source at
`src/mainl/crt/srbctr4.asm`. The far C++ entry
`@strstreambuf@$bctr$qnzcit1` conditionally allocates the 50-byte
object, calls the original `streambuf` base constructor, installs the true
DATA vtable, initializes its far buffer pointers through
`strstreambuf::init`, and increments the 32-bit destructor reference count.
The **239 original CODE bytes** include genuine typed RTTI for
`strstreambuf` at CODE+107 and its `streambuf` base at CODE+179, with
semantic field names, inherited-class pointer and far destructor symbols.

All **52 initialized DATA bytes** are maintained as actual 16-bit Borland
virtual-function slots, not anonymous zero constants: a far RTTI pointer,
reserved field and **11 far method references** for destructor, setbuf,
get, underflow, pbackfail, put, overflow, seekoff, seekpos, sync and
allocation. An initial translation matched *all 291 unlinked payload bytes*
while incorrectly swapping two virtual methods: the original target of
DATA+28 is `@streambuf@do_sputn$qnxci`, while DATA+32 is
`@strstreambuf@overflow$qi`. Both unlinked slots contain zero bytes, so
CODE/DATA equality alone could not catch the bug. Checking the real OMF
FIXUPP target at every site exposed it. Both virtual symbols were
corrected in source before native integration.

Native TASM now matches the complete **239 CODE + 52 DATA payload**,
original public/import interface (16 ordered imports), DATA-first GROUP,
segment sizes, and **all 20 logical original OMF relocation fields**
without target/frame normalization. Original Borland/TASM FIXUPP *record
order* still differs, and literal ordered FIXUPPs or raw Borland member
serialization are not falsely claimed equal. No executable byte arrays or
post-assembly patches were used.

`scripts/build_th03_mainl_after425_work.py` validates/reuses the unchanged
620-member after424 carrier and runs two fresh native TASM/TLIB/TLINK
rounds with entire OBJ/LIB/EXE/MAP vectors and writer logs. Both full
Japanese decoded MAINL EXE and MAP are byte-for-byte original-equal
(67,372-byte EXE and 677 ordered DOS MZ relocations). Working CRT:
**621/893** source members, **170,340 original-equal CODE bytes**, and
**272** unchanged contextual vendor programs. This is not full cold replay,
Factory acceptance or canonical packed-file source credit.

Focused verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after425_work.py strstreambuf-buffer-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after425_work -v
```

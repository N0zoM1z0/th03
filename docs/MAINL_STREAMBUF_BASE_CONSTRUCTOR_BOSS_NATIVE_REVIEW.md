# Original streambuf() base constructor and complete virtual table — after439

The previously contextual Japanese Borland `CL.LIB` member `stbctr1`
(index 854) is now owned by natural, maintained 8086 ASM in
`src/mainl/crt/stbctr1.asm`. The complete far C++ entry
`@streambuf@$bctr$qv` conditionally allocates the original **38-byte**
object, installs the real DATA-backed virtual table, initializes every
original near/far get/put/buffer pointer and flags, and increments the
original 32-bit destructor reference counter. Its original unchecked
large-model C++ ABI and branch layout are preserved.

Complete **237 CODE bytes and 52 initialized DATA bytes** match their
source-target original. CODE+177 contains the actual typed Borland
`streambuf` RTTI descriptor, not executable padding. DATA has a genuine
RTTI far pointer and eleven separately named far virtual-function
references. All **16 original logical OMF FIXUPPs** match site, width,
frame, target and addend; this includes CODE+39 -> DATA+8, DATA+0 ->
CODE+177, the distinct `do_sputn` and `overflow` vtable targets and all
other original interface symbols. The exact `_TEXTA`/`_DATA`/`_BSS`
segments, public/import ABI and DATA-first GROUP match. Borland's and
TASM's *literal FIXUPP record chronology* differs and complete original
OBJ record serialization is not claimed. No target CODE byte arrays or
post-assembly patches are used.

After439 validates/reuses the unchanged 646-member after438 source-bound
carrier and performs two fresh native TASM/TLIB/TLINK rounds, retaining
raw OBJ/LIB/EXE/MAP, logs and source hashes. Both complete decoded
Japanese MAINL EXE/MAP are byte-for-byte original-equal (67,372-byte EXE,
677 ordered MZ relocations). The working CRT now contains **647/893**
source-linked original members, **174,691 original-equal CODE bytes**,
with **246** unchanged contextual vendor programs. This is not Factory
source acceptance or a full cold replay.

Focused review:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after439_work.py streambuf-base-default-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after439_work -v
```

# Complete stdiostream destructor and typed RTTI — after418

The actual original Japanese Borland `CL.LIB` member `sddtr` (index 833),
previously contextual in the after417 CRT, now has complete maintained
16-bit ASM source in `src/mainl/crt/sddtr.asm`. The far public
`@stdiostream@$bdtr$qv` at `_TEXTA` CODE+0 implements original
`stdiostream::~stdiostream`: 32-bit destructor reference-count decrement,
actual `stdiobuf` member destructor, actual `ios` base destructor and
optional far-object free via `@$bdele$qnv`. The original unchecked pointer,
stack and register conventions remain intact.

The first **98 CODE bytes** are executable destructor instructions; the
remaining CODE+98..355 contains *complete typed Borland RTTI*, not an
unowned binary table. Four original classes (`stdiostream`, `stdiobuf`,
`ios`, `streambuf`), inherited-type descriptors and real symbolic far
destructor pointers are maintained in natural `dw`/`dd`/`db` source.
Unlike the matched constructor, this member has its own distinct local
RTTI offsets: +98, +174, +242 and +296. Original DATA is 12 bytes:
a far pointer to local RTTI at +98, a four-byte reserved field and a
far destructor pointer at DATA+8.

Native TASM emits all **356 original CODE bytes and 12 initialized DATA
bytes** exactly, with the original `_TEXTA`/`_DATA`/`_BSS` layout,
original public/import identities and **all 14 logical OMF FIXUPP
fields** (including the internal CODE and DATA pointers). The original
Borland emits the FIXUPP fields in different literal record order from
TASM: raw ordered FIXUPP and whole member-program equality are *not*
claimed. No executable target-byte arrays or object patches were used.

`scripts/build_th03_mainl_after418_work.py` reuses and validates the
unchanged after417 604-source native carrier, rebuilding only this member
and its affected CRT/link in two independent TASM/TLIB/TLINK rounds.
Both whole original Japanese decoded MAINL EXE and MAP remain byte-for-byte
equal (EXE 67,372 bytes with 677 ordered DOS relocations), with retained
OBJ/LIB/EXE/MAP outputs, source hashes and writer logs. The working CRT
reaches **605/893** source members, **168,062 original-equal CODE bytes**,
and **288** unchanged contextual vendor members. Factory/packed-unit
acceptance and a full cold replay are not implied.

Focused commands:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after418_work.py stdiostream-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after418_work -v
```

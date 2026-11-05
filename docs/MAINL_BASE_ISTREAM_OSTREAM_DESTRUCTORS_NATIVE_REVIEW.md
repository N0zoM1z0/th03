# Complete original istream/ostream base destructors and typed RTTI — after430

Two original Japanese Borland `CL.LIB` members, `istdtr1` (index 757) and
`ostdtr1` (index 809), were contextual in the live after429 working CRT.
Both now have complete natural 8086 ASM in `src/mainl/crt/` with the
original C++ ABI and all typed metadata. Their far `istream::~istream`
(**230 CODE, 20 DATA**) and `ostream::~ostream` (**253 CODE, 20 DATA**)
perform genuine 32-bit destructor reference-count updates, conditional
`ios` base destruction and optional far delete. `ostream` additionally
performs its real conditional `flush()` call before deletion; `istream`
does not. Each includes a local far-return destructor adjustment thunk
at CODE+98 (`-6`) or +121 (`-4`), and the typed `istream`/`ostream` and
`ios` RTTI descriptors in their own original CODE positions.

**A real OMF source correction was required.** An early translation
reproduced all **523 combined CODE/DATA bytes** exactly but exposed only
10/12 and 11/13 original FIXUPPs: the instructions at CODE+38 and +46
were written as numeric vtable offsets `8` and `16`. The original member
uses **genuine DATA+8 and DATA+16 symbolic relocations** there. The
sources now name those DATA/vtable pointers, yielding all **25 original
logical OMF relocations**, including their frames, targets, widths and
addends, without changing a single CODE byte. All original public,
ordered import, segment size and GROUP properties also match. TASM's
literal FIXUPP record chronology differs from Borland; exact raw member
record serialization is not claimed.

The after430 incremental producer validates the unchanged after429 parent,
then runs two fresh actual TASM/TLIB/TLINK rounds with full OBJ/LIB/EXE/MAP
and logs retained. Both Japanese decoded MAINL EXE and MAP reproduce the
original byte-for-byte (67,372-byte EXE and 677 ordered DOS relocations).
The working CRT reaches **628/893** source members, **172,082 original-
equal CODE bytes**, with **265** unchanged contextual vendor members.
No full cold replay or Factory source acceptance was performed or asserted.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after430_work.py base-istream-ostream-destructor-bosses
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after430_work -v
```

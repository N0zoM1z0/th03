# Complete original filebuf destructor and public DATA openprot — after438

Original Japanese Borland `CL.LIB` member `fsbdtr` (index 711) is now
reconstructed as maintainable 16-bit ASM in `src/mainl/crt/fsbdtr.asm`.
The far `@filebuf@$bdtr$qv` C++ entry decrements the 32-bit destructor
reference counter, installs the real class vtable, and distinguishes
filebuf's two cleanup paths: when the filebuf is associated with an open
file it invokes `filebuf::close`; otherwise it calls the original
virtual `overflow(-1)` through the vtable for buffer synchronization.
It then invokes the actual `streambuf` base destructor and optionally
frees the complete far object using `@$bdele$qnv`.

All **247 original CODE bytes and 54 initialized DATA bytes** are
source-assembled exactly, including complete typed RTTI at CODE+121
(`filebuf`) and +187 (`streambuf`), and eleven symbolic virtual methods.
**A real original DATA ABI detail was independently recovered:** unlike
filebuf's related constructor, the destructor member exports a separate
`@filebuf@openprot` public at **DATA+0**, containing the native word
`0180h`. Its class RTTI far pointer is at DATA+2, its reserved bytes
start at +6 and its local far destructor vtable pointer is at DATA+10.
The initial byte-exact assembler prototype lacked this public; the
source and scoped reviewer now require the genuine original export.

The complete original `_TEXTA`/`_DATA`/`_BSS` layout, DATA-first GROUP,
ordered fourteen imports, CODE/DATA publics and **all twenty original
logical OMF FIXUPPs** match site, width, frame, target and addend.
Borland's and TASM's literal FIXUPP chronology and full OBJ-record
serialization remain different; no complete raw-record equality is
claimed. No executable target-byte arrays or post-assembly patches.

The after438 incremental producer validates the unchanged after437
645-source parent and executes two independent fresh TASM/TLIB/TLINK
rounds, preserving complete source/driver hashes, OBJ/LIB/EXE/MAP and
writer logs. Both full decoded Japanese MAINL EXE/MAP are byte-for-byte
original-equal (67,372-byte EXE with 677 ordered MZ relocations).
Working CRT becomes **646/893** source members, **174,454 original-equal
CODE bytes**, with **247** unchanged contextual vendor members.
No full cold replay, Factory accepted-source claim or packed-unit credit.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after438_work.py filebuf-close-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after438_work -v
```

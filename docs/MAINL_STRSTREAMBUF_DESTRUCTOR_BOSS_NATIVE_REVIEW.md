# Complete original strstreambuf::~strstreambuf() and typed virtual table — after435

Previously contextual Japanese Borland `CL.LIB` member **srbdtr** (index
841) is recovered as natural 16-bit ASM in `src/mainl/crt/srbdtr.asm`.
The actual far `@strstreambuf@$bdtr$qv` destructor decrements its 32-bit
reference counter, reinstalls the original vtable, and follows the real
buffer-ownership mode: when the original mode requires cleanup, it calls
the far function pointer stored in the object at +2Ah if configured, or
invokes Borland `@$bdla$qnv` array deletion on the owned far buffer.
It then calls the authentic `streambuf` base destructor and optionally
frees the far C++ object using `@$bdele$qnv`. These are separate and
complete original control-flow branches, not a stub.

All **265 original CODE bytes** are reproduced from readable 8086
instructions. CODE+133/+205 contain genuinely typed `strstreambuf` and
`streambuf` RTTI (with named class strings, inheritance and symbolic
far destructor pointers). All **52 initialized DATA bytes** preserve
original RTTI, reserved fields and eleven *symbolically bound* virtual
method slots; the local destructor at DATA+8 is a real internal CODE
FIXUPP, not an unrelocated zero. The native source matches **all 20
original logical OMF FIXUPPs** exactly: original `DATA+8` vtable
address in CODE+37, real external array-delete at CODE+87, base
destructor at +103 and optional object delete at +123, together with
all RTTI and virtual slot references. Original ordered imports, mangled
public, segmentation and DATA-first group also match. Borland-vs-TASM
literal record order differs; exact raw original OMF serialization is
not asserted. No executable byte arrays or object patches were used.

The after435 source-bound builder validates/reuses the unchanged after434
642-source CRT carrier, then runs two actual fresh TASM/TLIB/TLINK rounds
retaining raw OBJ/LIB/EXE/MAP and writer logs. Both complete Japanese
decoded MAINL EXE and MAP remain byte-for-byte original-equal
(67,372-byte EXE with 677 ordered relocations). Working CRT reaches
**643/893** source members and **173,686 original-equal CODE bytes**,
with **250** unchanged vendor-context members. No full cold replay or
Factory/packed-file source acceptance is implied.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after435_work.py strstreambuf-complete-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after435_work -v
```

# Original istream_withassign destructor, FAR thunk and typed RTTI — after426

The live original Japanese `CL.LIB` member `istdtr2` (index 758) is now
reconstructed as natural 16-bit assembly in `src/mainl/crt/istdtr2.asm`.
The actual `@istream_withassign@$bdtr$qv` far entry maintains the original
32-bit destructor reference counter and conditionally destroys the `istream`
base, the `ios` subobject and the far object. This is the complete member,
not an external destructor veneer.

All **333 CODE bytes and 20 initialized DATA bytes** are reproduced. The
original CODE+115 local destructor adjustment thunk subtracts six bytes
from the stack's object pointer before a true *far* jump to the local
exported entry. Setting `assume cs:nothing` at this site preserves the
real Borland FAR branch instead of TASM relaxing it. The following CODE
also contains genuine typed RTTI for `istream_withassign`, `ios` and
`istream`, with symbolic class inheritance and destructor pointers.
DATA includes the real RTTI pointer, vtable entries, adjustment words
and pointer back to CODE+115. No embedded original executable byte arrays
or OBJ post-processing are involved.

Original segment names/sizes, public and ordered imports, DATA-first
GROUP, and all **16 logical OMF FIXUPP fields** (site, width, frame,
target and addend) agree. TASM's literal FIXUPP record chronology still
differs from Borland's; complete raw original OMF record equality is not
claimed. The matching CODE/DATA result was verified against the *live*
original member, not inferred from the related ostream destructor.

The incremental after426 build validates/reuses the unchanged after425
source-bound parent, then performs two fresh TASM/TLIB/TLINK rounds.
Both complete Japanese decoded MAINL EXE/MAP remain byte-for-byte equal
(67,372-byte EXE with 677 ordered MZ relocations), with raw
OBJ/LIB/EXE/MAP and logs retained. Working CRT is **622/893** source-built
members, **170,673 original-equal CODE bytes** and **271** unchanged
contextual vendor members. No full cold replay or Factory accepted-source
credit is implied.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after426_work.py istream-withassign-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after426_work -v
```

# Complete ostream_withassign destructor, local far thunk and RTTI — after420

The original Japanese Borland `CL.LIB` member `ostdtr2` (index 810)
has been recovered in natural 16-bit ASM at `src/mainl/crt/ostdtr2.asm`.
The far public `@ostream_withassign@$bdtr$qv` has real 16-bit C++
destruction logic: original 32-bit destructor reference counter decrement,
base `ostream` destruction, optional `ios` subobject destruction and
optional far deletion of the complete object.

The first **115 CODE bytes** are the real destructor. CODE+115..126 is the
original `this`-pointer adjustment thunk, which subtracts four from the
return-stack object argument and then performs an actual far JMP to the
*local* exported destructor. Under normal same-CS assumptions, TASM
relaxes that source instruction to a short relative JMP, yielding only
330 CODE bytes and dropping one original relocation. As with the
previously reviewed multiple-inheritance C++ thunks, `assume cs:nothing`
at this site forces the *original* far JMP and OMF reference without
copying machine bytes or patching an OBJ. The resulting **333 CODE bytes**,
**20 initialized DATA bytes**, and **16 logical original FIXUPP fields**
all match exactly.

The remaining CODE contains full typed Borland RTTI for
`ostream_withassign` (+127), `ios` (+213), `ostream` (+267), with
original C++ names, inherited-type descriptors and real far destructor
symbols. DATA supplies the original RTTI pointer, reserved fields,
destructor vtable pointer, actual vtable adjustment words and a symbolic
pointer to the CODE+115 thunk. All original `_TEXTA`/`_DATA`/`_BSS`
333/20/0 layout, DATA-first group, export/import ABI and complete OMF
frame/target/addend metadata match. Borland's and TASM's literal FIXUPP
record chronology and full raw library member records do *not* match;
this difference is explicitly retained.

The after420 source-bound builder inherits the unchanged after419 606-member
carrier and runs two fresh native TASM/TLIB/TLINK rounds, retaining full
OBJ/LIB/EXE/MAP outputs, writer logs and source hashes. Both complete
Japanese decoded MAINL EXE and MAP equal the original byte-for-byte
(67,372-byte EXE, 677 ordered MZ relocations). Working CRT reaches
**607/893** source-built members, **168,744 original-equal CODE bytes**,
with **286** contextual vendor members. This is not a new full cold replay
or Factory accepted-source claim.

Focused review:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after420_work.py ostream-withassign-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after420_work -v
```

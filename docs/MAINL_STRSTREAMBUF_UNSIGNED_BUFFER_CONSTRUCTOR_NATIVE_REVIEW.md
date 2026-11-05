# Original unsigned-char far-buffer strstreambuf constructor — after449

Japanese CL.LIB member srbctr5 (index 838), the FAR Borland
@strstreambuf@$bctr$qnucit1 overload, is now maintained in
[src/mainl/crt/srbctr5.asm](../src/mainl/crt/srbctr5.asm). Independent
comparison of the **original** members 837 (char overload), 838
(unsigned char overload) and 839 (char overload) establishes that
their complete 239 CODE byte streams and logical FIXUPPs agree. This
is not an assumption inherited from the earlier source notes: the
original library was enumerated again before recovery.

The source retains original conditional 50-byte object allocation,
the exact far streambuf base constructor call, DATA-backed vtable,
five raw arguments passed to strstreambuf::init, the native C++
reference-destructor counter and two semantically typed RTTI records
at CODE+107/+179. The 52-byte DATA contains a genuine class
descriptor, 11 separately named virtual-function far targets,
and unlinked reserved bytes. All **20 logical OMF relocations**
agree at the original locations, with the complete segment, group,
import/public ABI and exact 239 CODE / 52 DATA payload. Literal
Borland/TASM FIXUPP chronology and raw record serialization differ;
full original-OBJ equality is not claimed.

After449 verifies the inherited after448 native source-bound carrier,
then builds with TASM/TLIB/TLINK twice. Both independent rounds
retain raw OBJ/LIB/EXE/MAP pairs and writer logs. Both decoded
Japanese MAINL EXE/MAP are byte-for-byte target-equal, including
the 67,372-byte EXE and 677 ordered MZ relocations. This advances
the **working CRT** to **657/893 source members**,
**176,844 original-equal CODE bytes** and 236 contextual vendor
members, with no new Factory acceptance or full cold replay.

Focused review:
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after449_work.py strstreambuf-unsigned-far-buffer-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after449_work -v

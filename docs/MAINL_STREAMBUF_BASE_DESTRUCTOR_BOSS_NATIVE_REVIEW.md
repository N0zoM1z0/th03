# Original streambuf base destructor, RTTI and vtable — after440

The original Japanese Borland CL.LIB member stbdtr (index **859**) is
recovered in maintained natural 8086 source
[src/mainl/crt/stbdtr.asm](../src/mainl/crt/stbdtr.asm). The full FAR C++
destructor decrements the global 32-bit destructor reference count, checks
a null this pointer, resets the class vtable, releases an owned far buffer
through delete[] when its buffer-ownership flag is set, clears that flag,
and optionally invokes far delete on the object when the hidden
destructor-control argument requests it. No defensive product behavior
has been invented.

The original **153 CODE + 52 initialized DATA bytes** match exactly,
including the real Borland streambuf type descriptor at CODE+93,
the DATA+0 far RTTI pointer, and the 11 symbolic virtual-function
slots beginning at DATA+8. The original **17 logical OMF relocations**,
including CODE+37 -> DATA+8 and the distinct delete[] and delete
calls at CODE+55/+83, match completely (site, width, frame, target,
addend). The vendor literal FIXUPP record chronology and full OBJ
serialization are **not** identical to the TASM-emitted program, and
are not claimed as such.

After440 checks its unchanged after439 source-bound parent and creates
two independent TASM/TLIB/TLINK native rounds with retained raw
OBJ/LIB/EXE/MAP, logs and hashes. Both 67,372-byte Japanese MAINL
decoded EXE and complete MAP equal their targets; all 677 ordered
MZ relocations survive. The working CRT progresses to **648/893**
original source-linked members and **174,844 CODE bytes** while
**245 members** stay contextual vendor objects. This is scoped
working-source evidence, not a full cold build or Factory acceptance.

Focused review:
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after440_work.py streambuf-base-destructor-boss
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after440_work -v

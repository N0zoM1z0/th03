# Original ostream() default constructor, ios and dual vtables — after445

The original Japanese Borland CL.LIB member ostctr1 (index **806**) is
fully recovered as [natural native 8086 ASM](../src/mainl/crt/ostctr1.asm).
This complete C++ constructor conditionally allocates its **44-byte**
object, initializes its ios subobject at +4 when necessary, installs
the two different original vtable pointers and increments the 32-bit
Borland destructor reference count. Its local FAR adjusting destructor
thunk subtracts four from the hidden this pointer before chaining to
the original ostream destructor; it is not an anonymous byte fixture.

All **245 CODE + 20 initialized DATA bytes** agree with the Japanese
original. Original RTTI for both ostream and ios is encoded as typed
symbolic records, with true virtual pointers at DATA+8 and DATA+16,
and the local destructor thunk at CODE+113. All **12 logical OMF
relocations** agree (including CODE+75 -> DATA+8, CODE+83 -> DATA+16,
and DATA+0 -> CODE+125), with original public/import ABI and segment
layout. Borland and TASM literal FIXUPP order/full OBJ program differ;
that stronger equality is not asserted.

The after445 producer validates the existing after444 652-source
carrier and runs two independent TASM/TLIB/TLINK rounds retaining all
raw OBJ/LIB/EXE/MAP outputs, writer logs, source hashes and the parent
receipt. Both 67,372-byte Japanese decoded MAINL EXE and complete MAP
match the target, preserving 677 ordered MZ relocations. The working
CRT now has **653/893** original source-linked members,
**176,015 source CODE bytes** and 240 contextual vendor members.
This is not a full cold replay or new Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after445_work.py,
mode ostream-default-constructor-boss.
Unit tests: tests.test_mainl_after445_work.

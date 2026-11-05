# Complete original ios(streambuf FAR*) constructor, RTTI and vtable — after484

Japanese Borland CL.LIB member stctr2 (original index **876**) is
recovered as maintainable
[8086 source](../src/mainl/crt/stctr2.asm).
The actual FAR C++ constructor optionally allocates the original
40-byte ios object, installs the native DATA-backed destructor
vtable pointer, zeroes the two original ios status fields,
calls the true @ios@init$qn9streambuf with the original FAR
streambuf argument, updates the 32-bit reference destructor
count and returns the genuine FAR ios object pointer.

All **153 original CODE bytes and 12 initialized DATA bytes**
match exactly, including the actual 54-byte typed ios RTTI
descriptor in CODE+99..152 and the source-backed virtual table
at DATA+8. The original DATA+0 pointer refers symbolically
to CODE+99; the true destructor slot at DATA+8 points to
@ios@$bdtr$qv. All **seven original logical OMF FIXUPPs**
match site, kind, width, frame, target and addend, including
CODE+39 -> DATA+8, CODE+64 -> ios::init, and DATA+0 ->
CODE+99. The original _TEXTA/_DATA/_BSS, DATA-first group,
public name and all four ordered imports are maintained.
The TASM literal FIXUPP chronology is not the same as
Borland's; complete original raw OBJ record identity is
not claimed. There are no executable byte arrays or post-
assembly object modifications.

After484 independently checks the unchanged after483
691-member CRT carrier and performs two fresh native
TASM/TLIB/TLINK rounds with the complete OBJ/LIB/EXE/MAP
vectors, logs and source/driver hashes retained.
Both decoded Japanese MAINL EXE and MAP are original-equal
(67,372 EXE bytes and 677 ordered MZ relocations).
The working CRT is now **692/893 source-linked members**,
**184,085 original-equal CODE bytes**, and 201 contextual
vendor members. No full cold replay or new Factory
accepted-source credit was asserted.

Focused reviewer: scripts/review_th03_mainl_after484_work.py,
mode ios-streambuf-constructor-rtti-boss.
Tests: tests.test_mainl_after484_work.

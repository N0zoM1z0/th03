# Original ios destructor, global fmtflags, RTTI and BSS — after501

The Japanese Borland CL.LIB member stdtr (slot **877**) is now
maintained as real [8086 source](../src/mainl/crt/stdtr.asm).
The complete original 87-byte FAR ios::~ios destructs the user
word array through native Borland far array delete, conditionally
frees the ios object itself via the real scalar delete operator,
and adjusts the original 32-bit global destructor count. Its
vtable assignment at CODE+37 retains the original typed
DATA+26 destructor pointer. All register and FAR this/flag ABI
details match without host-side lifecycle substitutes.

**All 141 original CODE bytes, 30 initialized DATA bytes and
four true uninitialized BSS bytes match.** Typed DATA includes
five actual exported C++ globals: @ios@basefield at +0 (70h),
@ios@adjustfield at +4 (0Eh), @ios@floatfield at +8 (1800h),
@ios@nextbit at +12 (10h), and @ios@usercount at +16.
DATA+18 symbolically refers to the genuine 54-byte ios type
descriptor at CODE+87, and the true DATA+26 vtable points to
the destructor at CODE+0. The original BSS exposes the
four-byte @ios@stdioflush symbol at +0, preserved as
uninitialized data rather than a fabricated initial value.

All seven logical original OMF fixups match: five references
from CODE and two from DATA, including symbolic typed RTTI
and vtable pointers. Borland and TASM emit a different literal
FIXUPP chronology; raw vendor OBJ record equality is not
claimed. Original public names, five DATA exports, BSS export,
ordered imports, _TEXTA/_DATA/_BSS and GROUP are all preserved.

After501 validates the entire unchanged after500 **708-source**
carrier and performs two real TASM/TLIB/TLINK rounds with full
raw OBJ/LIB/EXE/MAP output vectors, writer logs and source hashes.
Both Japanese MAINL EXE/MAP are original-equal byte-for-byte:
67,372 EXE bytes and 677 ordered MZ relocations.
Working CRT: **709/893** complete original source-linked members,
**186,575 original-equal CODE bytes**, 184 contextual vendor
members. No full cold replay or formal Factory source acceptance
was claimed.

Focused reviewer: scripts/review_th03_mainl_after501_work.py
(mode ios-destructor-rtti-vtable-boss).
Tests: tests.test_mainl_after501_work.

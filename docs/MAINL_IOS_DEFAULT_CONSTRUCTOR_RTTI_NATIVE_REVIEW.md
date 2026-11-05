# Original ios() default constructor with complete typed RTTI — after485

Japanese Borland CL.LIB member stctr1 (slot **875**) is now
recovered as maintained [8086 source](../src/mainl/crt/stctr1.asm).
It contains the entire native FAR ios() default constructor.
The original optionally allocates a 40-byte object, installs its
real DATA-backed destructor vtable, initializes both original
status words, updates the 32-bit global destructor reference
count and returns the original FAR this. **It does not call
ios::init**, unlike the separately recovered stctr2
ios(streambuf far*) overload. Original stctr1 and stctr2
were independently compared in CL.LIB before deriving the
new source; the omission of the base init call is grounded
by the distinct original 135-byte versus 153-byte CODE.

All **135 CODE and 12 initialized DATA bytes** match the original
Borland object. The full 54-byte native typed ios class RTTI
occupies CODE+81..134 and its DATA+0 symbolic pointer refers
to CODE+81. The original vtable slot at DATA+8 points to the
far ios destructor. All **six logical OMF relocation fields**
match original segment/site/kind/frame/target/addend, including
CODE+39 -> DATA+8 and the genuine new/reference-count calls.
Original _TEXTA/_DATA/_BSS, DATA-first GROUP, exact FAR public
and three ordered imports match. Literal Borland/TASM FIXUPP
packet chronology differs; full original raw OBJ identity
is not asserted. No original executable-byte fixtures,
NOP padding or post-assembly object rewrites are used.

After485 verifies the inherited after484 **692-source** carrier
and runs two fresh real TASM/TLIB/TLINK native rounds. Both
full decoded Japanese MAINL EXE/MAP equal the targets byte-for-byte
(67,372 EXE bytes, 677 ordered MZ relocations). Raw native
OBJ/LIB/EXE/MAP pairs, writer logs, source/driver hashes and
the original parent receipt are retained. The working CRT
reaches **693/893** source-linked original members,
**184,220 original-equal CODE bytes**, 200 contextual vendor
members. No full cold replay or Factory source credit is claimed.

Focused reviewer: scripts/review_th03_mainl_after485_work.py
(mode ios-default-constructor-rtti-boss);
tests: tests.test_mainl_after485_work.

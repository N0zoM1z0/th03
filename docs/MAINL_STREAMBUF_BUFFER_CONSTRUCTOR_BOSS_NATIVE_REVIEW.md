# Original streambuf(far buffer, length) constructor — after441

The full original Japanese Borland streambuf member stbctr2 (CL.LIB
slot **855**) is recovered as natural 8086 source in
[src/mainl/crt/stbctr2.asm](../src/mainl/crt/stbctr2.asm).
The far constructor conditionally allocates an original 38-byte object,
installs the real class virtual table, initializes the external far buffer
and its end pointer, preserves the native signed length test and original
16-bit offset-only addition, clears all remaining stream get/put pointer
fields and increments the 32-bit reference destructor count. Both the
negative/nonpositive length path and the failed allocation path retain
the exact native behavior.

Its entire **258 CODE bytes** and **52 initialized DATA bytes** are
original-equal. This includes the typed Borland streambuf RTTI record at
CODE+198, the genuine DATA+0 RTTI far pointer and eleven distinct symbolic
far virtual methods at DATA+8 through DATA+48. All **16 logical original
OMF FIXUPPs** match, including the constructor vtable relocation at
CODE+42 -> DATA+8 and RTTI at DATA+0 -> CODE+198. Segment definitions,
DATA-first GROUP, publics and imported function ABI also match. The
literal Borland-vs-TASM FIXUPP serialization still differs; complete raw
OBJ equality is **not** claimed. No target-byte arrays or patches.

The after441 producer inherits unchanged after440 native source receipts
and performs two new native TASM/TLIB/TLINK builds. Both complete Japanese
MAINL decoded EXE/MAP are byte-exact, preserving the 67,372-byte executable
and its **677 ordered MZ relocations**. The working CRT now has
**649/893** source-linked original members, **175,102** source-built CODE
bytes and **244** unchanged contextual vendor members. This is bounded
working-source progress only; no formal Factory acceptance or full cold
replay is claimed.

Focused review:
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after441_work.py streambuf-buffer-constructor-boss
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after441_work -v

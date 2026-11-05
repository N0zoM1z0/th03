# Original streambuf base destructor, far buffer cleanup and RTTI — after440

The original Japanese Borland `CL.LIB` member `stbdtr` (index 859) is
reconstructed as readable 8086 source in `src/mainl/crt/stbdtr.asm`.
Its far public `@streambuf@$bdtr$qv` decrements the Borland 32-bit
reference destructor count; for non-null objects it installs the true
DATA-backed vtable, checks the original owned-buffer flag and optionally
calls `@$bdla$qnv` to release the far character array, clearing the
ownership field afterwards. Depending on the original destructor flag,
it optionally calls `@$bdele$qnv` to free the far object. This is the
complete base-class destructor and original 16-bit calling convention.

The source produces **153/153 original CODE bytes** and the complete
**52 initialized DATA bytes**. CODE+93 contains genuine typed
`streambuf` RTTI; DATA contains a real symbolic RTTI reference, reserved
fields and the original eleven distinct virtual-function slots.
**All 17 logical original OMF FIXUPPs** match at their true locations,
including CODE+37 -> DATA+8, `delete[]` at CODE+55, optional `delete`
at CODE+83, the CODE-local destructor pointer at DATA+8, and all other
virtual methods. Public/import ABIs, segment definitions and DATA-first
GROUP match the live original. Literal FIXUPP record serialization still
differs from Borland; full original raw OMF program equality is not
claimed. No target byte arrays or patched OBJ files were used.

The after440 source-bound native builder validates the unchanged after439
647-source carrier and executes two fresh TASM/TLIB/TLINK rounds, with
complete writer logs, source hashes, and OBJ/LIB/EXE/MAP pairs retained.
Both full decoded Japanese MAINL EXE/MAP match the original byte-for-byte
(67,372-byte EXE and 677 ordered DOS MZ relocations). The working CRT
now covers **648/893** source-linked members, **174,844 original-equal
CODE bytes**, with **245** unchanged contextual vendor programs.
No full cold replay or independent Factory accepted-source proof is implied.

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after440_work.py streambuf-base-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after440_work -v
```

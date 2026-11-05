# Original ostream_withassign() constructor, adjustment thunk and RTTI — after419

Original Japanese Borland `CL.LIB` member `ostctr3` (index 808) is
reconstructed as natural 16-bit ASM in `src/mainl/crt/ostctr3.asm`.
Its far C++ public `@ostream_withassign@$bctr$qv` conditionally allocates
44 bytes, initializes its `ios` base and `ostream` subobject with genuine
far calls, sets the original two DATA-resident vtable positions and
increments the 32-bit original reference destructor counter.

The whole **349-byte CODE** is owned: CODE+0..130 contains the executable
constructor; CODE+131..142 is the actual 12-byte destructor `this`-pointer
adjustment thunk (`SS:[BX+4] -= 4` and a symbolic far JMP), not a magic
byte sequence. CODE+143, +229 and +283 contain the typed Borland class RTTI
for `ostream_withassign`, `ios` and `ostream`, including original field
layout, real inherited-type pointers, class names and external destructor
symbols. The **20-byte DATA** contains a far pointer to typed RTTI,
reserved words, the actual destructor/vtable pointer, vtable displacement
words and a final far reference to the CODE+131 thunk. The source uses
semantic instructions, `dw`/`dd` and natural `db` names only; no target
CODE blob or object patch provides equality.

Native TASM reproduces all **349 CODE and 20 initialized DATA bytes**,
original `_TEXTA`/`_DATA`/`_BSS` sizes, DATA-first group, mangled public
and seven ordered imports. **All 16 original logical OMF FIXUPPs** match
site, type, width, frame, target and addend, including two symbolic
DATA-offset immediates in instructions, internal RTTI references and three
DATA source pointers. TASM emits these records in an order different
from original Borland: literal FIXUPP sequence and raw library member
serialization equality are *not* asserted.

The incremental after419 producer validates the unchanged 605-source
after418 parent receipt, then executes two independent native
TASM/TLIB/TLINK rounds with full source-/driver-bound OBJ/LIB/EXE/MAP
and writer logs retained. Both whole original decoded Japanese MAINL
EXE/MAP reproduce byte-for-byte (67,372-byte EXE, 677 ordered DOS MZ
relocations). The working CRT reaches **606/893** source-linked members,
**168,411 original-equal CODE bytes**, and **287** unchanged contextual
vendor members. No full cold replay or Factory accepted-source credit.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after419_work.py ostream-withassign-default-constructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after419_work -v
```

# Original streambuf bulk read/write bosses — after405

The Japanese Borland `CL.LIB` members `stbdsgtn` (index 857) and `stbdsptn`
(index 858), absent from the actual 561-source inherited native CRT, are
recovered into readable 8086 ASM at `src/mainl/crt/stbdsgtn.asm` and
`src/mainl/crt/stbdsptn.asm`. These are complete `streambuf::do_sgetn`
(**184 CODE bytes**) and `streambuf::do_sputn` (**168 CODE bytes**) far
C++ implementations, not trivial imported-call veneers. They update the
original far stream-buffer get/put cursors, batch-transfer available bytes
with `_memcpy`, and fall back to virtual `underflow`/`overflow` through the
real Borland object vtable and per-character loops when buffer space runs
out. Their return counts, unchecked input bounds and original ABI remain.

Both maintained translation units produce their entire original CODE
payload (all **352 bytes**) and original `_TEXTA`/`_DATA`/`_BSS` segment
sizes, public mangled names, and ordered `_memcpy` external import. The
single far imported relocation of each reproduces its original **literal
ordered OMF FIXUPP**, including frame TARGET, type, site and addend
(CODE+62 for `stbdsgtn`, +49 for `stbdsptn`). TASM and original Borland
member-program record serialization still differ in other non-semantic
OMF details; whole raw original member-program equality is not claimed.

`scripts/build_th03_mainl_after405_work.py` binds the unchanged after404
source/driver/receipt chain, then executes two fresh actual TASM/TLIB/TLINK
producer rounds with complete native OBJ/LIB/EXE/MAP and phase logs
retained. Both full decoded Japanese MAINL.EXE and MAP match the original
byte-for-byte (67,372-byte EXE and 677 ordered MZ relocations).
Working-source CRT: **563/893** members and **164,202** original-equal
CODE bytes, with **330** unchanged contextual vendor members. This is
not a new full cold replay, packed-file source ownership proof or Factory
accepted-source credit.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after405_work.py two-streambuf-bulk-transfer-bosses
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after405_work -v
```

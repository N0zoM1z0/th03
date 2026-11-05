# Eight complete C++ stream, DOS file and PC-98/IBM sound leaves — after421

Eight previously contextual original Japanese Borland `CL.LIB` members
have been recovered as maintained natural 16-bit ASM translation units:
`sdbpbfl`, `ostopfx`, `ostflush`, `ostwrite`, `stbsbuf`, `flength`,
`dosfattr` and `ccomsond`. Their full **496 original CODE bytes** include
real C++ `stdiobuf::pbackfail` with `ungetc(FILE*)`, ostream prefix/tie
handling, virtual streambuf sync, buffered binary `ostream::write` with
proper ios error status, `streambuf::setbuf`, DOS `INT 21h` seek-based
file-length preservation, DOS `INT 21h` get/set file attributes and the
original two-way NEC/IBM sound/nosound machine multiplexer.

Each member's entire CODE, segment layout, true far/near ABI, public
and import identities and all logical OMF FIXUPP fields match its live
original Japanese CRT member. **Six** match literal original FIXUPP
record chronology (`sdbpbfl`, `ostopfx`, `ostflush`, `stbsbuf`, `flength`,
`dosfattr`); `ostwrite` and `ccomsond` retain exactly the original
logical relocation site, target, frame and addend, but Borland and TASM
serialize their records in different orders. The reviewer does not
normalize any frame or relocation target for this batch and does not
claim complete original library-member record serialization equality.
No original executable byte arrays or object patches are involved.

`scripts/build_th03_mainl_after421_work.py` validates the unchanged
607-member after420 source carrier and creates two fresh native
TASM/TLIB/TLINK rounds with complete raw OBJ/LIB/EXE/MAP and writer logs
retained. Both full Japanese decoded MAINL EXE and MAP remain byte-for-byte
original-equal (67,372-byte EXE, 677 ordered DOS relocations). The working
CRT now contains **615/893** source-linked original members,
**169,240 original-equal CODE bytes**, and **278** contextual vendor
members. This is not a full cold replay or Factory accepted-source credit.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after421_work.py eight-stream-dos-sound-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after421_work -v
```

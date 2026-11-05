# Ten complete Japanese CRT ABI, video and locale leaf programs — after398

This source-bound step replaces **ten previously contextual** original Japanese
Borland `CL.LIB` members, from actual original member indices and the live
inherited 538-source carrier: `readu` (near `_read`→`___read`), `writeu`
(near `_write`→`___write`), three C++ stream leaves `srbsync`, `stboflow`,
`stbpbfl`, three original IBM/NEC video leaves `cibmpbel`, `cnecpbel`,
`cibmwhxy`, `fnmerge` (far `_fnmerge`→`__makepath`) and `cconv` (far
`_localeconv` and initialized DATA public `__localeconvention`). All ten
have maintained independent 16-bit ASM source in `src/mainl/crt/`.

The complete original **126 CODE** and **59 initialized DATA** bytes now
come from natural code and symbolic data. `cconv` has ten actual far-pointers
to the original locale decimal/separator empty-string fields, eight genuine
`CHAR_MAX` sentinel bytes and a named `__localeconvention` DATA public.
A naive TASM `DUP` generated sparse LIDATA and failed the original complete
DATA materialization check; eight explicit sentinel bytes preserve real
LEDATA and the original full 59-byte DATA extent. The other members preserve
near/far returns, public offsets, segment ordering and import ABIs. `readu`
and `writeu` each have their complete three-byte near jump and exact framed
FIXUPP, not inferred far-call wrappers.

**OMF distinctions are explicit:** Six of the ten members preserve *literal
ordered* original FIXUPP fields (including those with zero fields). The
three external near video calls in `cibmpbel` (CODE+7), `cnecpbel` (+9)
and `cibmwhxy` (+7) retain identical instructions and target/site, but
original Borland chooses frame 5 (`TARGET`) and native TASM frame 0
(`CODE`). The scoped reviewer only permits that precise two-way difference
at those three sites and asserts no other differences. `cconv` matches all
11 logical relocated fields, including their frames and addends, but TASM
and original Borland order the DATA-pointer FIXUPP records differently.
Original full Borland member record-program serialization is not asserted.

The incremental after398 producer validates/reuses its unchanged after397
source-bound receipt, replacing exactly these ten members in two fresh
TASM/TLIB/TLINK native rounds. Both complete Japanese decoded MAINL EXE and
MAP are byte-for-byte original-equal (67,372-byte EXE with 677 ordered DOS
MZ relocations). Maintained working-source CRT: **548/893 members**,
**162,203 original-equal CODE bytes**, and **345** unchanged contextual
vendor members. This is not a new full cold replay, packed-file source
unit acceptance, or Factory approval.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after398_work.py ten-abi-video-locale-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after398_work -v
```

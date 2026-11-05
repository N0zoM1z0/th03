# Eight original Japanese PC-98/IBM dispatch and DOS ABI leaf members — after403

Eight previously contextual Japanese Borland `CL.LIB` members are now
linked from maintained ASM translation units in `src/mainl/crt/`:
`ccompbel` (NEC/IBM bell), `ccomwhxy` (hardware WHEREXY), `ccomcrsr`
(cursor shape), `ccomdely` (delay), `ccomtxmd` (text mode), `ccomgtxy`
(cursor position), `wherexy` (two C far coordinate APIs), and `isatty`
(the original DOS INT 21h IOCTL 4400h entry). None was source-linked in the
actual inherited 552-member after402 native CRT carrier. The seven
PC-98/IBM dispatch sources are new; `isatty.asm` already existed. Its
maintained CODE and original GROUP record were independently reassembled
and checked equal, so the correct existing `isatty` source was preserved
instead of being rewritten merely to claim new authorship. Its historical
`stdio_layout.inc` include is now staged by this native driver and the
include hash is explicitly bound by the build/review receipts.

All **295 original CODE bytes** match the genuine original member programs.
This includes the original machine-type dispatch based on `___conio_type`,
NEC/IBM near/far calls, `__GOTOXY`'s original Pascal far `retf 4`, zero-return
behavior for unknown machines, `_wherex`/`_wherey`'s original `__video`
coordinate offsets, and the DOS segment-level `_isatty` IOCTL. The complete
original segment sizes, public offsets, ordered imports and GROUP membership
were reviewed for all eight. No original CODE arrays, synthetic byte padding
or object patches are used.

**OMF limits are explicit:** `isatty` has no FIXUPPs and matches its literal
ordered original fields. The other seven preserve complete original logical
site/target/width/addend values; their TASM FIXUPP record chronology differs
from Borland. Four near external call sites differ only in OMF frame method:
`ccomwhxy` CODE+10/+22 and `wherexy` CODE+3/+22 use original Borland
TARGET-frame method 5 versus TASM CODE-frame method 0. The affected scope
normalizes **only these four attested sites**, checking the original and TASM
frame alternatives, each exact target and no other field differences.
It does not claim literal ordered FIXUPP equality or full Borland
record-program serialization for those members.

The source-bound after403 producer validates the unchanged after402 parent
and performs two actual native TASM/TLIB/TLINK rounds, retaining complete
source/driver-bound OBJ/LIB/EXE/MAP vectors and logs. In both rounds the
whole Japanese decoded MAINL EXE and MAP remain original-equal byte for
byte (67,372-byte MZ EXE, 677 ordered DOS relocations). This brings the
working CRT to **560/893** source-built members, **163,558 original-equal
CODE bytes**, and **333** unchanged vendor context. No full cold replay,
canonical packed-file acceptance or Factory ownership credit was asserted.

Focused review and tests:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after403_work.py eight-machine-dispatch-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after403_work -v
```

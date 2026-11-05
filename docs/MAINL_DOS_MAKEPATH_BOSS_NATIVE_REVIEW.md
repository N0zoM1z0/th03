# Full Japanese DOS `_makepath` path-composition boss — after399

The original Borland `CL.LIB` member `makepath` (index 256) is recovered
as natural 8086 source in `src/mainl/crt/makepath.asm`: **255 complete CODE
bytes**, the real far `__makepath` interface (exported symbol `__makepath`),
no implicit DATA/BSS materialization, and three original ordered imports
`_strlen`, `__stpcpy`, `___path_issbcs`. It composes a drive letter and
colon, far directory, filename and optional extension; it explicitly checks
for `\\` or `/` directory separators, then invokes the original Japanese
SBCS predicate for the final directory byte before deciding whether to
insert a backslash. This preserves the original multibyte-path behavior
rather than replacing it with a generic libc implementation.

The original complete 255 CODE bytes, all five actual imported far-call
relocation sites (72,109,130,172,231), original target/frame/addend
fields, full public/import ABI and `_TEXT`/`_DATA`/`_BSS` layouts all
match. Native TASM and original Borland emit different literal FIXUPP
record order; original member OMF serialization is **not claimed exact**.
The full source CODE and logical relocations are exact; no target machine
byte arrays or post-assembly binary manipulation were used.

The incremental after399 native builder validates/reuses the 548-member
after398 source-bound receipt and performs two fresh TASM/TLIB/TLINK
producer rounds with complete raw OBJ/LIB/EXE/MAP and writer logs retained.
Both full Japanese decoded EXE and MAP match the originals byte-for-byte,
including the original 67,372-byte executable and all 677 ordered DOS
MZ relocations. This increases the maintained working-source CRT to
**549/893 members**, **162,458 original-equal CODE bytes**, with **344**
untouched original contextual vendor members. No full cold replay, packed
file source acceptance or Factory proof of whole-product ownership is claimed.

Focused commands:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after399_work.py dos-makepath-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after399_work -v
```

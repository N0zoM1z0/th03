# Original Japanese DOS `_mktemp` enumeration boss — after400

The original Japanese Borland `CL.LIB` member `mktemp` (index 264) is fully
reconstructed in maintained 16-bit assembly `src/mainl/crt/mktemp.asm`.
This is not a modern POSIX `mkstemp`: the real original checks the final
six characters of the far string against an initialized **`XXXXXX\0`**
DATA template, replaces the third character with a period, and performs
five nested `'A'..'Z'` loops for positions 0,1,3,4,5, checking each candidate
through the far DOS `_access` function. It returns the far original buffer in DX:AX
on the first nonexistent filename or zero DX:AX if no candidate succeeds.
Original unchecked 16-bit arithmetic, all branches and loop nesting are
retained; no modern sanitization or filename generator was substituted.

Source TASM reproduces the **253-byte original CODE** and the full
**7-byte initialized DATA**, native three-segment sizes 253/7/0,
public `_mktemp` at CODE+0, the ordered imports `_strcmp`, `_strlen`,
`_access` and the exact original group record. All four literal OMF
*logical relocation fields* (sites 15,50,58,175, with original frames,
targets and addends) agree. Original Borland and TASM place those FIXUPPs
in different *record order*, so raw original member-program serialization
is explicitly unclaimed. Code remains genuinely authored instructions and
the literal source template is semantic initialized DATA, not CODE padding.

The after400 native producer inherits the unchanged original-source after399
receipt and runs two fresh actual TASM/TLIB/TLINK rounds, retaining complete
raw OBJ/LIB/EXE/MAP outputs, writer logs and their source/driver hashes.
Both complete Japanese decoded MAINL EXE/MAP remain byte-for-byte equal to
the originals (67,372-byte EXE, 677 ordered DOS MZ relocations). The working
CRT reaches **550/893** source-built members, **162,711 original-equal CODE
bytes** and **343** unchanged contextual vendor members. This bounded working
CRT proof does not claim packed-original unit acceptance or Factory approval.
No full cold replay was run.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after400_work.py dos-mktemp-enumeration-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after400_work -v
```

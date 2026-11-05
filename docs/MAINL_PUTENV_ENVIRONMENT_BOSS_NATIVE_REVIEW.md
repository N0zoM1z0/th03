# Full original Japanese Borland DOS `_putenv` environment boss — after402

Original Japanese `CL.LIB` member `putenv` (index 272) is recovered in
`src/mainl/crt/putenv.asm` as complete native 8086 source (**261 CODE bytes**).
It scans an incoming far `NAME=VALUE` parameter, compares variable names
against the original far environment-string vector, replaces a matching
nonempty entry or shifts the vector to erase an empty one. For a new name,
it calculates the 16-bit vector slot/size, allocates a larger far table
through `_malloc` when necessary, copies previous entries with `rep movsb`,
updates the `__environ` pointer words, releases the old vector with `_free`,
and writes the new far pointer. No modern libc policy or defensive change
replaces the original unchecked control flow.

Original `_TEXT`/`_DATA`/`_BSS` = 261/0/0, `DGROUP` BSS-first record
`08ff03ff02`, public `_putenv`, ordered imports `_free`, `_malloc`,
`__environ`, `__envSize` and **all ten literal ordered original Borland
FIXUPPs** (not merely logical sites) match. These cover original
TARGET-framed DATA variables and imported far calls. Actual native TASM
object-program serialization beyond those OMF fields still differs, and
is not falsely claimed equal.

The bounded after402 builder validates the unchanged 551-member after401
source-bound parent and executes two fresh native TASM/TLIB/TLINK rounds,
retaining both complete raw OBJ/LIB/EXE/MAP vectors and phase logs. Both
whole original decoded Japanese MAINL EXE/MAP are byte-for-byte equal
(67,372-byte EXE with 677 DOS MZ ordered relocations). Working CRT becomes
**552/893** source-built original members, **163,263 CODE bytes**, with
**341 untouched vendor** programs. This is not a full cold replay or
Factory/packed-file source acceptance.

Focused commands:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after402_work.py dos-putenv-environment-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after402_work -v
```

# Twelve original DOS syscall and memory leaf programs — after407

Twelve previously contextual members of the **active Japanese MAINL source
carrier** are now compiled from maintained ASM: `allocmem`, `freemem`,
`setblock`, `dossetbl`, `getcurdi`, `getftime`, `setftime`, `bdosptr`,
`_chmoda`, `chmoda`, `ioctl` and `keep`. The active source count changes
**564→576/893**, replacing **396 complete original CODE bytes**. These
are real 16-bit DOS register/interrupt wrappers, including allocation and
resize errors, directory and file timestamp operations, 21h/43h and 44h
IOCTL/attribute calls, and terminate-and-stay-resident 21h/31h. All
original near/far ABI returns and stack cleanup are preserved. There are
11 new `.asm` translation units; the pre-existing `setblock.asm` has been
retained and newly source-linked only after independent review.

**Important independently verified source-provenance nuance:** The active
inherited MAINL CRT's `setblock` member (index 363) and the installed
`TC4/LIB/CL.LIB`/standalone vendor `setblock` OBJ have identical complete
CODE, public/imports, sizes and original ordered logical FIXUPP fields, but
their **GRPDEF differs**: the active target/maintained `setblock.asm` is
`08ff02ff03` (DATA-first), while the alternate installed vendor source
is `08ff03ff02` (BSS-first). An initial attempt to “fix” the maintained
GROUP to the installed variant would have invalidated the frozen historical
cold source graph and mismatched the active target. We preserved the
unmodified maintained `setblock.asm`, retained the actual active target
GROUP and added a *strict specific provenance-difference check*, requiring
all the other complete fields to match. We do not conflate these two
same-named original-context programs or repeat full cold replay.

The remaining eleven members match their source-target CODE and segment
GROUPs. For all twelve, the original source/compiled CODE is byte-identical,
with the exact original public/import identities and relocation locations.
**11 of 12 members reproduce literal ordered Borland FIXUPPs**; `dossetbl`
retains the original near `__DOSERROR` call at CODE+22, but Borland chose
TARGET-frame method 5 while TASM emits CODE-frame method 0. The reviewer
normalizes *only this original-known frame difference* while asserting the
complete exact target, site, width, addend and every other member field.
No full original raw library-member OMF record-program equality is claimed.

`scripts/build_th03_mainl_after407_work.py` validates the existing after406
source-bound parent receipt, then runs two fresh TASM/TLIB/TLINK producer
rounds with all original native OBJ/LIB/EXE/MAP and writer logs preserved.
Both complete Japanese decoded MAINL EXE/MAP are byte-for-byte original-equal
(67,372-byte EXE, 677 ordered DOS MZ relocations). The working CRT has
**576/893** source-linked members, **164,888 original-equal CODE bytes**
and **317** unchanged contextual library members. No packed-file canonical
credit, independent pristine-dump provenance, Factory accepted-source proof
or full cold replay is implied.

Focused tests:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after407_work.py twelve-dos-syscall-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after407_work -v
```

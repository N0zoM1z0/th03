# Original fstreambase::setbuf virtual filebuf and ios state — after520

Japanese Borland CL.LIB member fssbuf (slot 725) is now
maintained as [natural 8086 source](../src/mainl/crt/fssbuf.asm).
The complete 91-byte FAR fstreambase::setbuf uses the
authentic FAR filebuf pointer at object+4, dispatches
setbuf through the native virtual table call at +4,
then handles the returned FAR pointer by invoking
the original ios::clear on success or ios::setstate
with failure flag 2. The 16-bit stack, hidden this
pointer and all virtual-call argument ordering agree
with the original; this is not a host stream wrapper.

**All 91 original CODE bytes**, the sole FAR public name,
two real imported ios helper symbols, empty DATA/BSS and
original segment/GROUP definitions match the original.
Both logical original OMF FIXUPPs at CODE+60 and +78
match symbolic targets, frames, widths and addends.
Borland/TASM literal FIXUPP packet ordering differs,
so raw original OBJ record equality is not claimed.
No code-byte fixtures, filler or OBJ patches were used.

after520 revalidates the unchanged after519 **727-source**
CRT carrier and produces two native TASM/TLIB/TLINK rounds.
Both complete decoded Japanese MAINL EXE and MAP equal
the pinned originals byte-for-byte (67,372 EXE bytes,
677 ordered MZ relocations). Both complete OBJ/LIB/
EXE/MAP rounds, writer logs and source/driver hashes
are preserved. Working CRT reaches **728/893** complete
source-linked members, **194,292 original-equal CODE
bytes**, leaving 165 contextual vendor members.
No full cold replay or formal Factory source acceptance.

Independent reviewer:
scripts/review_th03_mainl_after520_work.py
(mode fstreambase-virtual-setbuf-ios-state).
Tests: tests.test_mainl_after520_work.

# Original far strtok with persistent BSS cursor — after472

The original Japanese CL.LIB member fstrtok (index **460**)
is recovered as natural [8086 source](../src/mainl/crt/fstrtok.asm),
including its full **203 CODE bytes** and real **four-byte BSS
state**, not a stateless strchr/strtok substitute.

The FAR __fstrtok entry preserves the original static
segment:offset cursor across calls; an incoming far string
resets this cursor, and null input resumes from it.
The source implements both nested delimiter scans, the actual
NUL-detection logic, token termination by writing zero at the
delimiter position, and the original offset-only cursor increments.
It preserves the 8-byte stack scratch, ES far-pointer comparisons,
and original FAR return value and all control flow. Strict
byte comparison detected a semantic source branch mistake at
CODE+80: the original empty delimiter test skips directly
to the later cursor-empty test, not back through the prior
delimiter loop. This was fixed using an explicit source label.

All original CODE payload, zero initialized DATA, four-byte BSS
SEGDEF and the complete public/import/group layout match.
All **12 original logical OMF FIXUPPs** point symbolically
to the true BSS segment 3, including the two BSS+2 segment
references at CODE+24/+113. All sites, widths, frame methods,
target indices and addends match exactly. Borland and TASM
emit their FIXUPP records in different literal orders and
whole vendor OBJ equality is not claimed. There are no
executable target-byte fixtures or post-assembly patches.

After472 validates its inherited after471 679-source native
carrier and runs two fresh real TASM/TLIB/TLINK rounds.
Both complete decoded Japanese MAINL EXE/MAP outputs are
byte-for-byte original-equal (67,372 EXE bytes and 677
ordered DOS MZ relocations), with full OBJ/LIB/EXE/MAP
pairs, logs and source hashes retained. Working CRT now
has **680/893** original source-linked CRT members,
**182,030 original-equal CODE bytes**, 213 contextual vendor
members. These are scoped working-source results, not full
cold replay or Factory formal accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after472_work.py
(mode far-tokenizer-persistent-bss-boss).
Tests: tests.test_mainl_after472_work.

# Original istream::do_get streambuf underflow and EOF handling — after503

Japanese Borland CL.LIB member istdget (slot 755) is fully
recovered in [maintained 8086 source](../src/mainl/crt/istdget.asm).
The complete 158-byte FAR @istream@do_get$qv dereferences
the original ios/streambuf FAR pointers, checks current buffer
position against end, performs a real streambuf vtable
underflow FAR call when needed, and otherwise consumes
one byte through the native buffer data segment and cursor.
It handles EOF by passing actual ios state 3 to the real
FAR @ios@setstate$qi and increments the original input
counter on success. All original register/segment/stack
semantics are retained.

Every one of the **158 original CODE bytes**, the sole
FAR public name and CODE offset, single ordered import,
empty DATA/BSS and original DATA-first GROUP match.
Its only **literal ordered original OMF FIXUPP** at
CODE+133 is an unchanged four-byte FAR ios::setstate call
with the exact original frame, target and addend.
No target opcode fixture or post-assembly patch was used.

After503 verifies the unchanged after502 710-source CRT
parent and performs two fresh TASM/TLIB/TLINK native
rounds. Both decoded Japanese MAINL EXE and MAP exactly
match the original target files (67,372 EXE bytes and
677 ordered MZ relocations). Both raw OBJ/LIB/EXE/MAP
rounds, writer logs, source/driver hashes and parent
receipt remain protected. Working CRT reaches **711/893**
source-linked original members, **186,811 original-equal
CODE bytes**, 182 remaining contextual vendor members.

This is scoped working-source evidence, not full cold replay
or Factory accepted-source credit. The separate h_ldiv
twelve-entry core remains a documented unaccepted source
candidate with a MAP-only alias-order difference and was
not included in the after503 source count.

Focused reviewer: scripts/review_th03_mainl_after503_work.py
(mode istream-virtual-underflow-do-get-boss).
Test: tests.test_mainl_after503_work.

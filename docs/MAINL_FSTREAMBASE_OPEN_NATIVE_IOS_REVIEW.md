# Original fstreambase::open mode handling and ios state — after519

Japanese Borland CL.LIB member fsopen (slot 724) has been
fully recovered as [natural 8086 source](../src/mainl/crt/fsopen.asm).
The original 105-byte FAR fstreambase::open implementation
adjusts the Borland file mode flags, checks existing buffer state,
calls the native FAR filebuf::open with the real pointer and
mode arguments, then uses the original FAR ios::clear to update
stream failure flags. The original Borland this-pointer/stack
ABI and unchecked behavior are retained.

**All 105 original CODE bytes**, the single FAR public and
two real imported symbols match. All two logical OMF
relocations match the original field kinds, widths, frame
methods, addends and imported identities: CODE+67 to
filebuf::open and +94 to ios::clear. TASM/Borland record
chronology differs, so no identical raw OBJ or literal
ordered FIXUPP chronology is claimed. No opcode arrays,
artificial padding or target OBJ modifications were used.

after519 independently validates the unchanged after518
**726-source** CRT parent, then creates two fresh native
TASM/TLIB/TLINK rounds and retains both complete
OBJ/LIB/EXE/MAP vectors, writer logs, source/driver
hashes and parent receipt. Both decoded Japanese MAINL
EXE/MAP match original byte-for-byte (67,372 EXE bytes,
677 ordered MZ relocations). Working CRT advances to
**727/893** complete source-linked members, **194,201
original-equal CODE bytes**, leaving 166 contextual vendor
members. This is local source parity, not Factory acceptance
or a full cold replay.

Reviewer: scripts/review_th03_mainl_after519_work.py
(mode fstreambase-open-native-ios-state).
Tests: tests.test_mainl_after519_work.

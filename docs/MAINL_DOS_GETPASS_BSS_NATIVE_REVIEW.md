# Original DOS no-echo getpass and nine-byte BSS — after497

Original Japanese Borland CL.LIB getpass (slot **354**) is fully
recovered in [maintained 8086 source](../src/mainl/crt/getpass.asm).
It contains an actual private FAR DOS console helper at CODE+0
and exported FAR _getpass at CODE+24. The public routine prints
the caller's prompt through the real __streams stderr handle
and far _fprintf, flushes through the original _bdos private
helper, reads with DOS direct console input without echo,
limits the buffer to eight characters, inserts a NUL byte
and prints the native CR/LF terminator.

All **168 original CODE bytes**, the three typed prompt DATA
bytes %s followed by a NUL, the genuine nine-byte uninitialized
BSS password buffer, the private/public FAR ABI and three
ordered imports match original CL.LIB. All nine original
logical OMF relocation fields match their original
site, target, frame, kind, width and addend, including
the original __streams+40 stderr handle, the typed DATA
prompt at DATA+0 and BSS+0 password buffer. Borland/TASM
literal FIXUPP chronology differs; whole vendor OBJ
record identity is not claimed. No copied executable
byte arrays, filler or object patching is used.

After497 checks its complete after496 **704-source**
carrier before two fresh native TASM/TLIB/TLINK rounds.
Both decoded Japanese MAINL EXE/MAP exactly match their
pinned original files (67,372 EXE bytes, 677 ordered MZ
relocations). All raw OBJ/LIB/EXE/MAP artifacts, logs,
source/driver hashes and parent receipt are retained.
Working CRT **705/893** source-linked original members,
**185,995 source CODE bytes**, 188 remaining vendor members.
No full cold replay or formal Factory source acceptance.

Focused reviewer: scripts/review_th03_mainl_after497_work.py
(mode dos-getpass-noecho-bss-boss);
tests: tests.test_mainl_after497_work.

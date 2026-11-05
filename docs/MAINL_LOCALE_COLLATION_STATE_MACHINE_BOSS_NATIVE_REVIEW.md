# Complete locale strcoll and LevelCollate state machine — after447

The original Japanese Borland library member _strcoll (slot **191**)
was independently identified as **unsourced** in the live after446 CRT
source carrier. This is not the already maintained short C-locale
strcoll module. It is a separate, full locale-sensitive collation
implementation with two exported procedures, __strcoll and the near
_LevelCollate, recovered as readable
[8086 source](../src/mainl/crt/_strcoll.asm).

The real algorithm loads locale rules and per-level weights, walks
both input strings using the imported GetNextKeyWeight, compares
primary and secondary weights, retains deferred weak differences,
handles terminal/expansion flags, and advances through the locale
strength levels. The original DS/ES swapping sequence, signed
one-byte result, local helper calls and loop branch widths are
preserved, including the *two* real near external weight calls.
This is not a substitute for the locale-aware implementation.

The entire **265 CODE bytes** and all three original logical **and
literal** OMF FIXUPPs match: the far locale pointer at CODE+12 and
the two near GetNextKeyWeight calls at +113 and +129. The exact
publics, seven original import records, DATA-only group, and
zero-length third STRCOLL_TEXT CODE segment are retained.
TASM originally chose alternate legal XCHG register encodings:
expressing the commutative operands in reverse made the natural
source emit the **actual original instruction bytes** without
padding, target-byte arrays or object patches. Full Borland OMF
program record serialization is not separately claimed.

After447 validates the complete after446 654-source native parent
and performs two fresh source-bound TASM/TLIB/TLINK rounds,
preserving raw OBJ/LIB/EXE/MAP, writer logs and source hashes.
Both full Japanese decoded MAINL EXE/MAP are byte-for-byte equal
to the target: **67,372 EXE bytes, 677 ordered MZ relocations**.
Working CRT: **655/893 source-linked original members, 176,421 CODE
bytes**, 238 remaining contextual vendor members. No full cold
replay or new Factory accepted-source credit is implied.

Focused reviewer: scripts/review_th03_mainl_after447_work.py,
mode locale-collation-state-machine-boss.
Tests: tests.test_mainl_after447_work.

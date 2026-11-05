# Original DOS clock() and initialized CRT baseline — after500

The Japanese Borland CL.LIB clock0 member (original slot 11)
is maintained as [native 8086 source](../src/mainl/crt/clock0.asm).
It consists of the complete FAR _clock at CODE+0 and private
FAR CRT initializer at CODE+68. Both invoke the real
Borland __ftime, capture the original timestamp and millisecond
fields and compute elapsed milliseconds through the authentic
near 32-bit N_LXMUL@ helper. Signed millisecond subtraction
and 32-bit return registers reproduce the original ABI.

The **113 CODE bytes**, six truly uninitialized BSS bytes
and six real INITDATA bytes are original-equal. INITDATA
contains original priority 1F01h and a symbolic FAR
CODE+68 initializer pointer. All **ten logical OMF fields**
match their original sites, targets, widths and addends.
The only Borland-vs-TASM difference is N_LXMUL@ at CODE+40:
original target-frame method 5 versus TASM CODE-frame
method 0. This exact site and import are locked and checked.
Other BSS and INITDATA FIXUPPs match fully. Raw original
Borland OBJ serialization and literal packet ordering
are not claimed; there are no target-opcode fixtures.

After500 checks its unchanged after499 707-source native
carrier, then runs two fresh TASM/TLIB/TLINK rounds with
all raw OBJ/LIB/EXE/MAP outputs, logs and source/driver
hashes retained. Both complete decoded Japanese MAINL
EXE and MAP are byte-exact, including the 67,372-byte
EXE and 677 ordered MZ relocations. Working CRT:
**708/893** original source-linked members, **186,434
source CODE bytes**, 185 contextual vendor members.
This is scoped source evidence, not a full cold replay
or Factory accepted-source credit.

Reviewer: scripts/review_th03_mainl_after500_work.py
(mode dos-clock-baseline-initdata-leaf).
Tests: tests.test_mainl_after500_work.

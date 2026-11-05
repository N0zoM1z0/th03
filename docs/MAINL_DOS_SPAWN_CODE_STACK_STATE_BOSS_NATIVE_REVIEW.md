# Original DOS spawn, saved SS:SP and PSP execution boss — after482

The Japanese original Borland CL.LIB spawn member (index **367**)
is now maintained as native [8086 source](../src/mainl/crt/spawn.asm).
It is the complete original near __spawn at CODE+4 with true
DOS INT 21h AX=2901h parameter scanning, copying the DOS command
tail into PSP:80h, AX=4B00h process execution, saving/restoring
SS:SP around the DOS exec, and calling the actual near __IOERROR
or DOS AX=4D00h child exit-status interface as appropriate.
The original DS/ES/BP/interrupt-flag/stack register transitions
are retained without introducing modern process abstractions.

Importantly this is a **198-byte CODE segment but only CODE+4..197
(194 bytes) was originally materialized as Borland LEDATA**. Its
first four bytes are genuine live CS-resident saved SP/SS words
used around EXEC, *not* initialized 0, padding, or executable
instructions. The source declares two typed DW ? words and
TASM produces precisely the original LEDATA starting at +4.
A first source draft initialized them with DW 0, which
incorrectly materialized CODE+0..3 despite a superficial
matching full zero-filled byte image. The original exact
LEDATA coverage detected this and was repaired in source.

Original segments are only _TEXT (198 CODE) and _DATA
(zero DATA); GROUP is 06ff02, with no _BSS SEGDEF.
The original near public, exact two imports __IOERROR and
__psp, **seven literal ordered OMF FIXUPPs** and their
frames/targets are original-equal: PSP segment references
at CODE+92/+124, four truly symbolic CODE SS:SP
relocations at +145/+150/+158/+163, and the near
IOERROR at +182. The full CODE payload including its
unmaterialized region and all native group/segment records
are reviewed, without code arrays or OMF patching.

After482 verifies its complete after481 689-source parent,
then runs two fresh native TASM/TLIB/TLINK rounds and
retains all raw OBJ/LIB/EXE/MAP files, writer logs
and source/driver/parent receipt hashes. Both full decoded
Japanese MAINL EXE/MAP match their original target files
(67,372 EXE bytes, 677 ordered MZ relocations). The working
CRT advances to **690/893** original source-linked members
and **183,737 CODE bytes**, with 203 contextual vendor
members. No full cold replay or formal Factory credit
is implied.

Focused reviewer: scripts/review_th03_mainl_after482_work.py
(mode dos-exec-spawn-segment-stack-boss);
tests: tests.test_mainl_after482_work.

# Original DOS dup and dup2 with FAR exitclose callbacks — after508

Japanese Borland CL.LIB member dup2 (slot 40) has been
fully recovered as [maintained 8086 source](../src/mainl/crt/dup2.asm).
Its two FAR exported functions, _dup2 at CODE+0 and _dup
at CODE+59, call the actual DOS INT 21h AH=46h / 45h handle
duplication services. The source copies the true __openfd
descriptor word flags to the returned/new handle, installs
the real mutable FAR __xclose callback in __exitopen and
propagates DOS errors through near __IOERROR, preserving
the original 16-bit register and caller-stack ABI.

All **116 original CODE bytes**, two public names/offsets,
four ordered imports, original DATA-before-BSS GROUP and
zero DATA/BSS match the Japanese CL.LIB member. All **14
literal ordered original OMF FIXUPPs** are identical, including
the paired segment/offset symbolic __exitopen/__xclose
references at CODE+37/+39/+43/+45 and +94/+96/+100/+102,
plus both original near __IOERROR references.
An initial source hypothesis had the GROUP members reversed;
original OMF evidence exposed it and the source declaration
was corrected before final native integration. No executable
target-byte arrays or object rewriting were used.

After508 independently verifies the retained after507 715-source
parent and performs **two new real TASM/TLIB/TLINK rounds**.
Both complete decoded Japanese MAINL EXE and MAP are byte-for-byte
original-equal (67,372 EXE bytes and all 677 ordered DOS MZ
relocations). Complete native OBJ/LIB/EXE/MAP output vectors,
writer logs, source/driver hashes and the parent receipt are
retained. Working CRT reaches **716/893** complete original
source-linked members, **187,412 source CODE bytes**, with 177
contextual vendor members. This is bounded working-source
evidence, not a full cold replay or formal Factory acceptance.

Focused reviewer: scripts/review_th03_mainl_after508_work.py
(mode dos-dup-dup2-close-callback-boss).
Tests: tests.test_mainl_after508_work.

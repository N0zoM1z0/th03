# Original ios::iword FAR user-word slot and usersize — after507

The Japanese Borland CL.LIB member stiword (slot 880) is
now maintained as natural [8086 source](../src/mainl/crt/stiword.asm).
It implements the complete 97-byte FAR ios::iword(int)
routine, not a stub. It validates the original global usercount,
checks the ios object array size at +26h, calls the actual FAR
ios::usersize when the requested slot is not present,
then returns the correctly offset 32-bit user-word slot
as a FAR pointer. Invalid or out-of-range positions use a
separate true four-byte initialized DATA sentinel.

All **97 CODE and four DATA bytes**, native public entrypoint,
two ordered imports, and DATA-first original GROUP match.
All four logical original OMF reference fields match:
global usercount at CODE+12, local DATA sentinel at
CODE+22/+68, and FAR usersize expansion at CODE+46.
Literal Borland/TASM FIXUPP packet chronology differs,
so full raw original OBJ identity is not claimed.
The original iword module was independently compared to
the separately completed pword overload; both retain their
own public symbols and original library member positions.

After506 validates the complete after506 **714-source** carrier
and performs two independent native TASM/TLIB/TLINK rounds.
Both decoded Japanese MAINL EXE/MAP equal their original
targets byte-for-byte (67,372 EXE bytes; 677 ordered MZ
relocations). All raw OBJ/LIB/EXE/MAP outputs, logs and
source/driver/parent receipt hashes are retained.
Working CRT: **715/893** complete source-built original
members, **187,296 CODE bytes**, and 178 contextual vendor
members. No cold replay or formal Factory source credit is
claimed.

Reviewer: scripts/review_th03_mainl_after507_work.py
(mode ios-iword-usersize-array-slot-boss).
Test: tests.test_mainl_after507_work.

# Complete original PC-98/IBM conio text dispatch boss — after464

The Japanese Borland CRT member ccomgptx (original CL.LIB index **512**)
is now maintained as readable [8086 source](../src/mainl/crt/ccomgptx.asm).
It provides three complete FAR APIs: _gettext (CODE+0), _puttext
(CODE+74), and __getputtextsize (CODE+148). Each independently checks
the original conio_type word, dispatches to the correct NEC (type 2)
or IBM (type 1) far native backend with its exact 16-bit parameter
order and stack cleanup, and returns zero for unsupported consoles.
The text rectangle operations use six pushed argument words; the
size query uses four. No cross-platform substitute behavior was added.

The entire **210 original CODE bytes**, zero DATA/BSS, true
_TEXT/_DATA/_BSS segment/GROUP declaration, the complete three FAR
PUBLIC symbols, seven ordered imports, and all **12 logical original
OMF FIXUPPs** match exactly. The six type checks target the true
___conio_type and the other six far FIXUPPs point to the matching
___nec_gettext, ___nec_puttext, ___nec_getputtextsize,
___ibm_gettext, ___ibm_puttext and ___ibm_getputtextsize names.
The native TASM/Borland FIXUPP packet chronology differs; full raw
original OBJ record equality is not claimed. No machine-code byte
fixtures or post-assembly patches are used.

After464 validates the retained after463 671-source carrier and
performs two fresh real native TASM/TLIB/TLINK rounds with full
OBJ/LIB/EXE/MAP outputs, writer logs and hashes preserved. Both full
Japanese decoded MAINL EXE/MAP match their targets (67,372 EXE bytes,
677 ordered DOS MZ relocations). The working CRT now contains
**672/893** original source-linked members, **180,440 CODE bytes**,
with 221 contextual vendor members. This is scoped working source,
not a full cold replay or new Factory accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after464_work.py
(mode pc98-ibm-conio-text-dispatch-boss);
tests: tests.test_mainl_after464_work.

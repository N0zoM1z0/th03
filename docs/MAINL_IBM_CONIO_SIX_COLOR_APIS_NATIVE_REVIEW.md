# Original six IBM console color/attribute FAR APIs — after490

Japanese Borland CL.LIB member cibmcolr (slot 522) has been
recovered as natural [8086 source](../src/mainl/crt/cibmcolr.asm).
This is not just an IBM color stub: all six FAR entrypoints are
complete, namely ___ibm_textcolor (CODE+0), ___ibm_textbackground
(+43), ___ibm_textattr (+104), ___ibm_highvideo (+129),
___ibm_lowvideo (+139) and ___ibm_normvideo (+149).

The source actually updates the native Borland __video text-color
word, selects the original 70h/F0h and 8Fh/0Fh masks based on the
__video+13 mode flag, handles shift/bit-preserving background
selection and exposes both intensity-bit and default-color
operations. All eleven original references use the true
__video+4, +6 and +13 locations and the original 16-bit FAR ABI.

The **160 CODE bytes**, public offsets, single ordered __video
import, original three-segment/GROUP definition and empty DATA/BSS
are identical to CL.LIB. All **eleven logical OMF FIXUPPs**
match original sites, kinds, frames, widths, targets and addends.
Borland vs native TASM literal FIXUPP chronology is different,
and raw original OBJ-program record equality is not claimed;
the source contains no copied executable byte fixtures or
post-assembly patches.

After490 checks the unchanged after489 697-source carrier,
performs two fresh TASM/TLIB/TLINK native rounds, and keeps
all raw OBJ/LIB/EXE/MAP outputs, writer logs and source/driver
hashes. Both complete decoded Japanese MAINL EXE/MAP match
the original files byte-for-byte: 67,372 EXE bytes and
677 ordered MZ relocations. The working CRT reaches
**698/893 source-linked original members**, **184,995
original-equal CODE bytes**, with 195 contextual vendor
members. No full cold replay or Factory source acceptance
is implied.

Focused reviewer: scripts/review_th03_mainl_after490_work.py
(mode ibm-conio-six-color-entrypoints).
Tests: tests.test_mainl_after490_work.

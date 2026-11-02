# Original DOS strftime: 1,256 CODE, 18 DATA, 52-source Japanese MAINL

The fixed Japanese Borland DOS CRT strftime member298 now has a
maintained, non-patched native 8086 source in
src/mainl/crt/strftime.asm. The actual 1,256-byte CODE segment
contains 1,168 executable 8086 instruction bytes (448 real
instructions), followed by **two distinct real 44-byte static
CODE tables**: 22 format-letter WORDs and 22 relocation-bearing
near jump target WORDs. A further 18 genuine initialized DATA
bytes define seven NUL-terminated formatting fragments
(00, space, space, comma-space, colon-zero, colon-zero and %).
These are source-owned program DATA and symbolic CODE lookup
constants, not executable machine-code arrays or patches.

The complete original format dispatcher handles the original
strftime percent conversion cases with the original 16-bit
far input/output pointers, per-case buffered formatting,
literal text handling, named weekday/month strings, timezone
name, AM/PM cases and the original imported numeric formatter.
Its imported CRT names/indices are the genuine 12 original
symbols __UTOA, __tzname, _strcat, _strcpy, _strlen, _strncpy,
_SWeekday, _LWeekday, _SMonth, _LMonth, _AmPm and _atime.
The one far _strftime PUBLIC at0, zero BSS and original
DATA-before-BSS group 08ff02ff03 are preserved.

Native TASM 5 emits **all 1,256 original CODE bytes** and
**all 18 initialized DATA bytes** byte-for-byte, including
all 22 original character classes and all 22 genuine
symbolic CODE-switch destination offsets. It emits
**all 66 original OMF relocation fields in the original
literal writer order and at their real sites/targets**.
The unusual original BCC writer order is 40 low-body
fields in descending CODE offsets, then 22 switch table
WORD relocations in descending offsets 1254..1212, then
the four high-body fields at 1090/1059/1036/1027.
The source uses original semantic 8086 mnemonic blocks,
symbolized format cases and individual DW OFFSET table
entries in disjoint CODE ranges with ORG declarations
at original instruction boundaries. No padding or object
rewriting was introduced to produce the exact bytes.

**One original OMF metadata difference remains open.**
The four near imported __UTOA calls (CODE sites879,811,
774,723) are TARGET-framed (method5) in genuine BCC
originals, but CODE-segment framed (method0) in TASM.
The other **62 OMF fields agree literally** and the
four differing fields retain identical widths, sites,
target types/indices and addends. Reviewers assert all
66 literal sites, these four precise frame differences
and no additional mismatch. This source is therefore
byte-exact in complete CODE/DATA and actual linked product
but **not completely original in native OBJ OMF metadata**.
Earlier fopen/fclose/_timecvt native OMF gaps also remain
open, individually identified rather than normalized away.

The scoped source-only builder replaces original CRT member298
alongside **51 already reconstructed source CRT modules**,
including full xx, two qsort bosses, the 974-byte buffered
putc, original directory, path, scanner and FILE routines,
the complete 820-byte DOS/Unix time converter and natural C++
fputs. All **841 of the 893 other original library member
program records** remain unchanged. Both genuine
TASM/TLIB/TLINK rounds independently reproduce the entire
**67,372-byte fixed Japanese decoded MAINL EXE and entire
original MAP bit-for-bit**, with all **677 ordered original
MZ relocations**. Fifty-two source CRT members now provide
**26,971 original CODE bytes**, plus source-exact DATA.
These working-library exactness bytes are not new accepted
ledger credit.

The accepted28-provider original CRT, 211-owner formally
published MAINL ledger, pinned target candidate-local-attested
identity and original cold pair stay frozen. No full cold/DIET
replay or unrelated native ancestor chain was run.

Affected-only source reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strftime_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strftime_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strftime_work

All actual real source OBJ/TLIB/EXE/MAP vectors, source/driver
hash receipts and native writer phase logs are retained under
.analysis/work/strftime-* and
mainl-strftime-native-{build,review}.json.

# Original Japanese NEC PC-98 video textmode and switch dispatch (`cnectxmd`)

The genuinely selected original Borland CRT member **548**, `cnectxmd`,
exports `___nec_textmode` at original CODE+87, with full **505-byte `_TEXT`
CODE**, **35-byte initialized `_DATA`** and zero BSS. It also includes
three internal near helpers for writing NEC terminal escape sequences,
querying the NEC video BIOS state and changing text-mode flags.

`src/mainl/crt/cnectxmd.asm` reconstructs the entire **451-byte executable
8086 code region** using original symbolic instructions, branch targets,
segment-register behavior and near/far BIOS calls. CODE+451..504 consists
of two genuine **relocatable word-indexed jump tables**, seven native
video-mode selector values and a third seven-entry CODE target table.
These are typed `dw offset label` and numeric selector words—not invented
machine-code instructions or a raw executable CODE byte array. `_DATA`
contains the six original NEC terminal escape strings such as ESC `[?5h`,
ESC `[>3n` and ESC `[2J`. The original DATA offsets and DGROUP order are
preserved naturally, without post-assembly patches or artificial padding.

Native TASM 5.0 `/m /mx /kh32768 /t` independently reproduces **505/505
original CODE and 35/35 original DATA bytes**, the original public offset,
all four ordered imported symbols and exact segment names/classes/GROUP.
**All 51 OMF fixup sites, kinds, targets, addends and widths agree**, and
**50 of the 51 frame methods** agree at those original sites. The sole
remaining frame discrepancy is the near `__NEC_VIDEOINTDC` call at
CODE+18: **BCC uses TARGET frame method 5, TASM uses CODE frame method 0**.
Source-level alternatives (`near ptr`, `ASSUME CS:NOTHING`, near/far
external declaration) were explored; none preserved the original 8086
instruction while changing that field to the BCC frame. TASM and BCC also
emit different FIXUPP record ordering. Thus literal original OMF identity
**is explicitly not claimed**, even though the native product is exact.

`scripts/build_th03_mainl_after260_work.py nec-textmode` inherits the
source-bound 260-source Japanese CRT and performs **two independent normal
TASM/TLIB/TLINK rounds**. Both reproduce the complete **67,372-byte decoded
original Japanese MAINL EXE and MAP byte-for-byte**, including all **677
ordered DOS MZ relocations** and **632 untouched original vendor CRT
program records**. Working source becomes **261 members / 97,661 original-
equal CODE bytes**. This is a working source proof, not formal accepted-ledger
credit or complete whole-product ownership. No full cold replay was run.

Verify with `review_th03_mainl_after260_work.py nec-textmode` and
`tests.test_mainl_after260_work`, including raw source-bound OBJ/LIB/EXE/MAP
vectors and actual Borland writer logs under `.analysis/work/after260-*`.

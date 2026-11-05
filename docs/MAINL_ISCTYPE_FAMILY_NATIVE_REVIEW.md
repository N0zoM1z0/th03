# Original Borland locale classifier: all 13 APIs in one complete CRT member

The original Japanese CL.LIB member **81** (`is`) is reconstructed in
`src/mainl/crt/is.asm` as a complete **333-byte** machine-CODE program.
It includes the real **`___isctype`** locale-table helper and the twelve
public far `isalnum`, `isascii`, `isalpha`, `iscntrl`, `isdigit`, `isgraph`,
`islower`, `isprint`, `ispunct`, `isspace`, `isupper`, and `isxdigit` APIs.
All 13 Borland public names have their exact original CODE offsets:

`0, 46, 68, 91, 113, 135, 157, 179, 201, 245, 267, 289, 311`.

The implementation preserves **the actual 8086 instructions**: 16-bit
arguments, `-1`/EOF handling, `__pLocale` indirection at locale-table
coordinate `+0x152`, original character masks and far wrappers which
push CS before near-calling `___isctype`. The `isprint` special case
accepts a regular literal space if the locale graphical mask is false.
All original unchecked behavior is retained, with no additional defensive
branches or fabricated CODE byte arrays.

The original module is `_TEXT` **333 CODE bytes**, empty `_DATA` and `_BSS`,
original `DGROUP` ordering `08ff03ff02`. One external original near framed
data relocation at CODE+19 references `__pLocale`: its original and new
**literal OMF FIXUPP fields match fully**, including `frame_method=1,
frame=1` and target/addend. The entire original CODE, original public/import
inventory and segment lengths are independently verified against the pinned
Japanese original CL.LIB program member. Full OMF record serialization still
differs from TASM's metadata: literal FIXUPP identity is **not** identical
full member record identity.

`scripts/build_th03_mainl_after330_work.py locale-isctype-family` extends
the 341-member verified source/receipt-bound CRT. Two independently
serialized TASM/TLIB/TLINK rounds retain **all 893 original CRT slots**,
now **342 source producers and 551 contextual original vendor members**,
and reproduce the **complete original 67,372-byte decoded Japanese MAINL
EXE/MAP**, including all **677 ordered MZ relocation entries**. This adds
**333 original-equal CODE bytes**, totaling **112,039 source-built CRT
CODE bytes**. Full raw OBJ/LIB/EXE/MAP rounds, phase logs and hash-bound
incremental receipt are retained under `.analysis/work/after330-*`.
Review with `scripts/review_th03_mainl_after330_work.py` and
`tests.test_mainl_after330_work` using the selected `locale-isctype-family`
mode. No cold replay, Factory-accepted extent or packed-file credit is
claimed by this working CRT extension.

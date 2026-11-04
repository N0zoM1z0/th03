# Original Japanese TH03 NEC PC-98 screen text APIs (`cnecgptx`)

The selected original Borland CRT member **540**, `cnecgptx`, contains
three complete real NEC PC-98 screen operations:
`___nec_gettext` at CODE+0, `___nec_puttext` at +106, and
`___nec_getputtextsize` at +446. The **whole 475-byte `_TEXT` CODE** was
reconstructed in symbolic 8086 source at `src/mainl/crt/cnecgptx.asm`.
It preserves large-model far destination/source pointers, `DS:SI` and
`ES:DI` character/attribute operations, original video row geometry,
and NEC direct-video/BIOS state. This is actual native code, not copied
machine-CODE byte arrays, artificial padding, or object binary patches.

The original selected object owns zero DATA/BSS, three imports
`__wgarbage`, `__video`, `__VALIDATEXY`, and the original
`08ff03ff02` DGROUP frame. It has **nine OMF relocation fields**. TASM 5.0
`/m /mx /kh32768 /t` independently reproduces all **475/475 original CODE
bytes**, the PUBLIC offsets, all imports and **all nine literal original
FIXUPP fields including original record order, sites, targets and frame
methods**. Distinct syntax for `DGROUP:__video+11` and the unqualified
`__video+10/+16` yields the source-original GROUP/TARGET frames.
The near `__VALIDATEXY` helper preserves its original CODE-frame0 calls.

An initial disassembly-to-source attempt revealed the difference between
Capstone's explicit textual operands and TASM's original implicit string
instructions. The true `LODSW`, `MOVSW` and `STOSW` operations were written
as natural operand-free 8086 mnemonics. Their exact original bytes and
source-level segment effects were verified, not patched after assembly.

`scripts/build_th03_mainl_after259_work.py nec-screen-text` extends the
source-bound original Japanese **259-source** CRT at selected slot540,
running two independent normal TASM/TLIB/TLINK rounds. Both reconstruct
the **entire 67,372-byte original decoded Japanese MAINL EXE and MAP
byte-for-byte**, including all **677 ordered MZ relocations**, while
preserving **633 untouched vendor CRT member records**. Working-source CRT
now has **260 source-built members and 97,156 original-equal CODE bytes**.
This is working source evidence and does not confer formal accepted-ledger
credit; no full cold replay was performed.

Proof: `review_th03_mainl_after259_work.py nec-screen-text`,
`tests.test_mainl_after259_work`, and two raw native OBJ/LIB/EXE/MAP vectors,
source/driver-hash-bound receipts and actual writer logs under
`.analysis/work/after259-*` and `.analysis/work/mainl-after259-*`.

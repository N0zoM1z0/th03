# Original Japanese NEC PC-98 delay and standard multibyte conversion core

Two genuinely selected original Japanese Borland CRT program members have
complete authored 16-bit 8086 source: CRT slot **539 `cnecdely`** has
**278 CODE bytes** implementing the original NEC delay logic and internal
hardware I/O loops, exporting `___nec_delay` at **CODE+233**; slot **257
`mbyte1`** has **240 CODE bytes** with all five original C multibyte
conversion APIs `mblen` (+0), `mbtowc` (+44), `wctomb` (+109),
`mbstowcs` (+152) and `wcstombs` (+192). Both original members use `_TEXT`
CODE, empty `_DATA/_BSS` and original `08ff03ff02` DGROUP.

`src/mainl/crt/cnecdely.asm` preserves real NEC port/polling behavior,
registers/flags, and the original internal helper procedures before the
public function entry. `src/mainl/crt/mbyte1.asm` preserves five complete
native 8086 conversion functions, including true original byte/wide-char
value handling and near/far calling conventions. None of this is copied
machine-CODE byte arrays, artificial padding or post-assembly OBJ patches.

An actual 8086 byte-level trap was fixed from the original selected object:
`TEST AH,AL` at NEC CODE+103/+108 uses the original `84 C4` ModRM encoding,
but TASM's first spelling emitted equivalent `84 E0`. Reversing the source
operands while keeping identical semantics reproduces the original opcodes.

Normal TASM `/m /mx /kh32768 /t` reproduces **518/518 original CODE bytes**,
all six public offsets, the original empty DATA/BSS/EXTDEF inventories,
and the **literally original empty OMF FIXUPP lists**. The per-member
original group membership is preserved; we do not claim literal identity
of unexamined unrelated OMF record classes.

`build_th03_mainl_after317_work.py nec-delay-mbyte` builds from the
source-bound original **317-source Japanese MAINL CRT**, replacing only
these two real selected slots. **Two independent normal TASM/TLIB/TLINK
rounds** both reproduce the complete original **67,372-byte decoded
Japanese MAINL EXE and full MAP byte-for-byte**, retaining **all 677
ordered DOS MZ relocations** and **574 unchanged vendor CRT programs**.
The working source CRT is now **319 members / 104,838 original-equal CODE
bytes**. Formal accepted-ledger credit is not changed and no cold replay
was performed.

Evidence: `review_th03_mainl_after317_work.py nec-delay-mbyte`,
`tests.test_mainl_after317_work`, and native OBJ/LIB/EXE/MAP round vectors,
source/driver hashes and actual tool writer logs under
`.analysis/work/after317-*` and `.analysis/work/mainl-after317-*`.

# Original Japanese PC-98 direct-video screen CRT: `cibmscrn`

Original Japanese Borland CRT member **530**, `cibmscrn`, owns **969
complete CODE bytes** with six original near screen APIs at selected offsets:
`__IBM_SCREENIO` +396, `__IBM_CHECK_DBCS_TRAIL` +471,
`__IBM_FILL_SPACE` +625, `__IBM_OFF_CURSOR` +691,
`__IBM_SET_CURSOR` +733 and `__IBM_MOVELINE` +752.

`src/mainl/crt/cibmscrn.asm` recovers 410 true 8086 instructions, with
symbolic branch labels, actual PC-98 screen geometry and cursor movement,
DBCS trail-byte detection, VRAM/text access, screen fill and line motion.
Fifteen original EXTDEF imports preserve near PC-98 video helpers and far
`malloc/free` and `gettext/puttext` routines, plus direct-video state,
`__mbctype` and `__video` DGROUP references. The originally empty DATA/BSS
segments and true `08ff03ff02` DGROUP membership are preserved. No
executable machine-byte CODE arrays, artificial padding or OBJ patches.

**Unusually strong original OMF result:** TASM `/m /mx /kh32768 /t`
reproduces all **969/969 CODE bytes**, original six public offsets and
all **30/30 native FIXUPP records literally**, including **record order,
frame method, site, target, relocation type, addend and width**. This is
stronger than the site-sorted evidence on some earlier C++ and PC-98 units.
It does *not* claim every byte of the complete original OMF OBJ stream is
identical (other record types have independent serialization).

Actual source-bound product evidence:
`build_th03_mainl_after130_work.py cibmscrn` recompiles this selected
original slot on the retained **130-source Japanese CRT** and runs two
independent native TASM/TLIB/TLINK rounds. Both reconstruct the **entire
67,372-byte decoded Japanese MAINL EXE and MAP byte-for-byte**, retaining
**677 ordered MZ relocations** and all **762 unchanged other vendor program
records**. Working CRT becomes **131 source-built members and 61,806
original-equal CODE bytes**. This remains working source evidence, **not**
new formally accepted-ledger credit; there was **no full cold replay**.

Verify with `review_th03_mainl_after130_work.py cibmscrn` and
`tests.test_mainl_after130_work`. Two raw OBJ/LIB/EXE/MAP pairs,
source/driver-bound receipts and actual tool writer logs remain under
`.analysis/work/after130-cibmscrn-*` and `.analysis/work/mainl-after130-*`.

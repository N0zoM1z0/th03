# TH03 MAIN VS.ASM: exact initialized DATA/BSS owner, not program CODE

The previously unselected original `VS.ASM` is a *storage-only* module.
It contributes **zero executable CODE bytes**, **eight initialized DATA
bytes**, **eight uninitialized BSS bytes** and **twelve PUBLIC aliases**
(two per callback/delay/mask/counter/vector field as applicable). The
maintained `src/main/hardware/vsync_storage.asm` declares the actual
original segment sizes and fields; the seventh DATA byte is the zeroed
interrupt-mask state and the eighth is the historical assembler `NOP`
mnemonic used for initialized DATA alignment. That trailing value is
not a callable instruction, scanner NOP, or fabricated EXE patch.

Original TASM/TLINK stage `af1337i` assembles this complete owner twice
and reuses the unchanged other 98 original project OBJ slots and CRT.
Both complete Japanese MAIN EXE files and ordered MZ relocations are
byte-identical with the frozen original link, and every initialized DATA
byte, BSS/segment size, and named PUBLIC address matches the original.

A TASM-version-sensitive detail is made explicit rather than hidden:
the original OMF grouped `VS.ASM` PUBDEF names, while current TASM 5.0
emits them in separate records. The MAP by-value listing reverses only
the `_vsync_OldMask` and `vsync_OldMask` aliases at identical DS:05A4.
The scoped reviewer requires their exact addresses/strings and narrowly
normalizes this one tied alias pair, together with the source module-name
column padding. The *raw* MAP text is therefore not byte-identical,
but the entire remaining normalized MAP, actual compiled objects,
linked EXE and MZ relocation list are exact. No general MAP mismatch
is tolerated.

The negative stage `af1337j` changed only the stored OldMask value
from zero to one; the strict initialized payload comparison rejected
it, despite unchanged storage sizes. Earlier unaccepted trial `af1337h`
also confirmed that a direct TASM `IF (($ and 1) ne 0)` is not valid
for this source form. The final file retains a native mnemonic and
natural even-size DATA contribution rather than target-code strings.

This adds one original physical source-bound object to the current
inventory but **adds zero to the CODE coverage total** and does not
resolve `input_s`'s separate 417/418-byte historical linker provenance.
It confers no canonical Factory packed-file acceptance.

Current read-only two-round verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_vsync_storage_asm.py --stage af1337i --check
```

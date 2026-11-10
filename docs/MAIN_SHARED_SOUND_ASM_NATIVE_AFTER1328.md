# Three original MAIN sound leaves: source-bound original TASM

The maintained symbolic assembly in `src/main/sound/mode.asm`, `pmd.asm`
and `reset.asm` now has a scoped original TASM 5.0/TLINK 6.10 proof
against the original `snd_mode_main.obj`, `snd_pmdr_main.obj` and
`snd_se_r_main.obj` in the 99-object Japanese TH03 MAIN linker response.
These are three distinct physical owners not previously selected in the
current native MAIN list. The functions perform PMD/MIDI mode detection,
resident driver signature probing and sound-effect state reset.

`af1328b` assembled all three sources twice using the original assembler.
The exact physical CODE (30 + 58 + 12 = **100 bytes**), nine ordered OMF
fixup fields, three PUBLICs and all segment definitions match. The native
OMF module headers bind the source paths. Both complete MAIN EXEs are
byte-identical to the frozen original normal link; the complete MAP after
source-module-name normalization and ordered MZ relocation vector also match.
No other project OBJ or CRT object was recompiled.

A negative TASM trial `af1328c` altered only the reset routine's frame
value from zero to one. The resulting 12-byte CODE was rejected by the
full-object comparison. The maintained source was never changed.

Recheck the exact current source inputs and saved output products:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_sound_asm.py --stage af1328b --check
```

Only these three source-bound physical scopes are new. Canonical packed-file
credit and the unrelated `input_s` alignment gap are not implied.

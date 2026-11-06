# MAINL sound hardware functions: source-natural 8086 + TASM EVEN (after570)

The earlier after558 scope successfully compiled four original C/C++ routines
from maintained source, but each original first-use object still depended on
a historical codestring literal 90h after the function. Although the entire
original MAINL decoded EXE matched, the four manual tail bytes did not have
natural source-layout explanations.

This stage supplies four new, independently TASM-assembled, readable symbolic
8086 source units alongside the retained original C/C++ sources:

| Maintained natural source | Routine | Original CODE | Actual function | TASM EVEN |
| --- | --- | ---: | ---: | ---: |
| src/mainl/sound/mode_detect.asm | snd_determine_mode | 30 | 29 | 1 |
| src/mainl/sound/pmd_resident.asm | snd_pmd_resident | 58 | 57 | 1 |
| src/mainl/sound/volume_wait.asm | snd_delay_until_volume | 28 | 27 | 1 |
| src/mainl/sound/se_reset.asm | snd_se_reset | 12 | 11 | 1 |
| Combined | four complete routines | 128 | 124 | 4 |

The named state variables, PMD interrupt 60h and MMD interrupt 61h, original
far returns, ES:BX PMD vector/signature verification, MIDI/FM mode selection,
volume polling and sound-effect reset operations are explicit in the source.
All 124 original instruction bytes were recovered symbolically without target
opcode arrays. Every odd-length body ends in ordinary EVEN, from which
TASM generates the actual original 90h CODE alignment byte. No manually
inserted NOP, byte-array padding or code string is present in the new TUs.

Each of the four original native objects matches the corresponding new
native object through its entire initialized CODE payload, all 10 literal
OMF FIXUPP sites and semantics, all PUBLIC symbol addresses and original
segment declarations. The new assembler emits the OMF fixups in ascending
source order, whereas Turbo C++ emitted three object streams in descending
site order. OMF LNAMES packetization also differs. Thus raw original OMF
packet ordering and original compiler identity remain unproven.

In two independent native assembly and normal-link rounds, the four
new TASM objects replaced the old four Turbo C++ objects simultaneously in
the after569 source-backed MAINL build. Neither the previously accepted C0,
root/picture/text DATA, vector functions, input scanner, registration DATA,
nor the shared compiler library was rebuilt. Both complete native links
produced the entire original 67,372-byte MAINL decoded EXE exactly with
all 677 original ordered MZ relocations. MAP contribution addresses and
sizes match after normalizing only module diagnostic paths and CODE ACBP
attributes associated with the different assembler toolchain.

Read-only targeted validation:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_sound_natural_after570_work.py

All native OBJ/EXE/MAP vectors, editor-independent source inputs, ten writer
logs and exact link responses are retained under
.analysis/work/mainl-sound-natural-after570-native-* and
TH03ML/probe/af570n. Historical after558 originals and their full C/C++
source proofs are unchanged.

This establishes a natural assembler origin for four previously manual CODE
tail bytes. It does not establish a new authored-game function denominator,
historical assembler/producer identity, canonical Factory acceptance, or
complete MAINL project source ownership.

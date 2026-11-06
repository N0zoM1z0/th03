# Four original MAINL sound producers — after558

This scoped source/native review recompiles four **complete** named
Turbo C/C++ sound routines from the maintained, readable product source
rather than accepting only a source-code or disassembly comparison.
The original first-use game/binary conditions are preserved:

| Original module | Maintained source | First-use binary | Native CODE |
| --- | --- | --- | ---: |
| th02/snd_mode.c | src/mainl/linked_game/sound_mode.c | OP (GAME=2, BINARY='O') | 30 B |
| th02/snd_pmdr.c | src/mainl/linked_game/sound_pmd.c | OP | 58 B |
| th02/snd_dlyv.c | src/mainl/linked_game/sound_volume.c | MAIN (BINARY='M') | 28 B |
| th02/snd_se_r.cpp | src/mainl/linked_game/sound_reset.cpp | OP | 12 B |

Their behavior includes detecting sound-hardware mode, probing the PMD vector
and signature, waiting on playback volume and resetting sound effect state.
This is **124 instruction bytes** across four natural C/C++ bodies. Each historical
source currently ends in a one-byte NOP codestring pragma, which emits one
further byte; the four explicit trailing bytes were **not recovered through
natural compiler output**, and must not be credited as source-exact instructions.

The stage compiled the real maintained sources with the original 16-bit TC4
-O -b- -3 -Z -d -ml profile, preserving each first-use GAME/BINARY pair
and the normal object order. Two real compiler/linker rounds confirm:

- Entire original four OBJ CODE payloads match (30+58+28+12 bytes).
- All original per-object literal FIXUPP fields and PUBLIC definitions agree.
- The entire **67,372-byte original decoded MAINL EXE matches**, including
  its **677 ordered MZ relocation entries**; all native MAP sizes and
  contribution addresses agree (only new wrapper diagnostic paths differ).
- Every OBJ/EXE/MAP output repeats between rounds; source snapshots,
  native outputs and **ten writer logs** are retained under
  .analysis/work/sound-group-after558-native-* and TH03ML/probe/af558g.

The selected link reuses the source-native C0/CRT, root, picture/text/data
banks and after557 vector producer. It does **not** cold-replay the unchanged
game or recompile the remaining 32 project objects.

Run only the current affected evidence check:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_sound_after558_work.py

Original object-header/COMENT ordering is not claimed exact, and the historical
tail codestring dependence remains a real natural-source recovery question.
This review does not promote canonical Factory unit acceptance, other products,
or entire MAINL source completeness.

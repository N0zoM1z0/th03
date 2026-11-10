# Input mode services: native joystick presence and signed wait semantics

The complete physical nine-function input-mode object now tests actual
joystick availability using an explicit nonzero byte condition in the
source-level merge macro and both joystick-versus-keyboard interfaces.
Without a connected joystick, no `js_sense()` call runs and the existing
keyboard-to-player assignments retain their original control flow.
The macro remains expanded inside each original caller: replacing it
with a helper function or reference had previously increased native CODE.

The `input_wait_for_change()` entry now compares the shared input word
against its named `INPUT_NONE` zero sentinel in both polling phases.
The release phase remains an **unbounded** loop regardless of the
caller-supplied frame bound. The press phase now uses a natural
`while(frames_waited < frames_to_wait)` signed-16-bit loop: a zero bound
selects the historical `9999` sentinel, negative bounds skip only the
press phase, and the sentinel counter reset still happens *after* one
real input poll and one frame delay. The zero/positive comparison does
not make the volatile or interrupt-driven state a Boolean function.

Genuine original TC4 4.02/TLINK source trials `af1344a` (both idle/press
zero comparisons), `af1344b` (signed bounded while-loop) and `af1344c`
(joystick presence in three source locations, expanding to all relevant
callers) each reproduced the entire physical object and normal MAIN link
in two independent rounds. Final current-source stage `af1344d`
reconstructed **367 CODE bytes, 58 ordered native fields and nine
PUBLICs**. The joint `af1344e` recompiled input modes, the CPU movement
controller and the VSYNC frame-delay leaf: **1,465 CODE bytes, 124
ordered native fields and 14 PUBLICs** matched both original complete
Japanese MAIN links and ordered MZ relocations. No full cold replay was
run.

This is *not* source acceptance of the separate 417-byte original
`input_s` BIOS scanner: its historical 418-byte TASM linker-carrier
alignment remains an independent open exact-original-OBJ provenance gate.

Read-only original source-bound evidence:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1344d af1344e
```

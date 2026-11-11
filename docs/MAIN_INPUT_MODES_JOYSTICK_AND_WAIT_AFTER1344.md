# Input mode services: native joystick presence and signed wait semantics

The earlier `af1344d` nine-function source tested joystick availability
with an explicit nonzero byte check inside its expanded merge macro and
the two joystick-versus-keyboard interfaces. With no joystick connected,
no `js_sense()` call ran, preserving keyboard-to-player assignment order.
Replacing the macro with an actual C++ helper function or reference had
increased native CODE, so each original caller retained inline actions.

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

## Current direct source, independent joystick actions and wait gates (2026-11-11)

The maintained `src/main/hardware/input_modes.cpp` now contains the
original four *explicit per-caller* joystick read/merge blocks rather
than a `merge_joystick` preprocessor macro. This is a source-level
recovery, not a helper call: each conditional still tests availability,
reads `js_sense()` once and ORs the corresponding physical input word
at its original position. The two joystick-versus-keyboard assignments
also use direct nonzero tests. Extracting the actions into a C++ helper
would change the original Turbo C++ register and call layout.

`input_wait_for_change()` now uses the native-equivalent input truth
checks: `if(!input_sp)` exits the **unbounded release** wait, while
`if(input_sp)` exits the bounded press wait. The separate `if(!frames_to_wait)`
selects the original 9999 sentinel. The signed frame comparison, delay
ordering, and negative-bound press skip remain unchanged.

Independent native stages `af1353g` (joystick truth), `af1353h`
(polling truth) and `af1353i` (actual per-caller C++ actions) each
recompiled the entire nine-function physical object with genuine original
TC4 in two rounds. The current `af1353i` reproduces **367 CODE bytes,
58 ordered native fields and 9 PUBLICs** plus both normal Japanese MAIN
links. The joint `af1353j` compiled input modes, CPU controller and
VSYNC delay: **1,465 CODE bytes, 124 native fields and 14 PUBLICs**,
full MAIN images and MZ relocations exact. The separate original `input_s`
417/418-byte historical-link-carrier gap remains open.

Current source receipt: `.analysis/work/exatt-layout-af1353i/report.json`,
SHA-256 `9c07a8322324a99627c9c30134c64a9fb57487574274a3b6ed78c5d417905fd1`.
Joint receipt: `.analysis/work/exatt-layout-af1353j/report.json`,
SHA-256 `5d70c9acc3aac2c6d3611546903b5eb9ff46a1b233e6a9acdee74efcc83bb65c`.

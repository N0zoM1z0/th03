# TH03 MAIN enemy script VM: natural first-operation and duration C++ after732

The `efornb` original physical TC4 translation unit contributes **four
complete functions**, including `enemy_run()` (an approximately 867-byte
ENEDAT movement/spawn/loop interpreter), angle update, velocity
calculation and chain-pellet speed. Full object ownership is **1,064
original CODE bytes, 37 literal ordered OMF FIXUPPs and 4 PUBLICs**.
Other enemy formation/update producers are different original physical
objects and remain unchanged.

This work recovered more natural C++ from the substantial unbounded VM:

- The script dispatch loop uses ordinary `for(;;)` instead of a numerical
  `while(1)`, with all original switch cases, shared wait epilogue, segmented
  `__es` script pointer and original instruction stepping retained.
- Four *different* movement opcode paths now use
  `if(!enemy.script_op_frame)` rather than explicit `== 0` for the first
  frame, preserving the original velocity/angle initialization order.
- Original time scaling is now named as three separate integer constants
  (divide by 2, multiply by 3, divide speed-dependent product by 6).
  The original two independent truncating signed divisions and operand
  order are **not** merged; this is important to correct per-opcode timing.
- Both ZUN `EO_LOOP_ABS`/`EO_LOOP_REL` interpreter quirks remain, including
  the stale `script` pointer and previous `op_size` use on taken iterations.
  We intentionally did not "fix" those original bugs or add validity
  checks for unknown opcodes/invalid memory.

A separate **negative** original TC4 trial `af732a` attempted to replace
original `enemy.pos_type |= ((p->clip_* != false) * EPT_CLIP_*)` expressions
with readable conditional OR assignments in the `EO_SPAWN` opcode.
Original CODE changed. Those expressions remain intact, with the failed
compiler output retained. `af732b` proved the natural first-frame tests;
`af732c` then proved those tests *together with* named duration gates.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af732c --units efornb
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af732c

Both fresh genuine Turbo C++ 4.02 compiler/full normal MAIN TLINK rounds
reproduce **all 1,064 original CODE bytes**, 37 original ordered literal
native FIXUPP fields, all 4 PUBLICs, original OMF segments, complete
normal MAIN EXE and path-normalized MAP, Japanese 124,642-byte loaded
program and all **1,553 literal ordered MZ relocations**. Independent
standard MZ serialization reproduces the complete original 130,882-byte
Japanese MAIN.EXE (this does not assert vendor TLINK direct header identity).
The other 98 project objects and the original CRT were reused, without
full cold replay or target/OBJ byte patching.

Source-bound retained original native writer evidence:
`.analysis/work/exatt-layout-af732c/report.json`, SHA-256
`6a4f566b7907f11931ec26af6677b8541fcca7e139d5d4bf959969884bbf20b2`.
Both real compiler/linker rounds' source dependency COMENT fields,
physical OBJ, EXE/MAP, response files, logs and original MZ bytes are
retained. These bytes were previously owned; fresh current-source
native codegen **does not** create additional canonical Factory packed
acceptance, prove historical raw vendor OMF packet identity or close
whole-game source ownership.

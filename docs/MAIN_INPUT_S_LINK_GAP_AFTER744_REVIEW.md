# TH03 original BIOS keyboard scanner: exact native C++ OBJ, one-byte full-link blocker after744

This is a **source-reconstruction and negative-link provenance finding**, not
an accepted exact normal MAIN compiler/linker result. The original physical
`input_s` unit is `obj/th03/input_s.obj`: the complete original 16-bit
`input_reset_sense_key_held` routine scans PC-98 BIOS key-state groups,
updates both players and the shared input word, and repeats a port-delay
loop between two key samples. The original OMF has **417 CODE bytes,
42 literal ordered FIXUPP fields, one PUBLIC and three original segments**.

## Natural C++ actually recovered and object-proved

`src/main/hardware/input_sense.cpp` now names the actual **two BIOS scan
passes** and original **1,024-iteration port delay** with compile-time enum
values. The outer sampling loop is natural `for(;;)` rather than numeric
`do { ... } while(1)`. The original `input_peekb` far-segment access,
`jmp sense` control-flow edge, BL decrement and FLAGS_ZERO branch, key
masks, `0x5F` port output and `loop delay_loop` hardware semantics remain
untouched. The source does **not** inject a trailing NOP or target bytes.

Two separate genuine native TC4 4.02 compilations (`af744c`, `af744d`)
each produced a real **417-byte object equal to the original** at the
entire initialized CODE payload, all **42 original ordered OMF FIXUPP
fields**, its original PUBLIC and segment definitions. The compiler's
actual source COMENT dependency was independently checked against the
current maintained `input_sense.cpp` in each materialized scope.

## Full normal MAIN link is **not** currently exact

The frozen after596 normal MAIN link response does **not** use the original
417-byte physical `obj/th03/input_s.obj` in its source-replacement slot.
It instead uses an older experimental `probe/af567c/r1-input_s.obj` object
with **418 CODE bytes**. The first 417 bytes exactly match the original;
the **one extra byte is `0x90` (NOP) at CODE offset 417**, after the
original final RET. This is a genuine historical source/linker-gap issue,
not a compiler source mismatch or a missing user build dependency.

Once the scoped compiler correctly selected that physical link slot,
`af744b` (unchanged current source), `af744c` and `af744d` (new natural
input scan source) each compiled the original-object code exactly but the
full normal MAIN link check **failed**, as it should. The candidate
EXE has `0x00` in place of the historical parent's `0x90` at **file
offset 68,141**, with every other EXE byte and every ordered MZ
relocation unchanged. This is not acceptable complete-source native
link equality, and neither a fake trailing NOP nor a byte-patched EXE
is an appropriate shortcut.

The read-only negative reviewer captures the **current** source/input
identity, compares the original 417-byte object and old 418-byte parent,
checks the 42 fixups and source dependencies, and requires the link gap
to be detected rather than ever accepting it:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py
    .venv/bin/python -m unittest discover -s tests -p test_main_input_s_link_gap.py -q

Its explicit structured result is
`status=blocked-by-historical-single-NOP-parent-link-gap`,
`native_current_source_object_CODE_exact=true`,
`normal_MAIN_exact=false` and `canonical_Factory_credit=false`.
The real compiler source and object/link writer logs remain in
`TH03WORK/probe/af744c` and `TH03WORK/probe/af744d` with their original
`.analysis/work/exatt-layout-af744*` logs; **no successful `report.json`
was published** for these trials. Do not cite this as a two-round passing
MAIN link, overwrite the original after567c parent, replace the target,
or increase canonical Factory acceptance. Further investigation requires
source- and linker-justified resolution of the one-byte historical
postfunction NOP without manufacturing an exact match.

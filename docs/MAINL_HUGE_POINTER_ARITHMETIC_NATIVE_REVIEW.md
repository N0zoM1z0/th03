# Huge pointer add/subtract and increment/decrement: exact original native link

The original Japanese CL.LIB **members 71 and 73**, `h_pada` and `h_pina`,
are now recovered in complete natural 8086 source. These are not short
placeholder leaves: `h_pada` is the original **136-byte** huge 16:16 pointer
add/subtract and normalizer; `h_pina` is the original **102-byte** huge
pointer increment/decrement and in-place far memory update routine.

All **12 original near/far public aliases** and their exact offsets are
recreated. `h_pada` exports `N_PADA@`, `F_PADA@`/`PADA@`, `N_PSBA@`,
`F_PSBA@`/`PSBA@` at offsets 0,3,68,71. `h_pina` exports `N_PINA@`,
`F_PINA@`/`PINA@`, `N_PDEA@`, `F_PDEA@`/`PDEA@` at 0,3,50,53. The source
preserves 1 MB real-mode segment normalization, carry/borrow handling,
original ES pointer access, and the near-to-far call adapter ABI. Both
original CODE payloads match **all 238 bytes** from the actual Japanese
CL.LIB members, along with original PUBDEF aliases, segment geometry and
DGROUP. No imported relocations exist in either original member.

## The unsolved adjacent long-division member was not hidden

A third, previously dirty source `src/mainl/crt/h_ldiv.asm` was investigated
independently. Its complete **174-byte** original signed/unsigned 32-bit
division and modulus CODE, 12 original aliases and zero FIXUPP fields match
the pinned member 67. Substituting that source in the same native carrier
produces a **byte-exact original complete EXE and all 677 ordered MZ
relocations**; its MAP differs at only **two pairs of synonymous public
symbols**: `LDIV@`/`F_LDIV@` and `LUMOD@`/`F_LUMOD@` at identical logical
code offsets. We also confirmed experimentally that swapping original
`PUBLIC` declaration order, label order, and `LABEL`/`EQU` definitions does
not restore the original TASM/TLINK MAP tie ordering. This is a genuine
source-emitted Borland-vs-TASM PUBDEF metadata problem, **not** proof of
an incorrect divide algorithm or original packed-file ownership. The source
remains available for follow-up; it is deliberately **not counted** as a
fully linked-source member in this checkpoint. The experimental alternate
native receipt is preserved under `.analysis/work/mainl-after353-huge-arithmetic-build.json`.

`scripts/build_th03_mainl_after354_work.py huge-pointer-adjustments` takes
the clean source/receipt-validated **404-member** parent, reassembles just
`h_pada` and `h_pina`, and reconstructs all **893 original CRT library slots**
under serialized native TASM/TLIB/TLINK in **two independent producer
rounds**. Both reproduce the original **67,372-byte decoded Japanese MAINL
EXE and MAP byte-for-byte**, including all **677 DOS MZ relocations in
original order**. The working CRT reaches **406 complete source-backed
members**, **487 unchanged contextual original programs** and **130,443
original-equal CODE bytes**, an increase of **238**. The complete OBJ/LIB/
EXE/MAP vectors, phase logs, source hashes, parent receipt and reviewer are
retained under `.analysis/work/after354-*`,
`scripts/review_th03_mainl_after354_work.py` and
`tests/test_mainl_after354_work.py`.

This proof is working CRT source, not a new formal Factory-accepted decoded
extent or canonical packed-file unit; no full native cold replay was run.

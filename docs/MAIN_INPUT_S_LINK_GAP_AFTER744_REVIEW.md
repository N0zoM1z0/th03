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
The original diagnostic writer outputs were recorded at
`TH03WORK/probe/af744c` and `TH03WORK/probe/af744d`; these historical private
outputs were subsequently retired. **No successful `report.json` was
published** for those failed full-link trials. See the newer fresh native
controls below. Do not cite this as a two-round passing
MAIN link, overwrite the original after567c parent, replace the target,
or increase canonical Factory acceptance. Further investigation requires
source- and linker-justified resolution of the one-byte historical
postfunction NOP without manufacturing an exact match.

## 2026-11-10: actual original OBJ normal-link control

The direct `af1305a` experiment replaced the old `af567c` source slot in
one frozen normal MAIN TLINK response with **`obj/th03/input_s.obj` itself**.
The actual original OBJ and native `af1193a` TC4 OBJ have the same `SHARED`
CODE SEGDEF length **417** and one LEDATA record covering all **417** bytes.
The old `af567c` parent is different: both its SEGDEF and LEDATA are **418**
bytes, ending in a literal `90` after the original `CB` return. The native
source did not generate that extra byte. `af1305a` successfully linked the
original OBJ without recompiling anything, and the result again differed
from the frozen parent at *only* EXE file offset 68141 (`90` versus `00`),
with the same MZ relocation order and full file length. The source is still
blocked from an exact **normal full link**, but this test narrows the cause
to historical one-byte linker padding/object provenance, not a missing C++
body or incorrect source fixups. No manufactured filler was introduced.

Evidence: retained ignored work directory
`.analysis/toolchain/wineprefix/drive_c/TH03WORK/probe/af1305a/`.

## 2026-11-10: two fresh native negative link rounds and alignment controls

The earlier `af744d` private outputs were no longer retained in this
worktree, which caused the dedicated read-only negative test to skip.
Fresh independent stages `af1320c` and `af1320d` each compiled the **current**
source with original TC4 into 417 initialized CODE bytes, 42 ordered fixup
fields and one PUBLIC, matching the unchanged reference object. TLINK ran
normally; each stage then failed the intended complete-image equality at
**exactly file offset 68141**, parent `90` versus actual `00`, with identical
ordered MZ relocations. The read-only reviewer and two-stage test now consume
these current private results instead of a missing historical directory.

The actual MAP shows `SHARED:019C` through `SHARED:033C` belongs to the
417-byte `input_s` code, and the following word-aligned module starts at
`SHARED:033E`. The intervening `SHARED:033D` is an alignment hole.
There are only three one-byte CODE-to-CODE alignment gaps in the native
SHARED map: `0031`, `033D`, and `05D3`. The other two contain `00` in both
the source-linked and frozen MAIN images, while `033D` alone changes
`90 → 00`. This rules out assuming a general TLINK policy of filling
odd-byte SHARED gaps with NOP. The old parent specifically used the 418-byte
assembled experimental object, whereas the genuine 417-byte current source
ends with the original RET. No filler instruction, link patch or unearned
normal-link acceptance was introduced.

Current focused read-only check:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py
.venv/bin/python -m unittest tests.test_main_input_s_link_gap -v
```

## 2026-11-10: original TASM EVEN explains the frozen 418-byte linker carrier

`src/main/hardware/input_scan.asm` is a complete symbolic keyboard scanner,
not an opcode array. The original TASM 5.0 produces the same first 417
initialized instruction bytes as the original TC4 `input_s.obj`, followed by
one natural `0x90` emitted by the *source's CODE `EVEN` directive* after the
far return. This yields a 418-byte SHARED contribution. Its complete 418
CODE bytes, 42 literal ordered OMF fields, one PUBLIC and segment definitions
match the historical `probe/af567c/r1-input_s.obj` used by the frozen
normal MAIN link. The genuine original TC4 object remains 417 bytes and
**does not** match the 418-byte assembled object at the full physical
object boundary.

New source-bound diagnostic `af1335b` assembled the maintained ASM source
in two independent original TASM rounds and replaced the historical
418-byte parent linker slot. Both TLINK outputs reproduce the *entire*
parent Japanese MAIN EXE byte-for-byte, full normalized MAP and ordered
MZ relocation vector. This establishes a plausible, fully reproducible
native provenance for the historical padding: the `EVEN` is assembler
layout rather than a new keyboard-scanning instruction, and not an
assumed general TLINK fill rule.

**Scope limit:** this is an *alternative historical linker carrier proof*,
not native acceptance of the **original 417-byte TC4 physical OBJ**. It is
intentionally excluded from `scripts/status.py` selected original-source
owner counts and confers no Factory canonical credit. The original C++
normal link still differs at file offset 68141 (`90` vs `00`). No target
mutation, manual filler, or compiler-output patch has been made.

Current read-only checks for both sides:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_input_alternative_asm.py --stage af1335b --check
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py
```

# Complete MAINL STAFF_TEXT decoded review

This bounded review covers the entire 424-byte `STAFF_TEXT` CODE segment:
two complete generated-assembly functions and the complete frozen C++
`flake_put` implementation. Raw bytes match both pinned scaffold rounds.
The generated 348-byte contribution still fails ordered MZ relocations;
the 76-byte C++ contribution has no MZ relocation words. No maintained source,
canonical stored-file extent or exact credit is added.

```sh
python3 scripts/review_th03_mainl_staff.py --output .analysis/NEW_STAFF_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_staff_review.py -v
```

Receipt: `.analysis/sol-mainl-staff-review-20261006.json`. It guards canonical
Japanese MAINL, decoded DIET lineage, both cached images/MAPs, compiler-provider
snapshots and analysis scripts before and after execution. Current Ghidra
headless-usage fails before the selected database can be checked. This review
uses independently guarded decoded bytes, not packed-database observations.

## Complete boundaries and source association

| Decoded CS:IP | Bytes | Frozen source candidate | Return |
| --- | ---: | --- | --- |
| `095F:233E` | 68 | `th03_mainl.asm`, `sub_B92E` | Near RET |
| `095F:2382` | 280 | `th03_mainl.asm`, `sub_B972` | Near RET |
| `095F:249A` | 76 | `th03/staff.cpp` → `th03/end/staff.cpp`, `flake_put` | Near RET 6 |

These bodies contain 147 instructions and partition the full segment without
padding or shared tails. The generated region is root assembly lines 1070–1186;
those labels remain provisional source associations, not authored C++ recovery.
The complete C++ implementation is 68 lines. Internal branches must remain
on instruction boundaries in their own body; every external near/far call has
an explicit interface descriptor. Automatic Ghidra functions receive no credit.

Both cached trees bind sixteen consulted providers to frozen revision
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. C++/header snapshots have byte
identity; the two consulted assembly files differ only by LF-to-CRLF conversion.
The C++ object's valid OMF identifies `TC86 Borland C++ 4.02` and matches after
dependency-timestamp normalization. This is a cached input/output association,
not current toolchain attestation or a fresh maintained build.

The MAP assigns `095F:233E`, size `015C`, to `th03_mainl.asm`, and
`095F:249A`, size `004C`, to `th03/staff.cpp`. C++ DATA and BSS contributions
are both zero: its flake array, page, center and score declarations allocate
no storage here. Generated-carrier definitions, sprite-table ownership and
the larger snowfall animation at `095F:2E1D` remain separate. The unresolved
`th03/sprites/flake.asp` asset input is not imported or closed. Relevant
type/register/flag declarations were inspected; full headers, cross-game
branches and toolchain headers retain their separate review scope.

The generated contribution has 21 relocation words. Target/candidate membership
and raw code are equal, but original directory order differs in both rounds.
Both sequences remain verbatim in the receipt; no sorting or target rewriting
grants acceptance. The flake contribution has zero words. Packing/stub ownership
and the canonical file-backed policy remain open for all three bodies.

## Music and ending dispatch contracts

The music function stops the song, calls C-style `snd_load` with `over.m` and
mode `0600`, starts playback, fades in, waits through
`snd_delay_until_measure(3,64)`, fades out, stops and returns. The caller removes
six bytes after the far cdecl load; its result is ignored. Sound/timing/fades
are interface models, not hardware observations.

The dispatcher releases CDG slots 0/1/2 and PI slot 0, then zero-extends the
resident packed character byte at offset `0C`. DEC/CWD/subtract/SAR implement
signed division toward zero by two; the result is stored in a byte local.
Packed zero yields zero from `(-1)/2`. The far pointer at DGROUP `0A5E` reaches
mutable `@00ED.TXT`: values at least ten add their quotient to character 1,
then the remainder is added to character 2. There is no range check or digit
clamp. Constructed packed 255 yields `@<7ED.TXT` (derived value 127); preserve
the byte additions rather than substituting formatted decimal text.

It sets palette tone zero, delays 96 frames, selects access/show page zero,
clears/shows graphics, loads/runs/frees the derived script and calls external
snowfall animation. Resident story stage becomes `63h` (99) before registration.
State is **reread after registration**: credits byte `36` must equal 3 and
packed byte `0C` must be below `0F` to run `@99ED.TXT`. The model leaves these
bytes unchanged through registration; actual registration side effects remain
unreviewed. Constructed invalid packed zero also satisfies this decoded gate.

Finally it clears text, restores gaiji, exits the game environment and calls
far cdecl `execl("op","op",far NULL)`. Caller cleanup is twelve bytes, followed
by LEAVE/RET. Every probe models **exec failure returning AX=FFFF**; successful
process replacement would not return and is not executed. Modeled script-load
failure also continues through animation/cleanup/exec, proving only the caller's
unchecked result, not the helpers' real failure behavior.

Capstone's displayed CDQ/CWDE names for single-byte `99/98` are not evidence
of 32-bit execution: raw bytes and 16-bit CPU mode establish CWD/CBW. Preserve
word stacks, byte locals, signed division, far pointers and near/far ABIs.

## Complete snowflake blitter contract

`flake_put(left,top,cel)` takes near Pascal word arguments in stack order
cel/top/left, saves BP/SI/DI and ends at RET 6. Destination offset is
`((signed left >> 3) + top * 80) & FFFF`, source is
`(0A62 + (cel << 4)) & FFFF`, ES is `A800`, and rotation is `left & 7`.
Eight iterations load/ROR/OR a word into blue-plane VRAM, advance destination
by 80/source by 2, then DEC/JNZ. There is no clipping, cel validation,
other-plane store or clearing. The source's symbolic word AND on CX must not
be replaced with unrelated emitted instruction bytes.

The model substitutes eight synthetic sprite words and A55A-filled blue VRAM.
Every word write, the complete memory result, offset wrap, ES, cleanup and saved
registers are checked. It covers all eight rotations, four declared cel indices,
top -1/0/399/400, plus four out-of-range/edge cases. With left=-1/top=0, the
first modeled word starts at FFFF and the next at 004F. Extra modeled bytes
permit that crossing; actual segment-limit/device/bus behavior and valid-caller
reachability are unproved. Invalid cel -1/4 cases initialize synthetic rows
outside the declared table; no neighboring game assets are inspected/imported.

## Evidence and remaining work

Each target/cached image runs 512 ending cases (every packed byte with credits
2/3), four failed-interface endings, 132 blitter cases and one music case:
1947 calls total. Load/exec/cutscene/registration, sound, palette, resources
and graphics helpers are explicit substitutes. Only the three STAFF bodies
execute; constructed stack/resident/sprite/VRAM inputs establish no real startup,
kernel, hardware or game runtime. Eight synthetic controls cover truncation,
return cleanup, operand/other-body branches, unknown/indirect calls, near/far
mismatches and callback errors caught outside Unicorn's FFI boundary.

This completes the bounded STAFF CODE/source-candidate review. MAINL and the
ending subgraph remain incomplete: cutscene interpreter, registration, snowfall
animation, assets/data/BSS, libraries, root ownership, cold maintained compiler
replay and stored packing/complete Oracles remain open. Intake and exact totals
are unchanged.

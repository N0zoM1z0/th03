# Complete MAINL VSYNC and vector/mode candidate review

Three complete frozen library includes cover 361 body bytes /166 instructions,
four bytes of saved CS state and three producer NOPs: 368 new decoded bytes.
The previously reviewed 38-byte VSYNC_WAIT executes as native context without
duplicate progress credit. All 406 scoped raw bytes and original ordered
relocations agree with both cached products. Three disjoint decoded module
rows add no maintained MAINL source, canonical stored-file offset or exact
acceptance.

```sh
python3 scripts/review_th03_mainl_vsync.py --output .analysis/NEW_VSYNC_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_vsync_review.py -v
```

Receipt: `.analysis/sol-mainl-vsync-review-20261006.json`, SHA-256
`d09b66220f232c57e69d45eccd8ab98e1f24efbfba365abfa832f49566e022e4`.
Its 513 guarded inputs retain the previous palette receipt's stored/decoded/
cached lineage. Twenty-eight consulted frozen providers bind both cached
trees. Only ASM/INC line endings normalize; seven prior MAIN-only Tupfile
substitutions are checked explicitly, with no VSYNC/mode/vector substitution.
Both root OMF objects are valid TASM5/th03_mainl.asm and equal after dependency
timestamp normalization. MAP containment places all includes inside the root
_TEXT carrier. Its other code, CRT/data/BSS and packaging remain unaccepted.

| Body | Decoded offset | Bytes /instructions | Return |
| --- | --- | ---: | --- |
| VSYNC_START | 1F6E | 106 /46 | RETF |
| CRTBIOS_COOK | 1FD8 | 9 /4 | IRET |
| VSYNC_COUNT | 1FE2 | 58 /32 | IRET |
| VSYNC_END /VSYNC_LEAVE alias | 201C | 71 /32 | RETF |
| DOS_SETVECT | 0704 | 31 /18 | RETF6 |
| GRAPH_EXTMODE | 0F02 | 86 /34 | RETF4 |

The VSYNC include owns 250 bytes at 1F6A..2063: four CS saved-vector bytes,
244 CODE bytes and two EVEN NOPs at 1FE1/2063. The complete vector helper owns
32 bytes at 0704..0723, including one NOP. Mode owns 86 bytes at 0F02..0F57.
The sole scoped relocation is VSYNC_COUNT's DGROUP immediate at 1FE5; original
and both caches retain the same ordered site. The private CS declaration's
four initial decoded zeros are guarded as observations, without inventing a
cold producer or general initialization guarantee. Instruction decoding
excludes those data words and all surrounding root bytes.

## Execution and declared environments

Each image has 9664 terminal scenarios, 13852 top-level calls and 29648 native
entries. Across three images, 41556 calls return and 88944 native entries
execute. Another 60 separate budget observations execute 1392 native entries
and 3996 old-IRQ fixture entries. All included procedures use native calls,
actual far returns and IRETs; the connected WAIT executes the real counter
handler instead of directly modifying a count fixture. Full 1MiB outside the
declared 64K stack matches an independent physical-memory scalar algorithm
after every terminal call and each budget observation. Cross-image comparisons
retain state, registers, flags, requests, ports and entry counts; unrelated
target/cached PI encodings keep whole-memory hashes per-image.

The image relocates to 2000, DGROUP to 2E3F and stack to 4000. Fixtures declare
the IVT, capability byte at 0000:045C, cursor byte at 0711, TextShown0840,
callback0842, Delay0846, OldMask0848, Count1/2 at 144E/1450, OldVect1452 and
delay accumulator1456. OldMask's neighboring high byte is explicitly A5 and
must remain unchanged by the native byte stores. This does not accept the
unowned target/cached DGROUP0849 difference or the generated DATA/BSS graph.

Only INT21/AH35 and25 are DOS models: get returns the declared IVT pointer in
ES:BX with independent CF, while a CF-clear set updates that vector. INT18
requests build an interrupt frame and dispatch through the declared IVT to
either native CRTBIOS_COOK or an old-BIOS fixture containing real IRET. That
fixture returns synthetic AL/BH for query31 and explicit AX for other requests;
it preserves other registers and its saved flags. A separate old-IRQ IRET
fixture and far callback RETF fixture have declared addresses. They are not
reconstructed DOS/BIOS/old-handler source. Actual kernel/vector ownership,
BIOS status conventions, display hardware and asynchronous scheduling remain
outside this proof.

Interrupt entry is an explicit fixture, including saved-IF0 cases. Connected
wait delivery occurs after a declared number of comparison visits and does
not claim that hardware could deliver a maskable IRQ while IF0. Native IRET
restores the supplied status/IF/DF frame. No MEM_READ hook is installed. Guards
check every instruction boundary, approved direct/indirect call, native far/
interrupt frame, service site, byte port access and owned write span. Only
declared globals, saved CS words and stack may receive native stores; IVT
changes belong to the DOS model and are independently checked in full memory.

Eight controls reject body/cleanup/interior-return changes, operand/data/
neighbor branches, unknown calls and missing PUSH CS, indirect operands,
saved-state/DGROUP/alignment mutation, unknown services/ports, guarded FFI
failures, unowned whole-span stores, wrong service AH/port width, invalid
native/interrupt frames and saved flags, undeclared vectors/targets, missing
callback CLD, stale completion and segment aliases. Positive controls execute
a real IRQ IRET, the nested old-BIOS/native-wrapper IRETs and a direct old-IRQ
fixture return. Synthetic mutants test guards without product acceptance.

## Start, repeat and mask restoration

START calls the actual GRAPH_EXTMODE with zero mask/value. It selects Delay
13311 when returned AX AND0C equals0C, otherwise zero. It clears both counters
before testing OldMask's low byte. Thus repeated start still queries the mode,
updates Delay and resets counts, while a nonzero byte suppresses reinstallation.
The delay accumulator, callback, old vectors and saved CS words are retained.
The repeat-start chains check the remaining phase across changed mode replies.

First installation saves/replaces vector0A with VSYNC_COUNT, reads PIC mask2
under PUSHF/CLI, outputs its value AND FB and restores flags. OldMask becomes
original-mask OR FB, normally FB or FF; only the original IRQ2-disable bit is
encoded. It saves/replaces vector18 with CRTBIOS_COOK and writes port64 using
the returned old BIOS offset's low byte. DOS carry is not checked. Failed
modeled vector sets can therefore leave an active housekeeping marker without
the native handler installed. Matrices follow the still-old IRQ vector and
check its declared no-counter-change behavior; no real DOS failure guarantee
is inferred.

END and its LEAVE alias share one entry. A zero low-byte marker skips all
cleanup. Otherwise it first restores BIOS18, masks IRQ2 with current PIC mask
OR4, restores IRQ0A, then outputs current mask AND OldMask. Each PIC update
uses PUSHF/CLI/POPF. For normal FB/FF markers this restores the saved IRQ2 bit
while retaining other current mask bits, rather than restoring the entire old
PIC mask. An arbitrary marker can clear additional bits; all 256 current masks
are checked with markers0/1/4/FB/FF. Finally it writes port64 and clears only
the marker byte. Counters, phase, callback and saved pointers remain. Native
ordering is reviewed; interrupt races between these operations are unproved.

## Counter handler, callback and waiting

VSYNC_COUNT saves AX/DS, loads relocated DGROUP, and adds Delay to its retained
16-bit accumulator. Carry skips both counter increments and callback, but
still sends byte20 to master PIC port0 and port64. Otherwise both counters
increment modulo65536. Callback dispatch tests only the far pointer's segment
word; a zero offset with a nonzero segment executes the declared callback.
Offsets with a zero segment are ignored.

The handler saves BX/CX/DX/SI/DI/ES, executes CLD and calls the far callback.
The fixture can clobber these registers, AX/DS, flags and BP. Native pops
restore all supplied general registers except BP, which the handler never
saves. Matrices separately cover ABI-conforming callbacks that retain BP and
adversarial BP clobbers; BP preservation depends on the callback contract.
After a callback, CLI runs before the acknowledgments even if the fixture
sets IF. The final IRET restores original flags and DF; callback CLD is not a
permanent change to interrupted DF. All64 arithmetic-status combinations are
checked under both IF and DF states, with a separate incoming DS5000 proving
the native DGROUP load and DS restoration. TF is0 throughout.

Matrices cover delay0/1/33FF/7FFF/8000/FFFE/FFFF, accumulator boundaries,
counter wrap, all256 install masks, repeated start/end, callback null-segment/
zero-offset cases and connected wait/handler sequences. The prior WAIT's
low-byte mode check and clear-to-rise polling remain scoped by its palette
receipt. New budgets distinguish no delivered IRQ, permanently-high/low
ports, many legitimate carry-skipped IRQs and an old-vector fixture that
does not change Count1. The slow FFFF phase is a finite execution budget,
not universal nontermination. Every partial state and trace is checked.

## Vector and mode helpers

DOS_SETVECT consumes the low byte of its word vector argument, fetches the
new DS:DX pointer from the far argument, performs get35 followed by set25,
and returns the get result in DX:AX. It preserves BX/ES/DS/BP and ignores both
carry results. All256 vector numbers and upper-word aliases100/1FF/FF00/FFFF,
including zero/FFFF pointers, execute with actual LDS and RETF6. These are
declared DOS fixtures, not independent DOS ABI certification.

GRAPH_EXTMODE always sets ES0. An absent capability bit40 at045C returns AX0
without BIOS calls. Otherwise query31 combines returned BH and AL. A zero
mask returns that value. A nonzero word mask merges selected value bits,
issues BIOS30, optionally restores text for TextShown bit0, sets an area for
merged bit0 and restores cursor for byte0711 bit0. It returns the merged word
without checking a BIOS success result. ES/BX/CX/DX can be clobbered by this
native helper; do not invent ordinary ES preservation for START. Masks,
values, capability/text/cursor gates and installed-wrapper BIOS re-entry are
checked independently. Remaining graphics/BFNT/sprite libraries, CRT/game
callers, real devices/interrupts, cold source/layout/ownership and canonical
DIET packaging/complete Oracles remain open with the full ReC98 intake.

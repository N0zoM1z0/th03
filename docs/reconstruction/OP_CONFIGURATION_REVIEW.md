# OP configuration and lifecycle candidate review

This review covers three complete near configuration functions, three complete
far lifecycle/plane functions and the complete far sound-mode body with its
one-byte producer. It adds 472 independently reviewed decoded bytes in seven
units. The native 28-byte compiler copy helper is context only. No maintained
OP source, exact owner, whole-file or whole-product acceptance is granted.

Frozen ReC98 revision is `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
The Japanese stored OP target remains `candidate-local-attested`; pristine
attestation is unknown. Its stored database was re-attested before decoded
analysis. The DIET restoration and original complete MAIN cold receipts bind
all three compared images, separately from canonical storage acceptance.

## Functions and original coordinates

| Unit | Decoded target entry | Cold MAP entry | Bytes | ABI |
| --- | --- | --- | ---: | --- |
| `cfg_load` | `0990:0008` | same | 120 | near, no arguments |
| `cfg_save` | `0990:0080` | same | 67 | near, no arguments |
| `cfg_save_exit` | `0990:00C3` | same | 84 | near, no arguments |
| `game_exit_to_dos` | `0BEB:0008` | same | 25 | far, no arguments |
| `vram_planes_set` | `0BEB:0021` | same | 41 | far, no arguments |
| `snd_determine_mode` | `0BEB:004A` | same | 29 +1 producer | far, no arguments, AX result |
| `game_init_op` | `0BEB:0571` | `0BEB:0570` | 105 | far cdecl, four-byte pointer argument |

The configuration functions are a bounded 271-byte portion of
`th03/op_01.cpp`. Its other menu functions remain unreviewed here. The other
four source carriers are `th02/exit_dos.cpp`, `th01/vplanset.cpp`,
`th02/snd_mode.c` and `th03/initop.cpp`. Complete boundaries, all interior
returns, direct branches, modeled interfaces, native helper calls and the
near-call PUSH CS frames are checked in both coordinate sets. The sound
producer at `0BEB:0067` is observed as NOP and checked in its original
checksummed OMF emission. The frozen source uses `#pragma codestring`; that
candidate mechanism is not imported as maintained source or exact encoding.

All unshifted CODE extents, the sound producer and native compiler helper
match both cold products with their original ordered relocation sequences.
Initialization fails the fixed-coordinate raw/relocation comparison. Even
when the two complete bodies are read at their respective entries, one raw
near-call displacement byte differs: the native plane callee remains `0021`
while the initializer shifts by one byte. Both literal slices and both fixed
relocation lists are retained. No shifted equality or whole-carrier acceptance
is claimed. The full OP comparison retains 4,867 changed image
bytes; this review does not classify that whole failure.

Receipt: `.analysis/sol-op-configuration-review-20261006.json`, SHA-256
`ecb383f145486d9b978408c09e40b540c37f2aff6c335a3952cd28fec2ce3fe1`; 330 guarded inputs.

## Configuration layout and observable hazards

The compiled configuration structure is eight bytes: BGM/key/rank at offsets
0/1/2, the unused signed word at3/4, the resident segment at5/6 and debug at7.
The resident far-pointer variable has zero offset and the loaded segment at
DGROUP `2464/2466`. Resident rank/BGM/key fields are at `0B/15/16`.
These offsets are bounded native observations rather than full resident
layout ownership. BSS fixtures are not initialized file slices.

`cfg_load()` opens `YUME.CFG`, requests eight bytes and closes the file without
checking the replies. It uses the resulting local bytes to replace the far
resident pointer and write the selected fields. Short reads preserve the
fixture's pre-existing stack bytes, including the segment. A zero segment is
also used directly. Rank, key mode and BGM bytes are not clamped here. The
matrix preserves these observations instead of adding validation.

The native sound-mode function executes INT60/AH09 under an explicit driver
reply fixture. Reply ALFF copies the raw `snd_midi_active` byte; other replies
set FM possible and active to1. Noncanonical active bytes2/FF are retained.
Configuration loading sets selection disabled only when this raw active byte
is zero, otherwise a configured BGM-off value clears active. Physical drivers,
interrupt handler execution and sound device eligibility remain open.

`cfg_save()` appends, seeks to0 and writes four bytes. It assigns only the
first three bytes of its stack local; byte3 comes from the fixture's prior
stack content. It leaves the on-disk bytes4..7, including the resident
segment, outside the write. Failed interface replies do not stop subsequent
calls. The file model captures the exact attempted write, without asserting
actual DOS persistence.

`cfg_save_exit()` copies the eight-byte zero template at DGROUP0091 through
the actual 28-byte `F_SCOPY@` helper, then assigns BGM/key/rank and writes all
eight bytes. Thus it zeroes the resident segment and debug fields. The native
helper clears DF and returns with far Pascal eight-byte cleanup while saving
BP/SI/DI/DS. The complete configuration caller uses a near return. The emitted
helper is compiled CRT context, separate from ReC98 authored-source progress.
The initialized zero template and nine-byte filename agree in all images;
this bounded association does not accept the complete DATA segment.

## Initialization and exit

Initialization requests22,000 paragraphs (352,000 bytes). Any nonzero
allocator reply returns1 without executing subsequent setup. On success,
actual plane initialization writes four full DWORD far pointers at DGROUP
19FA..1A09. Graphics and other library bodies remain explicit interfaces.
Native output instructions select access page1, page0, page0 and show page0
in order. The exact call sequence is graph start, two graph clears, VSYNC
start, beep off, system-line hide, cursor hide, EGC start, joystick start and
PF start. The original far filename argument is forwarded without validation.
The cdecl initializer retains its four argument bytes for its caller.

Exit executes the near PUSH CS call to `game_exit()` as a declared library
interface, followed by beep on, system-line show and cursor show. Complete
library behavior, allocation lifetime, physical display state and combined
menu/game execution are outside this bounded review.

## Native CPU diagnostics and replay

Each image runs4,320 terminal calls. The independent scalar specification
predicts exact ordered memory stores, file arguments and write snapshots,
native helper entries, driver replies, native port writes and AX outcomes.
All physical memory outside the64 KiB stack is compared per call. Native
near/far/helper return frames, saved registers, IF/DF and instruction boundaries
are checked. IF/DF combinations, driver replies, raw MIDI state, short reads,
zero and arbitrary resident segments, wrapped resident offsets, stack bytes,
failed file replies, allocator results and far filename extremes are covered.
Only `cfg_save_exit()` clears DF through the real copy helper.

All170 instruction positions execute in every image:153 new owned body
positions and17 compiler helper context positions. Across three images,
12,960 calls return. Producer NOP contributes a byte, not an executed
instruction. These counts do not add authored-source or exact progress.

Six source/root OMF objects per cold round are tied to their original
normalized object hashes. Four complete SHARED emissions have checked OMF/MAP
sizes; the sound producer remains an emitted byte. Twenty-two frozen
providers and both127-file archived source vectors bind source lineage. The parent receipt
retains152 historical input hashes;25 metadata/generated-probe paths are not
archived under the cold source trees and are not used as current source evidence. The plane
wrapper is the declared maintained MAIN forwarding provider, whose archived
body hash is checked. MAIN source/exact acceptance does not transfer to OP.

Eight portable negative controls reject incomplete returns/producers, operand
or neighbor branches, unknown interfaces/devices, missing near-call far frames,
whole-span stores, segment aliases, changed caller/model destinations, stale
completion and native helper stack corruption. The encoded fixtures are test
inputs, never maintained product source.

```sh
python3 scripts/review_th03_op_configuration.py --output .analysis/NEW_OP_CONFIGURATION.json
python3 -m unittest discover -s tests -p test_op_configuration_review.py
python3 scripts/ci.py
git diff --check
```

Continue the rest of `op_01.cpp`, OP music/main/selection/score carriers and
root/library intervals. Keep headers, dependencies, DATA/BSS, source encoding,
canonical DIET storage and full Oracle acceptance separate. The505-file intake
remains open; this cohort does not redefine completion around selected CODE.

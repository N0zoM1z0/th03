# Complete shared sound loader review

Frozen revision: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
Japanese YUMEZIKU targets remain `candidate-local-attested`; independent
pristine-dump attestation is unknown. Both packed Ghidra databases were
re-attested before target observations. DIET restorations remain diagnostic
images, with no replacement of canonical targets or invented stored offsets.

The complete `th02/snd_load.cpp` carrier is 112 bytes and 45 instruction
positions in each artifact. Independent bindings are OP `0BEB:00A2`,
DGROUP `0D7F`, filename `1A0E`, MIDI byte `1A0B`; and MAINL `0C7E:00A0`,
DGROUP `0E3F`, filename `1C74`, MIDI byte `1C71`. There are no carrier MZ
relocations. All branches stay within complete decoded instruction boundaries.
The far C function preserves its six caller-owned argument bytes: the far
filename pointer is at BP+6 and function word at BP+10. It executes a plain
RETF, with no Pascal cleanup. Thirteen forward byte copies use the actual far
source pointer, reloaded on each iteration, and wrap its effective offset.

One physical producer is reused: `obj/th02/snd_load.obj`, compiled by TC86
Borland C++ 4.02 with `-DGAME=2 -ml -DBINARY='O'`, then linked into TH03 OP and
MAINL at their original ordinals. The current link graph has no MAIN sound
loader input. The GAME2 flag is a compiler observation, without TH02 exactness
or product credit. The fixed filename width and read size are independently
bound by native instructions, rather than inferred from the compiler macro.

Twelve frozen providers cover the wrapper, complete implementation, headers,
inline dependency, BSS declarations and link graph. Both actual previous cold
trees retain the frozen sources, except the already recorded MAINL vector
input replacement. The diagnostic explicitly reverses that one known filename
replacement to check the complete original Tupfile; the source replay checks
the unchanged current link-graph digest. Headers, sound-driver buffers, BSS,
driver ISRs and full product ownership remain open.

Diagnostic receipt: `.analysis/sol-shared-snd-load-review-20261006.json`, SHA256
`59f2c5f6e99ab862fd0dfa554117a871c8f8c0f2f17a10c4ad8918fb99627ba9`, 590 input guards.
Each artifact's decoded target and two preceding math cold images passes 214
invocations: 213 native far returns and one bounded filename-scan prefix.
All 45 positions execute, with 2,947 ordered native byte stores and 852 declared
software interrupt requests per image. Complete original raw bytes, empty
original ordered relocation lists and original MAP contribution agree.

## Independent scalar and interrupt boundaries

`review_th03_shared_snd_load.py` runs the actual loader instructions without
substituting function bodies. Its scalar reads the pre-call physical memory,
including the actual source bytes, source/output overlap and saved-register
slots. Full physical 1 MiB memory equality includes the caller stack. The three
native prologue writes are separately constrained by CODE position, address,
width and value, and reproduced in the scalar. Ordered copy/extension stores,
software interrupt numbers and complete 16-bit register requests are checked.
The actual far return reaches its physical sentinel with the correct CS and
SP. Incoming IF and DF are preserved under the declared interrupt fixtures.
Unicorn code-hook IP reports a physical low word in this version; it is not
misinterpreted as logical IP. No memory-read hooks are used.

INT 21h open/read/close and INT 60h/61h driver responses are explicit fixtures.
Their supplied return registers, carry bit and physical memory writes are
distinct from native instruction effects. The read fixture writes only its
declared payload; successful byte count, short reads, errors and zero payload
are separate cases. It does not infer real DOS behavior or a driver buffer's
capacity. A segment:FFFF payload crossing is a physical fixture write, without
a claim about actual DOS or processor segment-limit handling.

The preserved hazards are observable in the native loader:

- Exactly 13 bytes are copied, regardless of an earlier NUL. A forward copy
  with the source one byte before the output propagates prior stores.
- MIDI song-name scanning starts at index 1. An empty name can scan stale
  bytes; a missing terminator can append beyond the 13-byte filename object.
  A bounded nonterminal scan is recorded without claiming a returned call.
- MIDI is checked both before extension and after DOS open. A declared open
  fixture can change the MIDI byte, so extension and driver choice can differ.
- Open carry/errors are ignored. The returned AX is used as BX even on error;
  the driver and DOS read still run, followed by close.
- Driver DS:DX determines the read destination. Driver or DOS read changes to
  BX reach close; the original opened handle is not saved separately.
- Read always requests `5000h` bytes. Close replaces AH with `3Eh` but keeps
  the preceding read result's AL. The saved DS is popped before close.
- A declared read payload aliasing saved DS/SI/BP changes the restored values.
  These stack effects are checked in the full memory comparison, without an
  assumption that saved values survive arbitrary buffer aliases.

The matrix includes song/SE/other function words, zero/nonzero MIDI bytes,
all 13 terminating positions, every incoming IF/DF combination, far offset
wrap, equivalent physical pointers, null and stack sources, output overlap,
long scans, full/partial/error read responses and driver-buffer aliases.
Three calls on one emulator retain filename and fixture state between calls;
caller registers and argument frames are refreshed. This tests persistence
without pretending that different caller frames have identical memory hashes.

Ten focused controls pass. They reject binding/branch/cleanup/count changes,
exercise all reachable positions, observe ignored open errors, empty-name
overruns, overlapping forward copies, live MIDI rechecking, BX flow and saved
stack aliases, reject a native INC-to-DEC copy mutation, and reject an extra
physical byte introduced into the scalar model. Fixtures give no actual DOS,
driver ISR, sound timing, asset, CRT, canonical packaging or complete Oracle
acceptance.

## Maintained source

`src/shared/sound/load.cpp` localizes the complete frozen implementation with
two compatibility imports. The new `compat/rec98/th02/snd/impl.hpp` forwarder
keeps the unreviewed inline/header dependency explicit. The fixed read helper
still belongs to the private scaffold; no inline/header or BSS acceptance is
inferred from the CODE migration. There are no target-byte arrays, codestring
padding or fake ABI declarations.

The first preparation stopped before compiler execution because a combined
ASM-wrapper check applied LF normalization to drawing wrappers whose declared
hashes preserve CRLF. Drawing and math checks now use their own recorded
line-ending conventions, as in the preceding replay. The first failure log
and original replay snapshot are retained separately; no byte, layout or
compiler gate was weakened.

Two source-c cold rounds passed the compiler and native gates, but tracking
rejected the new forwarding-header comment: compatibility forwarders must
contain only their declared include. The comment was removed and the complete
source-d replay repeated with frozen final inputs. Source-c remains historical,
with its deliberately superseded tracked forwarder hash; it is not rebased or
used as current source evidence.

Final source receipt:
`.analysis/th03-shared-snd-load/sol-shared-snd-load-source-20261006-d/receipt.json`,
SHA256 `0f54d49eb2f0f9c6db517fe6f367bf784826544a15b26860497f13b2f0dafdf9`, 597 guards.
Each of two fresh source images per artifact passes 99 calls: 98 far returns,
one bounded scan prefix, all 45 positions, 1,431 ordered native stores and 392
interrupt requests. Original complete raw/empty ordered relocation/public/MAP
and TC86 nondependency OMF records match. The physical producer retains its
CODE112/DATA0/BSS0 SEGDEF records: `287000020301`, `480000040501`,
`480000060701`. Both 20-product/351-game-object vectors are deterministic;
all 417 OMF hashes are recorded. All 20 products equal the preceding math
proof and 350 other game objects are unchanged. Nine nongame Research timestamp
changes in each round remain separate, without 417-object determinism credit.

OP has 26 reviewed decoded units/11,734 bytes and 19 source-present
extents/11,367 bytes. MAINL retains 145 rows, with 17 source-present
extents/2,004 bytes in three shared CPP TUs and four ASM TUs. One existing
MAINL row is upgraded without duplicate interval credit. The MAIN accepted
aggregate is unchanged. Whole OP six-byte/MAINL 21-byte and original relocation
order inequalities remain; OP/MAINL exact acceptance stays zero.

Current coverage receipt:
`.analysis/sol-current-decoded-coverage-after-shared-snd-load-20261006.json`,
SHA256 `4a086460d41dd2951382ce6294a78270791c97938a7b091ca1e4d5ac44394c18`, 612 guards.
OP's 100 carriers/55,262 bytes have 11,734 reviewed bytes and 43,528 gaps;
MAINL's 108 carriers/58,340 bytes retain 28,381 reviewed bytes and 29,959 gaps.
Both have zero overlap. MAINL interval credit is unchanged.

Cleanup receipt: `.analysis/sol-shared-snd-load-temporary-cleanup-20261006.json`,
SHA256 `a77b7fc18f74a790d4348748935d875fd6e7cfba23d1c4880748a0d119940a5f`, nine guards.
Two stopped preparations are removed: 4,038 files/46,571,507 bytes (44.4 MiB).
All 1,924 retained private input states are unchanged. Logs, failed forwarder
and replay snapshots remain outside the removed trees. Complete successful
source-c and current source-d proof trees remain; historical missing/stale
inputs are preserved without repair or guard rebasing.

Full CI passes 567 tests and all available private headless gates:
`.analysis/sol-shared-snd-load-complete-ci-20261006.log`, SHA256
`ae0e5246b39ac55f068bdf553d5fb04f5b5c167c3f0a26e4a98f5aa83bcee17d`. Tracking: 235 units, 2,283 evidence rows, 284 knowledge rows and
120 MAIN authored-function rows. The full 505-file review/migration goal remains
open. This bounded migration grants source presence, with no new exact claim.

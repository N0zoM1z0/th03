# Five OP helper maintained-source checkpoint

Five complete original source bodies now have fresh native producer evidence.
This adds 247 scoped function CODE bytes, taking OP to 42/45 source-present
units and 12,816 scoped CODE bytes. Exact credit stays zero.

| Function | Decoded extent (end exclusive) | Function bytes | Physical TU | Language/GAME |
| --- | --- | ---: | --- | --- |
| snd_determine_mode | 0BEB:004A-0067 |29| th02/snd_mode.c | C/2 |
| snd_pmd_resident | 0BEB:0068-00A1 |57| th02/snd_pmdr.c | C/2 |
| polar | 0BEB:0155-016F |26| th03/polar.cpp | C++/3 |
| SND_KAJA_INTERRUPT | 0BEB:0553-0571 |30| th03/snd_kaja.cpp | C++/3 |
| game_init_op | 0BEB:0571-05DA |105| th03/initop.cpp | C++/3 |

## Original source and target boundaries

Maintained bodies are copied from the original reference source, changing only
quoted include prefixes to explicit compat/rec98/ forwarders. Original physical
TUs, C versus C++, GAME macros, pragmas, far calling conventions, signed
arithmetic and call order remain intact. There are no byte payloads, ABI shims,
padding changes or output repair. The candidate config and source-only stager
remain the exact declarations consumed by the native attempt.

The earlier 30-byte snd_mode observation remains historical producer evidence.
A distinct target-side review establishes 29 function bytes, ending with RETF at
0066, and excludes the original codestring NOP at 0067. The three direct incoming
calls target 004A; internal branches land 005C/0060; no observed interior/NOP
entry or relocation straddle occurs in the bounded target scan. The neighbor
starts 0068. The new PMD, polar and KAJA rows were independently reviewed against
the OP target, not inherited from MAINL ownership.

PMD returns at 009D/00A0 and excludes its original NOP 00A1. Polar ends with RETF
at 016E and excludes alignment byte 016F. KAJA ends in RETF2 at 056E..0570. The
boundary report binds 142 reviewed bytes across these four bodies; game_init_op's
existing 105-byte reviewed scope is retained. Incoming-edge analysis has explicit
static scan limits and makes no claim about every possible indirect entry.

## Actual bounded native evidence

At clean historical HEAD 6e895a923632a94323b6ecba6fd0237ac78cebc5, the parent
completed five original compiler phases and one unchanged link in two groups.
Factory command 61f7b466fe894de993651d9c80390dc5 completed group1; command
d3d9c486f8b94dd38b0b8573823b62fd completed group2. All six exact-owned cleanup
and registry-transition receipts pass, with shared lock release, one CPU,
nice>=10, headless operation, 90 seconds work and 15 seconds bounded cleanup.
The actual carrier path is resolved from the final manifest, whose carrier is
OPRH101. Exactly 22 OPXH101 project objects are retained, never recredited.

Actual OMF dependencies identify the maintained sources and active forwarders;
original physical TU, compiler and language comments, literal non-COMENT
records, public ABI, producer CODE extents and zero DATA/BSS are checked.
Three game_init_op TC4 header dependencies bind to pinned compiler includes.
The inactive GAME3 KAJA TH04 include remains pinned context, not a fabricated
emitted dependency. All 247 function bytes and literal ordered fixups match the
decoded target. Full producer comparisons also preserve both uncredited NOPs.

The prior 37 bodies/12,569 bytes retain their raw bytes, ordered fixups and MAP
extents. Complete MAP publics, program bytes and global relocation order are
unchanged versus OPXH101. The resulting EXE SHA-256 remains
9f2e2af591645963d802489b45f9355a1e9f9b4da4b49ab0767f5be069ec204d.
Six whole-program target byte differences and 313 global relocation-order
differences remain. Whole-file target equality is false. This is not a repeat,
full cold build, runtime/model run, packing proof or whole-product acceptance.

## Guarded retained replay and installation

Run scripts/replay_th03_op_remaining_helpers.py with the repository virtualenv.
The compact config/op_remaining_helpers/proof.json pins an ignored retained-input
dictionary. Every retained artifact and actual current source/import closure is
checked before importing the structural verifier. Both native groups and all six
execution/cleanup/registry receipts replay without launching native tools.
Historical HEAD is receipt identity, not an obsolete whole-repository guard.
Only the five new owners receive new source-presence evidence; previous proofs
remain separate and unchanged.

The sparse installer updates only mode/init, adds PMD/polar/KAJA, and appends four
new evidence rows. It preserves every unrelated ledger row byte-for-byte,
including prior OP, ZUN and MAINL entries. Historical mode 30 evidence remains
untouched. New evidence canonical extent_start/extent_size and all new unit
packed file offsets are blank; decoded locations are recorded in notes.

Source-only tests also run under portable unittest discovery without mandatory
CLI arguments. The progress-layout test updates both numeric 42/45 and SVG text
Source 42/45 expectations. Parent regeneration of docs/PROGRESS.md and
resources/progress.svg follows ledger installation; no runtime or exact credit
is inferred from the resulting display.

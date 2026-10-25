# Architecture

TH03 has four products: OP.EXE (menu), MAIN.EXE (game), MAINL.EXE (ending)
and ZUN.COM (launcher). Product source belongs under the matching `src/`
directory; proved shared code belongs in `src/shared/`.
`.c`, `.cpp` and `.asm` are translation units; `.inl` files are bounded includes.

The Japanese targets are pinned in `config/targets.toml`. Their provenance is
`candidate-local-attested`; independent pristine-dump attestation is unknown.
OP/MAINL/ZUN use DIET storage envelopes. Decoded images are analysis inputs,
not replacements for the canonical stored targets.

All five ZUN payloads now have native project producers. ONGCHK (-1) uses a
self-contained recovered TASM TU: 892 CODE + 34 initialized DATA bytes and 42
separate uninitialized bytes. Its COM is an output, not a reference binary input.
Its complete initialized source scope has native and bounded full-state instruction
acceptance; original source/tool identity and whole-product ownership remain open.
MASTERS.LIB and installed Borland startup/runtime remain explicit unowned context.

`config/toolchain.toml` pins TC4J, TASM and TLINK. The game-local Wine prefix is
`.analysis/toolchain/wineprefix`; Ghidra projects are in `ghidra-project/`.
Installed tools are in `drive_c/TC4` and `drive_c/TASM50`; `drive_c/TH03WORK`
is the current MAIN build. `scripts/attest_toolchain.py` checks installed tools.
`_reference/ReC98` is candidate reference material, not authored progress.
Product dependencies use local source or explicit `compat/rec98/` forwarding.

The ZUN sprite16 driver also has a bounded compatible OMF producer pinned in
`config/th03_zun_driver_jwasm.toml`. Its public source and private native tool
are attested separately; the normal TLINK still links the resulting object.
This does not identify the original assembler or change the base Borland tools.
The syntax adapter preserves all maintained instruction and data includes.
The driver uses one translation unit with nine CODE contributions in DGROUP.
Root WORD/EVEN alignment and eight PARA contributions generate its 71 intergroup
zero bytes through normal TLINK layout; no sized filler arrays supply them.
This compatible organization preserves every linked byte and public address;
the original source/object organization is unknown. Three plus nine reserved
DATA bytes remain separate, unreviewed context.

Ten complete driver formatter/print procedures own 677 library CODE bytes.
Direct control-flow traversal proves four jumps (eleven bytes) unreachable;
the independent guest contracts execute all other 666 bytes. Preserve DWORD
argument slots in SS, signed WORD padding, sign-before-padding and the unchecked
208-byte wrapper buffer, including saved-BP overwrites at output lengths 208/209.
PUSHA restores WORD registers while numeric high halves can change. DOS AH=2 is
a bounded interface; actual formatting, reverse and strlen instructions execute.
The current formatter review binds a full cold pair and three relative WORD
fields plus one absolute DWORD digit-table field; the table adds no DATA credit.

Twelve driver graphics procedures own 814 library CODE bytes. Native ownership
checks 62 WORD fields; direct CFG proof separates four dead clipping-jump bytes
from 810 executed bytes. A bounded two-page/four-bank word-memory interface
checks CPU writes, page selection and exact port width/order/IF/DF. It does not
emulate EGC latches, raster operations or physical pixels. Real nested helpers
execute, including the 65,536-row zero-height loop. EGC begin/end force IF on;
top clipping does not perform a second bottom pass. Shared state and buffers
remain external dependencies, with no new DATA ownership.

Eight driver lifecycle procedures own the remaining 564 library procedure CODE
bytes. Their 69 native WORD fields include 27 relative calls. Actual maintained
parser, formatter and graphics helpers execute under independent specifications;
DOS allocation, resize, free and exit replies remain bounded. DOS 4C/31 are
terminal: 549 bytes execute and fifteen following bytes are unreachable under
that contract. Install compares the signature at segment:0102, saves the old
vector and retains two decimal-1000-paragraph buffers. Uninstall deliberately
restores offset zero, then frees environment, mask, solid and code in order.
IRET restores a six-byte frame and stacked flags, overriding the internal STI.
All 55 driver procedures have scoped acceptance. Four additional extents own
the startup header, digit alphabet, packed shared DATA and ON/OFF strings:
2 CODE + 1,294 DATA bytes, including a 512-byte initialized stack and 64 near
token pointers. Twenty-five native WORD fixups bind the option and service
tables. Independent consumers use raw defaults, strings and tables at two
loads. Option checks supply mutable argument-count/vector inputs and stop at
callback selection, with bodies covered by their own
procedure reviews. Separate semantic checks cover every initialized DATA byte.
Three plus nine reserved bytes still have no ownership. These DATA checks do
not promote the enclosing driver or establish the original source organization.

The outer ZUN launcher and two transfer TUs own 213 CODE + 21 DATA bytes.
Nine native WORD fixups bind the root's counts, names, entries and scratch word;
the transfer CALL/helper have none. Three individually linked tiny objects
keep their ORG 0100 and native entry/group records, then compose at their actual
outer COM positions. The three wrapper TUs exclude the directory metadata.
FCB filename bytes select the payload independently of the selector text.
Success leaves a WORD remaining count on the caller stack; the trailing helper
discards its CALL return and enters 0100 before any payload instruction runs.
Direct transfer contracts require DF clear, DI=0100 and a bounded payload span.
Three explicit DOS AL reply policies expose the AH-only termination status.
Complete memory and ordered stores are checked, including transient stack words,
forward overlapping moves and an SS different from DS. Unowned payload/runtime
dependencies and whole-product source ownership remain open.

The directory now has its own maintained semantic DATA TU under `src/zun`.
TASM/TLINK emit all 324 bytes from the count, fixed names, 32-slot ABI and seven
actual linked-length definitions. Four public labels rebase to count 01DF,
names 01E1, entries 02E1 and following CALL 0323. Six ordered WORD boundaries
cover the five opaque payloads; unused names and entry words are format slots.
Two literal OMF records and two bounded iterated records explain all storage.
The compositor consumes the complete linked directory directly; its independent
format contract checks every field. Capacity-31/33 native source controls emit
314/334 bytes and fail equality. No CODE or payload ownership follows from this
DATA scope, and the original directory generation tool remains unidentified.
The native composition adapter has its own module; the shared historical
constructor remains byte-identical to the promoted MAIN scheduling pin.

`src/shared/hardware/input_modes.cpp` is one complete nine-function / 367-byte
CODE producer in both OP and MAINL, retaining its GAME3/O first-use wrapper.
Its two link layouts and six ordered far-pointer relocations are reviewed
independently. `review_th03_shared_input_work.py` binds the full current cold
pairs to complete input-policy and wait witnesses; per-product publication
retains separate source acceptance. Keyboard, joystick and frame services are
bounded interfaces, with zero private DATA/BSS ownership in this producer.
MAINL also owns two ending waits / 126 CODE bytes in a separate GAME3/L
producer. They execute the owned input interface: its AX result replaces the
sound query result before the unsigned measure comparison. Frame waits use
an unsigned IRQ counter and preserve their distinct far Pascal cleanup sizes.

Six MAINL sound/timing procedures own 332 CODE bytes in five whole producers.
Native ownership checks 33 fields, a genuine TLINK same-CS call relaxation and
empty MZ relocation vectors. Source first-use slots remain GAME2/O for shared
load/delay, GAME3/M for SE, GAME3/O for KAJA and GAME3/L for measure wait.
Global sound tables/state, filename scratch and IRQ counter remain external
storage; 69 initialized dependency bytes gain no DATA credit. Keep BYTE frame
wrap and full-WORD priority indexing, fixed 13-byte far filename reads, unchecked
suffix extension, file-error continuation and DS restoration before close.
Loader MIDI uses nonzero; KAJA/measure use exactly one. Actual frame_delay runs
inside the no-BGM measure path. Finite counter updates and DOS/driver replies
bound these contracts; physical timing/audio and adjacent explicit padding
remain unproved.

OP independently owns the complete 112-byte sound loader and 21-byte delay
producers, with ten literal native WORD fields and no MZ relocations. OP global
addresses and both MAP tables are separate from MAINL. A shared independent
execution core supplies the same file/driver/counter contracts to both layouts;
product-specific case domains, native ownership and cold bindings stay separate.
The model refactor preserves the complete MAINL runtime trace vector.

OP additionally owns its 105-byte initializer, 30-byte KAJA and 21-byte duplicate
frame_delay_2. The KAJA/initializer wrappers each retain two explicit include
layers; every staged link and native dependency is checked before source credit.
Sixteen native fields and eleven ordered MZ relocations pass;
the actual plane-set far call relaxes normally and all 41 plane-helper bytes
execute. Initialization requests 22,000 paragraphs, returns one immediately on
any nonzero WORD allocation result, and otherwise forwards the far filename
unchanged while ignoring later errors. It is far cdecl; both sound/timing
helpers are far Pascal with two-byte cleanup. frame_delay_2 shares vsync_Count1
with frame_delay; its name does not indicate another counter. Global plane and
sound storage gains no additional ownership. Device/package/driver replies and
finite counter changes remain bounded interfaces.

OP's three near cfg functions own 271 CODE bytes inside the larger entry TU.
Containing menu CODE/DATA/BSS stays context; the flag, zero template and filename
are separately reviewed dependencies. `review_th03_op_cfg_work.py` guards the
five consumed SDK headers around an actual OP cold pair and binds full cfg
contracts. Ordinary saves retain the fourth uninitialized stack byte; exit saves
copy the real eight-byte zero initializer. PMD-mode and CRT helper instructions
execute, while file/PMD replies stay bounded interfaces. Helper alignment and
whole-entry ownership remain open.

The same entry TU has two accepted near demo/score dispatch bodies (296 CODE
bytes). They execute the real cfg save, sound routing and game cleanup; library,
driver and failed-exec replies remain bounded interfaces. Demo BYTE 255 wraps
to zero and reads adjacent table bytes. Score dispatch returns false in AL;
AH survives the failed execl reply. Its twelve argument bytes are caller-popped.
The screen ledger partitions its former 1,222 bytes without overlapping credit;
story/VS behavior still lacks current acceptance; the choice renderer is reviewed below.

The 105-byte near OP attract wait now also has scoped acceptance. It executes
423 real input/demo/cfg/sound/cleanup/delay bytes under independent contracts. Every
poll increments the resident DWORD random value and delays even after finding
input; poll 521 still calls demo first. Preserve signed WORD frame wrap and
fourteen box-column steps. Whole-entry cases and explicitly supplied loop
continuations have separate witness counts. The latter execute the real
prologue before supplying SI; they do not prove elapsed physical time or an
unbounded interactive lifetime. The actual frame-delay body executes on every
poll and animation step. Graphics/counter/device/exec replies stay bounded.

`.analysis` keeps targets, runtime files, tools, current Ghidra state and one
working build tree. Historical experiments and validation archives are disposable.
Download archives and installation media are needed only for installation;
bootstrap checks their hashes. Routine checks verify the installed tools.

Three complete choice renderers own 518 CODE bytes in that same entry producer:
VS 66, main 122 and option 330. Their 39 native fields include four internal
CODE WORD switch targets and seven MZ far-call relocations. Full raw bytes,
per-owner and cross-renderer relocation order are checked independently.
The option body has 321 instruction bytes and nine non-instruction bytes after
RET (a compiler-emitted zero and four WORD entries). All 509 renderer instruction
bytes execute; those nine bytes have complete native/table proof and no execution
credit. The 169 initialized string bytes remain external DATA dependencies.
Gaiji/text calls receive real far strings, WORD attributes and Pascal frames;
the library replies are bounded. Invalid selector and BYTE-state behavior,
register leaks and the fixed-white rank erasure remain intact. The source ledger
partitions existing screen/menu spans without adding source-present bytes.

A bounded sound layout diagnostic separates instruction recovery from unresolved
trailing bytes. Removing active codestrings in disposable source copies preserves
all nine selected OP/MAINL function bodies. Ordinary compiler-assembly output
changes link layout. An explicit WORD-segment annotation control preserves those
bodies and recovers the target headers and complete ordered relocation vectors,
leaving two OP and four MAINL gap values at 00 instead of 90. This control does
not prove an original or acceptable production recipe. The current product
sources/builds and all acceptance counters remain unchanged; the trailing-byte
producer is still open. DPMI -WX also changes real code and cannot be treated
as a pure alignment flag. The SE codestring is conditional on another GAME;
its GAME3/M diagnostic copy retains that inactive source branch.

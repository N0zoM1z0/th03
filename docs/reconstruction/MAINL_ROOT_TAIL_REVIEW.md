# MAINL remaining root helpers and producer review

This independently reviews the remaining sixteen disjoint gaps of the frozen
MAINL `th03_mainl.asm` root _TEXT carrier:722 bytes. They include701 body
bytes /351 instructions and21 separate producer bytes, not additional
maintained product source. Prior PFOPEN281 is context only. No canonical
stored-file offset or exact acceptance is assigned to the decoded namespace.

Receipt: `.analysis/sol-mainl-root-tail-review-20261006.json`, SHA-256
`a37eade687a70135c7a054420db3c38d8f7a4658854930e6e08b990e580f501a`; 881 guarded inputs.

```sh
DISPLAY= WAYLAND_DISPLAY= python3 scripts/review_th03_mainl_root_tail.py \
  --output .analysis/NEW_ROOT_TAIL_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_root_tail_review.py
```

## Boundaries and lineage

| New independent extent | Root offset | Bytes |
| --- | ---: | ---: |
| Endfunc EVEN before BFNT_PALETTE_SET |04C5|1|
| Endfunc EVEN before BREAD |060B|1|
| Endfunc EVEN before BSEEK_ |067D|1|
| Endfunc EVEN before DOS_AXDX |06AD|1|
| DOS_KEYCLEAR |06FE|6|
| GRCG_SETCOLOR/OFF with producer alignment |0C36|48|
| Explicit root db0 before GAIJI_BACKUP |0C71|1|
| IATAN2, trailing EVEN and JS_END |175E|114|
| EVEN before PFGETC1 |1903|1|
| Explicit pfgetc db0 |19A3|1|
| Endfunc EVEN before PFSEEK |1A0D|1|
| IRAND |1A3E|42|
| SOUND_O/I, TEXT_CLEAR/FILLCA and alignment |1EF6|116|
| RESPAL_EXIST/CREATE/SET_PALETTES and alignment |276E|226|
| Root db0, JS_START, SOUND_JOY, JS_SENSE, SAJOUT and alignment |2AAD|105|
| Prior PFOPEN alignment and private STR_IEQ |2C2F|57|

Seventeen tail bodies plus STR_IEQ contribute701 bytes. Eighteen complete
bodies have351 instruction positions;344 execute in the matrix. The seven
unexecuted positions are1799 (IATAN2's internal EVEN NOP) and the six
instructions at2B0C/2B0E/2B0F/2B11/2B12/2B14 of the unreferenced SAJOUT.
No approved public entry calls that private routine. It has structural/raw
review only; the harness rejects bare private execution. Seventeen separate
EVEN bytes are90, and four explicit source db0 bytes are00. Producers never
become execution boundaries. JS_END's leading nopcall NOP is inside its six
body bytes and executes before PUSH CS/real far DOS_KEYCLEAR return.

Both fresh cold MAINL products match all1003 scoped CODE/producer bytes,
including prior PFOPEN281, and290 initialized DATA bytes: atan256, random
seed4, joystick configuration8, text configuration8, resident segment2,
tone2 and signature10. All scoped ordered MZ relocations are empty and equal.
The256 atan bytes independently match nearest rounding of
`atan(index/256)*128/pi` and the frozen literals. Palette/current joystick
state are BSS fixtures, excluded from file-slice claims. Full ending image
and other physical carriers remain separately reviewed/open.

Thirty-nine consulted providers at frozen ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` match both cold source trees.
The func/endfunc EVEN macros, preceding BFILL/BOPENR/BSEEK_/PFREWIND
providers and root/pfgetc db0 directives distinguish emitted alignment from
explicit data. Root OMF identity and thirteen public MAP entries are pinned;
normalized object SHA-256 is
`776680636e46c2e12ebe1e3d5b78a7af34ed2b271080e96c3c333b01bf91cefe`.
The152 archived MAIN replay inputs retain their original hashes. Seven
MAIN-only Tup substitutions and existing MAIN forwarders remain explicit
compiler lineage, not MAINL acceptance. ASM/INC provider comparison alone
normalizes LF/CRLF. No new cold build is claimed.

Selected stored packed MAINL was re-attested before target-dependent work.
No unpacked Ghidra observations or automatic-function/authored-source credit
is used. Targets remain Japanese YUMEZIKU, candidate-local-attested, with
independent pristine-dump attestation unknown.

## Native execution and independent models

Each image has3895 tail scenarios/8445 top-level calls:8435 returns and10
native DIV stops. All three have25335 calls /25305 returns /30 faults and
28965 native entries. Another72 semantic prefixes retain open native frames.
The separate PFOPEN context adds318 calls:312 returns and6 search budgets,
with1734 native STR_IEQ entries. These counts remain separate from prior
receipts and grant no complete runtime or source acceptance.

Tail public entries execute natively with checked PUSH CS/near-call far
frames, real near helpers, return addresses, CS/SS/SP, complete instruction
boundaries, cleanup and BP/SI/DI/DS preservation. Independent scalar algorithms
compare ordered CPU stores, ports including live IF, DOS/console events,
native-entry counts, CF/AX where specified, IF/DF and all1MiB physical memory
outside64KiB stack. Each image keeps its own unrelated executable/DGROUP
bytes; cross-image normalization omits whole-memory hashes only.

DOS52/58/48/49/0C, INT29 console output, FM status/register reads and BIOS
row byte are explicit fixtures. The script models returned AX/Carry and
specified preserved service registers; it supplies no actual DOS, hardware,
keyboard-buffer, text-rendering or asynchronous IRQ Oracle. No real target
function is replaced in the tail CPU scopes.

STR_IEQ separately executes only through complete native PFOPEN281, retaining
its previous five explicit buffer/heap interfaces. The legacy matrix covers
full DGROUP,31-byte heap record and two64KiB input buffers, native comparison
frames/iterations and ordered interfaces/stores. It is not represented as
the same whole1MiB comparison or native heap model as TailProbe. Previous
PFOPEN receipts retain their original scope; their281 bytes are not credited
again. All29 STR_IEQ instructions execute through those public callers.

## Observed arithmetic, text and device behavior

- IATAN2 retains16-bit signed absolute-value comparison before unsigned DIV.
  INT_MIN can select a zero/small denominator, causing actual divide faults.
  Both DIV sites stop at INT0 without a handler/frame or fabricated return.
  Each case uses a fresh Unicorn engine. XLAT uses only the quotient low byte
  for nonfaulting extremes. All256 quotient indices, octants/quadrants and
 81 extreme pairs agree with the independent integer/table specification.
- IRAND updates the entire32-bit seed by `seed * 015A4E35h + 1`, modulo2^32,
  using two ordered word stores. The returned high word is masked7FFF;
  stored high bit remains. All32 basis bits, word/carry extremes and four
  1024-step native chains agree with the independent recurrence.
- GRCG_SETCOLOR uses low mode/color bytes, emits four per-plane00/FF tiles
  and masks IF throughout all five OUTs, restoring caller flags afterward.
  OFF emits0 and clears Carry through XOR. Real GRCG effects remain a model.
- TEXT_CLEAR emits ESC,[,2,J through four INT29 calls. FILLCA uses
  `80*(BIOS[0712]+1)` words per character and attribute plane, ignores the
  declared text width and retains DF. Both A000/E000 and BIOS row extremes
  show sequential stores,16-bit offset wrap and overlapping planes; display
  correctness and invalid BIOS geometry are not inferred.
- JS_START treats onlyFF as absent for up to256 probes, unlike sound helpers'
  bit80 busy test. An FF sequence through the256th probe returns0 even if a
 257th read would indicate presence. Present paths read register7, preserve
  bits0..5 and set upper bits10, with CLI/POPF around native sound calls.
- JS_SENSE has no-board AX retention and ORs the entry SI into js_stat:
  initial AX1111/SI1357/state8000 yields AX1111/state9357 with no ports.
  A board-present call ORs `~input & 3F` into accumulated state; it does not
  assign/clear prior bits. Native SOUND_JOY uses SOUND_O then a direct
  register0E selection/read, without another busy poll. Caller IF restores.

## Resident palette and lifetime hazards

RESPAL_EXIST always issues DOS52 and traverses actual modeled MCB memory.
Owner0 blocks are skipped even if the signature matches; nonzero-owner
blocks compare all ten `pal98 grb\0` bytes. A match can be accepted regardless
of the block type; nonmatches continue only for typeM. ResPalSeg is overwritten
with the found segment or0, and DF is cleared. List/MCB validity and cycles
are unchecked. Existing cached ResPalSeg does not bypass the native search
performed by CREATE. All signature-byte mismatches, owner/type and linked
chains are tested.

CREATE saves/restores allocation strategy without checking those statuses.
It allocates four paragraphs under strategy1; a segment above CS is freed
and retried under strategy2. The second allocation Carry is unchecked.
A modeled AX8/CF1 reply writes FFFF to physical0071 and the signature/header
at0080, stores ResPalSeg8 and returns1. This is an emulator observation of
unsafe code, not a real DOS-memory mutation. First allocation failure returns0;
a found palette returns2. Free/restore errors are retained as explicit service
results; no repaired lifetime or fallback is invented.

SET_PALETTES clears DF even when ResPalSeg0, writes the low tone byte and
converts R/G/B high nibbles into sixteen packed records. It loads R/G, writes
the word, then loads B. A destination alias can overwrite B before its read,
which the ordered memory scalar reproduces. All256 bytes in all three input
slots, tone boundaries and a live DGROUP alias are exercised. Current palette
BSS48 and joystick state are initialized synthetic runtime state, with no
file-backed/layout/source ownership inferred.

Twenty-four additional semantic prefixes per image retain genuinely open
native frames: sixteen sound-busy prefixes stop before the21st status read,
and eight cyclic-MCB prefixes stop before the8th block. Independent scalar
prefixes compute all ordered interfaces, stores, memory and final poll/block
position, without setting readiness, creating a terminator or fabricating
returns. The cycles use sizeFFFF, wrapping the next MCB segment to itself.

Ten controls reject incomplete/wrong returns, operand/neighbor/producer
branches, unknown calls/services/ports/widths, bare private entry, bad real
frames, full-span stores, stale completion and segment aliases. They also
verify palette alias read order, absent-stick SI behavior, unchecked second
allocation and a native open sound-prefix frame. Diagnostic opcodes/mocks
are test fixtures, never product source.

## Remaining acceptance and artifact scope

The refreshed interval coverage is recorded separately after this review.

Complete root decoded interval coverage is not a whole MAINL build or source
acceptance. Startup and remaining CRT carriers, root DATA/BSS layout, complete
callers, runtime/file/device lifetimes, other products and canonical DIET
packaging/full Oracle gates remain open. MAINL maintained source0/exact0 and
accepted MAIN101 functions/11628 bytes remain unchanged. The505-file intake
and69 scoped MAIN CODE paths are still a separate incomplete artifact review.

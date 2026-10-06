# Complete MAINL input and wait candidate review

Current input modes367, confirmation/measure waits126 and frame delay21 are
now maintained complete natural CPP carriers with independent OP/MAINL bindings
and two fresh cold rounds. Twelve existing MAINL rows are upgraded without
duplicate interval credit. Native scanner417 and the complete418-byte carrier
with trailing NOP remain contextual; its codestring is not imported. See
[SHARED_INPUT_REVIEW.md](SHARED_INPUT_REVIEW.md). The cached MAIN-remapped
observations and historical database failure below remain separate.

Three complete candidate TUs contain twelve functions, 910 decoded CODE bytes /
313 instructions. All raw bytes and six original ordered relocation sites match
both cached products. The actual 21-byte / eight-instruction frame-delay helper
also matches and executes. No maintained MAINL source, stored offset, cold build
or exact acceptance is added.

```sh
python3 scripts/review_th03_mainl_input.py --output .analysis/NEW_INPUT_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_input_review.py -v
```

Receipt: `.analysis/sol-mainl-input-review-20261006.json`. It guards the prior PI
receipt and its canonical/decoded/cached lineage. Eighteen consulted frozen
providers bind to both source trees. Three carriers are explicitly remapped:
input sensing, input modes and the frame-delay helper include maintained MAIN
implementations. Five maintained source/header files equal both cached copies.
The unused frozen implementations are candidate material, not those objects'
actual producers. No MAIN exactness is inherited. Ghidra fails headless-usage
before DB attestation, so no database observations are used.

| Function | Decoded 0C7E | Bytes / instructions | Far cleanup |
| --- | --- | ---: | ---: |
| Reset and sense keyboard | 0388 | 417 / 115 | 0 |
| Wait for OK or measure | 0C4D | 77 / 32 | 4 |
| Wait for OK | 0C9A | 49 / 19 | 2 |
| Interface mode | 0DC2 | 36 / 14 | 0 |
| Key versus key | 0DE6 | 10 / 7 | 0 |
| Joystick versus key | 0DF0 | 34 / 14 | 0 |
| Key versus joystick | 0E12 | 34 / 14 | 0 |
| One player versus CPU | 0E34 | 42 / 15 | 0 |
| CPU versus one player | 0E5E | 45 / 16 | 0 |
| CPU versus CPU | 0E8B | 42 / 14 | 0 |
| Attract mode | 0EB5 | 48 / 16 | 0 |
| Wait for change | 0EE5 | 76 / 37 | 2 |

Every branch stays inside complete instruction boundaries. Every optimized
near internal call has PUSH CS and targets a reviewed far entry. Multiple
returns in wait functions retain their exact cleanup. The only foreign call
is far joystick sensing at 0000:2AEA; measure interrupts are 60/61 and the
only output port is byte OUT 5F,AL. BP/SI/DI/DS and incoming DF are preserved
under the declared interfaces. ES is left zero by keyboard sensing, and BX/AX
are clobbered. No x87 behavior is present in these bodies.

## Native execution and model limits

All keyboard, eight mode, three wait and frame-delay instructions execute,
including internal calls, real far returns and the 1024-iteration delay loop.
BIOS key-state banks, joystick output, song-measure interrupt results and IRQ
counter updates are explicit fixtures. No real keyboard, joystick, music
driver, interrupt frame, scheduler or physical timing is proved.

The first BIOS bank is supplied at sense entry; the second is supplied after
the 1024th byte OUT 5F,0. The native function resets P1/P2/SP/js_stat[0], samples
nine groups twice and ORs their mappings across passes. Each terminal sensing
invocation emits exactly 1024 such writes. Keys present only in either pass
remain set. Contradictory direction bits are retained; they are not normalized
into a single direction. The upstream 614.4-microsecond comment is a device
timing claim, not a measured result of these CPU/port fixtures.

A separate source-level key/mode specification checks all 65536 DGROUP bytes
for terminal cases, preserving each image's own initial bytes. Before/after
hashes are separate, not a claim of full initial-DGROUP equality. Budgets check
that all bytes outside the five input/joystick/clock words remain unchanged,
and retain partial states rather than presenting them as completed returns.

Per image: 254 top-level calls, 242 returns and twelve 14000-instruction budgets.
Across target/two caches: 762 calls, 726 returns and 36 budgets. Each image has
332 native sensing entries, including entries interrupted by budgets; 331530
port writes are observed. Normalized observations agree across all three
images. Seventy-two individual BIOS-bit cases cover used and unused masks,
plus three all-bit union cases. The eight modes run three keyboard patterns,
joystick presence 0/1/FFFF and both DF states. Wait cases cover clock boundaries,
held release, negative/sentinel arguments, both sound interrupts and AX clobber.
Eight adversarial controls reject incomplete/wrong returns, operand/neighbor
branches, invalid near/far frames, unknown interfaces/interrupts/ports, aliases,
outside-state writes and stale terminal state; callbacks report errors outside
the native FFI boundary.

## Modes and joystick behavior

Joysticks are sensed only when the presence word is nonzero, except key/key
and CPU/CPU modes, which ignore them. Interface merges joystick and P1 keyboard
bits into SP while retaining multiplayer words. Joystick/key and key/joystick
replace the selected multiplayer word and use SP for the other player. The
one-player modes merge SP/P1/joystick and clear the CPU word. CPU/CPU collapses
OK/CANCEL to CANCEL and clears both multiplayer words; other SP bits remain.
Attract merges into SP then clears both multiplayer words. The joystick model
can return AX=FFFF; modes read its global state rather than this return value.

## Song-measure register clobber

The active-sound wait requests AH=5 at INT60 unless the MIDI-active byte at
DGROUP1C71 equals exactly1; then it uses INT61 with DX=C0 (48 ticks per quarter,
four quarters per measure). A MIDI byte of FF follows INT60, preserving the
source's equality check rather than treating every nonzero byte as MIDI.

After the interrupt, actual input_mode_interface runs the keyboard function,
optionally merges joystick state, and finally loads AX from P1 at1D08. The
following wait comparison therefore compares **P1 keyboard input**, not the
returned song measure. Its unsigned JB also treats the declared signed measure
argument as a word threshold. This is direct target/compiler behavior, not a
model returning zero from the input interface.

For returned song measures0/1/FFFF, P1 F gives AX4 and threshold3 exits false
after one poll. No keys gives AX0 and threshold1 remains nonterminal under
budget despite a returned measureFFFF. Comparisons record actual AX/threshold
at the native CMP instruction. OK/SHOT still exits true before the comparison.
Joystick-only movement does not replace the final P1 load; its SP merge and
the final AX are separate. No repair of this behavior is authored.

## Frame waits and release ordering

With sound disabled, measure wait delegates to the real OK wait, ignoring the
measure argument. OK wait resets the counter and always polls at least once,
even for frames0; OK/SHOT can therefore return true immediately. Otherwise
unsigned counter comparison determines timeout. Synthetic tick updates at
native sense entry cover0/1/3/FFFF; without ticks, a frames1 request remains
nonterminal. These updates are IRQ-counter models, not elapsed frame proof.

Change wait first waits for **all** interface input to be released, without
applying its frame limit. A negative argument still delays while a key is held,
then skips the press phase after release. The native frame-delay helper clears
the same counter and polls it; the fixture advances it at its actual read
instruction, checking real polling and far cleanup. Released frames1 polls
once more and performs one native delay; any nonzero interface input interrupts
the press phase. Both0 and9999 mean an unlimited press phase, with the native
counter local reset after each delay. Held-release and no-press cases remain
bounded nonterminal observations; no successful timeout is fabricated.

## Adjacent producer and acceptance boundary

Original sensor body ends with far RET at0528; original0529 is90 and PI begins
at052A. The cached remapped MAIN producer has the same417-byte body, omits the
untrusted frozen source's trailing `#pragma codestring "\x90"`, and places PI
at0529. This is a source-level candidate explanation for the one-byte layout
drift, not a cold reproduction of original compiler/OMF ownership. The NOP
remains unowned, and its cause is an open hypothesis. No codestring, padding or
target-byte injection is introduced into product source.

Twelve decoded boundary rows grant no authored MAINL source, accepted intake
path or exact credit. Remaining input data/BSS ownership, real devices/clocks,
whole libraries/CRT, localized cold builds, original producer records and
canonical DIET packaging/full Oracles remain open. The complete 505-file intake
and requested actual English commits are still unfinished.

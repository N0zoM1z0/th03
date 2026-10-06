# Complete MAINL shared sound candidate review

This historical sound-chain review is supplemented by
[the complete shared loader review](SHARED_SND_LOAD_REVIEW.md). The loader has
independent OP/MAINL bindings and complete physical-memory checks including
saved-stack aliases. The physical GAME2 object association is recorded
separately from target facts. Native driver/DOS ISRs and full sound ownership
remain open; previous caller fixtures are not upgraded by this supplement.

Eight complete candidate TUs contain nine functions: 535 decoded CODE bytes /
163 instructions, plus four observed trailing NOPs, totaling 539 bytes. All raw
bytes match both cached products; all eight contributions have no MZ relocation
sites in any image. The native 21-byte / eight-instruction frame-delay helper
also executes. No maintained MAINL source, canonical packed-file offset, cold
build, accepted intake path or exact acceptance is added.

```sh
python3 scripts/review_th03_mainl_sound.py --output .analysis/NEW_SOUND_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_sound_review.py -v
```

Receipt: `.analysis/sol-mainl-sound-review-20261006.json`. The prior input proof
and its canonical/decoded/cached lineage are guarded. Thirty-two consulted
frozen providers bind to both cached source trees. Only sound-effect play/update,
KAJA interrupt and the contextual frame-delay carrier forward to maintained
MAIN implementations; six maintained sources/headers match cached copies.
Mode, PMD residency and reset still use frozen TH02 C/C++ producers in MAINL;
the separate handwritten MAIN assembly owners are not their producers. Frozen
assembly-provider line endings are compared with explicit LF/CRLF conversion.
No MAIN or other-game exactness is inherited. Ghidra fails headless-usage before
DB attestation; no new database observations are used.

| Function | Decoded 0C7E | Bytes / instructions | Far cleanup |
| --- | --- | ---: | ---: |
| Determine mode | 002C | 29 / 12 | 0 |
| PMD resident | 004A | 57 / 17 | 0 |
| Wait for volume | 0084 | 27 / 13 | 0 |
| Load song/effects | 00A0 | 112 / 45 | 0 |
| Reset effect | 065E | 11 / 3 | 0 |
| Play effect | 066A | 60 / 21 | 2 |
| Update effect | 06A6 | 60 / 19 | 0 |
| KAJA interrupt | 06E2 | 30 / 12 | 2 |
| Wait for measure | 0C1C | 49 / 21 | 4 |

Trailing NOPs at0049/0083/009F/0669 are diagnostic producer bytes, not inserted
product padding. Complete source producer/cold OMF ownership remains open.
All branches remain within complete instruction boundaries. The only call is
an optimized PUSH CS / near CALL to the real far frame-delay helper. The C
volume/load functions retain their caller argument words; Pascal play/KAJA and
measure clean two/four bytes respectively. BP/SI/DI/DS and incoming DF survive
under the stated models. There is no x87 instruction in these bodies.

## Native execution and interface limits

All nine sound bodies, frame polling, internal call and real far returns execute.
Interrupts60/61 return injected registers; DOS21 records requests and returns
fixture status. The PMD vector/signature and frame IRQ counter are synthetic
memory fixtures. No actual PMD/MMD, interrupt frames, filesystem/payload writes,
physical elapsed timing, driver-buffer capacity or playback is proved.

A separate scalar specification checks all65536 DGROUP bytes, using each image's
own initial bytes. Both 33-byte priority/duration tables match the parsed frozen
assembly declarations at0896/08B7. These are diagnostic DATA observations, not
localized product ownership. Source filename fixtures cross a segment offset
boundary. Whole DGROUP catches filename writes beyond the thirteen-byte buffer;
budgets retain partial states without fabricating completed returns. Before/after
hashes stay separate; normalized cross-image records omit those initial/final
hashes because unrelated DGROUP0849 still differs.

Per image:1527 individual invocations (1511 returns /16 budgets), plus33 continuous
reset/play/update chains totaling798 native invocations. Total2325 native calls /
2309 returns /16 budgets per image;6975 calls /6927 returns /48 budgets across
original/two caches. The1511 terminal cases include every33x33 valid effect
priority pair, boundary/negative/truncated effect indices, byte-frame wrap,
PMD signatures/offset wrap, mode flags, driver routes, DOS statuses and wait
limits. All33 effect lifetimes execute continuously through one post-clear update.
Eight adversarial tests reject incomplete/wrong returns, operand/neighbor
branches, unknown interrupts/ports/edges, unframed near calls, changed producer
bytes, physical aliases, foreign-memory writes and stale terminal state.
Callback errors are raised outside the native FFI boundary.

## Driver flags and waiting

Mode always requests INT60 AH9. Any returned AL exceptFF selects FM, sets
FM-possible to1 and active to1. ALFF selects the complete MIDI-active byte as
active/AX, without clearing an already nonzero FM-possible flag. PMD residency
resets MIDI-active/FM-possible/MIDI-possible and sets the interrupt byte to60;
it leaves active untouched. It follows vector60 and checks only the three
bytes atISR+2..4 for `PMD`. The first two bytes do not affect the result. No
vector/driver validity beyond these observations is implied.

KAJA does nothing when active is zero and returns the incoming AX in the model.
Otherwise it forwards the caller's full AX and propagates driver AX. KAJA,
volume and measure choose INT61 only for MIDI-active exactly1; byteFF uses60.
Volume does not test active and waits for exact equality of returned AL with
its byte argument; the caller word's high byte is ignored. A driver skipping
that volume remains nonterminal under budget. Measure compares returned AX
with an unsigned word threshold, including8000/FFFF; it preserves the returned
measure, unlike the separately reviewed input wait that overwrites AX with P1.
MIDI measure sets DX=C0. With active zero it executes the real frame-delay helper,
ignores the measure and uses the unsigned frame argument. Frames0 still poll
once after clearing the clock. Synthetic tickFFFF satisfies0/1/3/FFFF; a stalled
frames1 remains nonterminal. No wall-clock or real interrupt-frame proof follows.

## DOS load requests and filename bounds

Load always copies exactly13 bytes, including bytes after the first NUL, from a
far source. Each byte recomputes the offset with word wrap; source-offset carry
does not advance its segment. For function0600 and any nonzero MIDI-active byte,
it scans the destination from index1, then appends `md` and NUL. A leading NUL
is ignored by the scan but still makes DOS open see an empty filename. A
12-character name writes beyond the13-byte buffer; an unterminated13-byte name
scans neighboring DGROUP until a later NUL. An all-nonzero DGROUP fixture stays
in that scan under budget, without reaching DOS or driver interrupts. No
universal infinite-loop conclusion follows from a bounded observation.

INT21 AX3D00 requests the resulting name. Its returned AX becomes BX regardless
of carry/error. The caller function0600 with nonzero MIDI uses INT61; all other
functions use60. The modeled driver supplies DS:DX and may clobber BX, which
becomes the read/close handle without restoration. Native DOS read always
requests AX3F00/CX5000; it does not query driver capacity or check read status.
The original DS is restored before close, whose AX has AH3E and retains the
read-result low byte. No sound-active check or stop-playback request occurs.
Zero/success/error handles, both CF states, short/full/error read results and
changed driver BX are retained. Buffer overflow in a real driver cannot be
proved without that driver's capacity and actual DOS memory writes.

## Effect state and unchecked indices

Play is gated by FM-possible, independently of BGM-active/MIDI-active. If no
effect is selected (FF), it stores the new low byte and retains the old frame.
Otherwise it compares the old effect's unsigned-byte priority against the new
**full word** index, with word offset wrap and no33-entry bounds check. Equal
priority replaces and resets frame; lower priority is ignored. The selected
index then truncates to a byte. NegativeFFFF and256 therefore read unrelated
DATA before storingFF/00. These are fixture-specific observed addresses and
state, not valid effect definitions.

Update is also FM-gated. A selected effect at frame0 requests INT60 AH0C/AL=id,
regardless of MIDI or active. It increments the byte frame and clears only when
frame exceeds the table threshold; equality retains the effect. Frame255 wraps
to0, retaining it, with playback postponed until the following update. Threshold0
requests playback then clears on that first update. Reset explicitly writes
frame0 and selectedFF. Continuous chains check these state transitions and
single driver requests for all33 declared table entries. No audible duration
or other-driver side effects are modeled.

Nine decoded function rows grant no source or exact credit. Cold localized
producer/layout, full DATA/BSS/CRT and device/library ownership, canonical DIET
packaging and complete Oracles remain open. The complete505-file intake and
requested actual English commits remain unfinished.

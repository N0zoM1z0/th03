# MAINL bounded snow and frame-control review

Seven complete generated-root bodies (464 bytes) have source/control-flow/ABI
candidate review. Selected operations execute with the actual 76-byte flake
blitter, 42-byte IRand and 69-byte vector2. Independent scalar checks cover
LCG arithmetic, sine/cosine values, movement and flat blue-plane writes. The
root still fails raw equality by three encoding bytes and original relocation
order by six reversed sites. No maintained source or exact owner is accepted.
This bounded cluster does not close the full staff animation or generated root.

```sh
python3 scripts/review_th03_mainl_snow.py --output .analysis/NEW_SNOW_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_snow_review.py -v
```

Receipt: `.analysis/sol-mainl-snow-review-20261006.json`. The complete cutscene
receipt is SHA-256 pinned, binding canonical Japanese MAINL to guarded decoded
MZ and two cached products/MAPs. Inputs are checked before/after execution.
Current selected Ghidra headless-usage fails before DB attestation; no database
observation is used. Sixteen consulted frozen providers match both cached
trees, with assembly LF-to-CRLF only and all other inputs byte-identical.
Frozen Tupfile is consulted for the resource/link rule only: cached orchestration
was patched by the earlier cold scaffold and is not claimed byte-identical.
The entire product graph and conditional/include closure remain open.

## Boundaries, data and retained failures

| Decoded segment:offset | Bytes | Complete body | Return |
| --- | ---: | --- | --- |
| 095F:2561 | 21 | Clear blue plane | near, no arguments |
| 095F:2576 | 26 | Reset eighty alive flags | near, no arguments |
| 095F:2590 | 169 | Spawn flakes | near, no arguments |
| 095F:2639 | 70 | Update flakes | near, no arguments |
| 095F:267F | 54 | Render flakes | near, no arguments |
| 095F:26B5 | 48 | Frame/music-measure gate | near RET 4 |
| 095F:26E5 | 76 | Snow update/render/wait/page frame | near, no arguments |
| 095F:249A | 76 | Prior reviewed C++ flake blitter | near RET 6 |
| 0000:1A3E | 42 | Actual master.lib IRand | far RET 0 |
| 0C7E:0110 | 69 | Actual C++ vector2 | far RET 12 |

Full decoding accounts for 189 instructions in the seven-body contiguous
root range 2561..2730 and 259 across all ten bodies. Direct branches stay on
owned instruction boundaries; calls enter declared complete bodies. Both MAPs
place the root cluster inside the generated `MAINL_03_TEXT` contribution
095F:24E6/3339. That containing module remains unaccepted. No padding/table
or intervening bytes are manufactured. The prior blitter is a dependency,
without duplicate unit/byte credit; the new unit covers only the 464-byte root.

Raw clear-blue differences at 256A/256C/256D retain target `31 C0 89 C7`
versus cached `33 C0 8B F8`: equivalent XOR AX,AX and MOV DI,AX encodings.
Natural assembler encoding/producer closure remains open. The other 443 root
bytes and all 187 selected dependency bytes match both cached products. The
six original spawn segment-relocation sites occur in descending order at
2624/2606/25F5/25E4/25D6/25BC, versus ascending cached order. All other selected
bodies have no segment-relocation sites. Semantic agreement cannot close
either original encoding or relocation-order gate; no normalization is used.

The complete C++ vector contribution is 160 bytes; only its first 69-byte
function is reviewed here. Valid cached TC86 Borland C++ 4.02 vector objects
agree after dependency timestamp normalization. Its following observed NOP
at 0155 corresponds to an upstream codestring; no authored producer acceptance
or review of the remaining vector function follows. MAIN's accepted vector
source/exact claims do not transfer to MAINL.

The candidate/source flake layout is sixteen bytes: alive byte at +0, padding
at +1, signed 16-bit Q12.4 left/top at +2/+4, velocity x/y at +6/+8, cel word
at +10 and four padding bytes. Eighty records occupy 1280 bytes at DS:22C2.
The loop capacity byte at 22C0 is separate; frame word at 27C2 immediately
follows the array, with page/flags at 27C4..27C6. The reset loop clears only
eighty alive bytes. Padding, coordinates, velocity, cel and adjacent fields
are preserved. No fresh layout compiler Oracle or BSS ownership is claimed.

## Resource and numerical checks

The frozen 190-byte BMP has a 40-byte DIB, width 16, height 32, one bit per
pixel, uncompressed bottom-up four-byte rows and black/white palette. The
Tupfile declares four 16x8 sprites. Independent native extraction reverses
the bitmap rows and removes row padding, producing 64 bytes that equal both
cached generated `flake.asp` data and decoded target data at DS:0A62.
Only bitmap metadata, hashes and replay logic are public; no asset or target
byte array is imported. Converter output is cached evidence, not a fresh
pipeline build or whole-resource producer Oracle.

The complete 320-word sine data spans DS:05BA..0839, with cosine starting
64 entries later at 063A. Frozen literals, target/candidate data and an
independent rounded `sin(angle*pi/128)*256` specification agree. The overlapping
sine/cosine allocation is one 640-byte table, without double credit. The one
unowned initialized-DGROUP difference at 0849 is target 90 versus cached 00;
it is retained as a neighboring-data failure and not silently rewritten.

Full per-image DGROUP comparisons check all expected writes and preservation
against that image's original state. Cross-image constructed-state hashes
cover only declared seed, sound-active, vsync and capacity/particle test fields;
their explicit scopes are in the receipt. They do not claim whole-DGROUP
equality or erase the 0849 difference. The constructed 255-record memory window
is deliberately larger than the declared array to observe unchecked indexing,
not evidence of a real allocation or valid caller range.

Actual IRand implements seed=`seed*015A4E35+1` modulo 2^32, returning bits
16..30. Five seeds with twenty successive actual calls each agree with the
independent integer LCG. Four random values are consumed per new flake: initial
position, angle, length and cel; vector2 supplies the
fifth executed far-return transition. Angle is 80..111, length 48..111 and
cel is random AND 3. Every fourth index starts at left=10112 with randomized
top modulo 6272; other indexes start at top zero with left modulo 10112.
Creation requires the signed frame to be at least index*8 and skips live slots.

Ninety-eight direct vector cases per image cover fourteen angles and seven
signed lengths, including negative and extreme words. Actual MOVSX/IMUL/SAR
preserves negative floor rounding, word result stores and low-byte angle ABI.
The unused argument high byte is deliberately 77. Spawn passes a word from
BP-1, whose upper byte is neighboring stack storage; only its low angle byte
is consumed. These checks do not upgrade the upstream opaque emitted opcode
prefix or codestring to natural maintained source.

## Movement, capacity and frame behavior

Thirty-five spawn cases per image cover capacities 0/1/4/50/80/81/255 and
signed frames -1/0/7/8/2040. At constructed capacity 255/frame 2040, 174 newly
spawned indexes 81..254 write beyond the eighty-record array. Index 80 aliases
the nonzero low frame byte and is skipped as already live. Counts are not
clamped to FLAKE_COUNT. Caller constraints remain unproved; no ordinary gameplay
reachability is inferred from these deliberately invalid controls.

Twenty-eight update cases check all seven capacities and four coordinate/velocity
sets. Live values become exactly 1. After word-wrapped velocity addition, left
<=0 receives a single +10112 and top>=6272 receives a single -6272. There is
no modulo loop, right-bound check or negative-top correction. A constructed
left=-10113 remains -1; signed overflow can leave the result outside the
rectangle. Updated slots beyond eighty follow the capacity byte and can alter
neighboring globals. Five render cases use valid capacities and actual blitter
calls; every word write and resulting blue-plane byte agrees with independent
ROR/OR/stride arithmetic over the target sprite.

Two clear calls check inherited DF. With DF clear, exactly 16000 word stores
clear offsets 0..31998. With DF set, the same REP STOSW starts at zero and
walks backwards through wrapped 16-bit offsets; it does not execute CLD and
preserves DF. The flat initialized 64-KiB blue window records this behavior;
physical video memory/banking and startup DF guarantees remain separate.

Thirty gate cases cover sound active/inactive, signed frame edges and unsigned
music measures. Without sound, it requires frame>256; with sound, interrupt
60/AH=5 supplies a modeled measure and the gate requires unsigned measure>=4
and signed frame>192. The interrupt is a music interface, not the unrelated
packet-driver annotation in the generated disassembly. No real driver executes.

Six terminal full snow frames run actual spawn/update/render before adaptation.
With adaptation enabled and initial vsync>1, capacity becomes 50 and both
observed flags become zero, **after** all eighty flakes have rendered for that
frame (640 word writes). Hidden slots are not cleared. The loop then waits for
nonzero vsync, clears the counter, shows the current page and accesses
byte `1-page`. Pages 2/255 give requests 2/255 and 255/2 without validation.
A modeled tick injected on the fifth wait poll permits exit; a late tick of
2 does not retroactively trigger adaptation. A zero-vsync budget case stays
in the wait, with no page port writes, rather than reporting a successful exit.

Load segment 2000, CS=295F, DS=2E3F and SS=4000 are constructed. Root/helper
instructions and **far RET instructions execute**, including cleanup 0/12.
Only memory-write hooks are installed; the previously reproduced read-hook
far-return defect is avoided by not adding a read hook. Synthetic controls
check actual return CS/IP and stack frames with the write hook. Clock updates,
music interrupt results and page-bank effects remain models; no graphics
device output, timing, interrupt scheduling or physical ABI is proved.

Per image: reset1 + spawn35 + update28 + render5 + clear2 + gate30 + frame6 +
zero-vsync budget1 + random100 + vector98 = 306 top-level calls. Across target
and both candidates: 918 calls, 915 terminal and three budget observations.
Seven synthetic tests reject malformed boundaries/edges, table/bitmap layout,
callback errors, stale terminal/cleanup and incorrect actual far cleanup.
Remaining staff drawing/transitions/animation root, all generated DATA/BSS,
device runtime, localized cold build, complete ownership/relocations and stored
packaging Oracles remain open alongside the broader 505-file intake.

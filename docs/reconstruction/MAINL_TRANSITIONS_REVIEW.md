# Remaining MAINL staff candidate bodies

Ten remaining complete bodies cover 2875 decoded CODE bytes. Combined with
the separate seven-body snow cluster (464 bytes), they account for all 3339
bytes of the generated MAINL_03_TEXT contribution, without gaps or duplicate
authored-byte credit. Source/control-flow/ABI review covers both handwritten
CDG includes and the generated entrance, exit, transition, verdict and staff
root procedures. This is complete candidate analysis of this contribution,
without maintained source, physical runtime or exact acceptance.

```sh
python3 scripts/review_th03_mainl_transitions.py --output .analysis/NEW_TRANSITIONS_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_transitions_review.py -v
```

Receipt: `.analysis/sol-mainl-transitions-review-20261006.json`. The replay
pins the prior snow receipt, inherited decoded/canonical lineage,
both cached images/MAPs and its script. Thirteen consulted frozen providers
bind to both cached source trees, with assembly LF-to-CRLF only and all other
files byte-identical. Relevant source includes, CDG metadata/pattern, resident
fields, score/character and sound declarations were read. Selected Ghidra
headless-usage fails before database attestation, so no DB observations are
used. Cached observations do not establish a fresh compiler or full root
DATA/BSS/resource ownership.

## Complete new boundaries

| Decoded 095F entry | Bytes | Body | Near cleanup |
| --- | ---: | --- | ---: |
| 24E6 | 123 | CDG upward-motion E-plane restoration | 6 |
| 2731 | 211 | CDG E-plane dissolve | 8 |
| 2804 | 211 | Entrance frame | 2 |
| 28D7 | 183 | Exit frame | 2 |
| 298E | 52 | Final gallery dissolve frame | 6 |
| 29C2 | 229 | Single-image transition | 6 |
| 2AA7 | 358 | Paired-image transition | 6 |
| 2C0D | 139 | Entrance/hold transition | 6 |
| 2C98 | 389 | Verdict rendering requests | 0 |
| 2E1D | 980 | Complete staff orchestration root | 0 |

Full decoding checks direct branches against local instruction boundaries,
near calls against the new entries or declared snow interfaces, and far calls
against typed imports. Complete body/return checks use actual decoded bytes;
automatic functions and disassembler comments are not independent Oracles.
The prior 464-byte cluster remains separate. The generated carrier and whole
staff/source product graph are not accepted owners.

The two handwritten includes retain seventeen raw bytes of failure: fifteen
in unput at 2545/2546/2547/2548/2549/254B/254C/254F/2550/2551/2552/2555/2556/
2557/2558, and two in dissolve at 27DA/27DB. They are equivalent register
instruction encodings, without a natural encoding-producer closure. All other
new bodies have cached raw identity. The complete carrier still also contains
the prior three clear-blue failures. Original ordered segment relocations are
reported per new body; neither reordered lists nor semantic agreement count
as equality. Dissolve/exit/single/paired/verdict have 2/3/6/9/9 reversed
original sites. The staff root has 34 sites with a different interleaving,
not merely a single reversal. Target/candidate entry labels are candidate source associations,
not canonical stored-file offsets.

The unput declaration in `th03/formats/cdg.h` lacks the explicit near/Pascal
qualifiers present in the implementation's near RET 6 contract. Its actual
callers here are assembler instructions that establish the observed ABI.
Do not infer a compatible C++ large-model call from that header or import
it into product code without a separate compiler/layout check. The generated
root's declaration/data ownership remains open.

## Native CDG operations and retained hazards

All native unput/dissolve instructions execute. Foreign CDG blits record
requests without producing pixels; initialized flat E-plane memory provides
the operand values for actual stores/AND operations. Thus checks prove helper
arithmetic, mask operations, addresses and request ordering under constructed
metadata, not loaded CDG pixels, real page banks or physical GRCG behavior.
Clock, snow, frame/music gate, font, load/free, palette, sound and other
external interfaces are explicit models in the orchestration probe.

Sixteen unput calls per image cover widths 0/16/32/33, heights 8/9 and DF
clear/set. Center offsets use signed division by two with truncation toward
zero, followed by arithmetic left-to-byte conversion. Width uses unsigned
SHR 4; each of three rows clears width>>4 words. Odd widths discard the partial
word. No clipping or segment normalization occurs. DF remains inherited;
the subsequent stride arithmetic still assumes forward stores, so DF-set
rows follow different offsets. The independently computed flat window and
every word store are checked, including unchanged bytes.

Forty dissolve calls per image cover strengths 0..8/FFFF and both alpha/slow
flags. Strength is masked to three bits. Zero skips mask application after
the CDG blit; nonzero strength uses four target-pattern words indexed by
destination Y modulo four. Alpha CDG is selected only when both observed
flags are nonzero; otherwise the no-alpha library request is used. Actual
plane words are ANDed with the complement of the pattern. The complete
64-byte frozen pattern agrees with decoded/cached data, without importing an
asset or target array into maintained source.

The header's **strength 7 = full** comment is false for the observed pattern:
three row phases clear all sixteen bits, while phase 1 leaves mask 8888.
Over a complete four-row tile this retains 4 of 64 bits. Strength 8 becomes
zero and skips masking. This result is actual E-plane arithmetic over
constructed FFFF words; the foreign CDG renderer is still a model.

A constructed zero-width/zero-height dissolve enters the word loop with
CX=0, so LOOP wraps to FFFF and continues. Its bounded CPU call stops without
a terminal return. No zero-size guard or successful draw is fabricated.
An entrance duration of 7 divides by its truncated duration/8, causing an
observed divide-error interrupt instead of a normal return. These deliberately
invalid metadata/parameter cases do not prove normal gameplay reachability.

## Frame and transition contracts

Thirty frame calls per image check entrance, exit and gallery at signed
frames -1/0/63/64/65/66/159/160/161/162. Incoming dissolve arguments are
captured at the actual near entry; expected strengths are checked against
those words, rather than only against a render count. Entrance draws while
frame<=duration, moves each page's center toward the configured bound and
uses max(0,7-frame/(duration/8)). Exit moves upward by one while frame<160,
uses min(7,frame/20), clears the interior at 160/161 and stops after 161.
Gallery draws while frame<=160 with max(0,7-frame/20). No universal frame
normalization or clipping is added.

Twelve complete single/paired/hold transitions per image cover speed 1/2 and
sound inactive/active. Declared gate models exit at frame 257 without sound
or 193 with modeled measure FFFF. Single/paired transitions have two phases
and two cleanup snow frames; hold has two phases without those cleanup calls.
With constructed duration 65, initial centers 280 (speed 1) or 264/263 (speed
2) become 247/200 during entrance, then 167/120 after the exit's eighty upward
updates per page. Hold copies the active page center into secondary storage.
The paired path maintains the second image and its alpha flag independently.
These are actual transition instructions with declared clock/snow/gate models;
actual snow and gate behavior remains in the separate prior review.

Twenty-five direct verdict calls per image cover five score vectors and skill
0/9/10/99/100. Actual font request pointers, color, positions and ordering
agree with an independent decimal formatting specification. Leading score
zeros are skipped, but the continue byte is appended as another score digit
and also printed on its own line. An all-zero score therefore renders the
continue digit without an extra score zero. Skill centers one/two/three digits
and then appends its unit string. Font traversal/pixel output and generated
string/table ownership are not accepted by these request checks.

## Full staff orchestration scope

Five complete root calls per image cover the skill branches, highest score
digit, remaining credits and sound modes. Resident score bytes 18..1F copy
to local digits 1..8; local digit 0 is byte `3-credits`. Character packing
and rank select verdict pointers. Skill is read from resident+38, following
the separate animation-fast byte at +37. Score digit 7 equal to 3 executes
both the +2 and +7 branches; 4 only executes +7; >=5 adds 15. Intermediate
byte additions wrap before the unsigned clamp to 100. With base skill 250,
digit6=9/digit7=3/digit8=0, the resulting skill is 11. A nonzero digit8 forces
100. No arithmetic is repaired to match an upstream intention.

The root requests the twelve frozen `stf*.cdg` filenames in their actual
slot order, initializes resident RNG seed, runs nine transitions and the
gallery, and renders verdict requests to both pages. CDG load models supply
32x4 metadata even when their constructed return is zero: this isolates
ignored returns and does not assert that a failed real loader supplies valid
metadata. No CDG asset is read or imported. The source root performs no return
checks at those interfaces.

The explicit clock/gate models produce 4332 snow-frame requests with sound,
5612 without sound. Held nonzero input reaches the strict >256 verdict wait
threshold after 257 calls; the subsequent fade uses 199 frames, totaling
456 input calls. Fade emits tone 100 once, then 99..1 twice each, decrementing
on odd frame counts. The root frees all 32 slots, then returns. A separate
no-input budget observation remains in the verdict wait, with no free calls.
Actual driver time, interrupt schedules, snow/GRCG/page pixels and asset I/O
are not proved by this orchestration model.

Across target and two cached products, replay compares native operation,
frame, transition, verdict and root observations. The complete root candidate
still requires localized source, a fresh cold build, original encodings and
ordered relocations, generated data/BSS/resources, actual devices/whole
dependencies and canonical DIET packaging/complete Oracles. The remaining
MAINL root segments and broader ReC98 intake stay open.

Per image: 16 unput + 40 dissolve + 1 zero-width budget + 30 frame + 1 divide
trap + 12 transition + 25 verdict + 5 staff root + 1 no-input budget = 131
top-level calls. Across three images: 393, comprising 384 terminal calls,
six budget observations and three divide traps. Seven synthetic controls
protect ownership/cleanup, callback errors, stale terminal handling, explicit
divide-fault classification and interface segment aliases. The new bodies
contain 949 instructions; together with prior snow, all 1138 instructions
in the complete carrier are accounted for as diagnostics.

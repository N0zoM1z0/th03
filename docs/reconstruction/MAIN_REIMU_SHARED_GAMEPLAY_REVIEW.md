# MAIN Reimu gameplay and shared bomb lifecycle

## Scope and current result

This candidate reconstructs 14 complete routines in the original Japanese
MAIN load interval 0x14A76..0x153BB: 2,373 bytes and 23 original ordered MZ
relocation sites. The largest bodies are the 435-byte gauge pattern,
272-byte charge update, 209-byte bomb update and 474-byte bomb renderer.
The gauge's early RET 2 at 0x14EB0 is internal to its complete function.

Status: source-present, with zero exactness credit. A retained-context native
link reproduces all 2,373 owned bytes and all 23 literal ordered target MZ
relocations. Strict outside-interval relocation-order preservation FAILS.
The unchanged outside payload and equal relocation tuple multiset do not
satisfy that ordered gate. No full cold build or exact acceptance is claimed.

The three maintained source files and candidate manifest are installed as a
source-present checkpoint. This review, comment-only source-header updates
and the accompanying ledger additions are proposed for installation. Native compilation produced charge/gauge
(cs_reimu, 1,448 bytes) and shared/Reimu bomb (bm_reish, 925 bytes), with all
14 function lengths and returns matching and zero allocated DATA/BSS.
Original source text, historical object identity and whole-game completion
are not claimed.

## Semantics, storage and ABI

The charge state contains 24 slots, 12 per player. Each slot is 32 bytes:
state/frame bytes at offsets 0/1, seven signed 16-bit Q12.4 X coordinates at
2, seven Y coordinates at 16, and angle/speed bytes at 30/31. The typed
PlayfieldSubpixel fields retain explicit .v access for raw operations; the
clipping helper receives typed values directly, without rescaling.

Charge reset/add, Hyper insertion, trail update, collision and rendering are
complete. Collision deliberately scans six slots although update/render
traverse twelve. The gauge produces spread/ring bullet patterns and restores
the opponent's palette on completion. Reimu's bomb uses 32 eight-byte
particles per player: active at 0, an uninterpreted byte at 1, signed X/Y at
2/4 and signed vertical velocity at 6. That unused byte is preserved.

Storage remains external at its historical DGROUP locations: shared gauge
records 0x2D58, Reimu gauge frames 0x2D68, charge slots 0x2D6A, charge pointer
0x306A, alternating-hit flag 0x306C, bomb particles 0x3080 and particle
pointer 0x3280. Proposed aliases label existing reserves; they allocate
nothing. Shared scratch reuse and original physical DATA/BSS ownership must
not be confused with the semantic names. A separate retained-link MAP review found all 33 nonempty DATA/BSS rows
unchanged in order, all 506 existing DGROUP publics preserved and these
aliases at the stated offsets. Cold-build verification remains open. The compiler truncates the hit-flag import to
_reimu_chargeshot_alternate_hit_f; integration must use its observed spelling.

Charge/Hyper addition is far Pascal with two word arguments and RETF 4.
The charge sprite helper is near Pascal with three words and RET 6; the
gauge helper is near Pascal with a byte argument in a word stack slot and
RET 2. Hit testing returns in AL. Other callbacks are far; the particle
renderer remains near to its caller. Existing helper declarations, packing
and legitimate same-frame bullet-call relationship are retained.

The 110-byte shared lifecycle serves both players of Marisa, Kotohime,
Kana, Rikako, Chiyuri and Yumemi. All twelve callback assignments must remain.
Reimu uses its own particle updater. Placing these routines in one physical
producer does not make that lifecycle Reimu-exclusive.

## Why two natural producers

The target's ten charge relocation sites form two descending groups of five.
The remaining thirteen sites descend across the entire shared-lifecycle and
Reimu-bomb region. Separate lifecycle/bomb objects predict the wrong group
order. A single natural 925-byte bomb translation unit preserves all four
function bodies and their order, with the union of their existing includes
and the same packing envelope.

Observed native output supports this proposal: charge LEDATA lengths are
1,024 and 424, followed by their native FIXUPP records; the combined bomb
has one 925-byte LEDATA and one FIXUPP. The retained native link now reproduces all 23 literal ordered target sites.
Its four same-frame bullets_add calls naturally lower to NOP/PUSH CS/CALL
and resolve to load address 0x17730. No records were sorted, reversed,
resized or rewritten. This result supports the two-producer proposal without
establishing historical translation-unit identity.

## Source refinements and retained counterexamples

- v01 failed compilation because raw integer coordinates could not be passed
  to the existing typed clipping API.
- v02 compiled, but temporary typed copies added ten bytes to charge update.
  Other differences exposed source-block boundaries, scalar allocation and
  compound byte arithmetic; compiling was not equivalent to matching.
- v03 used genuine typed coordinate fields, explicit raw accesses, equivalent
  early-continue guards, separate phase assignments and explicit gauge flag
  addition. Thirteen lengths matched; charge-add remained three bytes short.
- Moving the two genuinely used charge-add counters to function scope fixed
  that allocation hypothesis in the later probe, without forced registers.
  v05 still emitted 33 D2 for the renderer's DX-zero operation; self-XOR
  intrinsics did not fix the encoding and were discarded from the baseline.
- v06 combined the unchanged shared/bomb bodies. v07 uses one symbolic
  instruction at the actual sprite hardware interface, described below.

Earlier sources, failed compiler output and successful-but-mismatching object
evidence remain separate. No target-byte arrays, padding calibration, fake
storage, broad immediate masking or OMF patching were used.

## The symbolic DX-zero boundary

SPRITE16 monochrome service 3 consumes DX=enable. The target at 0x14E18
executes XOR DX,DX; MOV AH,3; INT 42h to disable monochrome before drawing the
full-color head sprite. The candidate expresses this real boundary with
asm xor dx, dx; followed by the existing service selector and interrupt.
The subsequent sprite-helper phase-zero argument is distinct and unchanged.

The maintained Kana renderer in src/main/player/chargeshot_kana.cpp already
uses this symbolic DX-zero idiom before the SPRITE16 interrupt. Kana selects
the different overlap service; Reimu's monochrome selector is independently
supported by the target and pinned sprite16.h. This precedent does not claim
original source spelling. In the actual v07 object, the renderer's offset
149 contains literal 31 D2, matching the target encoding.

## Evidence and remaining gates

The pinned target SHA256 is
f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b.
Reference semantics come from ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47;
reference source is corroboration, not independent exactness evidence.
The accompanying REIMU_SHARED_EVIDENCE.json pins the three proposed source
files, native compile receipt, objects, raw diagnostic reports and candidate
manifest. Large compiler and binary artifacts stay in their retained trees. Checkpoint
source headers only update status comments and the review-document path;
all non-comment lines are identical to the compiled inputs. Both input hashes
are retained. These final comment-only files have not been cold-built.

The installed config/th03_main_reimu_shared_candidate.toml preserves the
existing Marisa unit and adds this logical owner with two physical producers.
The original carrier pin and retained post-Marisa carrier pin are distinct.
The actual target header is 0x1860 bytes, making load 0x14A76 correspond to
target file offset 0x162D6 (90,838), not the candidate executable's offset.
The MAP start is HITBOX_TEXT:10A6 in MAIN_04. Semantic partitions are
charge/gauge [0x14A76,0x1501E), shared lifecycle [0x1501E,0x1508C), and
Reimu bomb [0x1508C,0x153BB).

## Preservation failure and remaining gates

The retained-link audit preserves all 74 previously accepted extents (53,122
bytes) and the 1,958-byte Marisa candidate, including their literal ordered
relocations. Outside the new interval, payload bytes are unchanged from the
retained baseline. The outside relocation tuple multiset is also unchanged,
but its literal order is different, so strict preservation is false.

Two changes explain the failure. Startup sites change from baseline order
0x9F39,0x9F3E to 0x9F3E,0x9F39 when a local binding becomes external. This
matches the target's startup order but still changes the baseline. Native
carrier record framing also moves Mima site 0x1564A before five sites. The
candidate sequence is 1564A,15452,154BE,15536,15606,15631; the target sequence
is 1564A,15631,15606,15536,154BE,15452. Mima order is not target-exact.
Outside the interval, 21 payload bytes still differ from the original target.

A normal candidate replay can be requested with the command below. It has
not been run for this installed checkpoint, and is not a reproduction claim:

```sh
python3 scripts/replay_th03_main_exact_units.py --candidate-manifest config/th03_main_reimu_shared_candidate.toml --run-id reimu-shared-cold-review-v01
```

Two fresh full cold candidate builds, strict outside-order resolution and
separate full-product preservation checks remain required. Runtime behavior
and historical storage ownership remain separate obligations. Factory formal
TH03 replay is still unconfigured. This checkpoint does not promote any
accepted ledger or platform exactness state.

# MAIN resident configuration, extra attacks and hit-circle review

Three complete maintained owners replace the frozen cfg-lres, p-exatt and
hitcirc wrappers and their implementations. Their raw boundary report is
replayable independently of Ghidra's automatic types:

```sh
python3 scripts/review_th03_main_code.py \
  --owner th03-main-cfg-resident --owner th03-main-extra-attack \
  --owner th03-main-hitcircles \
  --output .analysis/th03-main-exact/sol-cfg-exatt-hitcircle-target-review/raw-review.json
```

The Japanese target SHA-256 is
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
Read-only Ghidra function/caller/callee queries re-attested the complete MAIN
MZ in the same process. Source/MAP names are candidate semantic labels;
raw offsets, operations, returns and relocations are target observations.
No runtime or external-driver behavior is independently attested here.

| Maintained owner | CODE contribution | Offset | Bytes | Functions |
| --- | --- | --- | ---: | ---: |
| `src/main/formats/cfg_lres.cpp` | MAIN_01 / CFG_LRES_TEXT | 096E:0C66 | 49 | 1 |
| `src/main/player/exatt.cpp` | MAIN_06 / P_EXATT_TEXT | 18FE:119E | 41 | 1 |
| `src/main/collision/hitcircle.cpp` | MAIN_01 / HITCIRC_TEXT | 096E:205A | 445 | 4 |

The full 535 bytes are function bodies, with no switch tables or alignment
ranges. All CODE contributions, including the separate MAIN_06 contribution,
are included in the manifest. There are no shared tails or unowned holes.

## Resident configuration target facts

`cfg_load_resident_ptr` is near cdecl, has no arguments and ends in RET.
Its natural local frame is eight bytes. It supplies a DS:0634 filename pointer
to the far open routine, an SS-local buffer and byte count 8 to the far read
routine, then invokes the far close routine. All three calls are unconditional.
The resident segment word is loaded at configuration byte offset 5. The target
stores that word to resident pointer segment DGROUP:1D92, stores zero to its
offset at 1D90, and returns the segment-only pointer in AX. `__seg*` remains a
16-bit segment pointer; it has not been replaced with an ordinary far pointer.

The scoped CFG record observations are size 8 and resident offset 5. They do
not grant separate acceptance to the whole cfg header, file contents or resident
storage. The frozen inline implementation remains an explicit compatibility
input. Its GAME>=4/5 branches are separate intake questions. The owner has one
direct caller and three direct callees. Ordered relocation sites are 29, 24, 12.

## Extra-attack target facts

`exatt_add` is far Pascal and ends in RETF 6. Two subpixel objects occupy word
slots at BP+0A and BP+08, and the byte player ID occupies the word slot at BP+06.
Zero selects the far callback at DGROUP:290C and passes ID 0. Every nonzero ID
selects the far callback at 2918 and passes ID 1. These are indirect far calls,
so the observed empty immediate-relocation vector and Ghidra's zero direct
callees do not mean that the routine makes no calls. The 12-byte callback-table
stride agrees with three four-byte function pointers per player in the candidate
declaration. Callback implementations/table storage are outside this owner.
Two direct callers are observed.

## Hit-circle target facts

The four contiguous bodies are enemy add at 205A (121 bytes, far Pascal,
RETF 6), player add at 20D3 (50 bytes, far Pascal, RETF 6), update at 2105
(38 bytes, near cdecl, RET), and render at 212B (236 bytes, near cdecl, RET).
The add functions take signed subpixel words and a word player ID; the stored
ID is its low byte. No argument width was altered to force a match.

Enemy add increments the external ring index before use and resets it when
it reaches 12. Records have a six-byte stride: age, player byte, X word and
Y word. It sets age to 1. Unless the external suppression byte is nonzero,
it calls the far random-mod helper twice with twice the hitbox X/Y radii and
adds the corresponding top-left origins. The far-return coordinate helper
uses the target's compiler-generated NOP/PUSH CS/near CALL sequence. X then
subtracts 24 pixels; Y shifts arithmetically by four and subtracts 8 pixels.
Player add uses the one record at base+72 (record 12), without randomization.
These storage references do not grant initialized/BSS ownership.

Update scans all 13 records, increments nonzero age as an unsigned byte, and
clears it when the resulting value is above 16. The byte increment/wrap and
post-increment comparison are retained. Render first selects monochrome mode
through INT 42 with AH=3/DX=1. Enemy color uses AH=4 and DX=11+(frame&1).
Sprite size is byte width 3 / half-height word 24. A zero player byte selects
clip 0–319; any nonzero player byte selects 320–639. The cell expression is
`1910 + ((age-1)/4)*6`, preserving the target's register/multiply sequence.
It draws the twelve enemy records, switches color to white (15), and handles
the one player record before disabling monochrome mode.

The stock C++ expansion of the final disable operation used `33 D2` for
XOR DX,DX at 220D, while the target uses `31 D2`. The maintained source spells
this operation as symbolic `xor dx, dx`, then sets AH=3 and invokes INT 42.
A single diagnostic rebuild matched the whole 445-byte owner and original
ordered relocations. The source uses no codestring padding, emitted instruction
bytes or target-byte arrays. All other hit-circle C++ logic remains frozen.
The two random calls and two sprite calls own ordered relocation sites
433, 335, 79, 62. Direct caller/callee counts are 9/2, 1/1, 1/0 and 1/1;
INT 42 is recorded separately from call edges.

## Ownership and acceptance

Cfg/hitcircle candidate MAP DATA/BSS contributions are zero bytes at
1D56:0BEC / 1D56:68DC. Extra-attack contributions are zero bytes at
1D56:0BEE / 1D56:8DFA. All nonlocalized declarations and inline dependencies
are explicit `compat/rec98/` inputs in the replay manifest. Headers, external
state, resources and whole-product linkage remain separate and open.

The complete two-round `sol-cfg-exatt-hitcircle-probe-20261005` replay passed
all configured local gates for the three complete owners and the entire
earlier accepted aggregate: 60 functions / 26 CODE extents / 8880 owned bytes,
all raw bytes and original ordered relocations, MAP ownership, all 417 OMF
objects, and the deterministic 20-product / 351-game-object vector. Scoped
evidence promotes the three owners locally to exact. The 8758 function-body
bytes and 122 producer bytes remain separate. Whole-product ownership and
independent pristine-dump attestation remain open.

The final accepted-state `sol-cfg-exatt-hitcircle-final-20261005` replay also
passed both complete cold rounds with promoted ledger inputs frozen.

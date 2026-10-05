# MAIN player collision, hit damage and story skill review

The complete maintained `src/main/player/stuff.cpp` owner replaces the frozen
`th03/main_010.cpp` wrapper and `th03/main/player/stuff.cpp` implementation.
Its single MAIN_010_TEXT contribution is 096E:4A17–4B85, 367 bytes in MAIN_01.
It contains three contiguous functions: `player_hittest` (222 bytes),
`players_hit_damage_update` (118 bytes), and `story_skill_decrement` (27 bytes).
There are no producer-only bytes or owned MZ relocations. Candidate MAP DATA
and BSS contributions are zero bytes at 1D56:0BEC / 1D56:68DC.

The Japanese target is bound to SHA-256
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
MAIN Ghidra was re-attested before read-only function/caller/callee queries.
Automatic bodies agree with these raw boundaries; they do not prove the types.
The independent byte/RET/CFG/relocation observations are replayable with:

```sh
python3 scripts/review_th03_main_code.py --owner th03-main-player-state \
  --output .analysis/th03-main-exact/sol-player-state-target-review/raw-review.json
```

Source/MAP semantic names remain distinct from the target's observed offsets,
operations, edges and widths. This review makes no gameplay runtime claim.

## Collision source and producer review

The frozen register-pseudovariable C++ collision implementation differed in
34 raw bytes. Its 93 decoded instructions had matching addresses, lengths and
operations, but 19 register-to-register instructions used opposite opcode
direction forms. Examples are target `89 C3` versus candidate `8B D8` for
MOV BX,AX, target `29 C2` versus candidate `2B D0` for SUB DX,AX, and target
`31 C9` versus candidate `33 C9` for XOR CX,CX. Decoded equivalence alone did
not satisfy the raw Oracle. The upstream function-order warning did not
explain this observed encoding difference; all three function positions and
orders already matched.

A pinned TC4J probe confirmed that symbolic inline assembly emits the target
register forms. Merely substituting individual C++ expressions disturbed
register allocation and layout. The maintained collision routine therefore
expresses the complete observed bitmap algorithm with symbolic instructions
and meaningful labels, retaining natural C++ locals for top and bottom.
Field offsets derive from `offsetof` and `sizeof`; coordinates, flags, bitmap
pointer, dimensions and shifts use the real declarations and constants.
There are no target-byte arrays, instruction-byte emissions, synthetic
padding, fabricated arguments or manual prologue/epilogue. TC4J owns the
four-byte local frame, SI/DI preservation and near Pascal RET 2.
The two companion functions retain their frozen C++ bodies. `decomp.hpp` is
no longer a product dependency because its optimization barrier and register
pseudovariable helpers are not used by the maintained routine.

## Collision target facts

The guard reads invincibility at player +06 and hyper at +1E. Either nonzero
returns without clearing existing hit state. The signed word tile-size
argument is halved arithmetically. Center words at +00/+02 are shifted by
five (16 subpixels × 2-pixel tiles), then the radius is subtracted.
Negative top clamps to zero and skips the bottom-clipping branch; otherwise
bottom >=184 clamps to 183. This original asymmetric control flow is retained.

The bitmap is column-major, 18 bytes wide by 184 rows per player (3312 bytes).
The low three X bits select the first-byte mask; signed X shifts right by
three to select the byte column. The initial width includes those low bits,
and the mask removes right-side carry bits when width <=8. The target uses
unsigned byte MUL to form the bitmap offset and adds 3312 only when the
current player byte equals 1. The current player source is the redundant
`pid.current` byte at DGROUP:6590, not a rewritten argument.

Right clipping compares the signed byte column against 18. Negative columns
skip testing but still advance the pointer/width. Each visited column uses
a do-loop over rows and unsigned AH/DH comparison, followed by residual
column-stride adjustment. Width is a signed word for continuation but uses
an unsigned comparison for the final-byte mask. These mixed widths, the
at-least-once row visit and wrap behavior remain explicit.

On the first masked collision, the target zeroes the high X byte, shifts the
byte-column by eight, and stores it to the collision point. It clears AH
before shifting the original top by five for Y. Thus the reported point has
16×2-pixel granularity and uses the hitbox's original top, rather than the
actual row where the bit was encountered. Player +04 is set to 1. No hit path
clears the flag. There are zero CALL instructions; Ghidra reports three direct
callers. The signature is a near Pascal signed word argument with RET 2.

## Hit damage and skill target facts

The damage function takes a near player reference and returns the signed
half-heart byte in AL with RET 2. It reads CPU at +15 and next damage at +73,
adds the external CPU damage byte only for CPU players, resets next damage
to 3, and decrements the other player's value only when it is above 3.
Other-player indexing uses sign extension and the 128-byte player stride.
Health is the signed byte at +07. If the signed difference would be <=0 while
health >1, damage becomes health minus 1. Byte arithmetic and conversions
retain the original wrap behavior. The routine invokes the third function
before returning; its one direct caller and one callee are recorded.

The skill routine is near cdecl with RET. For current player zero only, it
loads the far resident pointer using LES and decrements the unsigned skill
byte at resident +38 only when it is nonzero. It has two direct callers and
no callees. Resident storage and the player's initialized/BSS state remain
outside this CODE ownership claim. Compatibility dependencies are listed
explicitly in the replay manifest; header presence grants no separate
whole-structure/data acceptance.

## Acceptance

The symbolic candidate's preliminary single rebuild matched the complete
367-byte owner and its empty ordered relocation vector. That diagnostic alone
granted no acceptance. The complete two-round maintained-source replay
`sol-player-state-probe-20261005` then passed every configured local gate:
54 functions / 23 CODE extents / 8345 owned bytes, complete raw equality,
ordered relocations, MAP contributions, all 417 OMF objects, and the
deterministic 20-product / 351-game-object vector. Scoped evidence promotes
the complete owner locally to exact, with all earlier accepted owners checked
in the same aggregate. The 8223 function-body bytes and 122 producer-owned
bytes remain separate. Whole-product ownership and independent pristine-dump
attestation remain open.

The final accepted-state replay `sol-player-state-final-20261005` passed the
same complete aggregate in two cold rounds, with promoted ledgers frozen at
build start.

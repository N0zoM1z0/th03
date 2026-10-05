# MAIN player movement and ordinary shots review

The complete maintained owners are `src/main/player/move.cpp` and
`src/main/player/shot.cpp`. The frozen upstream wrappers are `th03/player_m.cpp`
and `th03/p_shot.cpp`. Acceptance covers their complete CODE contributions,
not the original assembly contributions with the same segment names.
External state, sprite routines, speed tables and input producers remain
separate dependencies explicitly forwarded through `compat/rec98/`.

The Japanese target SHA-256 is
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
MAIN's Ghidra database was re-attested before read-only queries. Raw observations
can be replayed independently of Ghidra's automatic boundaries:

```sh
python3 scripts/review_th03_main_code.py \
  --owner th03-main-player-move --owner th03-main-shots \
  --output .analysis/th03-main-exact/sol-player-target-review/raw-review.json
```

Names are source/MAP hypotheses; offsets, bytes, branches and relocation sites
are observed from the pinned target. No gameplay runtime observations are claimed.

| Owner | MAIN_01 segment | 096E offset | Bytes |
| --- | --- | --- | ---: |
| player movement | PLAYER_M_TEXT | 3FF4 | 284 |
| ordinary shots | P_SHOT_TEXT | 515F | 185 |

## Movement target facts

`player_pos_update_and_clamp` occupies 3FF4–403D (74 bytes). It is near Pascal,
takes a near point reference and ends in RET 2. The velocity bytes at
DGROUP:6586/6587 are sign extended before addition to the signed word coordinates.
Opcode 98 is CBW in this 16-bit context; Capstone's `cwde` spelling is a decoder
presentation issue. X clamps inclusively to 0080–1180, or 8–280 pixels at
16 subpixels per pixel. Y clamps to 0180–1600, or 24–352 pixels.

`player_move` occupies 403E–4100 (195 bytes). It clears both velocity bytes,
reads a word input, uses the aligned/diagonal speed bytes at 6582–6585, and
returns AL=0 for invalid combinations, 1 for a valid direction, and 2 for no
input. All three exits use RET 2. The source retains the byte-sized enum,
Pascal word argument and compiler's `-a2` directive.

The bounded dispatch at 405E uses `CS:[BX+4102]` after checking input <=6 and
doubling its index. The seven target words at 4102–410F are 40FB, 40D3, 40A5,
40EF, 408B, 40DD and 4095. Every destination starts an instruction within the
195-byte body. Input 8 is handled separately; 9/0A and dedicated diagonal
0100/0200/0400/0800 inputs share the observed directional paths. The zero byte
at 4101 aligns the table. These 15 bytes are compiler producer ownership,
not function bodies or authored padding. No owner relocation exists.

Ghidra's automatic `FUN_196e_403e` has 223 addresses and incorrectly joins
an unrelated range near load address 11E06. Its reported extra callee comes
from that range. The raw body has zero CALL instructions and ends before the
alignment/table bytes. The authored boundary ledger records this correction;
it does not inherit the automatic function's span or calling convention.

## Shot target facts

`shots_update` occupies 515F–5189 (43 bytes), and `shots_render` occupies
518A–5217 (142 bytes). Both are near cdecl and end in RET. They iterate 32
14-byte records at DGROUP:66A6. Alive is any nonzero byte, unlike hitbox's
comparison against exactly 1. Update adds the signed velocity word at +06 to
Y at +04, then clears alive when Y <= -0010 (minus one pixel).

Render sets the sprite size representation to byte width 1 / half-height 8,
and global horizontal clip limits to 0 and 639. Sprite offsets combine the
unsigned animation byte at +0A and player offset word at +08. The near call
at 51C9 uses NOP/PUSH CS to enter a far-return coordinate helper at 096E:0BF0.
Y uses an arithmetic shift by four and adds the 16-pixel playfield top.
Two far sprite calls at 51E2/51F4 draw at X and X+16. The animation byte adds
two with byte arithmetic and resets at >=8. The owner's ordered MZ relocation
sites are 152 then 134, even though their numerical order is the reverse.
The exact gate retains this original ordering.

Both owner MAP rows have zero-byte DATA/BSS contributions at
1D56:0BEC / 1D56:68DC. Their local headers retain the upstream declaration
layout. Unreviewed compatibility declarations remain explicit scaffold inputs;
this review does not grant them separate data/layout acceptance.

## Acceptance

The first probe stopped at the MAP public check because the manifest spelled
the point typedef as `PlayfieldPoint`; the producer spells its underlying type
`sppoint`. That manifest hypothesis was corrected without changing product
source or gates. The fresh `sol-player-move-shots-probe-20261005-b` replay passed
two independent cold builds: all 51 functions / 22 CODE extents / 7978 owned
bytes, MAP contributions, original ordered relocations, validated 417 OMF
outputs and the deterministic 20-product / 351-game-object vector. Scoped
evidence promotes both complete owners locally to exact. The producer bytes
remain distinct from the 7856 function-body bytes. Whole-product ownership
and independent pristine-dump attestation remain open.

The final accepted-state aggregate `sol-player-move-shots-final-20261005`
repeated all gates with the promoted ledger inputs frozen at build start;
it also passed both cold rounds.

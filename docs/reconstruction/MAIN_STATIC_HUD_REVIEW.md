# MAIN static HUD review

`src/main/hud/static.cpp` is the complete maintained owner of HUD_STAT_TEXT,
096E:2217–2431 in MAIN_01. It replaces frozen `th03/hud_stat.cpp` and
`th03/main/hud/static.cpp`. All 539 bytes are seven complete function bodies;
there are no alignment bytes, dispatch tables or shared tails.

MAIN's Ghidra database was re-attested before read-only function/caller/callee
queries. Raw observations bind the Japanese target SHA-256
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`:

```sh
python3 scripts/review_th03_main_code.py --owner th03-main-static-hud \
  --output .analysis/th03-main-exact/sol-static-hud-target-review/raw-review.json
```

| Function candidate | Offset | Bytes | Observed ABI/return |
| --- | --- | ---: | --- |
| hud_wipe | 2217 | 56 | far cdecl; RETF |
| hud_static_halfhearts_put | 224F | 124 | far Pascal; byte pid in word slot; RETF 2 |
| hud_static_bombs_put | 22CB | 103 | far Pascal; byte pid in word slot; RETF 2 |
| hud_static_rounds_won_put | 2332 | 73 | near Pascal; byte pid in word slot; RET 2 |
| hud_static_story_lives_put | 237B | 54 | near cdecl; RET |
| hud_static_gauge_levels_put | 23B1 | 79 | far Pascal; word pid; RETF 2 |
| hud_static_put | 2400 | 50 | far cdecl; RETF |

Names and glyph/color meanings are frozen source/MAP interpretations. Numeric
arguments, field accesses, branches and stack effects are target observations.
Glyph bitmaps, library implementations and gameplay runtime behavior are
outside this CODE acceptance scope.

The wipe routine supplies character 0020/attribute 0005 to its fill call,
then box coordinates (2,1)–(37,24) and (42,1)–(77,24), both with attribute 00E1.
Compiler DWORD pushes pack two adjacent Pascal word parameters; they do not
change the declared argument widths. The configuration retains `-3 -Z`.

Half-heart display sign extends the player's byte at record +07 and scans
in steps of two. A remaining count >=2 uses glyph 5, otherwise glyph 6; the
second loop uses glyph 4 until the index reaches 10. X starts at 15 or 55,
Y at 1, with X step 2. The first loop does not clamp invalid values to 10.
Bomb display zero extends record +1D, uses glyph 7 at Y=23, and clears exactly
one following slot with glyph 00CF. P1 starts at X=36 with step -2; P2 starts
at 42 with step +2. Round display zero extends record +6C, starts at X=2 or
42/Y=1, and uses glyph 9 with step 2. These fields use the 128-byte player
stride. Signed/unsigned distinctions and the separate clear call are retained.

Story lives use LES to load the far resident pointer and zero extend byte
+34. The loop uses glyph 2 at Y=2, starts at X=36, and steps -2. Gauge display
indexes the byte array at DGROUP:2D56 with the word pid and uses glyph 001F
plus that value, attribute 0081. Boss level is the byte at 1E3E: values >=16
are decremented once before adding glyph base 0020, with attribute 0041.
The code does not independently establish an interpretation of current versus
next boss level. Both displays use Y=24, and the second X is 34 cells farther.

The aggregate routine loops over exactly two players and calls heart, bomb,
round and gauge routines. Same-owner far-return calls use PUSH CS/near CALL;
the near round call is ordinary CALL. It invokes story lives only when the
resident byte at +28 equals 1. Every function has two observed direct callers.
Unique direct callee counts are 2, 1, 1, 1, 1, 1 and 5 respectively.
Original ordered relocation sites are 481, 451, 395, 339, 275, 251, 161, 133,
52, 32 and 12. The required comparison preserves that order.

The candidate owner has zero-byte DATA/BSS contributions at
1D56:0BEC / 1D56:68DC. External player/resident/gauge state and glyph data
remain unowned here. Compatibility dependencies are explicit manifest inputs;
their presence does not grant separate header/data acceptance.

`sol-static-hud-probe-20261005` passed two full maintained-source cold builds
with all earlier accepted owners: 67 functions / 27 CODE extents / 9419 owned
bytes, raw equality, ordered relocations, MAP contributions, all 417 validated
OMF objects and the deterministic 20-product / 351-game-object vector.
The 9297 function-body bytes and 122 producer-owned bytes remain distinct.
Scoped evidence promotes this complete owner locally to exact. Whole-product
closure and independent pristine-dump attestation remain open.

The final accepted-state `sol-static-hud-final-20261005` replay also passed
both cold rounds with the promoted ledger inputs frozen at build start.

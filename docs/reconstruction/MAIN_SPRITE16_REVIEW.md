# MAIN sprite16 wrapper review

`src/main/graphics/sprite16.asm` maintains the complete SHARED contribution
0E8F:07FE–0909. Its 268 bytes consist of four complete function bodies
(266 bytes) and two genuine assembler word-alignment bytes. It replaces
frozen `th03/sprite16.cpp` and `th03/main/sprite16.cpp` for MAIN.

Same-process-attested Ghidra queries and the raw target review bind Japanese
MAIN SHA-256 `f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`:

```sh
python3 scripts/review_th03_main_code.py --owner th03-main-sprite16 \
  --output .analysis/th03-main-exact/sol-sprite16-target-review/raw-review.json
```

| Function candidate | Offset | Bytes | Observed ABI/return |
| --- | --- | ---: | --- |
| sprite16_sprites_commit | 07FE | 18 | far Pascal, no arguments; RETF |
| sprite16_put | 0810 | 97 | far Pascal, three words; SI/DI saved; RETF 6 |
| sprite16_putx | 0872 | 111 | far Pascal, four words; SI/DI saved; RETF 8 |
| sprite16_put_noclip | 08E2 | 40 | far Pascal, three words; DI saved; RETF 6 |

Ghidra's four contiguous body sizes agree with the raw boundaries. Observed
direct caller counts are 1, 52, 2 and 4. Commit has one direct far callee at
0000:2C42; the other functions have no CALL instructions. The only ordered
MZ relocation is at owner-relative offset 5, the far callee segment word.
API and constant names are frozen source/MAP interpretations; numeric port,
interrupt, operands, branches and stack effects are target observations.

Commit pushes word 1 to the sprite-copy call, outputs AL=0 to port 00A6,
then invokes INT 42h with AH=1. Put and putx load DI with the sprite offset,
DX with signed left, and AL with the byte at DGROUP:1D8A. They zero BH and
form the signed right edge as left plus AL*16. Clip boundaries are signed
words at DGROUP:1D84/1D86. Comparisons and their asymmetry are preserved:
right >= clip-right enters the right-clipping path; left >= clip-right
returns. Otherwise, left < clip-left enters left clipping, where a right
edge < clip-left returns. Left clipping advances DX by 16 and DI by 2;
right clipping subtracts 16 from BX. Both decrement AL and return on the
DEC zero flag. The branch structure does not combine both clipping loops.

Drawing sets AH=2, replaces BX with the signed top word arithmetic-shifted
right one, and loads CX with the height word at DGROUP:1D88 before INT 42h.
Putx additionally loads SI from the drawing-function word on every interrupt
iteration. It decrements the post-interrupt SI and returns if zero; otherwise
it adds the post-interrupt CX to BX, compares BX signed against 200, and
repeats if smaller. The interrupt handler's register effects are not assumed
to be the input values. No runtime or handler implementation acceptance is
claimed here.

Noclip deliberately retains the read of incoming AL in a discarded right-edge
calculation. It subsequently overwrites BX with top and reloads AL with width
before drawing. This unnecessary sequence remains part of the observed body.

The complete symbolic TASM source uses normal EVEN directives after procedures
instead of the upstream codestring NOPs. Alignment emits bytes at relative
offsets 115 and 227, and emits nothing after the two even-sized bodies.
There are no raw instruction emissions, target-byte arrays or authored padding.
The contribution remains BYTE PUBLIC; the assembler's alignment warning and
actual absolute alignment are checked against MAP/raw observations. Zero-byte
DGROUP DATA/BSS contributions are at 1D56:0BEE / 1D56:8DFA. External sprite
state, the far copy routine, INT handler, header/layout and other products are
outside this CODE scope. Header dependencies are frozen explicitly, including
the maintained playfield declaration and a compatibility VRAM forwarder.

`sol-sprite16-probe-20261006` passed two independent complete cold builds:
74 functions / 29 CODE extents / 9805 owned bytes, comprising 9679 function
bytes and 126 producer-owned bytes. Full raw equality, original ordered
relocations, MAP ownership, all 417 OMF outputs and the deterministic
20-product / 351-game-object vector passed with all earlier accepted owners.
Scoped evidence promotes this complete owner locally to exact. Whole-product
closure and independent pristine-dump attestation remain open.

The final accepted-state `sol-sprite16-final-20261006` replay also passed
both cold rounds with promoted ledger inputs frozen at build start.

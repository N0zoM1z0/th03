# MAIN playfield review

`src/main/playfield/playfld.asm` maintains the complete PLAYFLD_TEXT owner,
096E:0BF0–0C65 in MAIN_01. The 118 bytes contain three complete functions
(116 bytes) and two assembler-produced word-alignment bytes. It replaces
frozen `th03/playfld.cpp` and `th03/main/playfld.cpp`; the accompanying header
retains their declarations through explicit compatibility dependencies.

MAIN Ghidra queries re-attested the selected database in the same process.
The replayable raw review binds the Japanese MAIN target SHA-256
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`:

```sh
python3 scripts/review_th03_main_code.py --owner th03-main-playfield \
  --output .analysis/th03-main-exact/sol-playfield-target-review/raw-review.json
```

| Function candidate | Offset | Bytes | Observed ABI/return |
| --- | --- | ---: | --- |
| playfield_fg_x_to_screen | 0BF0 | 33 | far Pascal; two words; AX; RETF 4 |
| screen_x_to_playfield | 0C12 | 30 | far Pascal; two words; AX; RETF 4 |
| playfield_clip | 0C30 | 53 | far Pascal; two subpixel words; AL, AH=0; RETF 4 |

All three are leaf functions with zero observed CALL instructions and empty
ordered MZ relocation vectors. Ghidra identifies the first two complete
bodies, but its automatic third body covers only 8 bytes with an unknown
calling convention. The full raw 53-byte CFG, signed comparisons and terminal
RETF 4 establish the maintained third boundary. Observed direct caller counts
are 62, 3 and 6; automatic analysis is not an independent Oracle.

Foreground conversion arithmetic-shifts the signed X word by four, tests the
complete pid word, adds 320 for any nonzero pid and selects the second shift
word in that case. It then adds the DGROUP:659C indexed shift and 16.
Screen conversion retains the target's MOV BX,SP and tests only the low pid
byte. A nonzero low byte replaces DX with 320; a zero low byte leaves the
original full word in DX. It subtracts DX and 16 from X, then shifts left four
with native 16-bit wrap. The distinction between these pid tests is preserved.

Clipping begins with AX=0 and uses signed bounds from DGROUP:1D8C/1D8E.
X <= negative radius or X >= its negation plus 288*16 is outside.
Y <= negative radius or Y >= its negation plus 368*16 is outside.
Outside sets AL=1; every return retains AH=0. Names, subpixel interpretation
and dimension meanings come from the frozen source; numeric operands,
branch relations and stack cleanup are target observations. No runtime
observation is claimed.

The upstream C++ contains two explicit codestring NOPs. The maintained owner
instead uses complete symbolic TASM procedures and genuine EVEN alignment
after each procedure, as in the existing vector-far owner. This produces the
two bytes at relative offsets 33 and 117; the middle alignment emits no byte.
There are no raw instruction emissions, target-byte arrays or authored padding.
The CODE contribution remains BYTE PUBLIC; TASM's alignment warning is retained
and the actual absolute word alignment is checked by the MAP/byte Oracles.
Real DGROUP DATA/BSS declarations preserve near global operands, with zero-byte
MAP contributions at 1D56:0BEC / 1D56:68DC. Pascal exports match the frozen C++
names and callers. External shift/radius storage is not owned by this acceptance.

`sol-playfield-probe-20261005` passed two independent complete cold builds:
70 functions / 28 CODE extents / 9537 owned bytes, comprising 9413 function
bytes and 124 producer-owned bytes. Full raw equality, original ordered
relocations, MAP ownership, all 417 OMF outputs and the deterministic
20-product / 351-game-object vector passed with every earlier accepted owner.
Scoped evidence promotes this complete owner locally to exact. Header/data,
other-artifact ownership, whole-product closure and independent pristine-dump
attestation remain open.

The final accepted-state `sol-playfield-final-20261005` replay also passed
both cold rounds with promoted ledger inputs frozen at build start.

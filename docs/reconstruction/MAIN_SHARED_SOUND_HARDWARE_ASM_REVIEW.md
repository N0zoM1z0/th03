# MAIN shared sound, hardware and assembly review

Six complete owners contribute 603 bytes and eight functions: 598 function
bytes and five producer alignment bytes. This is MAIN CODE acceptance scope;
the reference paths also serve other products/games, which remain separate.
Every query re-attested MAIN's Ghidra database in the same process. Raw review
binds Japanese MAIN SHA-256
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`:

```sh
python3 scripts/review_th03_main_code.py \
  --owner th03-main-vram-planes --owner th03-main-sound-mode \
  --owner th03-main-pmd-resident --owner th03-main-se-reset \
  --owner th03-main-hflip-lut --owner th03-main-collision-map \
  --output .analysis/th03-main-exact/sol-main-shared-target-review/raw-review.json
```

| Function candidate | Segment:offset | Bytes | Direct callers |
| --- | --- | ---: | ---: |
| vram_planes_set | 0E8F:0008 | 41 | 1 |
| snd_determine_mode | 0E8F:0032 | 29 | 1 |
| snd_pmd_resident | 0E8F:0050 | 57 | unknown; no observed xrefs |
| snd_se_reset | 0E8F:033E | 11 | 4 |
| hflip_lut_generate | 0E8F:05D4 | 30 | 1 |
| collmap_set_rect_striped | 139D:009E | 212 | 17 |
| collmap_set_vline | 139D:0172 | 87 | 1 |
| collmap_set_slope_striped | 139D:01CA | 131 | 1 |

All use far no-argument cdecl interfaces and RETF; all have zero CALL
instructions and empty MZ relocation vectors. Sound predicates return the
16-bit result in AX. The reversal generator preserves DI; slope generation
preserves SI/DI through TASM USES. Ghidra's contiguous bodies agree except PMD,
which has no automatic function. Its complete 57-byte raw CFG includes both
RETF returns, and the frozen MAP marks it idle. Missing automatic analysis is
not evidence of an absent body or proof of runtime unreachability.

VRAM initialization retains the natural C++ algorithm from
`th01/hardware/vplanset.cpp`, with localized includes. Four dword stores to
DGROUP:19FC,1A00,1A04,1A08 set far pointer values A800:0000, B000:0000,
B800:0000 and E000:0000. Borland's source segment-pointer expressions convert
to the original planar declarations; the observed destination writes are four
bytes each. The linker gap at 0E8F:0031 is outside this 41-byte owner.

Mode detection invokes INT 60h with AH=9 and clears BX. If returned AL differs
from FFh, it increments BX and stores 1 to DGROUP:1A0C. Otherwise it loads BL
from 1A0D while BH remains zero; it does not clear the existing 1A0C byte.
It stores BL to 05DC and returns BX in AX, preserving any noncanonical MIDI
byte value rather than normalizing it. PMD detection first writes 60h to 1A0E
and zero to 1A0D,1A0C,1A0F, then uses ES=0 and LES BX from interrupt-vector
address 0180h. It compares bytes ES:BX+2,+3,+4 against 50h,4Dh,44h and returns
AX=1 or 0. Reset writes zero to 05EB and FFh to 05EA. API names, flag meanings
and the PMD interpretation are frozen-source interpretations of these numeric
target observations; driver installation and interrupt behavior are untested.

The three maintained sound owners use symbolic TASM and normal EVEN directives
instead of upstream codestring NOPs. They retain original WORD/BYTE PUBLIC
alignment, real DGROUP DATA/BSS frames and one alignment byte per owner.
MAIN uses distinct `snd_mode_main`, `snd_pmdr_main`, `snd_se_r_main` objects;
the existing shared C/C++ objects remain available to other products. This
adds three objects to the deterministic vector, making it 354 game objects
and 420 total OMF objects; the configured product count remains 20. The build
anchors are MAIN-specific and apply after the existing vector-far replacement.

The reversal generator retains the complete original TH03 assembly. It assigns
the zero entry first, then enumerates AL=1 through FFh. Eight ROL AL/RCR DL
iterations reverse each byte's bits while restoring AL for enumeration. DI
starts at DGROUP:1C64, advances exactly 256 bytes and is restored on return.
The table storage is external to this CODE owner.

Collision-map assembly retains the complete three-function source from
`th03/main/collmap.asm`, including its genuine self-modifying instructions.
The bitmap base is DGROUP:4BA0; any nonzero pid byte at 4B9A selects the second
3312-byte bitmap. Center and top-left share 4B8E/4B90, stripe width is 4B92,
height 4B94 and bottom-right 4B96. The source dimensions produce 18 columns
of 184 bytes each, with two-pixel tiles and four fractional coordinate bits.
Numeric addresses/widths are target observations; names/layout meanings are
source interpretations, not separate acceptance of those data objects.

Rectangle generation rejects signed center Y outside [0,5888), converts to
tiles with SAR 5, subtracts logical half-height, and clamps negative top to
zero. Its bottom comparison is unsigned and clamps values >=184 to 183.
It stores the selected base/top, resulting height and column stride into
writable instruction operands at CS:012E,0149,015E. Signed negative left
reduces word width; first-bit and byte-column calculations retain AL/DL byte
limits. CS:0136 receives the shift count. Each column ORs the pattern every
four rows using signed height checks; width decrements/comparisons operate on
DL. AL >=18 stops further columns. The source's degenerate-input behavior and
asymmetric clipping remain unchanged.

Vertical-line generation rejects signed X/Y outside [0,4608)/[0,5888), then
forms column-major offset and an 80h >> first-bit mask. The row loop writes
before testing bounds, decrements rows remaining to the bottom and uses
LOOPNE with the input height in CX. An initial CX=0 therefore wraps instead
of drawing zero rows. The internal EVEN byte at 01C1 remains inside its body.

Slope generation writes its bitmap base, rotated pattern and signed horizontal
delta into CS:021A,021F,0233. The initial bitmap row is 183 and DI starts at
91. It writes a byte mask and any carry mask to the next column, decrements
DI and returns at zero: the observed loop emits 91 stripes, not 92. Subsequent
X values use signed IMUL DI and IDIV 92 on DX:AX, then add top-left X. Each
iteration decrements the stored bitmap base by two. There is no added X
clipping. Normal TASM symbol expressions resolve writable operand addresses;
the initial 1234h values are real upstream self-modifying parameter slots,
not target-byte arrays. The short jumps to the next instruction are retained
as part of the original self-modifying sequence.

Collision-map alignment bytes outside bodies are at relative 299 and 431;
its other EVEN directives align internal loops. Forwarded assembler constants
and macros use explicit native `compat/rec98/*.inc` includes. The tracking
validator now checks assembler includes as well as C/C++ includes and permits
only one native include in an assembler forwarder. Focused positive and
negative tests cover valid forwarding, copied macros, missing forwarders,
direct reference paths, uppercase directives and DOS path separators.

VRAM initialization and the three sound owners have zero-byte DATA/BSS
contributions at 1D56:0BEC / 1D56:68DC. Collision-map original and maintained
OMF records define only empty DATA, grouped in DGROUP; no BSS contribution
is present or required. Reversal generation has neither contribution. An
initial erroneous BSS expectation and the temporary declaration used to test
it were both removed after comparing the original/maintained SEGDEF and
GRPDEF records. The diagnostic `sol-main-shared-probe-20261006-d` is not used
for acceptance. These metadata frames do not grant data, header, asset,
other-artifact or runtime acceptance.
The cached diagnostic reproduced all six complete contributions, but only
full maintained-source cold replay can grant exact credit.

`sol-main-shared-probe-20261006-e` passed two independent complete cold builds
with the original collision-map segment footprint: 87 functions / 36 CODE
extents / 10932 owned bytes, comprising 10797 function bytes and 135 producer
bytes. Full raw equality, original ordered relocations, MAP contributions,
all 420 OMF objects and the deterministic 20-product / 354-game-object vector
passed with every earlier accepted owner. Scoped evidence promotes all six
complete owners locally to exact. Independent pristine-dump attestation and
whole-product closure remain open.

The final accepted-state `sol-main-shared-final-20261006` replay also passed
both cold rounds with promoted ledger inputs frozen at build start.

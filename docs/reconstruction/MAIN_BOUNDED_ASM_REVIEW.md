# MAIN bounded assembly includes

The frozen ReC98 `th03_main.asm` identifies itself as IDA-generated disassembly
of MD5 `43ee91a800f1f0fe35a87149c90b037d`. This matches the pinned Japanese
MAIN target, whose SHA-256 is
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`.
This is candidate-local-attested evidence; independent pristine provenance
remains unknown. Reassembling that generated translation unit does not establish
authored-source progress for its other code, data, assets or library includes.

Five complete handwritten CODE includes are maintained as `.inl` files. They
retain symbolic algorithms, original near/far conventions and original include
positions. Each has a distinct logical owner, while its physical object remains
`obj/th03/main.obj`. No new object, public symbol, segment or artificial ABI is
introduced. The unaccepted carrier is only a frozen diagnostic build context.

| Maintained include | Target CODE | Function bytes | Producer bytes | Containing MAP contribution |
| --- | --- | ---: | ---: | --- |
| `src/main/graphics/sprite16_copy.inl` | `0000:2C2C` | 95 (two functions) | 1 | _TEXT `0000:0272`, size `2C3E`, no group, ACBP 48 |
| `src/main/formats/pfopen.inl` | `0000:2D5E` | 281 | 1 | _TEXT `0000:0272`, size `2C3E`, no group, ACBP 48 |
| `src/main/math/randring_fill.inl` | `096E:0D1A` | 18 | 0 | HITCIRC_TEXT `096E:0C98`, size `13C2`, MAIN_01, ACBP 48 |
| `src/main/collision/reset.inl` | `096E:0D58` | 19 | 1 | HITCIRC_TEXT `096E:0C98`, size `13C2`, MAIN_01, ACBP 48 |
| `src/main/player/score_add.inl` | `096E:3ED0` | 88 | 0 | PLAYER_M_TEXT `096E:2432`, size `1BC2`, MAIN_01, ACBP 28 |

The three producer bytes are natural `EVEN` alignment at `0000:2C41`,
`0000:2E77` and `096E:0D6B`.
The random getter macro between fill and reset belongs to a separate, unaccepted
review scope. No bytes between the five includes receive ownership credit.

## Target observations and interfaces

`sprite16_sprites_copy_page` is far Pascal with a page word and RETF 2. Its
private 21-byte near helper is called eight times, twice per B/R/G/E plane.
The helper toggles AL, outputs port A6h, copies 4000 dwords with ambient DF,
and swaps source/destination segments in BX/DX. The wrapper obtains one
16000-byte temporary plane from `smem_wget`, preserves DS/SI/DI on success,
copies each plane via temporary storage and releases that storage before
returning AX=1. Allocation failure takes the carry branch and returns AX=0
from the initial DX zero exchanged with AX; it does not take the success saves.
ES and page/flags are not newly restored. The argument macro uses SS:[BX+4].
Plane segments are ABE8/B3E8/BBE8/E3E8, reflecting real sprite VRAM offset.

Upstream `nopcall` explicitly inserted a compatibility NOP. The maintained
include instead uses real far CALLs with local `NOSMART`/`SMART` directives.
Without NOSMART, TASM shortens each same-segment call to four bytes and moves
the wrapper's later code; that diagnostic fails. With NOSMART, TASM emits
normal five-byte far CALL instructions and TLINK's original optimization
produces NOP/PUSH CS/near CALL at the original positions. No opcode array or
explicit fill NOP is supplied. The cached diagnostic with this change had the
same full MAIN product hash as before; only fresh complete replay can accept
it. The complete CODE extent has no remaining MZ relocation. The private
helper keeps its original visibility; replay proves all eight near calls from
the owned public wrapper in both target and candidate rather than adding a
public alias solely for MAP lookup.

`PFOPEN` is far Pascal with two far pointers and RETF 8. It uses ENTER/LEAVE,
saves SI/DI, allocates a packed 31-byte PFILE and opens the archive. It scans
32-byte cached headers in FS, calling private near `STR_IEQ` at `0000:2E78`
with far filename pointers. Header fields remain type word at 0, auxiliary
byte at 2, 13-byte filename at 3, packed/original size words at 16/18,
dword offset at 20 and eight reserved bytes at 24. The scan uses the first
type byte for its terminator test. The target's not-found branch continues
into the shared seek path; no new early error return is introduced.

The archive handle sits at PFILE+0. Decoder offsets are at +2/+4; sizes,
read/home/location counters are dwords at +6/+10/+14/+18/+22. RLE count/byte
state are words at +26/+28; key is the byte at +30. The code preserves the
original transient `MOV ES,CX`, later replacing ES with SI before accesses.
Packed/original sizes are zero-extended from words, counters cleared as
original words, and decoder functions chosen by F388h/9595h and the key byte.
Unknown type closes/frees, allocation failure stores only the low error byte,
and other original error behavior is retained. FS/ES are clobbered; external
heap, archive cache, decoder and error state are separate owners. The source's
GAME=5 alternatives receive no TH03 acceptance. The master `_call` macro's
PUSH CS/near CALL is a genuine same-segment far-return interface and remains
part of the reviewed calling convention, distinct from compatibility padding.
The function and complete include have no ordered MZ relocation entries.

`randring_fill` saves SI, starts at byte 255 and calls far `IRand` at
`0000:1EEC` once per byte, storing AL and counting down through byte zero. Its
only ordered MZ relocation site is relative 7, the far call's segment word.
The target ring occupies DGROUP `1E52..1F51`; byte index `1F52` is untouched.
The GAME >= 4 index reset in upstream source is inactive for GAME=3 and is not
accepted for another game. The function returns near with SI restored. Other
registers/flags follow the actual call and loop, rather than an invented clean
ABI. The generator itself and the ring's BSS are outside this CODE owner.

`collmap_reset` saves DI, copies DS into ES, and clears 1656 dwords using
386 `XOR EAX,EAX` and `REP STOSD`. This corresponds to two 3312-byte collision
bitmaps at DGROUP `4BA0..657F`. It does not execute CLD: forward DF is a caller
contract. ES remains equal to DS; EAX and CX are clobbered, DI is restored, and
return is near. The maintained include allocates no storage and owns no BSS.

`score_add(unsigned int,unsigned char)` is far Pascal with score at BP+8 and
pid's low byte at BP+6, both occupying word stack slots. Any nonzero pid byte
selects the second score, independent of the slot's high byte. It preserves
BP/SI and returns with RETF 4. The eight-byte little-endian decimal scratch
buffer is at DGROUP `4B74`; scores are two eight-byte buffers at `4B64`.
The word table at `08A8` contains 10000, 1000, 100, 10, 1. Four unsigned DIVs
construct the lower five scratch digits while the upper three are cleared.
Seven AAA iterations propagate carries; the last digit is added without AAA.
There is no newly imposed saturation, overflow handling, reentrancy or pid
validation. Scratch storage, scores and the table are external dependencies;
matching these operands establishes the reviewed CODE layout, not ownership
of their DATA/BSS producers.

The raw Capstone16 review partitions every owned byte and checks complete
returns and relocation edges. A fresh same-process-attested Factory Ghidra
query agrees on the fill/reset/score and private/public copy bodies
(18, 19, 88, 21, 74 bytes). PFOPEN has an automatic 260-address body
spanning 281 bytes; the complete 281-byte raw CFG is reviewed manually,
including the automatic discovery omissions. Its
automatic prototypes and discovery remain provisional. No gameplay runtime
observation or independent Oracle is inferred from this agreement.

## Carrier and replay gates

The diagnostic carrier is pinned byte-for-byte to SHA-256
`94c52b803ebcf3df018c18cffc35891f074c45b3cafbf5927db1907024f54d62`
in the frozen reference archive. Each replacement include must occur exactly
once in that carrier. The maintained fragment owns its full reviewed body,
including real producer alignment, and must lie wholly inside the explicitly
matched containing MAP contribution. Its public start, segment/group/alignment,
full raw bytes and ordered relocation entries must match in both fresh builds.
Source, ledgers and replay inputs are frozen and checked for mutation.

Object-format and determinism observations inspect the complete physical
carrier object without accepting its surrounding generated code. The full
accepted-owner aggregate and configured 20-product / 354-game-object vector
are checked alongside the fragments. This remains a scoped reconstruction
experiment; whole-product ownership, standalone linking and gameplay remain
open. Random-getter macro expansions and the remaining root CODE/DATA/BSS/resource
scopes still require separate complete reviews.

## Accepted local scope

`sol-main-bounded-all-probe-20261006` passed both fresh full builds with all
five bounded includes and every previously accepted MAIN owner. This adds
six complete functions, 501 function bytes and three genuine alignment bytes.
The aggregate is 37 maintained source owners / 41 CODE extents / 93 functions /
11436 owned bytes (11298 function bytes, 118 table bytes, 20 alignment bytes).
The vector remains 20 products / 354 game objects / 420 OMF objects because
all five includes share the original physical carrier. The first three-include
probe `sol-main-bounded-probe-20261006-b` passed its then-current 90-function
aggregate; the initial attempt failed the legacy comment decoder before build.
That failed attempt and the shortened-call cached diagnostic grant no credit.

The final accepted-state replay is `sol-main-bounded-final-20261006-b`. Raw target
reviews are `.analysis/sol-main-bounded-raw-20261006.json` and
`.analysis/sol-main-bounded-all-raw-20261006.json`; attested Factory function
observations are `.analysis/sol-main-bounded-functions-20261006.json` and
`.analysis/sol-main-bounded-more-functions-20261006.json`. The latter exports
plain text despite the output name. None is a gameplay runtime acceptance.

The existing DOS behavior probe checks input/math; it does not establish
gameplay runtime equivalence for these five newly owned includes. The initial
accepted-state replay also passed; final replay `-b` freezes corrected boundary
command metadata and separate, explicitly provisional Ghidra observations.

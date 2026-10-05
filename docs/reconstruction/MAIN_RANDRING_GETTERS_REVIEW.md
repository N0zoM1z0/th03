# MAIN random-ring getter macros

The frozen `th03/math/randring.inc` defines two handwritten macros. MAIN expands
`RANDRING_NEXT_DEF_NOMOD 1, near`, `RANDRING_NEXT_DEF 2, near` and
`RANDRING_NEXT_DEF _FAR, far`. All eight generated functions are maintained in
`src/main/math/randring_getters.inl`, with the original symbolic macros and
native near/far procedures. The explicit upstream NOP is replaced with natural
`EVEN`; all three getter starts are even and their 17-byte bodies need exactly
one alignment byte. There is no target-byte emitter or invented ABI.

| Complete source expansion | Target segment:offset | Owned bytes | Function bodies | Genuine alignment |
| --- | --- | ---: | --- | --- |
| Instance 1, NOMOD | `096E:0D2C` | 44 | 17, 26 | relative 17 |
| Instance 2 plus FAR | `139D:000A` | 148 | 17, 26, 30, 17, 26, 30 | relative 17, 91 |

The source has one logical owner and two separately ledgered CODE extents.
HITCIRC_TEXT containment is `096E:0C98`, size `13C2`, MAIN_01, ACBP 48.
The entire MAIN_04_TEXT contribution is `139D:000A`, size `0094`, MAIN_04,
ACBP 28. Both contributions belong to generated `th03_main.asm`; the shared
physical object is `obj/th03/main.obj`. Its surrounding CODE and DATA/BSS
remain unaccepted.

## Target facts and ABI

Every getter zeroes BH, loads the byte index from DGROUP `1F52`, adds ring base
`1E52` to BX, increments that byte index, then reads a word at DS:BX. None
wraps the high byte of a word read back to ring element zero. At index 255,
the high byte is the adjacent index byte after it has wrapped to zero. Other
indices read consecutive ring bytes, including unaligned words. All instances
share the same mutable index. These facts follow the reviewed raw instructions;
no runtime distribution or randomness claim is made.

Plain entries return AX with RET or RETF. Masked entries save BP, establish a
frame, apply an unsigned word mask at BP+4 (near) or BP+6 (far), restore BP and
return with RET 2 or RETF 2. Modulo entries use the same argument slots, zero DX,
perform unsigned DIV, and move the remainder from DX to AX before returning.
Zero divisor behavior is the original processor divide fault; no check is
introduced. BX is clobbered, modulo also clobbers DX, and flag behavior remains
that of the real instructions. SI/DI/CX and DS/ES are untouched by these
functions. TASM's native `arg` declaration follows the actual procedure distance.
The ring and index allocations are separate unaccepted BSS producers.

The complete 189 function bytes plus three producer bytes have no MZ relocation
entries. Raw decoding proves every return and full partition. Seven automatic
Ghidra bodies agree with sizes 17/26/30 after same-process target attestation;
there is no automatic function at the plain instance-2 entry `139D:000A`.
Its full 17-byte raw body and original public MAP start are reviewed manually.
Automatic discovery and prototypes are provisional and give no authored credit.

## Context and compiler observations

The definitions enter the generated root through a nested include chain:
`th03_main.asm` includes `th03/th03.inc`, which includes `th03/math/randring.inc`.
The context header SHA-256 is
`8fe390f050f785440c55bd7c320c9f57c9f9fdc04c1fc9fa819d41c4e1ab7920`;
the root SHA-256 is
`94c52b803ebcf3df018c18cffc35891f074c45b3cafbf5927db1907024f54d62`.
Both must match frozen bytes and contain their respective child exactly once.
The chain must reach the actual MAP module. Reordered, omitted, duplicated or
changed carriers fail before compilation. The frozen root also binds the three
invocation sites and the surrounding segment declarations. Other artifacts
may parse these definitions, but receive no CODE acceptance from this review.

The cached `sol-main-randring-natural` diagnostic naturally reproduced all
192 target bytes and original ordered relocation lists. It is a compiler
observation, not a cold acceptance result. Raw observations are replayable via:

```sh
python3 scripts/review_th03_main_code.py --owner th03-main-randring-getters \
  --output .analysis/NEW_RANDRING_RAW.json
```

The target remains the pinned Japanese MAIN, SHA-256
`f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b`, with
candidate-local-attested provenance. Independent pristine provenance is unknown.
Exact promotion requires two complete fresh builds and the entire accepted
MAIN aggregate. Neither shared carrier metadata nor the existing input/math
DOS probe establishes standalone linking or gameplay runtime equivalence.

## Local acceptance

`sol-main-randring-probe-20261006` passes both complete fresh builds: all eight
getters, 192 complete CODE bytes, natural alignment, ordered relocations,
public MAP starts and pinned nested carriers match. The aggregate now covers
38 maintained source owners / 43 CODE extents / 101 functions / 11628 owned
bytes (11487 function bytes, 118 tables, 23 alignment). The vector remains
20 products / 354 game objects / 420 OMF objects. The final accepted-state
receipt is `sol-main-randring-final-20261006`.

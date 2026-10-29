# MAINL BFNT native source review

The complete BFNT library512 CODE, BFNT_PALETTE_SET64 CODE and signature6 DATA
add582 accepted library bytes and five procedures. They use the actual GAME3
MAINL root. The maintained `super_types.inl` contains the original constants
and packed BFNT structure; `bfnt_signature.inl` contains the signature and its
original NUL. No literal instruction arrays or object patches are involved.

## Source and native reproduction

`build_th03_mainl_bfnt_work.py` substitutes the signature include at its original
root position. The original nested super.inc path forwards directly to the
maintained types include during this selected build. Complete declaration tokens
equal the original provider; the native dependency list proves consumption of
both maintained includes. All containing native records, literal FIXUPP order
and complete public records/multiplicity equal the retained root.

Two serialized actual TASM/TLINK rounds rebuild only this root and reuse35
project objects plus the current CRT library. Complete raw OBJ/EXE/MAP vectors
repeat. Both EXEs equal the pinned Japanese decoded target, and both MAPs equal
the retained MAP. The original wrapper, nested include and all938 cold outputs
are restored and validated. The full cold pair and prior runtime observations
are reused without replay.

The initial selected driver accidentally reused the file review's private output
names. It now uses independent BFNT paths. Two actual file-driver assembly/link
rounds restored that pair and reproduced every original output hash. Its original
report and logs remain unchanged; the recovery run is recorded separately.

## Ownership, ABI and self modification

| Procedure | Address | Bytes | RETF argument cleanup |
| --- | --- | ---: | ---: |
| BFNT_ENTRY_PAT | 0000:0286 | 302 | 8 |
| BFNT_EXTEND_HEADER_SKIP | 0000:03B4 | 34 | 6 |
| BFNT_HEADER_READ | 0000:03D6 | 59 | 6 |
| BFNT_EXTEND_HEADER_ANALYSIS | 0000:0412 | 95 | 6 |
| BFNT_PALETTE_SET | 0000:04C6 | 64 | 6 |

The BFNT512 owner additionally contains a20-byte error/unwind path at0272 and
ordinary outer EVEN bytes at0411/0471. Its error labels borrow BFNT_ENTRY_PAT's
frame and add no procedures. Internal EVEN instructions remain within their
complete procedure extents. Branch targets, public/MAP boundaries and complete
far Pascal returns are checked against the actual native producer.

Eleven own-CS fields cover eight real MOV-immediate operand writers and three
saved-DS reads. The written slots hold clear color, saved DS, file handle, x/y
byte counts, pattern size, plane size and read size. All operand widths and exact
instruction destinations are reviewed; the original JMOV placeholders remain
native instructions. The twelfth BFNT field resolves the signature in DATA.
The palette routine's sole field resolves Palettes in BSS at0E3F:141E. None of
these13 fields produces an MZ segment entry; the complete scoped ordered vectors
are empty. Root CODE begins at0000:0272, DATA at0E3F:0112, BSS at0E3F:13F6.

The main routine pushes SI then DI and pops SI then DI on its exits, swapping
the caller's values. Its shared unwind has the same ordering. This is original
behavior, and the recovered code preserves it. Allocation failures, dimensions,
zero pattern counts and caller DF remain unchecked. The pattern reader checks
both DOS carry and returned length; header, extension and palette readers retain
their weaker length checks. Header comparison does not add CLD. Extension
analysis does execute CLD. BFNT_PALETTE_SET rotates sixteen BGR triples into RGB
in memory and performs no hardware-palette output.

## Storage

The header is32 packed bytes: id0..4, col5, ver6, x00=7, Xdots8, Ydots10,
START12, END_14, font_name16..23, time24..27, extSize28 and hdrSize30. Complete
source declarations and native field accesses agree. These type declarations
allocate no file storage.

BFNT_ID/_BFNT_ID at0E3F:051C owns all six bytes `BFNT`,1Ah,NUL. The reader compares
the first five bytes. The original sixth byte is an explicit terminator, with no
new padding. Complete containing LEDATA has no FIXUPP fields. Header scratch and
palette BSS remain outside this DATA owner and add no file-byte credit.

The verifier is `scripts/lib/decoded_mainl_bfnt_native.py`. Its negative controls
check independent native byte resolution, an actual self-modified slot, the
terminator and the distinction between an offset field and an MZ relocation.
Private proof inputs are `mainl-bfnt-build.json`, `mainl-bfnt-native.json`, both
`bfnt-roundN.obj/.exe/.map` vectors, and `bfnt-root.asm/.lnk` under `.analysis/work/`.
This review makes no physical DOS/device or whole-product source claim.

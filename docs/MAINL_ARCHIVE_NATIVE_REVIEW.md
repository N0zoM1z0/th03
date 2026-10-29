# MAINL buffered and archive readers

This step accepts24 disjoint extents:17 complete procedures, six ordinary TASM
EVEN bytes and five initialized state bytes. The1,045 additional bytes comprise
1,040 CODE and5 DATA. TH03's PFOPEN281 is authored game code; the other764 bytes
are library code/storage. Existing107 owners and nested observations are unchanged.

## Native production and natural alignment

`build_th03_mainl_archive_work.py` assembles and links the actual GAME3 root twice,
reusing35 project objects and the current CRT library. Its nested pf.inc forwards
to maintained `archive_types.inl`. Complete native records, public records and
literal FIXUPP order equal the retained root. Both complete raw OBJ/EXE/MAP vectors
repeat; both EXEs equal the pinned Japanese decoded target and both MAPs equal
the retained MAP. The original wrapper/nested provider and938 cold outputs are
restored and validated. No full cold/DIET or ancestor runtime replay is performed.

Two further native links answer the actual alignment question. Five small TUs use
the real BFILL/BGETC, new `pf_getc.inl`, real PFREAD, new five-byte state provider,
and original random seed provider. The carrier has a normal32-byte stack. All
five OMFs and the complete MZ/MAP repeat. Their native SEGDEFs declare WORD
alignment. PFGETC's175-byte contribution ends at mini011B; following PFREAD starts
at011C. The five-byte DATA contribution is followed by the WORD-aligned random
seed at local6. TLINK emits both intervening zeros, with no source filler.

`pf_getc.inl` contains the four complete original reader functions and their
internal macro EVEN, without the old final `db 0`. The state include declares
WORD512, WORD0 and BYTE0, without a trailing dummy declaration. Original globals
and four getter bodies are token-identical after removing exactly those final
legacy filler statements. Their independently produced native bytes are checked
against the product. The sole new external field is a real self-relative WORD
call to BGETC; its literal OMF stream resolves for both actual MAPs.

The frozen full-root provider still spells those zeros explicitly as contextual
transport. Its complete link equality is not proof of recovered whole-product
TU layout. Product0000:19A3 and DATA0E3F:05B5 receive zero source-byte credit.
The old19A3 source-present row is corrected to excluded/linker-gap; its historical
evidence remains intact. Future full recipe work must integrate the independent
module boundaries. TASM EVEN/ALIGN inside the monolithic DATA contribution emitted
90 rather than00 in direct experiments, so those directives are not a substitute
for the demonstrated module boundary.

## Complete procedure ownership

| Procedures | CODE bytes | ABI |
| --- | ---: | --- |
| BCLOSER, BFILL, BGETC, BOPENR, BREAD, BSEEK, BSEEK_, DOS_ROPEN | 400 | Eight far Pascal APIs |
| PFCLOSE, PFGETC, PFGETC1, PFGETX0, PFGETX1, PFREAD, PFREWIND, PFSEEK | 353 | Five far Pascal APIs, three register-ES near readers |
| PFOPEN | 281 | Far Pascal, pops8 |

Six separately owned outer EVEN bytes are at04C5,060B,067D,06AD,1903 and1A0D.
They are not extra procedures. Complete instruction coverage, public names,
both MAP tables, every branch destination and near/far return cleanup are checked.
All13 containing-root native fields resolve independently in their literal order;
all scoped MZ relocation vectors are empty. Three own-CS fields in PFOPEN select
PFGETX0, PFGETX1 and PFGETC1. Five actual indirect calls consume near slots2/4.

BFILE is9 packed bytes: handle0, left2, position4, capacity6 and first buffer
BYTE8. The allocation remains bbufsiz+9. PFILE is31 packed bytes: bf0, getc2,
getx4, size6, read10, home14, loc18, osize22, count26, character28 and key30.
These WORD/DWORD/BYTE declarations are preserved. Initialized bbufsiz/pferrno/
pfkey at0E3F:05B0..05B4 retain both underscore/plain aliases. BSS adds no credit.

## Preserved behavior

TH03 PFOPEN consumes the prefetched32-byte directory records:16-bit sizes at16/
18,32-bit offset20 and filename3. It uses the hook's cached entries pointer at
1D06. It differs substantially from TH02's directory-reading SEEK routine. Its
missing-entry path still falls through to seeking, seek failures remain unchecked,
and all original allocation/error paths and BYTE/WORD pferrno writes remain.

BREAD rejects signed nonpositive sizes; PFREAD only rejects zero, then iterates
the full WORD count. BSEEK failure storesFFFF in b_left; BSEEK_ clears b_left before
DOS and retains that cleared state on failure. PFGETX0 advances physical/logical
counters before BGETC. RLE repetition and count-byte reads preserve their distinct
logical/physical accounting; XOR decoding remains the Touhou variant. PFSEEK
increments and decrements the high WORD of its stack argument. No defensive fixes
or new runtime contracts are introduced.

The verifier is `scripts/lib/decoded_mainl_archive_native.py`. Current private
inputs are `mainl-archive-build.json`, `mainl-archive-native.json`, both
`archive-roundN.obj/.exe/.map` vectors, `archive-root.asm/.lnk` and both
`archive-mini-roundN-*`/mini EXE/MAP vectors under `.analysis/work/`. This review
makes no physical DOS/heap execution or whole-product source claim.

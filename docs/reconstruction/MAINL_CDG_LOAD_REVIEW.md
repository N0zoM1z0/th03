# Complete MAINL CDG loading candidate review

The complete frozen `th03/cdg_load.cpp` TU contributes 593 decoded CODE bytes:
five functions / 219 instructions, without intervening unclassified bytes.
Both cached products match all raw bytes and the 24 original ordered relocation
sites. Source/control-flow and far-Pascal review is complete for this bounded
candidate contribution. No maintained source, cold build or exact acceptance
follows from those cached observations.

```sh
python3 scripts/review_th03_mainl_cdg_load.py --output .analysis/NEW_CDG_LOAD_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_cdg_load_review.py -v
```

Receipt: `.analysis/sol-mainl-cdg-load-review-20261006.json`. It inherits guarded
canonical/decoded/cached lineage and pins eight consulted frozen providers in
both source trees: complete root/include, CDG layout, plane constants, integer
and bool definitions, and master.lib interface/memory-model declarations.
All eight providers match byte-for-byte; this carrier has no maintained-source
remap. Ghidra fails headless-usage before DB attestation; no database observation
is used. Wine is unavailable for current cold producer validation.

| Entry in decoded 0C7E | Function | Bytes / instructions | Return |
| --- | --- | ---: | --- |
| 073E | Single image | 138 / 50 | far RET 8 |
| 07C8 | Single image without alpha | 134 / 48 | far RET 8 |
| 084E | All images | 230 / 83 | far RET 6 |
| 0934 | All images without alpha | 28 / 10 | far RET 6 |
| 0950 | Free slot | 63 / 28 | far RET 2 |

Every branch stays inside complete instruction boundaries of its own body.
All five optimized near internal calls have an actual preceding PUSH CS and
enter the complete far-returning free/all function. Six foreign far interfaces
are modeled: FILE_ROPEN/READ/SEEK/CLOSE and HMEM_ALLOCBYTE/FREE. Their observed
Pascal argument cleanups are 4/6/6/0/2/2 bytes. Native returns preserve BP/SI/DI
and DS. Incoming DF is retained in every constructed contract; no x87 operation
is present in this contribution.

## Explicit file and heap scope

All five functions, their internal calls and far returns execute unchanged
native CODE. Only the six external bodies are substituted. A constructed
16-byte header, absent header, or two-byte short header is injected by the
FILE_READ interface. Subsequent payload reads record pointer and size requests;
they write no payload bytes. Repeated model allocation segments deliberately
alias artificial 5000/7000 buffers, or return zero. This is a file/heap argument
and control-flow contract, without real allocation, DOS handles, file contents,
physical null-segment stores or rendered graphics.

A separate source-level specification with explicit word/long promotions checks
every ordered interface event and the entire 65536-byte DGROUP result. The
target and each cache retain their own starting DGROUP bytes; before/after hashes
are recorded separately, not misrepresented as whole initial-DGROUP equality.
Normalized request/control observations agree across all three images. Native
entry traces verify internal free/all calls rather than replacing them with
interfaces. Each case then invokes the real free body again, checking retained
pointers and complete DGROUP state after cleanup.

There are 78 base contracts in both DF states: 156 records and 312 top-level
invocations per image, including the follow-up frees. Across three images,
936 invocations terminate normally. Seven synthetic adversarial tests reject
truncated bodies, incorrect cleanups, operand/neighbor branches, incorrect
near/far frames, unknown/indirect interfaces, segment aliases, outside-memory
writes, escaped interrupts and stale terminal state.

## Arithmetic and failure contracts

The single-image seek calculation first forms `(bitplane_size * 5) mod 65536`
in AX, zero-extends it, sign-extends the 16-bit image number, and multiplies in
32 bits. Thus size13107/image1 requests65535; size13108/image1 requests4.
With size65535/image-1 the signed seek is -65531 (`FFFF0005`), not -327675.
Size65535/image-32768 produces `80028000`. Color allocation/read sizes are
`(bitplane_size * 4) mod 65536`; size16384 produces a zero-byte color request.
Zero sizes and negative image numbers have no caller guard here. Noalpha adds
a separate zero-extended single-plane seek before reading colors.

Single loaders free the old slot before opening; all-image loading opens before
freeing the first slot. All-image loading reads the header, frees remaining
slots, then allocates/reads sequentially. Modeled open/read failure status,
CF and zero allocation segments do not stop the native caller: requests still
continue through close. A failed header read retains stale metadata after the
old pointers have been zeroed; a short header only replaces the size word.
Failed frees still cause the native pointer word to be cleared.

The unsigned header image-count byte controls both all-image loops (zero-extended
then compared against a signed word counter); count0 loads no images. Single
loading ignores that count and loads one image, matching the frozen header's
comment that single-image files may declare zero. Batch loading copies the
metadata fields and forces plane_layout0; single loading retains the supplied
layout byte. The header declares segment words must be zero, but the caller
does not validate them: count0 with ABCD/DEAD words retains both, and a subsequent
real free issues both corresponding model free requests. Equal nonzero pointers
also produce two free requests; no allocator-level double-free behavior is proved.

## Slot and shared-flag hazards

Slot addressing uses `1D0E + ((slot << 4) mod 65536)`, with final word wrap.
Neither loading nor freeing checks the declared 32-slot array. Constructed
cases include slot31,32,FFFF, count255, batch crossing slot31, and DGROUP wrap.
Native field stores and free calls beyond the table are retained as observations;
normal game/resource reachability is unproved.

The shared noalpha byte is at decoded DGROUP0894 and is reread for every image.
`all_noalpha` writes1 before its actual call to `all`, then writes0 afterward;
it does not restore a previous nonzero value. A constructed batch starting at
slot0E30 with count140 reaches metadata at088E on image index136. Copying its
bottom-offset80 writes flag0894=50, so an initially alpha-loading `all` skips
alpha for its final four images (276 allocations and four alpha seek requests).
Starting at slot0DE0/count255 wraps and produces the same alias at index216,
skipping alpha for the final39 images. The wrapper's final flag reset can itself
change the aliased bottom-offset byte. These are actual native writes over
explicit malformed caller/header fixtures, without a claim about shipped CDGs.

## Acceptance boundary

Five decoded boundary-reviewed rows have empty source/stored offsets. None is
authored, structural or exact progress; the frozen queue's accepted-path count
does not increase. Current cold localized producer/source ownership, complete
DATA/BSS/DGROUP and library/heap/file behavior, CRT/link order, canonical DIET
packaging and the complete Oracle set remain open. MAIN exactness and cached
ReC98 source association grant no inherited MAINL acceptance.

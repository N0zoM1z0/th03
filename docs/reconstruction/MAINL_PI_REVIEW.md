# Complete MAINL PI wrapper chain candidate review

This historical shifted-cache review is supplemented by
[the complete shared/ending PI review](SHARED_PI_REVIEW.md). Current independent
OP/MAINL bindings and four maintained CPP carriers pass two cold rounds and
original raw/ordered/MAP/OMF gates. Five existing MAINL rows gain source presence
without extra interval credit. The old shifted-cache failures and unowned
neighbor0529 remain historical; no old receipt or operand is normalized. Native
graphics/heap/decoder/device/asset and full product/exact gates remain open.

Four complete candidate TUs contain five functions, 555 decoded CODE bytes /
197 instructions. Their complete bodies agree with both caches at separately
reviewed entry coordinates. Palette/ordinary/interlace entries are displaced
by one byte; complete fixed-coordinate raw contributions and relocations still
fail there. Loading and quarter contributions match raw bytes and original
ordered relocations. No cold build, maintained MAINL source or exact acceptance
is added.

```sh
python3 scripts/review_th03_mainl_pi.py --output .analysis/NEW_PI_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_pi_review.py -v
```

Receipt: `.analysis/sol-mainl-pi-review-20261006.json`. Canonical stored lineage,
decoded/cached images and previous findings are hash-guarded through the prior
CDG loading receipt. Nineteen consulted frozen providers bind to both caches.
Assembly differs only by LF-to-CRLF conversion. The loading carrier is an
explicit exception: cached `th03/pi_load.cpp` includes maintained
`src/main/formats/pi_load.cpp`, with its maintained header. Both current local
providers match both caches. The unused frozen implementation is candidate
material, not that object's actual producer. MAIN exactness is not inherited.

Ghidra headless-usage fails before DB attestation; no DB observation is used.
Wine execution blocks current cold verification. Stored offsets remain unknown
for these decoded CODE entries, and pristine-dump attestation remains unknown.

| Function | Original 0C7E | Cached 0C7E | Bytes / instructions | Far return |
| --- | --- | --- | ---: | --- |
| Palette apply | 052A | 0529 | 37 / 15 | RET 2 |
| Ordinary put | 054F | 054E | 136 / 48 | RET 6 |
| Interlace put | 05D7 | 05D6 | 135 / 47 | RET 6 |
| Load | 0CCB | 0CCB | 70 / 28 | RET 6 |
| Quarter put | 0D11 | 0D11 | 177 / 59 | RET 8 |

All branches stay within complete instruction boundaries. The containing
173/135-byte cached contributions differ by 168/132 bytes at fixed coordinates;
their three/one original relocation sites also differ. Complete bodies match
only at their separately established coordinates. Original offset 0529 is 90, while
cached offset 065D is 00; these neighboring bytes remain unowned. No target-byte array,
alignment insertion or padding repair is authored. The 70/177-byte loading/
quarter contributions have equal two/one original relocation sites.

## Native execution and explicit interfaces

All five caller bodies execute, along with the actual GRAPH_PI_FREE body
at 0000:0FEC (76 bytes / 33 instructions) and actual CRT memcpy at 0000:4B7D
(36 bytes / 20 instructions). Both helper bodies match both caches. The adjacent GRAPH_PI_LOAD_PACK
error tail beginning at 1038 is outside the reviewed free helper. CRT source
ownership and complete graph/heap library ownership remain open.

The four substituted far interfaces are palette_show (RET 0), clipped packed
put (RET 10), graph_pi_load_pack (RET 12), and hmem_free (RET 2). No PI asset is
read, decoded, rendered or committed. Packed requests record their arguments,
without a physical clipping/page/pixel model. Load results and optional pointer
replacement are explicit library fixtures, not claims about actual decoder
failure paths. HMEM_FREE preserves BX/CX/ES/DS in the interface model: the
consulted complete frozen function and its shared error return preserve those
registers, and native GRAPH_PI_FREE relies on CX=0/BX/ES after those calls.
Actual heap mutation and error flags remain unexecuted.

The full 65536-byte DGROUP state is checked against an independent specification,
along with every ordered request and actual helper-entry trace. Each image
retains its own initial DGROUP bytes, with separate before/after hashes; these
are not whole initial-DGROUP equality. Eight synthetic controls reject incorrect
boundaries/cleanups, missing PUSH-CS/far frames, unknown/indirect interfaces,
operand/neighbor branches, physical segment aliases, outside-memory writes,
escaped interrupts, stale terminal state, extra unclassified changed bytes
and unequal complete image lengths.

Per image, 92 base contracts run in both DF states (184 terminal records),
with 50 additional repeat-load calls, plus two 2000-instruction budget records.
Across three images: 708 top-level invocations, 702 returns and six budgets.
All normalized observations agree. Native returns preserve BP/SI/DI/DS under
the declared interface contracts. Native memcpy executes CLD, so palette
application returns DF clear; the other callers retain incoming DF.

## Pointer, geometry and metadata behavior

Pointers normalize as: add to the low offset word with wrap, add its upper 12
bits to the segment word with wrap, then retain only its lower 4 offset bits.
The carry from the initial offset addition is lost. Ordinary and interlace
put pass the initial pointer unchanged on the first request, normalizing only
after advancing a row. Quarter put normalizes before its first request.
Constructed offset FFFE / segment 5000 cases preserve this 64K discontinuity;
segment FFFF fixtures retain segment arithmetic wrap without asserting physical
A20 behavior or dereferencing the packed source.

Ordinary stride is unsigned xsize/2, truncating odd widths. Interlace stride
is full xsize, not twice the truncated ordinary stride: for odd width 3, the
steps are 1 versus 3. Interlace advances its source counter by 2 but destination
top by 1, producing consecutive output rows. Width/height are reread from the
header: a model changing 640/20 to 3/3 during the first draw changes that same
iteration's source advance, subsequent length and loop termination. The initial
buffer pointer stays captured. These mutations are explicit caller/library
fixtures, not real library side effects.

Both ordinary/interlace height comparisons are unsigned. Zero height makes no
draw request. With unchanged height FFFF, ordinary eventually reaches counter FFFF;
interlace's word counter visits only even values. Its ADD 2 and unsigned
comparison imply a cycle from FFFE to 0 that cannot reach FFFF; this is an
arithmetic inference under the fixed-header condition. The 2000-instruction observations stop after 64 ordinary/66 interlace
requests without returning; every observed prefix is checked. The ordinary
budget is not evidence of an infinite loop. No physical draw outcome follows.

Top advances as a word, followed by a signed comparison and at most one 400-line
subtraction. Starting at 800 requests 800 then 401 then 2; starting at 7FFF wraps to 8000,
so the signed comparison suppresses correction. Negative/unclipped coordinates
and raw length FFFF are retained as interface words rather than repaired or
claimed valid for the downstream clipping implementation.

Quarter selection recognizes only 1/2/3, adding 160/64000/64160 bytes; -1/0/4/255
all use the initial quarter. Each call requests 320 pixels for 200 rows with a
320-byte packed stride, regardless of header dimensions (fixtures include
width 1 / height 0). No quarter, resource-size or coordinate validation occurs here.

PI headers have 72-byte stride, buffers have 4-byte stride and six declared slots.
Addressing truncates slot multiplication/addition to words without checking
the table. Slot 6 header aliases the following hflip lookup table, and its
buffer pointer aliases the first PI header. FFFF selects header 1EDE / buffer 1F0A.
Fixtures supply those bytes explicitly; shipped-game reachability is unproved.

## Loading, freeing and palette state

Load always invokes the real free body before requesting decode, and returns
the model's AX unchanged for 0/1/7FFF/8000/FFFF, independently of its CF.
GRAPH_PI_FREE checks comment, machine-info and image segment words, ignoring
their offset words for deciding whether to free. Nonzero comment/machine
segments issue ordered frees and zero all three corresponding metadata words,
even under failure-status fixtures. A zero segment with nonzero offset is
skipped, retaining its metadata. Equal segments issue repeated free requests;
no actual allocator double-free outcome is proved.

The image pointer in pi_buffers is not cleared by native free. Repeat loading
therefore requests another image free under the explicit unchanged-buffer
load model, while comment/machine fields already zeroed are skipped. A model
replacing the pointer changes the next image-free segment. This proves caller
behavior conditional on declared model outputs, not actual decoder-failure
semantics. No result check or metadata validation is invented.

Palette application copies exactly 48 bytes from header+24 to Palettes at 141E
using actual memcpy, then requests palette_show. The full copy/stores and
DGROUP result are checked; tone processing, DAC ports and displayed colors
remain behind the palette interface.

## Complete cached raw-failure classification and acceptance

Both 63276-byte program images differ from decoded MAINL at 340 byte positions.
The replay accounts for all of them without normalization:

| Scope | Changed bytes |
| --- | ---: |
| Shifted PI region | 300 |
| Root PI call operands | 10 |
| Cutscene PI call operands | 3 |
| Registration PI call operands | 6 |
| Previously reviewed snow/transition native encodings | 20 |
| Unowned DGROUP0849 | 1 |

The earlier bounded receipts remain the evidence for those other scopes.
This classification preserves every raw failure and rejects an extra changed
byte; it does not establish ownership or semantic review of all equal bytes.
Remaining sound/input/delay/text/CRT/library CODE, DATA/BSS/resources and the
complete intake still require review. Five decoded boundary rows grant no
authored MAINL source, accepted-intake path or exact credit. Cold localized
producer/layout/complete relocations, canonical DIET packing, complete ownership
and the full Oracle set stay open.

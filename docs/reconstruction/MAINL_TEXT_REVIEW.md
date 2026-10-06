# Complete MAINL graph_putsa_fx candidate review

This historical cached/interface review is supplemented by the later
[shared text review](SHARED_TEXT_REVIEW.md): independent OP/MAINL bindings,
localized CPP/glyph macros and two fresh cold producer/native replays. The
existing613-byte MAINL row gains source presence without duplicate interval
credit; complete product/exact gates remain open. The scope below is historical.

The complete `th03/grppsafx.cpp` contribution is one613-byte /226-instruction
far Pascal function at decoded0C7E:09B7..0C1B, with RET10. All raw bytes and
three original ordered relocation sites match both cached products. Native
GRCG setup41bytes /21instructions and off5 /3 also execute. No maintained
MAINL source, canonical packed-file offset, cold build or exact credit is added.

```sh
python3 scripts/review_th03_mainl_text.py --output .analysis/NEW_TEXT_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_text_review.py -v
```

Receipt: `.analysis/sol-mainl-text-review-20261006.json`. It guards the previous
sound receipt and canonical/decoded/cached lineage. Sixteen consulted frozen
providers bind to both source trees. The actual carrier includes frozen
TH02 hardware code, which includes TH01 glyph macros; there is no maintained
MAIN producer remap. Assembly/include line endings are compared with explicit
LF/CRLF conversion. Three pinned TC4 headers supply the actual classifier
macros and conversion declaration; proprietary header bytes stay private.
The Ghidra headless-usage check fails before DB attestation; no new database
observations are used. No TH01/TH02/MAIN exactness is inherited.

The complete CFG has internal branches at instruction boundaries and three
far calls: native GRCG_SETCOLOR0000:0C36, native GRCG_OFF0000:0C60, and
CRT conversion0000:924C. The latter is the only substituted function. Its
cdecl word argument remains on the caller stack for the real POP CX at0A3B.
The text entry receives the far string, effect, top and left in reverse
Pascal word order, cleans all10 argument bytes, and preserves BP/SI/DI/DS
and incoming DF under these interfaces. ES and scratch registers are clobbered.
GRCG's two adjacent NOPs are outside the46 contextual body bytes; no producer
padding is credited. No x87 instruction occurs in these bodies.

## Native execution and model limits

The entire text function and both real GRCG bodies execute, including far
returns, character-table tests, signed divides, glyph-local arrays, boldness,
port accesses and flat byte stores. CG-ROM bytes are deterministic synthetic
fixtures, not NEC fonts or assets. CRT Shift-JIS-to-JIS returns are explicit
fixtures, including invalid/boundary values; neither the real converter body
nor a whole codec is proved. No read-memory hook is used. GRCG register writes
execute but physical RMW, page selection, colors and pixels are not emulated.
CPU flat writes and port transcripts are the verified results.

A separate source-level scalar model checks every byte in a65536-byte flat
A800:0000..FFFF fixture and every ordered byte-store/port transcript for terminal
cases. Every DGROUP byte remains unchanged. Each image's own before/after
hashes stay distinct; normalized cross-image observations omit only those
hashes because unrelated DGROUP0849 differs. Both256-byte multibyte classifier
and the256-byte signed graph lookup window match across images. These are
unowned CRT DATA diagnostics, not localized generated data acceptance.

Each image has660 top-level invocations:658 returns and two10000-instruction
budgets. Across original/two caches:1980 calls /1974 returns /6 budgets.
Each image records35142 port events,26720 byte stores and268 converter
invocations, including partial budgets. Cases include all255 nonzero input
bytes, four weights /eight alignments /both DF states for half/full glyphs,
all16 colors, eight spacings, mixed strings, JIS classification endpoints,
clipping boundaries, extreme signed coordinates and string/VRAM offset wrap.
Eight adversarial tests reject incomplete/wrong returns, operand/neighbor
branches, unknown interfaces/interrupts/ports, bad helper cleanup, converter
frames and segment aliases, DGROUP/wide-plane writes, and stale terminal state.
Callback errors are raised outside the native FFI boundary.

## Character classification and string pointers

A lead byte is tested first through the actual multibyte table's mask04;
it consumes two bytes and forwards their word to the modeled converter.
The second byte is not checked for NUL or validity. A lead followed by NUL
therefore consumes that terminator, and drawing continues from the following
byte. Returned codepoint0 still writes A1=00 and A3=E0 and enters the fullwidth
path. The upstream claim about a particular visible fallback glyph is not
proved by synthetic font bytes.

Kana is tested next with mask3 and maps to byte+2980; graph characters map to
byte+2900; other bytes map to2B21. The lead/kana tables index unsigned bytes,
while isgraph uses a signed `char`. High bytes that fail the first two tests
therefore read below the ordinary graph-table base at DGROUP0F05. TC4's macro
accepts the signed argument without conversion; source-level valid-domain
semantics are not assumed for negative values. The replay checks actual pinned
lookup bytes and resulting native branches, not universal locale behavior.

All pointer increments update only the low word. A source at offsetFFFF can
read its second byte at0000 and continue after a two-byte increment at0001,
without advancing the segment. Fixtures specifically cross that boundary.
Parameter-copy offset changes are checked at the actual caller stack location.
No string length or lead-trail validation is introduced into product code.

## Clipping and signed coordinate arithmetic

The base offset is word-wrapped top*80 plus signed left/8, truncating division
toward zero. First-bit is the signed remainder, not a nonnegative bit mask.
Negative left values are not rejected. Their negative remainders reach CL;
the x86 shift-count mask and16-/8-bit operand widths determine resulting bytes.
For example left-1 divides to0, remainder-1; the three stores use shifts7,31,9.
This differs from arithmetic-right-shift floor positioning and remains intact.

Codepoint2921..2B7E inclusive is halfwidth. It admits signed left<=632; all
other codepoints admit left<=624. Both limits include equality. There is no
left or top/bottom clipping. Character consumption and A1/A3 selection occur
before the right-edge test, so a clipped glyph has already advanced the string
and emitted its codepoint without reading rows or writing VRAM. Cleanup still
switches CG access back and disables GRCG.

Each glyph writes16 rows and advances its far offset by80 using only the low
word. Neither the visible32000-byte plane limit nor a64K offset crossing rolls
or normalizes its segment. Negative top and top399/400/819/820/32767 fixtures
cover these boundaries. Only flat addresses are proved, not corresponding
physical page/plane consequences. An unterminated string beginning at signed
left-32768 remains mid-draw under the recorded budgets. The source still has a
right-edge break; no universal infinite-loop claim follows from those budgets.

## Glyph rows, weights and spacing

Halfwidth reads sixteen A9 high bytes selected by A5=row|20 and stores a zero
low half. Fullwidth adds a second A9 read selected by A5=row. Only after all
rows are fetched does the native draw loop apply weight and write them.
Weight0 retains the row; heavy ORs one left shift. Bold applies that doubling
and removes selected new adjacent bits; black doubles once before the same
bold operation. Every intermediate is16bits, retaining the source's lost
left extension. No widened or corrected row is substituted.

At aligned positions the function writes two bytes; any nonzero signed
remainder produces three stores, including zero values. Those stores can cross
row/offset boundaries. A real GRCG write mask may treat zero bytes differently
from flat memory; the replay reports CPU stores without claiming final pixels.
Left advances by8 for halfwidth or16 for fullwidth, plus effect bits6..8 as
spacing0..7, with word arithmetic. Four weights and all spacings execute in
mixed and clipped strings. GRCG setup always receives modeC0 and the low four
color bits, even for an empty string; the real library programs7C and four7E
tile bytes, then text writes68=0B. Normal cleanup writes68=0A and7C=0. Existing
mode/access state is not saved and restored by this function.

One decoded boundary row grants no authored MAINL source or exact credit.
Localized cold producer/OMF, remaining CRT/libraries/DATA/BSS ownership,
physical font/GRCG/page behavior and canonical DIET packaging/full Oracles
remain open. The entire505-file review and requested actual English commits
are still unfinished.

# MAINL complete text renderer

Prepared 2026-10-26 against checkpoint `2b9fe1c`. This promotes verified
ownership of existing maintained C++, not a new source implementation.

## Complete producer and source

`src/shared/graphics/text.cpp` includes `text_glyph.inl` through the exact
`th03/grppsafx.cpp` wrapper. The real first-use producer is GAME3/BINARY O,
first_binary op, Borland C++4.02 large-model. MAINL does not invent a new L
compilation. Native grppsafx.obj has613 CODE bytes, zero DATA/BSS, one public
at0C7E:09B7 and a complete far Pascal RETF10 body:226 instructions.
There is no inline table or trailing padding in this producer.

Source lineage localizes the TH03 wrapper/TH02 renderer/TH01 glyph macros;
the maintained game routine is not a master.lib service body. Positive
specialization includes the color/effect bitfield, weight and spacing,
TH03 win-message control-character filtering and direct CG-ROM glyph drawing.
This supports game-renderer classification, not certainty about historical
legal authorship, original filename, or exact original source text.

The separate GRCG_SETCOLOR/GRCG_OFF routines, Borland SJIS converter,
ctype/mbctype tables and vendor headers are dependencies, not credited code.
The existing bounded analyzer checks46 contextual GRCG bytes without owning
them. SDK headers remain independently bound by the full current cold graph.

## Native equality and boundaries

All six explicit ordered OMF fields are independently resolved from literal
native identities: three far external services and three DGROUP classifier
plus-one references. The five EXTDEF names, both MAP tables, all records,
segment/group alignment, one LEDATA and entire613-byte result are checked.
Original ordered MZ vector contains exactly three segment words. No masking,
patching, sorting or target-derived synthesis is used.

The existing bounded shared-text analyzer checks complete instruction decode,
all branch destinations, three far call sites, classifier masks/addresses,
and far cleanup10. Its runtime harness is not run or expanded here.

## Preserved behavior

- Arguments are signed16 left/top/effect and a far unsigned-byte string.
  Effect uses color low4, weight bits4..5 and spacing bits6..8.
- Lead-byte lookup is unsigned; the isgraph path deliberately sign-extends
  char before indexing its classifier table. Far string offset increments
  wrap as a WORD without segment carry. A lead byte consumes a trailing byte
  without first checking that it is nonzero.
- Invalid SJIS conversion still emits CG access; zero converts the high
  selector through subtraction to E0. Controls become halfwidth spaces.
- Negative left and top are unchecked. Signed division/remainder,16-bit VRAM
  offset wrap and only right-edge glyph clipping remain unchanged.
- Sixteen-bit bold operations lose additional left-edge dots. Halfwidth
  glyphs occupy the high byte; unaligned rows write three bytes, aligned rows
  two. No bug fixes or clipping cleanup were introduced.
- CG dot/code mode and GRCG calls remain in their original order, even for an
  empty string. Physical font contents, emulator pixels, CRT correctness and
  hardware timing are not claimed by this source proof.

## Acceptance and verification

Prior96 complete owner observations remain identical to `2b9fe1c`.
Current totals become97 extents/102 procedures,16138 CODE+224 DATA bytes.
The live ledger has193 rows; frozen historical145 and mock numerator150
retain their original eligibility. Whole-game percentage remains unknown.

Use `.venv/bin/python scripts/review_th03_mainl_text_work.py --current-cold`.
The unchanged full938-output two-cold graph is revalidated. Existing reports
were preserved before refresh; the new report publishes atomically on success.
No native source edit/rebuild, ancestor chain or new runtime harness is needed.
Existing focused checks and final full CI are pending at writing; durable
terminal logs/exit receipts, not post-CI prose edits, establish their result.

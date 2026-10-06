# Whole MAINL cutscene candidate analysis

The complete frozen TH03 cutscene translation unit has source/control-flow/ABI
review against guarded decoded MAINL: thirteen complete bodies (3122 bytes),
72 bytes of switch tables and one observed alignment byte. The complete 3195-byte
candidate still differs at three call-address bytes. This is boundary-reviewed
candidate analysis, not maintained source or exact acceptance. Selected CPU
contracts cover loader, parameter readers, gaiji and its cursor advance;
Additional box/cursor and complete-loop CPU/model reviews are documented in
`MAINL_BOX_REVIEW.md`, `MAINL_ANIMATE_REVIEW.md` and `MAINL_PICTURE_REVIEW.md`.
Remaining opcode branches and physical graphics/input/timing remain open.

```sh
python3 scripts/review_th03_mainl_cutscene.py --output .analysis/NEW_CUTSCENE_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_cutscene_review.py -v
```

Receipt: `.analysis/sol-mainl-cutscene-review-20261006.json`. Canonical Japanese
MAINL, DIET restoration, decoded bytes, both cached images/MAPs/objects,
sixteen source-provider snapshots and scripts are checked before/after analysis.
Current Ghidra headless-usage fails; no database observation is used. Provenance
remains candidate-local-attested with independent pristine evidence unknown.

## Complete source and byte partition

Frozen revision: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
`th03/cutscene.cpp` includes the complete 1159-line
`th03/cutscene/cutscene.cpp`, which includes the 159-line script helpers and
seven-line EGC start implementation. GAME=3 branches were reviewed explicitly;
TH04/TH05 colmap, crossfade and return-key animation branches are not TH03 code.
Relevant dimensions, PI, flags and calling declarations remain scoped provider
observations, not acceptance of entire headers/dependencies.

| Decoded `095F:` offset | Body bytes | Function | Near cleanup |
| --- | ---: | --- | ---: |
| `0B3E` | 70 | cutscene_script_load | 4 |
| `0B84` | 31 | cutscene_script_free | 0 |
| `0BA3` | 52 | egc_start_copy | 0 |
| `0BD7` | 117 | pic_copy_to_other | 4 |
| `0C4C` | 303 | pic_put_both_masked | 8 |
| `0D7B` | 209 | box_bg_allocate_and_snap | 0 |
| `0E4C` | 31 | box_bg_free | 0 |
| `0E6B` | 175 | box_bg_put | 0 |
| `0F1A` | 201 | script_param_read_number_first | 4 |
| `0FE3` | 41 | script_param_read_number_second | 4 |
| `100C` | 81 | cursor_advance_and_animate | 0 |
| `105D` | 1496 | script_op | 2 |
| `167E` | 315 | cutscene_animate | 0 |

The bodies contain 1057 instructions. Every direct branch remains on a body-local
instruction boundary; near calls reach the thirteen complete entries. Foreign
far-call coordinates are tracked separately from ownership. `script_op` has
exactly two recognized indirect dispatches: a four-entry weight table at `1636`
and a sixteen-entry opcode table (keys `163E`, destinations `165E`). Every table
destination reaches owned instructions. Byte `1635=00` precedes the word-aligned
tables. Neither the tables nor the alignment byte are mis-disassembled as code;
their cached compiler association is provisional producer evidence, not a
manufactured exact source array or independent ownership Oracle.

Both cached C++/header snapshots have byte identity with the consulted frozen
providers; the one assembly provider differs only by LF-to-CRLF conversion.
Both valid TC86 Borland C++ 4.02 objects match after dependency-timestamp
normalization. These are old input/output associations, not fresh compiler
attestation. The MAP places the whole TU at `095F:0B3E`, size `0C7B`, and its
56 original ordered relocation words match both rounds. Canonical stored-file
offsets remain absent; packing/stub and complete product ownership remain open.

## Three raw failures and direct PI helpers

The only root differences are operand bytes at `140A/1414/144B`. Target calls
PI palette at `0C7E:052A` and PI put at `0C7E:054F`; cached public entries are
`0529/054E`. Target entries are established by actual direct callers, not an
equality-maximizing alignment search. The complete 37-byte palette and 136-byte
put bodies equal their corresponding cached bodies at those distinct entries
and end at far RET 2/6. Both implementations in the 27-line
`th02/formats/pi_put.cpp` were reviewed through the TH03 carrier.

Target `0529` is NOP before the palette prologue; target `054E` is the final
operand byte of the preceding return, **not** another NOP. The body equality
does not close the natural producer/linker boundary that moves the symbols.
Root call operands are retained verbatim and raw equality remains false. No
padding, target-byte array, alias normalization or callee exactness is added.
These helper observations receive no separate authored or exact byte credit.

## TH03 interpreter, pictures and text box

The box is x=80..559, y=320..383. Backup allocates `3C00h` bytes and interleaves
four plane words per 16-pixel cell across 64 rows/30 cells; allocate/snap frees
the previous buffer first, selects page 0 and never checks allocation success.
Restore copies the buffer back; free clears the far pointer after the external
free call without checking its result. Cursor advances 16 pixels, wraps at
x=560 to x=144/y+16, and at y=384 optionally waits then resets to x=80/y=320
and restores both pages. The separate box CPU review executes these routines
with flat plane/interface models; physical page banks and complete
memory-allocation behavior remain unproved.

Picture copy loops over 320x200 pixels as twenty word copies per row, switching
access pages 0/1 for every word under EGC. Masked picture drawing stages each
packed row at y=400, configures the EGC mask for row modulo four, copies twenty
words, advances/normalizes the far packed-data pointer, then copies the result
to the other page. Quarter offsets are 0/A0/FA00/FAA0; word offset addition
precedes normalization. EGC/bus, banks, assets, clipping and tearing remain
unverified. The separate picture CPU review executes these loops and actual
packed conversion while logging ports and modeling far-return transitions;
no flat-memory substitute is claimed to reproduce these devices.

The interpreter initializes cursor, interval 1, white color and bold effect,
snaps the box and senses input on every iteration. CANCEL sets fast_forward;
other nonzero input uses interval/3, delaying only odd byte cycles when that
division yields zero. Ordinary text consumes two bytes without validating
Shift-JIS and renders to both pages. Controls/space are skipped; backslash selects
a command. A NUL byte is skipped as control, not treated as end-of-file. STOP
requires the explicit `$` command. Selected complete-loop execution is covered
by the separate interpreter CPU/model review; all-command/device execution
remains open.

| Opcode | Reviewed GAME=3 source/decoded behavior |
| --- | --- |
| `$` | Return STOP in AL; no implicit buffer-length check |
| `n` | Newline; full box falls through to box change |
| `s` | Optional wait (or `-`), reset cursor and restore both pages |
| `c` | Parse default 15, truncate color to a byte |
| `b` | Parse default 2; only weights 0..3 change the effect byte |
| `w` | White fade in/out, frame/key wait, or measure/key-or-measure wait; defaults 1/64 |
| `v` | Text interval default 1, or `vp` show-page selection |
| `t` | Tone default 100; optional one-frame wait before palette show |
| `f` | Black fade in/out; `fm` adds an unchecked word parameter to `0200h` |
| `g` | Inclusive shake loop with optional delays, or `ga` dual-page gaiji and cursor advance |
| `k` | Parse parameter but pass zero to input_wait_for_change in TH03 |
| `@` | Clear both pages without refreshing the saved text-box background |
| `p` | Load filename, palette/whole-picture/copy, palette-only or free; GAME=3 load does not pre-free |
| `=` | Immediate quarter/blank, or four masked crossfade steps; temporary show-page changes preserved |
| `m` | Stop/play/load music; filename truncates at twelve characters |
| `e` | Forced sound effect; missing parameter uses the existing shared default |

Command letter lowercasing is distinct from subcommand handling. The font, PI,
palette, audio, key waits and timing helpers are foreign code; their complete
Oracles cannot be inferred from this candidate review.

## Selected CPU observations and the incorrect CF comment

Each image runs 36 standalone parameter cases, twelve gaiji commands with twelve
companion parameter probes, and five loader cases: 195 calls across target and
two cached images. Actual root instructions and the real 24-byte gaiji prefix
`0000:0F58–0F6F` execute. File interfaces and ASCII tolower are models; after
gaiji's real ADC/AND prefix, its hardware suffix/return is substituted. Actual
rendered glyphs, suffix flags/device effects and game-runtime behavior are open.

Number-first always reads three bytes before classifying them, then rewinds
unconsumed bytes. Number-second consumes comma when present, otherwise returns
the shared default without three-byte reads. Far script advancement changes
only its 16-bit offset, including FFFD/FFFE/FFFF wrap; the segment does not advance.
The far reference argument consumes four stack bytes. All observed BP/SI/DI
and near Pascal/cdecl cleanup contracts pass.

At ordinary offset, the default/one-digit paths return CF=0 because their pointer
SUB replaces arithmetic carry; two/three digits retain CF=1 (DEC does not change
it). Near offset wrap, pointer subtraction can set CF even on default/one-digit
paths. The frozen gaiji comment claiming that digit conversion always sets CF
is therefore false. The caller passes `p1-1` on page 1 and `p1` on page 0.
With a normal one-digit `ga1`, the real prefixes compute JIS words 5600/5601;
with two-digit `ga12`, both compute 560C. The AND after ADC clears CF before the
modeled suffix. This establishes prefix/caller behavior, not final pixel output
or a valid-caller assertion for the constructed wrapping offsets.

Loader cases confirm old script free/reset before open, true/error return on
modeled open failure, word-size truncation (constructed DX:AX=1:3 allocates/reads
three bytes), zero-byte read results ignored, and allocation segment zero still
issuing a NULL read request and returning false/success. The file-read model
records that request without writing low memory. Actual file/library/kernel
failure semantics remain separate.

Ten synthetic controls cover complete code/table partition, cleanup/truncation,
table targets/keys/alignment, direct/indirect edges, unknown calls and callback
failures caught outside Unicorn's FFI boundary. The whole interpreter/graphics,
remaining dependencies/data/BSS/assets, source localization, natural PI producer,
cold maintained build and stored packing/complete Oracles remain unfinished.

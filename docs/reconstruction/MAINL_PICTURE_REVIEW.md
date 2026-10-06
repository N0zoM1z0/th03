# MAINL picture and packed-pixel CPU diagnostics

The actual cutscene EGC setup, 320x200 copy and masked picture bodies execute
with the actual library EGC and packed-pixel operations. Seventy-two top-level
calls across guarded decoded target and both cached images agree. The complete
packed-pixel conversion is checked against an independent scalar pixel-bit
specification. EGC logic, page banks and device timing remain unmodeled; this
is diagnostic evidence, not physical picture, maintained-source or exact
acceptance. No code/data byte credit or new unit is added.

```sh
python3 scripts/review_th03_mainl_picture.py --output .analysis/NEW_PICTURE_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_picture_review.py -v
```

Receipt: `.analysis/sol-mainl-picture-review-20261006.json`. The complete
cutscene receipt is SHA-256 pinned and all inherited inputs are checked
before/after execution, including canonical Japanese MAINL identity. Seven
consulted frozen providers match both cached trees: C++/headers byte-identical,
assembly LF-to-CRLF only. Frozen RotTbl literals and a separately generated
pixel-bit specification both match the target/candidate table. These cached
associations are not fresh compiler or independent ownership Oracles. Current
Ghidra headless-usage fails; no database observations are used.

## Bodies, tables and actual operations

The previous complete cutscene analysis owns the diagnostic boundaries at
095F:0BA3/0BD7/0C4C (52/117/303 bytes). Its actual foreign callers establish
EGC_ON at 0000:0724, EGC_OFF at 073A and GRAPH_PACK_PUT_8_NOCLIP at 2C6E.
The complete source/control-flow/ABI review includes the consulted EGC,
packed-pixel, rotation-table and initial clipping declarations.

| Inner CS=0000 region | Bytes | Boundary/meaning |
| --- | ---: | --- |
| 0724..0738 | 21 | Complete EGC_ON, far RET 0 |
| 073A..0758 | 31 | Complete EGC_OFF, far RET 0 |
| 075A..0784 | 43 | EGC_START/EGC_END public alias, far RET 0 |
| 2C68..2C6D | 6 | Packed helper's shared early-return tail, far RET 10 |
| 2C6E..2D31 | 196 | Complete packed helper body, far RET 10 |
| 1AAA..1EA9 | 1024 | 256 four-byte rotation-table entries; not code |

The complete EGC provider contribution spans 98 bytes: three bodies totaling
95 bytes and observed EVEN NOPs at 0739/0759/0785. Both MAPs associate START
and END with 075A; source defines two public aliases for the same body.
Packed body includes its own observed EVEN NOP at 2CB5. Direct packed branches
remain on owned instruction boundaries or the complete shared tail, excluding
the preceding unrelated body. All helper bodies/table have raw identity
across the three images and no original MZ segment-relocation sites. OMF/whole
library ownership, alignment producer acceptance and stored-file offsets stay
open. No target-byte array, padding or alias normalization is authored.

The table maps each high/low packed-pixel nibble into four plane bits. Actual
SHL/OR table operations read four bytes per eight pixels and write B/R/G/E
bytes. Every input address and output byte/address is checked against the
independent nibble/pixel-bit specification. USE_TABLE=1 and USE_GRCG=0 are the
observed active source branches; alternate branches do not earn TH03 credit.
ClipYT_seg has target/candidate initial word A800 at DS:052E. Other mutable
clipping state and its runtime initialization are not proved by that word.

## Environment and return-transition limitation

Images relocate to segment 2000, CS=295F, DS=2E3F, SS=4000. A constructed
initialized blue-plane pointer at DS:1C60 points to A800:0000. Synthetic packed
bytes fill linear 50000..7FFFF; no PI assets are imported. Memory is flat:
port writes are recorded with their exact widths and values, without EGC,
GRCG or bank effects. Packed stores are actual CPU byte stores to the modeled
plane addresses. Root EGC transfers operate through the blue-plane word
window; their all-plane latch/mask behavior is not reproduced or proved.

Unicorn 1.0.2rc4 has a reproduced **memory-read-hook far-RET defect**. A purely
synthetic CALL FAR / RETF control returns correctly without the read hook and
incorrectly with it; both runs have the correct `[0005,295F]` stack frame.
With the hook, the first destination becomes 49D14 instead of 295F5. The
control stops before executing that unexpected instruction.

The probe therefore substitutes only each helper's architectural far-return
transition: verify actual CB/CA0A00 opcode, read the actual return frame,
advance SP by four plus declared cleanup, and restore CS/IP without changing
flags. Each transition is recorded. Helper arithmetic, loads/stores, CLD,
ports and saved-register pops still execute; their RETF instructions do not.
This is an explicit ISA transition model, not a silently accepted engine
result or hardware/ABI Oracle. Near root returns execute normally. Unknown
bodies/ports, interrupts, aliases, budgets and callback errors are rejected;
all terminal DS/BP/SI/DI and stack contracts are checked.

## Copy and masked-loop observations

Four direct copy cases per image cover (160,64), (0,0), constructed (-1,-1),
and (638,399). Each has exactly 4000 word read/write pairs: twenty words per
row, 200 rows, stride 80, signed left>>3 and word-offset wrap. Access page
requests alternate A6=0 before read and A6=1 before write on every word.
Real EGC_ON/setup/OFF operations execute; exit requests A6=0. There is no
root clipping or source/destination segment normalization. Invalid coordinates
are arithmetic controls, not proof of valid callers or physical bus behavior.

Nine masked cases per image cover quarters 0..3 with masks 0..3, an initial
FF80 offset with quarter 2, quarters -1/4, and masks -1/4. Each calls the
actual packed helper 200 times with x=0, y=400, len=320 (160 source bytes).
It writes exact EGC configuration/mask values, copies twenty words from the
staging row per row, advances the packed row by 320 bytes, then copies the
whole picture through the actual 320x200 root. Show-page requests go 1 then 0;
all access/word/port sequences are checked. No expected masked pixels are
asserted against flat memory, because that would manufacture a device result.

Quarter offsets are 0/A0/FA00/FAA0, added to the word offset **before**
normalization. Constructed initial 5000:FF80 plus quarter 2 becomes 5F98:0000,
one 64-KiB unit below a carry-preserving linear addition. Quarters -1/4 fall
through to quarter-zero data. Row advancement normalizes the local pointer;
the original pi_buffers[0] far pointer is preserved. Actual allocation/caller
constraints remain separate; no wrap is silently repaired.

Mask indexing uses the unchecked word expression `8*mask_id + 2*(row&3)`.
Mask -1 reads neighboring `over.pi` string words (766F/7265/702E/0069).
Mask 4 reads 2020/0000/0982/2E3F, including adjacent glyph/pointer data after
the relocated load. Those actual words are issued to port 4A8. Normal mask
table values match both candidates. No valid-caller assertion or resulting
hardware pixel claim follows from these deliberately invalid indexes.

## Packed-helper clipping and DF

Nine direct packed cases per image cover normal staging, left/right clipping,
fully clipped and nonpositive lengths, y=-1, and a source at 5000:FFFE.
For constructed left=-8, len=16, the helper emits one eight-pixel group but
reads from pointer-4 (0100 becomes 00FC), preserving the source's negative
offset adjustment. It does not read pointer+4. Source offset FFFE wraps
within segment 5000 as SI increments; it is not a huge pointer.

Normal drawing performs CLD. Early clipping returns before CLD and preserves
constructed inherited DF. There is no Y clipping in this helper: y=400 and
y=-1 produce their actual word offsets. Right clipping limits the result to
the 80-byte row width. The scalar check covers actual conversion output at
the modeled addresses, including constructed invalid positions, not screen
clipping or hardware alias effects.

Per image: four copies, nine masked pictures, nine direct packed calls, one
root EGC setup and one library START/END call = 24, seventy-two across three
images. Eight synthetic controls protect cleanup, shared-tail ownership,
table/clipping/EVEN bytes, callback failures, budget/sentinel handling,
far-return opcode and the engine-defect diagnosis. Remaining complete command
paths, PI loading/assets, physical EGC/GRCG/pages/tearing, full library/layout
ownership, cold maintained build and packed-file Oracles remain open. The
cutscene root still retains its three raw PI call-operand failures.

# MAINL registration and score-data candidate review

The complete frozen registration and score-data CODE contributions have bounded
source/control-flow/ABI analysis: fourteen registration functions (2720 bytes)
and three score-data functions (229 bytes). All seventeen bodies execute in
selected CPU/interface cases. Registration retains six raw PI call-operand
differences; score-data has cached raw equality. Neither receives maintained
source or exact acceptance. Canonical stored MAINL remains the pinned Japanese
DIET image; the coordinates below belong only to its guarded decoded lineage.

```sh
python3 scripts/review_th03_mainl_regist.py --output .analysis/NEW_REGIST_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_regist_review.py -v
```

Receipt: `.analysis/sol-mainl-regist-review-20261006.json`. The complete cutscene
receipt is SHA-256 pinned and inherited inputs, canonical identity, both cached
images/MAPs, consulted cached providers and objects are checked before/after.
Twenty-six frozen providers match both cached trees: assembly LF-to-CRLF only,
other files byte-identical. The roots are `th03/regist.cpp` including
`th03/hiscore/regist.cpp`, and `th03/scoredat.cpp` including
`th03/formats/scoredat.cpp`. The former also includes score load/save helpers.
Complete root source, relevant declarations, score encoding, glyph definitions,
resident/input ABI and generated data declarations were read. Whole foreign
libraries, assets, generated-root ownership and product graph remain open.

## Complete boundaries and cached compiler diagnostics

| Decoded CS=095F entry | Bytes | Function | Near RET cleanup |
| --- | ---: | --- | ---: |
| 17B9 | 60 | Decode section | 0 |
| 17F5 | 127 | Recreate file | 0 |
| 1874 | 42 | Checksum invalid | 0 |
| 189E | 98 | Load and decode | 2 |
| 1900 | 188 | Encode and save | 2 |
| 19BC | 145 | Load initial images and sprites | 0 |
| 1A4D | 330 | Insert resident score | 0 |
| 1B97 | 56 | Initial alphabet | 0 |
| 1BCF | 55 | Alphabet selection | 4 |
| 1C06 | 183 | Restore background under glyph | 4 |
| 1CBD | 66 | Render registration glyph | 8 |
| 1CFF | 314 | Render score row at coordinates | 6 |
| 1E39 | 39 | Restore/render rows | 0 |
| 1E60 | 27 | Render entered row | 2 |
| 1E7B | 739 | Name entry loop | 0 |
| 215E | 132 | Replace identical letters with character default | 0 |
| 21E2 | 348 | Registration menu | 0 |

The two adjacent complete contributions end at 233E, without CODE gaps/tables
or invented padding. Full Capstone coverage verifies every direct branch stays
on an instruction boundary inside its body, near calls use one of these entry
points, and far calls use declared interfaces. No automatic Ghidra function or
decompiler output is used: current headless-usage fails before DB attestation.

Both MAPs associate REGIST_TEXT with 095F:189E/2720 and SCOREDAT_TEXT with
095F:17B9/229. Valid root OMFs identify TC86 Borland C++ 4.02; two-round object
hashes agree after dependency timestamp normalization. This is old cached
compiler evidence, not a current cold build. Both roots have zero separately
attributed DATA/BSS contributions; their globals reside in the generated root
and remain unowned for acceptance.

All 54 ordered registration MZ segment-relocation sites agree; score-data has
none. Raw registration comparison fails at 19E2/19EC, 22D8/22E2 and 230F/2319:
three PI palette/put pairs target C7E:052A/054F versus cached 0529/054E. The
earlier cutscene review proves shifted helper-body equality, while the entry
producer stays open. All six differences remain failures, without address
normalization, aliases in product source or forged byte equality. The 229-byte
score-data raw match does not prove ownership, cold layout or complete Oracles.

## Layout and CPU/interface scope

Constructed load segment 2000 gives CS=295F, DS=2E3F and SS=4000. Root/dependency
instructions, loops, near calls/returns, arithmetic, stores and port writes
execute. Foreign file, RNG, structure-copy, input, sprite/font, PI/CDG, sound,
palette and timing interfaces substitute explicit behavior and far-return
transitions. Source calls establish argument order/width and Pascal cleanup;
`snd_load` and volume wait use caller cleanup. The structure-copy interface
requires CX=8 and copies exactly eight bytes. Four initialized B/R/G/E pointers
address flat 32-KiB planes; ports A4/A6 log page requests without actual banking.
Glyph background restoration executes actual DWORD copies for all four planes,
but foreign rendering produces no pixels. Interrupts, unknown calls/ports,
callback failures, wrong near cleanup and unexpected budget exits fail closed.
This does not prove actual DOS I/O, drivers, graphics or physical ABI.

| Section-relative bytes | Meaning |
| --- | --- |
| 0..1 | 16-bit sum of bytes 2..205 |
| 2..81 | Ten backwards eight-byte names |
| 82, 83 | Cleared flag and unknown random byte |
| 84..183 | Ten ten-byte scores: continue byte, eight digits, reserved byte |
| 184..193 | Optional character IDs |
| 194..203 | Stage glyph IDs |
| 204, 205 | Plaintext key bytes |

Observed section size is 206, with the 204-byte score payload at DS:21F0 and
section base 21EE. The entered-place word at 22BC follows the section. Enum and
resident fields use observed byte/word widths, including packed character at
resident+0C, rank+0B, stage+33, credits+36 and eight score digits at +18. Layout
is candidate/source/target corroboration, without a new compiler layout Oracle.
Generated default-name declarations contain nine eight-byte names, including
the literal ELEN spelling; the helper writes them backwards. Generated rank
filename and initial input-hold storage are mutable and zero-initialized,
respectively. No copied target byte array is added to product source.

## Observed contracts and retained hazards

Forty-three insertion cases per image check strict high-to-low comparison of
eight digits, all ten places, ties and nonqualification. Continue/reserved bytes
do not break ties. Lower rows shift all name/score/stage/character fields.
Insertion fills spaces, keeps the selected row's reserved tenth score byte,
stores continue as byte `35-credits`, and maps stage 99 to ALL=48. Constructed
digit 255 compares as widened 287 but stores byte 31 after adding 32. Invalid
credits/stages and packed character 0 demonstrate width behavior, without
claiming reachable normal gameplay.

Twenty-one default-name cases cover spaces, repeated D and distinct letters,
with packed characters 0/1/2/3/18/19/255. Any identical eight-letter name becomes
the character default. Character arithmetic truncates signed `(packed-1)/2`
toward zero; unchecked invalid IDs read adjacent data, rather than validated
defaults. Those constructed reads are recorded and agree in all three images.

Five terminal name loops check eight A selections, held Enter locking, held
Right repetition, bomb backspace and END. Direction acts on the first held
frame and again at frames 32/36; Enter requires release before another selection.
Eight ordinary selections finish after fifteen input/frame calls. On the
eighth, the actual unsigned byte cursor decrements 0 to 255 and sets done,
but the current iteration still rerenders: the constructed place-zero call
writes space=14 at DS:22EF, outside the 206-byte section. It also requests a
preview at left=-5880 and executes background copying at the corresponding
wrapped word offset. END retains cursor 7 and does not make this outside write.
A held-Enter budget case remains in the loop after one selection; it is an
explicit nonterminal observation, not a successful menu exit.

Two initial-loader calls with rank 2 request `rft2.cdg` then `rft4.cdg`: the
source adds rank to the mutable filename character on every call. Actual caller
frequency and valid lifecycle remain unproved; the model records rather than
repairs the accumulated value.

Sixteen crypto vectors per image cover four random-word triplets and rank words
0/3/FFFF/319. Actual encode agrees byte-for-byte with an independent backwards
feedback specification: keys remain plaintext, each preceding byte subtracts
key1 and feedback, then feedback is ROR3(ciphertext) XOR key2. Decode roundtrips
all bytes, and checksum tests reject a single changed checksum byte. Random
words truncate to byte key1/key2/unknown. Save uses a 16-bit multiplication of
rank by 206 before zero-extending the file offset, so rank FFFF seeks 65330 and
319 seeks 178. Constructed write return zero is ignored; the captured request
is still 206 bytes. Capture is a file-interface model, not a real file write.

Four load cases cover missing file, valid contents, corrupt checksum and a
failed read supplying no bytes over a preexisting valid encrypted section.
That stale section is decoded and accepted: open/seek/read results are not
checked. Missing/corrupt files recreate four rank sections despite constructed
create/append/write failures. With resident stage 99 and credits 3, recreation
sets cleared=99 for **all four ranks**, because save tests resident state
without requiring the rank being saved to equal the resident rank. Eight
additional actual decode calls verify the four captured sections in each of
the two recreation cases. Device/filesystem reachability stays open.

Four complete menus cover viewer stage 255 with credits 3/0, clear stage 99 and
ordinary stage 5. All seed the RNG from resident state, load `regib.pi` and
`rft2.cdg`, render rows, fade and save one section, including viewer mode.
Only insert paths run name input/default replacement. Viewer with credits 3
still loads `conti.pi` and `conti.cd2`; credits 0 or stage 99 loads `over.pi`,
requests fade 0210, volume wait 00FF and stop 0100. The wait argument is an
observed word 00FF, not an assumed FFFF. Ports, filenames, requests and order
are recorded; no assets, music or graphical output are claimed.

Per image: 43 insertions + 21 defaults + 5 terminal name loops + 1 budget name
loop + 2 initial loaders + 64 crypto/decode/checksum calls + 4 loads + 8
captured-section decodes + 4 menus = 152 calls, 456 across three images (453
terminal, three budget observations). Seven synthetic tests protect ownership,
cleanup, callbacks, budget/sentinel handling and the structure-copy interface.
Cold maintained source/localized dependencies, generated DATA/BSS, physical
devices, full ownership/relocations and canonical packaging/complete Oracles
remain open. The broader ReC98 intake is still incomplete.

# Current project composition (2026-11-11)

MAIN, OP and MAINL have two target-equal links composed from current source
outputs. The four-file package also repeats with a freshly assembled shared
startup. MAIN's deferred input carrier remains unchanged. MAINL's historical
aggregate ranges are explained below. [Generated progress](PROGRESS.md) supplies the current totals.

## Four-file package with source startup

`scripts/build_th03_package_current.py --stage af1386p` independently reviews
those current object pairs and ZUN's unchanged source-bound cold pair, assembles
`src/shared/crt/startup_large.asm`, and links MAIN, OP and MAINL with that fresh
startup object. Project objects and runtime libraries retain their reviewed
input bindings and original link order. ZUN reuses its current decoded output.
MAIN uses the established compact MZ serialization; the other three programs
use the pinned original DIET 1.45f `-B` command. Each is restored with `-ra` and
compared with the entire decoded input. Both DIET operations return 1 on success.

Both rounds reproduce all four canonical Japanese files byte for byte:

| Stored program | Bytes |
| --- | ---: |
| MAIN.EXE | 130,882 |
| OP.EXE | 36,041 |
| MAINL.EXE | 37,975 |
| ZUN.COM | 16,242 |

All loaded MZ bytes and the original ordered relocation vectors are checked:
1,553 for MAIN, 607 for OP and 677 for MAINL. Every complete MAP equals its
corresponding current parent. Thirteen of fourteen raw outputs repeat exactly;
MAIN's MAP retains the independently compiled `r1`/`r2` module filenames and
is checked verbatim against each parent instead of being normalized.

The freshly assembled C0 object preserves all 17 original segments, 767
initialized bytes, genuine cache holes, reserved stack and all 58 literal
ordered fixup fields. All 32 PUBLIC packets match as a set; their emitted
order still differs. The startup comparator reuses the complete physical scope
from after548 without replaying the historical runtime build chain.

The receipt and actual inputs, outputs, commands and logs are under
`.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1386p/`. Run the command above
without `--build` for a current read-only review; add `--build` and a fresh
stage for native execution. `.analysis/work/package-controls.log` records the
independent review and bounded negative controls for command, target-byte and
startup-byte changes.

This closes local four-file artifact reproduction with the current composition.
Whole-product source ownership remains open: vendor runtime inputs, ZUN's
reserved spans and the deferred MAIN carrier are still present. Build and
acceptance run directly through the local repository scripts.

## OP: maintained IRAND and selection state compose together

`build_th03_op_linked_current.py --stage af1377o` assembles the complete
physical OP ASM owner with `src/op/libs/random.asm`, then links it together
with the independently verified natural selection-state TC4 object. The other
28 project objects, compiler startup and libraries retain their current cold
bindings. The original cold source graph and outputs are unchanged.

Both rounds reproduce the complete 63,866-byte Japanese decoded EXE and its
607 literal ordered MZ relocations. The containing ASM object's entire native
program records match the baseline, including initialized storage, segment
attributes, groups, PUBLICs, imports and all 367 ordered fields. Only its module
filename and dependency comments differ. All three raw OBJ/EXE/MAP outputs
repeat. The complete MAP differs solely in the three diagnostic ASM module
filenames; the comparison retains every address, attribute and symbol row.

The 42-byte far IRAND function has five original native seed-reference fields
and no MZ relocation. Its source implements the original 32-bit LCG through
8086 WORD operations. It adds library ownership, not authored-game bytes.
The historical character-selection aggregate is covered by its existing
48-byte unlock and 2,858-byte tail owners, adding no duplicate bytes or gates.
The publication now covers every tracked OP range. Whole-product source
ownership outside that inventory remains open.

## MAIN: current owners compose together

`build_th03_main_linked_current.py --stage af1373m` rechecks the selected
source-native proofs and both composed links. All 97 selected physical objects
participate together in their original slots. Each round reuses its separately
compiled, reviewed objects. Only the historical 418-byte `input_s` carrier,
compiler startup and compiler libraries remain contextual inputs.

The normal links repeat byte for byte. Their complete loaded images and all
1,553 ordered MZ relocations match the Japanese target; standard compact MZ
serialization reproduces the 130,882-byte file. The full MAP equals the
composition of the individually reviewed MAP changes, including module
ownership and the existing same-address VSYNC alias order. No module rows,
addresses or public symbols are discarded from the comparison.

This establishes composition without another cold compilation. The original
417-byte TC4 scanner's one-byte link discrepancy remains deferred at the
user's request. Keep its existing diagnostics and the frozen after596 inputs.

## MAINL: complete project rebuild and natural function bodies

`build_th03_mainl_linked_current.py --stage af1369m` verifies two fresh native
builds of all 36 project objects plus the maintained BCC4.5 `xx` object. The
other 28 reviewed source CRT providers are reused; native TLIB preserves the
893-member library order. Each complete decoded EXE and original MAP matches
the retained Japanese target, including all 677 ordered MZ relocations. All
41 raw native outputs per round repeat.

The complete `xx` object reproduces 12,622 CODE bytes, 18 initialized DATA
bytes, 187 literal ordered fields, 22 PUBLICs and three segments. Its 50
function boundaries bind to current source definitions and actual native
LINNUM/dependency records. Inline compiler tables retain DATA credit. Earlier
architecture summaries saying this maintained `xx` source was raw-different
were stale; the [focused xx review](MAINL_XX_PRODUCT_REVIEW.md) already recorded
the exact source recovery.

The same build proves the two vector functions and eight natural ASM
producer/alignment bytes. The comparison alignment byte at `0000:2C2F` belongs
to **PFOPEN's endfunc**, rather than the following STR_IEQ source; its ledger
source is corrected to `src/mainl/archive_io/pfopen.asm`.

`build_th03_mainl_function_bodies.py --stage af1371f` additionally compiles the
five input/mode/PMD/volume/reset functions in two original first-use TC4 rounds,
omitting only their explicit final legacy codestring directives in disposable
source snapshots. All 541 function bytes, ordered fields, PUBLICs and storage
layout match the corresponding complete linked objects. Every body ends at
its actual far return. The containing target-equal objects still provide link
context; their legacy trailer bytes receive no new source credit.

## Why the inventory is not 259 accepted independent owners

All 259 tracked ranges are now covered by 249 independent source owners.
Ten historical aggregate rows are fully covered by accepted smaller extents:

| Historical row suffix | Accepted replacement scopes |
| --- | --- |
| `cfg-resident` | Root orchestration CFG loader |
| `win-load`, `win-text` | Root orchestration window functions |
| `staff-music` | Registration music function |
| `cutscene` | Cutscene functions and switch tables |
| `regist` | Registration functions |
| `scoredat` | Score-file functions |
| `root` | Root/continue functions and switch tables |
| `graph-putsa-fx` | Text renderer |
| `math-lut` | Hflip LUT generator |

These remain addressable historical rows. The verifier derives each coverage
reference from the canonical ledger and accepted byte ownership, rejecting any
unowned byte, overlapping source owners or boundary cutting a relocation word.
They receive no additional source-owner gates, byte credit or procedure count.
The excluded PFGETC WORD-link alignment byte remains outside the source-present
denominator.

## Four natural sound alignment producers

`build_th03_mainl_sound_current.py --stage af1375s` assembles the complete
mode/PMD/volume/reset providers in two rounds and links them with the current
project and library from `af1369m`. All four objects and the complete EXE/MAP
repeat. The Japanese decoded target and its 677 ordered MZ relocations match.
This adds natural source ownership for the four bytes at `0C7E:0049`, `0083`,
`009F` and `0669`, emitted by the existing symbolic ASM bodies' `EVEN` directives.

The [after570 investigation](MAINL_SOUND_NATURAL_AFTER570_NATIVE_REVIEW.md)
already recovered these bodies. The current source corrects PMD and volume
SHARED to BYTE alignment, and orders the empty DATA/BSS group declaration to
match TC4's literal emitted GROUP membership. Complete SEGDEF, GRPDEF and
EXTDEF records now agree with the retained compiler carriers. Full MAP
comparison changes only the four module filenames; ACBP alignment attributes,
group/layout rows and PUBLICs are compared exactly.

Each actual TASM field stream is checked in its literal reviewed order, with
all ten widths, sites, DGROUP frames and external indices intact. The retained
TC4 streams are recorded separately: three use reverse field chronology.
No sorting or packet rewriting conceals that compiler difference. These are
reconstructed compiler carriers rather than shipped OMF; the linked Japanese
MZ relocation vector is the target's ordered relocation evidence. The four
new owners are alignment bytes containing no instruction or fixup. Their
complete surrounding functions retain the independent TC4 body proofs above.

## Repeat or extend

Omit `--build` for read-only reviews of the stages above. For fresh
native execution, pass `--build` and a new unused DOS-safe stage; do not
overwrite a retained stage. The function-body builder records its complete-link
parent explicitly. The decoded publisher uses the selected build stages in
`lib/decoded_mainl_linked_current.py`, `build_th03_mainl_function_bodies.py`
and `build_th03_mainl_sound_current.py`.
After changing their selection, run the publisher and regenerate progress.
Whole-product source ownership remains open.
The local stored-file comparison is covered by the four-file package above.

## Remaining source questions: ZUN reserves and setvbuf

The isolated ZUN trial `TH03ZUN/probe/af1387z` retains the actual tiny MODEL
and instruction assumptions, separates the ON/OFF strings into a PARA
contribution, and removes both explicit reserved declarations. Its 4,215-byte
COM exactly equals the first 4,215 bytes of the original 4,224-byte `-4`
payload. TLINK supplies the three-byte gap before ON/OFF, but an empty following
segment does not write the nine terminal zero bytes. The earlier `af1380z`
manual-MODEL trial changed instruction encoding and is superseded. Neither
trial changes the maintained driver or grants the enclosing scope ownership.
The directory's `decoded_file_offset` must select this payload; its runtime
address includes the COM 100h bias. The corrected complete-prefix check is
`.analysis/work/zun-paragraph-check.log`.

TC4's internal assembler naturally emits the reverse operand-field order
needed by setvbuf's two callback MOVs. Both a minimal C pointer assignment and
inline assembly demonstrate this in `TH03OP/probe/af1378c`. TASM emits the
opposite order. This gives a concrete alternative to object-record rewriting.
A complete inline-assembly function still differs in register-save handling
and instruction encodings. The ordinary C reconstruction in `af1388c` emits
286 CODE bytes versus the original 289, with different epilogues and operand
fields; it is not adopted. `-1-` and `-2-` disable the default 286 instruction
selection and produce the same 8086 result with `-O -r-`; `-0` is invalid in
this TC4 compiler. The source-startup `/ml` case-sensitivity trial in
`TH03OP/probe/af1389s` preserves storage and all ordered fields but leaves the
PUBLIC order different, just as `/mx` does. The maintained shared ASM's two field-order mismatches
remain open. These small source trials and their logs remain in the local
probe directories; `.analysis/work/bounded-next.py` reproduces the latter two
trials in fresh stages after changing their stage names. The older installed
TC2.01 candidate emits a different 291-byte C function with or without
register allocation (`TH03OP/probe/af1390c`); it does not resolve setvbuf.

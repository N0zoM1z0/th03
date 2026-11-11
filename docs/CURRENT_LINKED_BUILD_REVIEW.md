# Current project composition (2026-11-11)

MAIN, OP and MAINL have two target-equal links composed from current source
outputs, all displayed CL contributors and an original-exact supplier C0 OBJ.
The final four-file package is freshly packed and restored in two rounds.
MAIN's deferred input carrier remains unchanged. MAINL's historical
aggregate ranges are explained below. [Generated progress](PROGRESS.md) supplies the current totals.

## Complete current build and final package

The current build uses the verified MAIN/OP/MAINL project pairs, freshly
rebuilt CL contributors (`af1405r`), original-exact supplier startup (`af1408s`)
and six complete native links (`af1409l`). ZUN retains its reviewed exact
decoded output; the user has deferred its nine terminal bytes along with
MAIN's earlier one-byte input-carrier question.

`scripts/package_th03_runtime_current.py --stage af1410p` consumes those actual
link outputs. Each round compactly serializes MAIN and runs the pinned DIET
1.45f `-B` / `-ra` pair on OP, MAINL and ZUN. All four stored files equal the
canonical Japanese targets byte for byte, and every restored file equals
its complete current decoded input. All seven final outputs repeat exactly.
The full EXE images and ordered MZ relocations were checked by the preceding
link review. The file sizes are listed in the baseline table below.

The actual packed outputs have also been installed and played in an isolated
PC-98 DOS disk, including OP/MAIN/MAINL transitions and score saving. See
[DOS runtime notes](RUNTIME.md) for the TH04-derived procedure, evidence and
remaining gameplay coverage.

The final receipt is `TH03PKG/af1410p/runtime-package.json`; the ready files
are under `r1/packed/` and `r2/packed/` in that directory. Review the complete
current build with:

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/package_th03_runtime_current.py
```

The command defaults to read-only verification, including its current linked
parent. Use `--build --stage afNNNNp` with an unused DOS-safe stage for a fresh
packing run. `.analysis/work/runtime-package-controls.log` records the complete
positive review and rejects a changed DIET command, a changed stored target
byte and a changed restored-input byte, including self-consistent output pins.

## Retained four-file packing baseline

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

That baseline's freshly assembled C0 object preserves all 17 original segments, 767
initialized bytes, genuine cache holes, reserved stack and all 58 literal
ordered fixup fields. All 32 PUBLIC packets match as a set; their emitted
order differs. The current supplier-source route below closes that gap.
The baseline startup comparator reuses the complete physical scope
from after548 without replaying the historical runtime build chain.

The receipt and actual inputs, outputs, commands and logs are under
`.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1386p/`. Run the command above
without `--build` for a current read-only review; add `--build` and a fresh
stage for native execution. `.analysis/work/package-controls.log` records the
independent review and bounded negative controls for command, target-byte and
startup-byte changes.

This closes local four-file artifact reproduction with the current composition.
The package route retains its reviewed runtime inputs. The source-runtime
composition below replaces all displayed CL contributors; ZUN's reserved
spans and the deferred MAIN carrier remain open. Build and
acceptance run directly through the local repository scripts.

## Current source runtime composes across all three MZ programs

`build_th03_runtime_current.py --stage af1405r` derives the union of CL
contributors from all three current detailed MAPs. It freshly assembles 75
maintained providers and compiles natural C `setvbuf` in two rounds, then
reuses the independently compiled current BCC4.5 `xx` pair. These 77 members cover every CL contributor displayed
in the three MAPs. Native TLIB preserves the original 893-member order and the
complete program records of all 816 other supplier members. Both complete
78-file OBJ/library output vectors repeat byte for byte.

Every provider reproduces the original initialized bytes, true holes, segment
sizes/attributes, group/entry metadata, imports, PUBLIC ownership and ALIAS
records. The complete literal ordered fields now match for all 77 members,
including both `setvbuf` MOV operand pairs. PUBLIC emission order is recorded
independently; these checks add no duplicate canonical owner credit.

The complete check found two missing C++ overload aliases in
`src/mainl/crt/strrchr.asm`. Their ordinary ALIAS declarations now match both
original records; instruction bytes and the existing C entry are unchanged.
The bounded controls reject that actual old alias-incomplete object, a changed
native field and an archive that disagrees with its actual source producer.
It also rejects the actual old `setvbuf` object with its two swapped operand
pairs. See `.analysis/work/runtime-current-controls.log`.

`build_th03_runtime_linked_current.py --stage af1409l` composes each current
project pair with this new library and the original-exact supplier C0 pair
from `af1408s`.
All six complete EXEs equal the preceding Japanese-target links, including
all loaded bytes and ordered MZ relocations. EMU.LIB and MATHL.LIB are removed
from these responses; neither is needed by the three current links. The same
raw EXEs also match the retained four-file baseline. The final package above
freshly packs and restores these current outputs.

The full MAP comparison permits only six exact same-address alias-order swaps
(two in MAIN, one in OP and three in MAINL), plus three zero-length MAINL BSS
carrier rows: add `ioerror`/`setblock` and remove `fbrk`. These reflect the
original CL segment declarations instead of the older 29-provider carrier.
Every other MAP byte remains identical. All three EXEs and both repeatable
OP/MAINL MAPs agree across rounds; MAIN retains its original round-path names.
The source runtime and link receipts are under `TH03RT/af1405r` and
`TH03PKG/af1409l` in this game's Wine drive. Both commands default to read-only
review; use `--build` and a fresh stage for native production.

TH04 supplied a useful comparison method rather than missing implementation:
its `TH04_ZUN_RUNTIME_INVENTORY_V537.md` likewise removes unused float libraries,
and `TH04_ZUN_FILE_STATE_V535.md` records a bounded same-address PUBLIC swap.
The inspected local TH04 revision is `d21200a`. Its referenced sprite16 ASM is
identical to this repository's candidate, and that file's input MD5 is the
actual TH03 `-4` payload MD5. Its TH04 filename comment therefore supplies no
independent evidence for the nine terminal bytes.

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

## Natural C closes setvbuf's ordered-field gap

`src/shared/crt/stdio_buffer.c` follows the supplier's
[SETVBUF.C](https://github.com/earthsiege2/borland-cpp-ide/blob/602b99a9fcd8429387d4c54cb1f455854e513886/SOURCE/RTL/CRTL/CLIB/SETVBUF.C)
at the already inspected BCC4.0 candidate revision. Its original Git blob is
`a11bc1eeaf3d9014697217b5363f05ab79a6d059`. The same tree supplies
`CLIB/TURBOC.CFG`, `RULES.MAK` and `BUILD-C0.BAT`; each acquired file was
checked against that tree's blob ID before use. These provide the original
control flow and library compiler settings rather than guessed flag variants.

The maintained provider uses the already pinned BCC4.5 compiler and TC4 headers.
`BCC_FLAGS` in the current runtime builder records the complete native recipe,
including `-a- -k- -O1 -2- -Vs -X` and the original segment-name options.
All five transitively consumed headers and the compiler/extender binaries are
bound as actual inputs. The provider reproduces all 289 CODE bytes, four DATA
bytes, true holes, segment attributes, imports, PUBLIC ownership, group/entry
metadata and all 13 literal ordered fields. Both callback MOV pairs now match
without a comparator exception. The source preserves the supplier's unchecked
behavior and original declaration structure.

The bounded `af1404c` control keeps that C source unchanged and adds `-r-`:
CODE shrinks to 285 bytes and the complete physical comparison rejects it.
Removing only the `register` keyword retains the exact physical output, so
that spelling alone is not the cause. See `.analysis/work/setvbuf-register-control.log`.

The unmodified supplier source also passes the complete physical comparison
with BCC4.0 and BCC4.5 in `af1403r`. Earlier hand-written C candidates used
different control flow and compiler settings and emitted 285/286 bytes;
the TC2.01 candidate emitted 291. The complete inline-ASM candidate duplicated
register saves and selected different instruction encodings. None is adopted.
TASM MASM51/IDEAL modes and JWasm `-Zg` leave the two MOV pairs ascending
(`af1400f`). The DOS TASM/TASMX executables extracted from the pinned TASM5
media identify as 4.1 and have the same operand ordering (`af1399t`).

## Deferred source question: ZUN reserves

The user has deferred the nine terminal bytes. Keep the maintained exact
payload while building and accepting the complete package.

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
Linking that same object as a normal MZ in `af1398z` also leaves a 4,215-byte
image after the COM origin; it has no relocations and equals the tiny-link
output completely. Current TLINK's MZ-to-COM route therefore does not explain
the missing tail. See `.analysis/work/zun-mz-tail.log`.
The DOS TLINK 7.1.30.1 from the pinned TASM installation media also emits
exactly that 4,215-byte prefix (`af1407z`); changing to this linker version
does not supply the tail. See `.analysis/work/zun-dos-linker.log`.

## Supplier startup reproduces the entire original OBJ

`src/shared/crt/startup/c0.asm` and `rules.asi` retain the pinned TC4 supplier
sources, with text formatting normalized. The same supplier tree's
[BUILD-C0.BAT](https://github.com/earthsiege2/borland-cpp-ide/blob/602b99a9fcd8429387d4c54cb1f455854e513886/SOURCE/RTL/CRTL/BUILD-C0.BAT)
provides the original command: `TASM /m /mx /q /t /d__LARGE__ c0,c0l`.
Use the DOS TASM 4.1 executable from `CMD16.PAK` in the already pinned
TASM5.0 media, not TASM32. Its 136,018-byte executable has SHA-256
`cafc42bbd1df39ab36e775be74ccb82c0a80da7d2a6dff4dcc2f16ba0e220f95`
and is installed only in this game's `C:\TASM41` directory.

`scripts/build_th03_startup_current.py --stage af1408s` checks both native
rounds against the entire original 2,438-byte OBJ. They match byte for byte:
all 17 segments, 767 initialized bytes, genuine holes, 58 ordered fields,
32 PUBLIC packets in their literal order and every other OMF record. The
builder binds both maintained source files, the original object, tools,
actual command and logs. Its receipt is `TH03CRT/af1408s/startup-build.json`.
The command defaults to read-only review; use `--build` with a fresh stage
for native execution. The complete three-program links above consume this pair.
The bounded controls reject a changed assembler command and the actual old
PUBLIC-order-different object even with its consistent output hash; see
`.analysis/work/startup-current-controls.log`.

Source context, assembler version and the original flags all matter here.
The earlier compact hand-maintained source retains a PUBLIC-order difference
with `/ml` or `/mx`, including DOS TASM 4.1 (`af1389s`, `af1399t`). Supplier
C0/RULES assembled with TASM32 preserve the physical scope but still change
packet order. The DOS assembler with the original invocation reproduces the
whole object (`.analysis/work/startup-supplier-recipe.log`). Keep the old
`startup_large.asm` unchanged while the four-file packing baseline binds it.

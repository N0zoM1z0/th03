# TH03 — agent handoff (verified 2026-11-05, after438)

**Start here.** Work on the actual Japanese PC-98 originals. Inspect
`git status -sb` and the last commits; continue **all** dirty edits rather
than reverting or avoiding them. The current Git `main` branch has local
commits not necessarily pushed. Do not push without authorization. Every
meaningful reconstruction advance should be committed as `gpt-web: ...`;
make several scoped commits where practical. Read
[AGENTS.md](../AGENTS.md), [workflow](RE_WORKFLOW.md), and
[architecture](ARCHITECTURE.md) before changing a product recipe.

## 1. Current original Japanese MAINL CRT checkpoint

| Property | Verified working-source evidence |
| --- | ---: |
| Original CL.LIB member slots | **893** |
| Complete members compiled from maintained source | **646** |
| Remaining unchanged contextual vendor member programs | **247** |
| Source-built, original-equal logical CRT CODE | **174,454 bytes** |
| Original decoded Japanese MAINL EXE size | **67,372 bytes** |
| Original ordered DOS MZ relocations | **677** |
| Actual native TASM/TLIB/TLINK production rounds | **2, byte-identical EXE and MAP** |
| Latest source build | `after438 / filebuf-close-destructor-boss` |
| Formal Factory acceptance of this 646-member CRT expansion | **No** |

**Source-bound proof:**
`scripts/review_th03_mainl_after438_work.py filebuf-close-destructor-boss`
and `tests.test_mainl_after438_work`, using
`.analysis/work/mainl-after438-filebuf-close-destructor-boss-build.json`.
The current reviewer checks the inherited **176-stage** receipt DAG,
source/driver/parent hashes, selected original member CODE/DATA/ABI, two
complete raw native OBJ/LIB/EXE/MAP rounds and writer logs. It is **not**
a full cold replay. The 646 individual members are not claimed to have
byte-identical original Borland OBJ *record serialization*; literal
ordered FIXUPP equality is separately recorded per module.

The original targets in `config/targets.toml` have
`candidate-local-attested` provenance, **not** independently established
pristine-dump origin. MAINL.EXE is the ending program. Do not substitute
translated/patched binaries, TH04 products, stored packed images, or
artificial target-byte arrays for native source recovery.

## 2. Acceptance and ledger: distinguish the claims

- [Generated progress](PROGRESS.md) is generated from ledgers, **not** from
  the 646-source working CRT. The packed-file canonical MAINL ledger remains
  **0 exact units**. `scripts/status.py` currently reports MAINL decoded
  product **pending**, `0/250` nonexcluded ledger units and no newly accepted
  bytes. `config/units.csv` has **251 MAINL rows**, including one excluded;
  do not confuse this denominator with source-present units.
- Earlier documentation reported **211 decoded MAINL extents / 288
  procedures / 36,946 bytes** of accepted source. This is a *historical
  reviewed figure*, **not currently attested acceptance**: the live
  `mainl_product_status()` verifier currently fails at the maintained far
  heap native source/recipe/unchanged-cold-context guard. Re-establish that
  guard independently before restoring any active decoded-acceptance claim.
  Do not erase the older source work or treat this status gate as proof that
  the underlying program has changed.
- MAIN has 106 exact file-backed units and 459 exact functions, totaling
  78,737 ledger bytes. OP has 60 currently decoded-accepted extents
  (14,985 bytes), ZUN 77 decoded-accepted extents (8,635 bytes); these
  **are different scopes**, not portions of a single whole-game percentage.
- Current WORKING MAINL EXE/MAP equality, OMF site/frame fidelity,
  previously reviewed decoded scope, and Factory/packed-file acceptance
  are four different facts. The whole-game source completion percentage
  remains unknown.

## 3. Important history and outstanding technical issues

After418 reconstructs the paired full **356-CODE/12-DATA
`stdiostream` destructor Boss**: real reference-count and optional-delete
paths, four original typed RTTI tables and all 14 logical original OMF
fixups including the *local* destructor pointer at CODE+128 and DATA+8.
Native EXE/MAP remains byte exact in both rounds; Borland/TASM literal
FIXUPP chronology differs. See
[the stdiostream destructor review](MAINL_STDIOSTREAM_DESTRUCTOR_BOSS_NATIVE_REVIEW.md).
After438 recovers the paired **247-CODE/54-DATA filebuf destructor**
with real close/virtual-overflow paths, original typed RTTI and all twenty
logical FIXUPPs. Its previously missing public DATA+0 `@filebuf@openprot`
(0180h) was restored and strictly reviewed. Both full Japanese native
EXE/MAP rounds remain byte-exact. See
[the filebuf destructor review](MAINL_FILEBUF_DESTRUCTOR_BOSS_NATIVE_REVIEW.md).
After437 reconstructs the **259-CODE/52-DATA original filebuf
constructor**, including virtual setbuf dispatch, true typed filebuf and
streambuf RTTI and all eleven original symbolic virtual function slots.
All 19 logical OMF fixups and both full Japanese EXE/MAP rounds match;
Borland/TASM literal record chronology differs. See
[the filebuf constructor review](MAINL_FILEBUF_VIRTUAL_SETBUF_CONSTRUCTOR_NATIVE_REVIEW.md).
After436 recovers the original complete 262-CODE `istream::ipfx(int)`
Boss, including real gcount reset, tied ostream flush, buffered-availability
checks and `skipws`/`eatwhite`/error handling. All four logical OMF fields
and two full Japanese EXE/MAP rounds match the original. See
[the prefix review](MAINL_ISTREAM_PREFIX_BOSS_NATIVE_REVIEW.md).
After435 reconstructs the complete `strstreambuf` destructor boss,
**265 CODE + 52 DATA bytes** with both original far-buffer cleanup paths,
true base/object destruction, two typed RTTI records and all 20 exact
logical OMF fields. Two native Japanese EXE/MAP rounds remain byte exact.
See [the destructor review](MAINL_STRSTREAMBUF_DESTRUCTOR_BOSS_NATIVE_REVIEW.md).
After434 adds eleven full Japanese Borland formatted I/O, scanner and
conio leaves (515 original-equal CODE bytes), including real callbacks,
window bounds and insert/delete line paths. All 43 logical OMF sites
match with only 15 narrowly attested near-call frame differences;
two full Japanese EXE/MAP rounds remain byte exact. See
[the eleven-leaf review](MAINL_ELEVEN_FORMAT_SCAN_CONSOLE_LEAVES_NATIVE_REVIEW.md).
After433 recovers the complete dynamic `strstreambuf(int)` constructor,
**320 CODE + 52 initialized DATA bytes**: genuine Borland `new[]`,
minimum 16-byte allocation, far buffer setb, typed RTTI and 11 vtable
slots. All 21 logical FIXUPPs and two Japanese native EXE/MAP rounds match.
See [the dynamic constructor review](MAINL_STRSTREAMBUF_DYNAMIC_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After432 reconstructs the complete `strstreambuf` far-buffer
constructor, **254 CODE + 52 initialized DATA bytes** with the two
original far buffer boundaries, typed RTTI and all 19 logical OMF
relocations. Two fresh Japanese native EXE/MAP rounds are exact. See
[the far-buffer constructor review](MAINL_STRSTREAMBUF_FAR_BUFFER_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After431 recovers the complete `strstreambuf()` default C++
constructor (250 CODE + 52 DATA), including the true buffer-state fields,
two typed RTTI records and all 11 virtual function slots. All 19 logical
OMF FIXUPPs and two Japanese native EXE/MAP rounds match the live original.
See [the default constructor review](MAINL_STRSTREAMBUF_DEFAULT_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After430 recovers both complete `istream` and `ostream` base
destructor bosses (230+253 CODE and 20+20 DATA bytes). Four real OMF
relocations at CODE+38/46 that looked like plain 8/16 constants in
byte-equal prototypes are now symbolic DATA/vtable references. All 25
logical fields and two full native Japanese EXE/MAP rounds match.
See [the two-destructor review](MAINL_BASE_ISTREAM_OSTREAM_DESTRUCTORS_NATIVE_REVIEW.md).
After429 restores the complete 227-CODE `strstreambuf::init` buffer
manager and 45-CODE `clrscr` leaf. All 12 original logical OMF fields
match, with only the explicitly bounded Borland-vs-TASM near __SCROLL
frame difference at clrscr CODE+27; both Japanese native EXE/MAP rounds
remain byte exact. See
[the buffer/console native review](MAINL_STRSTREAM_INIT_CONSOLE_CLEAR_NATIVE_REVIEW.md).
After428 recovers the complete **349-CODE/20-DATA istream_withassign()
constructor**, including the +6 ios base adjustment, the true FAR
this-adjustor at CODE+131, three typed RTTI records and all 16 original
logical OMF fields. Both full Japanese EXE/MAP native rounds are byte-exact;
literal Borland/TASM FIXUPP record order differs. See
[the constructor review](MAINL_ISTREAM_WITHASSIGN_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After427 recovers the full original `istream(streambuf*,ostream*)`
constructor, **305 CODE + 20 DATA bytes**, including real ios::skip and
ios::tie imports, the original 22-byte argument cleanup, typed RTTI and
15 exact logical OMF fields. Two Japanese native EXE/MAP rounds remain
byte exact. See
[the tied-stream ctor review](MAINL_ISTREAM_TIED_STREAM_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After426 reconstructs the complete **333-CODE/20-DATA
`istream_withassign` destructor**, including the true CODE+115 local
FAR this-adjusting thunk, three typed RTTI records and all 16 logical
OMF relocations. Two fresh Japanese EXE/MAP rounds remain byte-exact;
literal Borland/TASM FIXUPP order differs. See
[the destructor review](MAINL_ISTREAM_WITHASSIGN_DESTRUCTOR_BOSS_NATIVE_REVIEW.md).
After425 recovers the full original `strstreambuf` buffer constructor,
239 CODE + 52 initialized DATA bytes with typed RTTI and 11 original
virtual-function slots. The original DATA+28 `do_sputn` and DATA+32
`overflow` bindings were restored after OMF checking revealed that an
initial byte-equal translation had swapped their targets. All 20 logical
FIXUPPs and both full Japanese EXE/MAP native rounds now match. See
[the constructor review](MAINL_STRSTREAMBUF_BUFFER_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After424 adds full C++ `strstreambuf::underflow` (188 CODE),
NEC hardware/BIOS GOTOXY (74 CODE) and far `strnset` (58 CODE).
All eight original logical OMF fields and two full native Japanese
EXE/MAP rounds match; `cnecgtxy` additionally matches the original
literal FIXUPP chronology. See
[the after424 review](MAINL_UNDERFLOW_NEC_FAR_STRING_NATIVE_REVIEW.md).
After423 recovers the complete **`istream(streambuf*)` constructor**,
275 CODE + 20 DATA bytes with the true +6 `ios` base adjustment, input
state word, two typed RTTI classes, CODE+143 FAR destructor thunk and
all 13 logical OMF relocations. Both Japanese native EXE/MAP rounds match;
original Borland/TASM literal FIXUPP order remains different. See
[the istream constructor review](MAINL_ISTREAM_STREAMBUF_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After422 reconstructs the **full `ostream(streambuf*)` C++ constructor**,
266 CODE + 20 DATA bytes including real C++ base construction,
CODE+134 destructor adjustment thunk, typed ostream/ios RTTI and all
13 complete original logical FIXUPP fields. Both Japanese native EXE/MAP
rounds are byte exact; Borland/TASM literal FIXUPP record order differs.
See [the constructor native review](MAINL_OSTREAM_STREAMBUF_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After421 adds eight C++ stream, DOS file and NEC/IBM sound leaves,
**496 complete original CODE bytes**. All logical OMF fields match,
with six members preserving *literal ordered* FIXUPPs and two retaining
Borland/TASM record-order differences. Both Japanese native EXE/MAP rounds
remain byte exact. See
[the eight-leaf review](MAINL_EIGHT_STREAM_DOS_SOUND_LEAVES_NATIVE_REVIEW.md).
After420 recovers the paired complete `ostream_withassign` destructor
boss: 333 CODE + 20 initialized DATA bytes and 16 logical OMF fields,
including the original CODE+115 local FAR destructor thunk forced with a
correct segment assumption. Both Japanese native EXE/MAP rounds remain
byte-for-byte original-equal. See
[the destructor native review](MAINL_OSTREAM_WITHASSIGN_DESTRUCTOR_BOSS_NATIVE_REVIEW.md).
After419 reconstructs the full `ostream_withassign()` constructor boss,
349 CODE + 20 DATA bytes with the real CODE+131 `this`-adjusting destructor
thunk, three typed RTTI classes and 16 exact logical OMF relocations.
Two native Japanese EXE/MAP rounds remain byte-identical. Literal Borland
FIXUPP ordering remains different; see
[the constructor review](MAINL_OSTREAM_WITHASSIGN_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After418 recovers the complete paired C++ `stdiostream` destructor boss,
356 CODE + 12 initialized DATA bytes and all four typed RTTI records.
The full 14 logical OMF relocations and both Japanese EXE/MAP rounds match;
Borland/TASM literal FIXUPP chronology differs. See
[the destructor native review](MAINL_STDIOSTREAM_DESTRUCTOR_BOSS_NATIVE_REVIEW.md).
After417 reconstructs the **full 383-CODE/12-DATA `stdiostream(FILE*)`
constructor Boss** with its actual 125-byte constructor plus four typed
CODE-resident RTTI tables and all 15 logical OMF relocation fields.
Original CODE+155 is a real `stdiostream` destructor symbol, not a zero
constant; restoring the missing FIXUPP left byte-perfect CODE unchanged.
Both native Japanese EXE/MAP rounds remain exact; literal Borland/TASM
FIXUPP record chronology differs. See
[the stdiostream constructor review](MAINL_STDIOSTREAM_FILE_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md).
After416 integrates **twelve original DOS-drive, PC-98/IBM video,
Japanese MBCS and C++ ios ABI leaves** (640 CODE bytes): eleven new ASM
sources plus one verified retained `dosgdriv.asm`. Original `ccomscrn`
intermediate jump was corrected, and five exact near-call frame gaps are
narrowly attested; both Japanese EXE/MAP rounds remain byte-identical.
See [the twelve-leaf review](MAINL_TWELVE_DRIVE_VIDEO_MBCS_IOS_LEAVES_NATIVE_REVIEW.md).
After415 restores the complete original PC-98 x87/equipment probe
`pc98eqip` (213 CODE bytes): actual hardware BIOS flags, x87 detection,
the semantic inline IEEE infinity and both **literal original ordered**
CODE fixups. An overlooked `or al,dl` after the constant was restored from
the true original; two native Japanese EXE/MAP rounds remain byte-exact.
See [the equipment/FPU review](MAINL_PC98_EQUIPMENT_FPU_BOSS_NATIVE_REVIEW.md).
After414 restores the full six-API NEC/IBM text-color and attribute
dispatch boss `ccomcolr` (216 CODE bytes). All 24 logical OMF fields, including
original GROUP and TARGET frames, match; Borland/TASM raw FIXUPP chronology
differs. Both full Japanese EXE/MAP native rounds are exact. See
[the six-color native review](MAINL_SIX_CONSOLE_COLOR_BOSS_NATIVE_REVIEW.md).
After413 recovers the complete **170-CODE NEC text console scroll boss**
with original move/clear directions and stack ABI. All five original
logical FIXUPP sites/targets match, with strictly limited Borland/TASM
TARGET-vs-CODE near-call frame differences; both Japanese native EXE/MAP
rounds remain byte exact. See
[the native scroll review](MAINL_NEC_CONSOLE_SCROLL_BOSS_NATIVE_REVIEW.md).
After412 reconstructs the complete original **171-CODE / 8-DATA NEC BIOS
disk controller boss**, with authentic `INT 1Bh`, 50h/70h/80h drive
request handling and firmware parameter copy. The single original literal
ordered FIXUPP and both Japanese EXE/MAP rounds match precisely. See
[the BIOS disk review](MAINL_NEC_BIOS_DISK_CONTROLLER_BOSS_NATIVE_REVIEW.md).
After411 adds **eight source-linked Japanese MBCS, far-string, BGI
and `strstreambuf` leaves** (335 original-equal CODE bytes), with six
original literal ordered FIXUPPs and two explicitly retained Borland/TASM
record-order differences. Both full native Japanese EXE/MAP rounds remain
byte exact. See [the eight-leaf native review](MAINL_EIGHT_MBCS_STRING_BGI_LEAVES_NATIVE_REVIEW.md).
After410 recovers the complete **201-byte original IBM VRAM boss**
with near `__IBM_VPTR`, `__IBM_VRAM`, `__IBM_REFRESH_VRAM`, authentic
03DAh retrace/CLI-STI bidirectional transfers and all seven **literal
ordered original FIXUPPs**. Two Japanese native EXE/MAP rounds agree.
See [the IBM VRAM review](MAINL_IBM_TEXT_VRAM_BOSS_NATIVE_REVIEW.md).
After409 restores the complete 227-byte NEC PC-98 BIOS serial-controller
Boss `bion_com`, including actual `INT 19h/D4h/D5h` dispatch,
A000h/D000h controller setup and serial parameter result writes. Full
CODE and the original zero-FIXUPP scope reproduce in two exact Japanese
EXE/MAP rounds. See
[the serial native review](MAINL_NEC_BIOS_SERIAL_CONTROLLER_BOSS_NATIVE_REVIEW.md).
After408 recovers the complete NEC PC-98 BIOS equipment/memory/time
Boss `bion_equ` (262 CODE + 41 initialized DATA bytes), including real
x87 detection, DOS 33h resident mouse signature, A000h/D000h status
reads and time-of-day. Its single **literal ordered** original FIXUPP
and both full Japanese EXE/MAP rounds match exactly. See
[the NEC BIOS native review](MAINL_NEC_BIOS_EQUIPMENT_BOSS_NATIVE_REVIEW.md).
After407 adds **12 original DOS syscall leaves** (396 CODE bytes)
covering allocation/resize, time, directory, IOCTL and DOS TSR. **11/12
literal ordered FIXUPPs** match; `dossetbl` has one strictly bounded
near-call frame gap. Crucially, the active target `setblock` and the
installed TC4 vendor have different GRPDEFs despite identical CODE and
FIXUPPs; the pre-existing maintained source matching the active target
was preserved. See [the detailed 12-leaf review](MAINL_TWELVE_DOS_SYSCALL_LEAVES_NATIVE_REVIEW.md).
After406 restores the full 290-CODE C++ `ostream << streambuf*`
Boss, including virtual underflow/overflow, prefix/suffix calls and
error-state handling, with three complete original logical OMF fields.
Two full Japanese native EXE/MAP rounds remain byte exact; original
Borland literal FIXUPP order differs. See
[the ostream insertion review](MAINL_OSTREAM_STREAMBUF_INSERTION_BOSS_NATIVE_REVIEW.md).
After405 restores the paired full C++ `streambuf::do_sgetn` /
`streambuf::do_sputn` bulk-transfer bosses, 184 + 168 original-equal
CODE bytes, with real far buffers and virtual overflow/underflow paths.
Both original **literal ordered** `_memcpy` FIXUPPs match, as do both
full Japanese native EXE/MAP rounds. See
[the streambuf bulk review](MAINL_STREAMBUF_BULK_TRANSFER_BOSSES_NATIVE_REVIEW.md).
After404 reconstructs original absolute DOS disk I/O: **292 CODE + 2
DATA + 2 BSS bytes**, original _absread/_abswrite and INT25h/INT26h paths,
including the far-return probe and all eight logical OMF relocations.
Japanese EXE/MAP remains original-equal in both native rounds; original
FIXUPP record chronology differs. See
[the absolute I/O review](MAINL_ABSOLUTE_DOS_DISK_IO_BOSS_NATIVE_REVIEW.md).
After403 adds **eight complete NEC/IBM machine dispatch and DOS ABI
leaf members** (295 original CODE bytes), including near/far callback
routing and the real `isatty` IOCTL. Four narrowly scoped Borland/TASM
external-near-call frame differences remain visible; both Japanese
EXE/MAP rounds stay byte exact. See
[the eight-leaf review](MAINL_EIGHT_MACHINE_DISPATCH_LEAVES_NATIVE_REVIEW.md).
After402 recovers the complete 261-CODE DOS `_putenv` environment
manager: original far environment name matching, table growth, old-vector
freeing and entry removal. All **ten original literal ordered** OMF
FIXUPPs and both full native Japanese EXE/MAP rounds match. See
[the putenv native review](MAINL_PUTENV_ENVIRONMENT_BOSS_NATIVE_REVIEW.md).
After401 adds the complete 291-CODE C++ `stdiobuf::seekoff` boss: real
32-bit file offsets, stream vtable flush, far `fseek` / `ftell`, put/get
buffer reset and all four original logical OMF relocations. The two
Japanese native EXE/MAP rounds remain byte exact, while literal Borland
FIXUPP record chronology differs. See
[the seekoff native review](MAINL_STDIOBUF_SEEKOFF_BOSS_NATIVE_REVIEW.md).
After400 reconstructs the full original Japanese DOS `mktemp` boss:
253 CODE + 7 initialized DATA bytes, genuine `XXXXXX` template and five
nested A..Z filename selection loops, with four exact logical original
OMF relocation fields. The native two-round Japanese EXE/MAP is still
original-equal; raw Borland FIXUPP chronology differs. See
[the DOS mktemp review](MAINL_DOS_MKTEMP_ENUMERATION_BOSS_NATIVE_REVIEW.md).
After400 recovers the complete **253 CODE + 7 DATA** DOS `_mktemp`
filename enumeration boss, with the real `XXXXXX` template and original
five-character candidate search. All four logical OMF FIXUPPs match;
literal record order differs. See
[the mktemp native review](MAINL_MKTEMP_ENUMERATION_BOSS_NATIVE_REVIEW.md).
After399 reconstructs the complete original 255-byte DOS `__makepath`
boss, including the real Japanese SBCS-aware directory separator logic and
all five original logical imported far-call FIXUPPs. Both native Japanese
EXE/MAP rounds remain byte exact; raw Borland FIXUPP record order differs.
See [the DOS path boss review](MAINL_DOS_MAKEPATH_BOSS_NATIVE_REVIEW.md).
After398 adds ten originally contextual ABI/video/stream/locale leaf
members, **126 CODE + 59 initialized DATA bytes**. Three original-vs-TASM
near-call framing differences and a locale-pointer FIXUPP chronology
difference are narrowly tracked; the full Japanese EXE/MAP remains exact
in both rounds. See [the ten-leaf review](MAINL_TEN_ABI_VIDEO_LOCALE_LEAVES_NATIVE_REVIEW.md).
After397 recovers the complete NEC text-color and attribute Boss with
six original far APIs, 222 CODE and 128 initialized DATA bytes (four
16-WORD palettes). All 21 original logical FIXUPP fields, source DATA,
layout and the two native Japanese EXE/MAP rounds match. Literal Borland
FIXUPP record order remains different. See
[the native text-color review](MAINL_PC98_TEXT_COLOR_ATTRIBUTE_BOSS_NATIVE_REVIEW.md).
After396 recovers the complete **247-CODE / 4-BSS PC-98 VRAM text
output boss** with four actual near APIs and all 21 **literal original
ordered** OMF FIXUPPs. Original disassembly invalidated a row/column
assumption and a blanket DGROUP framing assumption; the real original
frame and cursor access patterns now agree. See
[the VRAM output review](MAINL_PC98_TEXT_VRAM_OUTPUT_BOSS_NATIVE_REVIEW.md).
After395 restores the complete original PC-98 NEC hardware cursor boss
`cneccrsr`: 346 CODE + 12 DATA bytes, direct port/INT18h/INTDC
paths and seven **literal original ordered** OMF FIXUPPs. An original
DATA pointer-order error and a DGROUP member-order error were corrected
against the real CL.LIB member, not historical assumptions. See
[the cursor native review](MAINL_PC98_CURSOR_CONTROL_BOSS_NATIVE_REVIEW.md).
After394 restores the **272-byte DOS date/time formatting member**, including
a genuine 159-byte near formatter shared by far `__strdate`/`__strtime`
entry points. The entire CODE and two logical OMF far-call relocations
match; literal FIXUPP record order differs. Two original Japanese native
EXE/MAP rounds remain identical. See
[the date/time native review](MAINL_DOS_DATE_TIME_FORMAT_NATIVE_REVIEW.md).
After393 recovers **two complete C++ vector-construction bosses**:
`vnew` 313 CODE bytes and `vnewv` 345 CODE bytes, covering array
allocation and 16 near/far calling-convention paths. All 18 logical OMF
relocations and two Japanese EXE/MAP rounds match; Borland/TASM FIXUPP
record order differs. See [the native constructors review](MAINL_VECTOR_CONSTRUCTORS_BOSSES_NATIVE_REVIEW.md).
After392 recovers the previously uncommitted original 343-byte C++
`__vector_delete_` destructor boss: reverse element traversal, near/far
callback modes, seven relocatable dispatch entries, optional header
adjustment and original delete call. Nine complete logical FIXUPPs and
two native Japanese EXE/MAP rounds match; Borland's literal FIXUPP record
order remains different. See
[the native vector-delete review](MAINL_VECTOR_DELETE_BOSS_NATIVE_REVIEW.md).
After391 replaces 18 genuinely unowned CRT ABI leaves (268 CODE bytes):
17 members reproduce literal original ordered FIXUPPs; `stxalc` has two
correct relocations but a different record order. The source-linked native
EXE/MAP remains exactly original in both rounds. See
[the 18-member native review](MAINL_EIGHTEEN_RUNTIME_ABI_LEAVES_NATIVE_REVIEW.md).
After390 adds the full 300-byte original DOS INT 24h critical-error boss
with 12-byte shared BSS, four far public APIs and 20 logical exact OMF
fixups. The original Japanese EXE/MAP are byte-exact in both source-bound
rounds. See [the INT 24h native review](MAINL_DOS_HARDERR_NATIVE_REVIEW.md).
After388 added the original default `string` constructor. After389 adds the
complete original 310-byte `_locking` DOS file-locking boss with 16 exact
logical OMF FIXUPPs, five relocation-backed jump-table entries and exact
two-round Japanese EXE/MAP; literal Borland FIXUPP record *order* still
differs. See [the _locking native review](MAINL_DOS_LOCKING_BOSS_NATIVE_REVIEW.md).

The former 200-line chronological source list has been moved to the
[MAINL working CRT recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md).
That index links the original per-member review files. Recent milestones
include `ctor3`, `substr2`, eight near/far MBCS routines, and the complete
`ctor1` default constructor. Avoid redoing them simply because an older
note recommended them. Inspect the actual member and status first.

- **`h_ldiv`** (`src/mainl/crt/h_ldiv.asm`) has original-equal **174
  CODE bytes and 12 aliases**, but TASM and Borland still order two
  same-address aliases differently in the **MAP**. It is deliberately
  **not counted** in the 646 source-linked members. See
  [its bounded investigation](MAINL_H_LDIV_SCOPED_CODE_ONLY_REVIEW.md)
  and `tests.test_mainl_h_ldiv_original_scope`. Preserve its source and
  diagnostic evidence, do not reorder a MAP to fake acceptance.
- **`doslock`** retains two original-vs-TASM near-call FIXUPP frame
  differences despite complete linked EXE/MAP equality. `setargv` has
  original-equal logical relocation fields but different raw BCC FIXUPP
  record order. See their scoped review files; don't generalize these gaps
  to every member.
- **`xxv`** has original CODE/DATA/BSS and logical relocation equality
  but different literal OMF FIXUPP chronology. **`cnectxmd`** has a
  reviewed near-call TARGET/CODE-frame distinction plus raw record-order
  differences. See [OMF gaps](MAINL_OMF_GAPS.md). Conversely `checks`
  *does* now reproduce its 89 literal ordered FIXUPPs; older attempts
  that said otherwise are superseded.
- The original full game and accepted source-to-packed reconstruction
  remain open, even when this decoded MAINL program links exactly.

Remaining useful targets include complete larger CRT C++ functions and
small near/far functions, plus product-module MAIN/OP/ZUN ownership. Choose
based on **actual** original CL.LIB/IDA/Ghidra evidence, not old guessed
candidate lists. Keep both Boss and leaf work moving.

## 4. Handoff commands (scoped; no full cold replay)

Run from the repository root using the installed `.venv` and local Wine
prefix; serialize native writers. A recent Python 3.12 toolchain requires
loading `setuptools`' compatibility shim and raising the recursion limit
inside some deep historical CLI/test entrypoints (already handled by the
latest reviewer/test).

```sh
git status -sb
git log -5 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after438_work.py filebuf-close-destructor-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after438_work -v
.venv/bin/python scripts/status.py
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
```

For a new source replacement: check the raw original CL.LIB member,
**complete** CODE/DATA/BSS/INIT/EXIT and public/import/ABI, logical and
**literal ordered** original FIXUPPs, and both actual byte-exact decoded
Japanese EXE/MAP rounds. Commit each substantial result and update the
latest handoff counts/commands. Do not run full cold replay for an unchanged
parent; a successful Git commit or a plain assembler exit is not Oracle
acceptance.

## 5. Storage and cleanup

[Current protected native DAG / storage cleanup guide](STORAGE_HANDOFF_CURRENT.md)
explains what can be deleted and how to preview it safely. **Keep all
176 active source-bound stages**: build receipts, every phase log, and both
raw native OBJ/LIB/EXE/MAP rounds. Also keep targets, .venv, Wine/Borland
prefix, Ghidra/JDK attestations, source/ledgers, runtime images and the
old-named `reference.tar` input. At the prior after388 cleanup, 256 retired/scratch files were safely removed
(**7.04 MiB**) plus approximately **5.4 MiB** of regenerable caches, with
the same source reviewer still passing. The older
[2026-11-05 319-member audit](STORAGE_HANDOFF_2026-11-05.md) is a **historical
snapshot only**; its frozen cleanup tool intentionally refuses to run on
this newer checkout. Never run a blanket `clean_generated.py --apply` on
this active MAINL DAG. The guarded after388 cleanup script is obsolete for the newer source checkpoint;
do not apply it until its audit has been refreshed.

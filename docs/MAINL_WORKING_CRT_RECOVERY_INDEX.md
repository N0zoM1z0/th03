# MAINL working CRT reconstruction — historical source index

These are **historical, scoped reconstruction notes** extracted from the
former long-form agent handoff on 2026-11-05. They are not the current
acceptance ledger and should not be summed to claim product coverage;
individual module review files provide the relevant original OMF and
source/receipt details. For the verified, live total and command, return
to [the current handoff](RE_HANDOFF.md). Several historical paragraphs
refer to intermediate snapshots; after439 had 647 source members but
newer stages may exist. Inspect Git, the source receipt and the actual
latest reviewer rather than using this index as a live counter.

[Five full DOS file/date/drive/search CRT members](MAINL_DOS_FILE_DATE_LOCK_FIND_NATIVE_REVIEW.md)
add 462 original CODE bytes across ten public entries. Four match original
literal FIXUPPs; `doslock` records the **two exact TARGET-vs-CODE near-call
frame gaps**, with byte-exact native linking. [Five-API `find1` boss](MAINL_FIND1_BOSS_NATIVE_REVIEW.md) recovers 1,379 CODE bytes and literal original FIXUPPs. The [complete PC-98 function-key and MBCS strchr programs](MAINL_PC98_FUNCTION_KEYS_MBSCHR_NATIVE_REVIEW.md)
add 312 original CODE bytes, five far BIOS/DBCS APIs and three literal
original FIXUPPs. The [full `string` substring constructor Boss](MAINL_STRING_CTOR5_SUBSTRING_NATIVE_REVIEW.md)
adds 716 original CODE bytes, a complete reference-counted construction
path, five typed RTTI structures and 22 literal ordered FIXUPPs. Three [complete `string::append` and `prepend` exception bosses](MAINL_STRING_APPEND_PREPEND_BOSSES_NATIVE_REVIEW.md)
add 1,651 original CODE bytes and 63 literal ordered FIXUPPs across three
full C++ programs and nine original typed RTTI descriptors. Ten [complete Japanese MBCS compare/search near/far functions](MAINL_JAPANESE_MBCS_SEARCH_COMPARATORS_NATIVE_REVIEW.md)
add 1,926 original CODE bytes and 26 literal ordered `__ctype`/`__mbctype`
FIXUPPs. The [complete `string(TSubString&)` constructor](MAINL_CTOR6_TSUBSTRING_NATIVE_REVIEW.md)
adds 621 original CODE bytes, five RTTI structures and 22 literal
original ordered FIXUPPs. The [complete original string default constructor](MAINL_STRING_DEFAULT_CONSTRUCTOR_NATIVE_REVIEW.md)
adds 560 original CODE bytes and 23 literal original ordered FIXUPPs, including
the genuine DGROUP-framed `@string@initial_capac` read and five RTTI types.
Eight [complete Japanese near/far MBCS append/search/case functions](MAINL_MBCS_APPEND_SEARCH_CASE_NATIVE_REVIEW.md)
add 1,432 original CODE bytes and 18 literal ordered FIXUPPs, including
real far helper calls and `__ctype`/`__mbctype` table accesses.
The [complete indexed-range `string::substr` exception Boss](MAINL_STRING_SUBSTR_RANGE_NATIVE_REVIEW.md)
adds 572 original CODE bytes and 24 original literal ordered FIXUPPs
across its full two-index method, cleanup helpers and five typed RTTI.
The [complete C-string constructor `ctor3`](MAINL_STRING_CSTR_CONSTRUCTOR_NATIVE_REVIEW.md)
adds 747 original CODE bytes and 29 literal original ordered FIXUPPs,
including its two far cleanup helpers and six original typed RTTI records.
The [500-source milestone: eleven complete Japanese MBCS count/navigation leaves](MAINL_MBCS_COUNT_NAVIGATION_500_NATIVE_REVIEW.md)
adds 620 CODE bytes and 11 original literal FIXUPPs for character length,
next, increment, copy and second lead-byte classification.
The [complete indexed `string::substr` exception Boss](MAINL_STRING_SUBSTR_BOSS_NATIVE_REVIEW.md)
adds 570 original CODE bytes, full bounds/cleanup paths and five RTTI types,
including 24 literal original ordered FIXUPPs.
The [complete original `string::clone` Boss](MAINL_STRING_CLONE_BOSS_NATIVE_REVIEW.md)
adds 328 original CODE bytes, 12 literal ordered original FIXUPPs and three
typed RTTI records, including the actual copy-on-write path.
Ten [complete near/far Japanese MBCS compare and pointer operations](MAINL_MBCS_POINTER_OPS_TEN_NATIVE_REVIEW.md)
add 1,726 original CODE bytes and 20 literal original ordered FIXUPPs
across compare, span-pointer, set, and backward traversal routines.
The [complete `string::copy` reference-counted Boss](MAINL_STRING_REFERENCE_COPY_BOSS_NATIVE_REVIEW.md)
adds 737 original CODE bytes, seven typed C++ RTTI records and 27 literal
ordered original FIXUPPs, including the actual reference cleanup helper.
The [complete original C-string range constructor](MAINL_STRING_CSTR_RANGE_CONSTRUCTOR_NATIVE_REVIEW.md)
adds 811 CODE bytes, six typed RTTI records, and 29 original literal
ordered FIXUPPs, including both exception-cleanup helpers. The [complete `string::reserve` capacity Boss](MAINL_STRING_RESERVE_BOSS_NATIVE_REVIEW.md)
adds 431 original CODE bytes, three RTTI records and 19 literal original
ordered FIXUPPs. The [complete `string::append` substring Boss](MAINL_STRING_APPEND_SLICE_BOSS_NATIVE_REVIEW.md)
adds 578 original CODE bytes and 20 literal original ordered FIXUPPs,
including the original RTTI and two real far cleanup helpers. Six [complete Japanese MBCS near/far span and bounded compare routines](MAINL_JAPANESE_MBCS_SPANS_NATIVE_REVIEW.md)
add 1,136 original CODE bytes and 12 exact original ordered `__mbctype+1`
FIXUPPs. The [complete `string::remove` exception Boss](MAINL_STRING_REMOVE_EXCEPTION_BOSS_NATIVE_REVIEW.md)
adds 822 CODE bytes, the real 30-byte bounds-message DATA, full cleanup
and RTTI and 37 literal original ordered FIXUPPs. Six [complete near/far Japanese string comparators](MAINL_JAPANESE_MBCS_COMPARATORS_NATIVE_REVIEW.md)
add 1,408 original CODE bytes and 16 exact original ordered `__ctype`/
`__mbctype` fields. The [complete 791-byte `string::assign` boss](MAINL_STRING_ASSIGN_BOSS_NATIVE_REVIEW.md)
adds full reference-counted assignment, exception cleanup and five RTTI
types, including all 24 literal original ordered FIXUPPs. The [ten-API `MBBIS` Japanese byte-classification member](MAINL_MBBIS_TEN_API_NATIVE_REVIEW.md)
adds 345 CODE bytes and 15 literal original ordered `__ctype`/`__mbctype`
relocations. It also resolves a previously uncommitted source without
skipping or discarding it. Five [complete `istream` get/extraction/eatwhite methods](MAINL_ISTREAM_EXTRACTION_EATWHITE_NATIVE_REVIEW.md)
add 1,162 original CODE bytes and 10 ordered FIXUPPs, including the real
`__ctype+1` table reference. Six [complete `istream` bulk/read/get/putback methods](MAINL_ISTREAM_READ_IGNORE_GET_PUTBACK_NATIVE_REVIEW.md)
add 1,586 original CODE bytes and 15 literal ordered original imported far
FIXUPPs. The [complete 999-byte C++ operator+ exception boss](MAINL_OPERATOR_PLUS_EXCEPTION_BOSS_NATIVE_REVIEW.md)
recovers the original reference-counted string concatenation and eight typed
RTTI descriptors, with all 38 literal ordered original FIXUPPs. The [complete DOS `setargv` startup/DBCS boss](MAINL_SETARGV_DOS_STARTUP_NATIVE_REVIEW.md)
adds 343 original CODE bytes, true sparse DATA and INIT segments, absolute
`__setargv__` PUBDEF, and 30 original logical relocation fields. Original
FIXUPP record order differs, while the two linked Japanese EXE/MAP rounds
remain byte-exact. Six [complete `streambuf`/`istream`/`ostream` methods](MAINL_STREAMBUF_IO_SIX_NATIVE_REVIEW.md)
add 673 original CODE bytes, six complete far C++ APIs and eight literal
original OMF FIXUPPs, including the three-field `ws` ordering. The [complete `checks` diagnostic C++ boss](MAINL_DIAGNOSTIC_CHECKS_FULL_NATIVE_REVIEW.md)
adds 1,708 original CODE and 143 materialized initialized DATA bytes, with
seven far methods, eight typed RTTI records and 89 exact logical FIXUPPs.
Its **89 original literal ordered FIXUPP fields now match** after a second
source declaration-order review; the entire two-round Japanese EXE/MAP
still matches. Complete Borland OBJ metadata serialization remains distinct.
Eight [complete MBCS string near/far routines](MAINL_MBCS_STRING_ROUTINES_NATIVE_REVIEW.md)
add 722 original CODE bytes, eight character-string APIs and ten literal
original `__mbctype`/`__ctype` FIXUPPs. The [complete `filebuf::overflow` buffer-management boss](MAINL_FILEBUF_OVERFLOW_FULL_NATIVE_REVIEW.md)
adds 333 original CODE bytes, exact buffered write/put/get state transitions
and three literal original far-call FIXUPPs. The [complete original `string::strip` boss](MAINL_STRING_STRIP_NATIVE_REVIEW.md)
adds 317 CODE bytes, original trim/COW logic, and both literal original
far allocation FIXUPPs in native order. The [complete `istream::get`/`getline` methods](MAINL_ISTREAM_GET_GETLINE_NATIVE_REVIEW.md)
add 652 original CODE bytes, four original literal ordered FIXUPPs and exact
two-round Japanese streambuf underflow/EOF/delimiter behavior. The [complete static `hash`/`TCharMask` boss](MAINL_HASH_STATIC_BOSS_NATIVE_REVIEW.md)
adds 421 original CODE bytes, four genuine BSS bytes, six INITDATA bytes,
three C++ far methods and 17 literal ordered original FIXUPPs. The complete [six-API `uprlwr` case-conversion boss](MAINL_UPRLWR_SIX_API_NATIVE_REVIEW.md)
adds 912 original CODE bytes across six far C++ interfaces, retains original
typed pointer/class RTTI and all 48 literal ordered FIXUPPs. [Huge 16:16 pointer add/increment members](MAINL_HUGE_POINTER_ARITHMETIC_NATIVE_REVIEW.md)
add 238 complete original CODE bytes across 12 near/far public aliases.
The related full [`h_ldiv` 32-bit division/modulo source](MAINL_H_LDIV_SCOPED_CODE_ONLY_REVIEW.md)
is byte-exact (174 CODE bytes, 12 original aliases), but two original MAP
alias order discrepancies remain and it is explicitly **not counted** in
the 408 source-linked members. The runnable
`tests.test_mainl_h_ldiv_original_scope` keeps that investigation bound to
the actual CL.LIB and native TASM without any binary patch. [Three-API `rfind` boss](MAINL_RFIND_BOSS_NATIVE_REVIEW.md) adds 971 CODE bytes. Recent substantive original-source recoveries: C++ `fstreambase`,
`strstreambase` and `iostream` constructors/destructors, the complete nine-API
`xxv` exception/termination runtime (including original DATA and BSS), ten
near/far Japanese DBCS copy/reverse/case algorithms, NEC PC-98 delay and all
five `mbyte1` conversion APIs. Representative evidence:
[C++ exception boss](MAINL_CXX_EXCEPTION_NATIVE_REVIEW.md),
[`iostream` constructors](MAINL_IOSTREAM_CONSTRUCTORS_NATIVE_REVIEW.md),
[`iostream` destructors](MAINL_IOSTREAM_DESTRUCTORS_NATIVE_REVIEW.md),
[base destructors](MAINL_BASE_DESTRUCTORS_NATIVE_REVIEW.md),
[JIS algorithms](MAINL_JIS_COPY_CASE_NATIVE_REVIEW.md),
[NEC delay and `mbyte1`](MAINL_NEC_DELAY_MBYTE_NATIVE_REVIEW.md).
The complete 342-byte [`stdiobuf::overflow`](MAINL_STDIOBUF_OVERFLOW_NATIVE_REVIEW.md)
and 346-byte [`filebuf::open`](MAINL_FILEBUF_OPEN_NATIVE_REVIEW.md)
now join the full 345-CODE/52-DATA-byte [`stdiobuf(FILE*)` constructor](MAINL_STDIOBUF_CONSTRUCTOR_NATIVE_REVIEW.md).
All three have source-bound Japanese EXE/MAP parity; their literal OMF
FIXUPP ordering is not the original. The complete 960-CODE/30-DATA-byte
 [`string::insert` exception/RTTI boss](MAINL_STRING_INSERT_BOSS_NATIVE_REVIEW.md)
 is now independently source-bound and linked exact as well. Five complete
[8086 rotation/multiply/near-and-far-copy leaves](MAINL_ASSEMBLER_LEAVES_NATIVE_REVIEW.md)
add 109 original-equal CRT CODE bytes. The second large
[bounded `string::insert` boss](MAINL_STRING_INSERT_RANGE_NATIVE_REVIEW.md)
adds 1,036 original-equal CODE bytes and 30 DATA bytes. Older milestone writeups are **historical**; consult the selected original OBJ
and current receipts rather than accepting a previous guess as fact.

The combined [ranged string insert / replace exception pair](MAINL_STRING_RANGE_BOSSES_NATIVE_REVIEW.md)
account for 2,112 original-equal CODE bytes and two 30-byte
DATA segments across the two independent checkpoints.

The latest [five exact CRT leaves](MAINL_ASSEMBLER_LEAVES_NATIVE_REVIEW.md)
add rotate, multiply, and near/far block-copy helpers. The complete
[955-byte five-API `xmsg` exception boss](MAINL_XMSG_EXCEPTION_NATIVE_REVIEW.md)
adds full symbolic RTTI and recovers the original Japanese MZ ordering
using compiler-block source ordering, rather than a link/OBJ patch.
Eight [DOS/pointer/IBM/arithmetic native leaves](MAINL_DOS_POINTER_IBM_LEAVES_NATIVE_REVIEW.md)
now add another 216 original-equal CODE bytes; their imported near frame
serialization differences remain explicitly documented.
Eight [full DOS path/ostream leaves](MAINL_STREAM_PATH_LEAVES_NATIVE_REVIEW.md)
add 248 original-equal CODE bytes, including exact stream `endl`/`ends`/
`flush` and the original `umask` global with separately documented OMF
FIXUPP ordering. Two [complete stdio flush finalizers](MAINL_STDIO_PATH_FINALIZERS_NATIVE_REVIEW.md)
add 139 original CODE bytes with five ordered original FIXUPPs. Combined
with the preceding 3+2 members, the I/O/path source-bound extension now
covers seven whole CRT members (+1,243 CODE, +4 initialized DATA).
Two [complete original current-directory and raw-write CRT members](MAINL_DIRECTORY_RAW_WRITE_NATIVE_REVIEW.md)
add 248 CODE bytes, matching eight original literal FIXUPPs and two
independent Japanese linked EXE/MAP rounds. The complete [original `write`/`setvbuf`/`fflush` I/O family](MAINL_STDIO_WRITE_BUFFER_FLUSH_NATIVE_REVIEW.md)
adds 856 CODE bytes and four initialized DATA bytes with 24 **literal
original FIXUPPs**; the source-bound driver also hashes the actual
`stdio_layout.inc` and reconciles a one-field original-library versus
standalone `write.obj` frame discrepancy. The [complete C++ operator-new boss](MAINL_NEW_OPERATOR_BOSS_NATIVE_REVIEW.md)
adds 754 original CODE bytes, genuine six-byte-uninitialized DATA,
INIT/EXIT startup hooks, three public APIs and 49 literal original
FIXUPPs. Symbolic exception/RTTI declarations also restore original
Japanese MZ chronology. Ten
[complete MBCS classifier/convert leaves](MAINL_MBCS_CLASSIFIERS_NATIVE_REVIEW.md)
add 355 original-equal CODE bytes and recover all 11 literal ordered
`__ctype`/`__mbctype` FIXUPPs, including the two-pointer class test.
The original [heap-break manager `fbrk`](MAINL_FBRK_AFTER345_NATIVE_REVIEW.md)
contributes near `__brk`/`__sbrk`, `grow_break`, 352 CODE bytes, 2 DATA bytes
and 33 literal original FIXUPPs. We verified actual CL.LIB import names and
DGROUP rather than assuming the alternate standalone OBJ is identical.
The complete [fbrk heap-break manager](MAINL_FBRK_HEAP_BREAK_NATIVE_REVIEW.md)
adds 352 original CODE bytes and two near public APIs; its original CL.LIB
member differs from standalone vendor/fbrk.obj in EXTDEF indices, DGROUP
ordering and six near-call frames, corrected without relaxing the source
reference. The original
[setenvp startup initializer](MAINL_SETENVP_STARTUP_NATIVE_REVIEW.md)
recovers all CODE/DATA, the sparse six-byte INITDATA record, and its
original **absolute `__setenvp__` public**. That genuine PUBDEF was necessary
to restore the native MAP without touching the exact EXE. The
[complete 17-method `strings` class runtime](MAINL_STRINGS_17_API_BOSS_NATIVE_REVIEW.md)
recovers 2,958 original CODE bytes and 102 DATA bytes, six global option
symbols, all 166 literal ordered FIXUPPs and all five Borland C++ RTTI
structures. The actual three original CODE4 LEDATA/FIXUPP sections guided
the source declaration order to restore original MZ chronology. The
[281-CODE/126-DATA streambuf debug printer](MAINL_STREAMBUF_DBP_NATIVE_REVIEW.md)
adds all four original formatted cursor/allocator diagnostics, complete
original OMF relocation site/frame metadata and exact Japanese native link.
The [new complete `xalloc` 513-byte exception boss](MAINL_XALLOC_EXCEPTION_NATIVE_REVIEW.md)
recovers original typed RTTI, throw/copy/destructor helpers, all 24 OMF
relocation fields and the exact ordered Japanese MZ by genuine 8086/RTTI
source declaration order. The full
[DOSCMD and DOSENV near constructor pair](MAINL_DOSCONSTRUCT_AFTER340_SOURCE_REVIEW.md)
adds 676 original-equal CODE bytes, and both original OMF member record
programs match literally in both native rounds. These constructors now share
the source-bound dependency chain with LoadProg and exec. Eight
[complete locale character / string case leaves](MAINL_LOCALE_CASE_LEAVES_NATIVE_REVIEW.md)
add 345 original CODE bytes and preserve eight literal original OMF
FIXUPP fields, including a recovered locale TARGET-frame distinction.
The [complete DOS overlay executor `__exec`](MAINL_EXEC_AFTER338_SOURCE_REVIEW.md)
recovers its 933-byte CODE segment including 257 uninitialized bytes,
original overlay continuation, 21 ordered relocations and, in both native
rounds, literal complete Borland OMF library member equality. The
[complete `__LoadProg` program-resolution boss](MAINL_LOADPROG_AFTER337_SOURCE_REVIEW.md)
adds 871 original CODE + 40 DATA bytes and resolves the two real vendor-OBJ
versus CL.LIB near-frame discrepancies at original CODE+633/+754. The original
[347-byte DBCS console `cgets`](MAINL_CGETS_DBCS_NATIVE_REVIEW.md)
adds an entire far console input/editing member and near backspace helper,
including genuine PC-98 multibyte logic. The
[complete 2,522-byte regexp matching boss](MAINL_REGEXP_MATCH_BOSS_NATIVE_REVIEW.md)
recovers all four `makepat`/`matchs`/`patcmp`/`esc` interfaces, 3 typed
CODE-resident dispatch tables, 46 original relocation fields and the exact
Japanese two-round native link. Eight
[directory/file/stream helper leaves](MAINL_STREAM_PATH_LEAVES_NATIVE_REVIEW.md)
add 248 bytes of original CODE, including three original `_TEXTA` ostream
manipulators and frame-accurate direct DGROUP `umask` access. Eight
[complete DOS file/time/memory leaves](MAINL_DOS_FILE_MEMORY_LEAVES_NATIVE_REVIEW.md)
now add another 287 original CODE bytes across independently checked native
members. The [full 1,115-byte farheap memory manager](MAINL_FARHEAP_MANAGER_NATIVE_REVIEW.md)
reconstructs the original near/far alloc/free/realloc family, original CODE
uninitialized state and even the complete literal 49-relocation Borland OMF
member record. The integrated [11-API `stringio` boss](MAINL_STRINGIO_BOSS_NATIVE_REVIEW.md)
adds 1,466 original CODE bytes after the 333-byte 13-API isctype family;
the earlier `after330` locale driver/receipt is kept byte-identical and
`stringio` is now verified as the subsequent `after331` layer.
The [complete `TRegexp` C++ boss](MAINL_REGEXP_BOSS_NATIVE_REVIEW.md)
recovers five methods, two original CODE segments (649 bytes), typed RTTI,
31 original relocations and two bytes of exported `maxpat` DATA.
The [complete 13-API locale classifier](MAINL_ISCTYPE_FAMILY_NATIVE_REVIEW.md)
adds another 333 original-equal CODE bytes with an exact original framed
`__pLocale` relocation.

The [original 310-byte `_locking` DOS file-locking boss](MAINL_DOS_LOCKING_BOSS_NATIVE_REVIEW.md)
adds the actual five-way relocatable CODE dispatch table, exact logical 16
FIXUPP fields, and reproducible full Japanese EXE/MAP; raw Borland FIXUPP
record chronology remains open.

The [original 300-CODE/12-BSS DOS INT 24h critical-error boss](MAINL_DOS_HARDERR_NATIVE_REVIEW.md)
restores its true interrupt frame, both callback conventions, four CRT APIs
and 20 exact logical relocations with native source-built Japanese EXE/MAP.

The [18 original CRT ABI leaf members](MAINL_EIGHTEEN_RUNTIME_ABI_LEAVES_NATIVE_REVIEW.md)
add 268 CODE bytes across memory, stack, C++ vector, scan and `ios` helper
APIs: 17/18 preserve literal ordered original FIXUPPs; the remaining two
`stxalc` logical relocations have a documented native chronology gap.

The [343-byte `__vector_delete_` C++ array-destructor boss](MAINL_VECTOR_DELETE_BOSS_NATIVE_REVIEW.md)
recovers reverse iteration, seven table-driven cases plus a default,
the original far free path and all nine logical OMF fields. Borland vs
TASM FIXUPP chronology differs while the Japanese EXE/MAP remains exact.

The [two complete original C++ array constructor bosses](MAINL_VECTOR_CONSTRUCTORS_BOSSES_NATIVE_REVIEW.md)
add 658 CODE bytes and full allocation/count-header/multi-ABI callback
dispatch for `vnew` and `vnewv`, retaining all 18 logical OMF relocations.

The [full original DOS date/time formatting CRT member](MAINL_DOS_DATE_TIME_FORMAT_NATIVE_REVIEW.md)
adds 272 CODE bytes: one near signed-`idiv` three-field formatter and
two far DOS date/time entry points, with two logical OMF far-call fixups.

The [complete NEC PC-98 cursor controller](MAINL_PC98_CURSOR_CONTROL_BOSS_NATIVE_REVIEW.md)
adds 346 CODE and 12 initialized DATA bytes, actual cursor video/port
control, original group order and all seven literal ordered FIXUPPs.

The [PC-98 text VRAM and double-byte character-output boss](MAINL_PC98_TEXT_VRAM_OUTPUT_BOSS_NATIVE_REVIEW.md)
adds 247 CODE + 4 BSS bytes and all 21 original literal ordered FIXUPPs
across four far/near video interface entry points.

The [complete NEC text-color and attribute boss](MAINL_PC98_TEXT_COLOR_ATTRIBUTE_BOSS_NATIVE_REVIEW.md)
adds six far APIs, 222 CODE + 128 initialized DATA bytes in four palette
tables, and all 21 original logical OMF fields in two exact native rounds.

The [ten ABI/video/stream/locale leaves](MAINL_TEN_ABI_VIDEO_LOCALE_LEAVES_NATIVE_REVIEW.md)
add 126 source CODE bytes and 59 genuine `localeconv` DATA bytes, with
three specific near-video frame gaps and a DATA FIXUPP chronology difference
kept visible in the scoped reviewer.

The [complete Japanese DOS `_makepath` boss](MAINL_DOS_MAKEPATH_BOSS_NATIVE_REVIEW.md)
adds 255 CODE bytes of far path composition, DBCS-aware trailing slash
recognition, and five original logical OMF far-call relocations.

The [original DOS `_mktemp` five-level name enumeration boss](MAINL_DOS_MKTEMP_ENUMERATION_BOSS_NATIVE_REVIEW.md)
adds 253 CODE + 7 original `XXXXXX` DATA bytes, the real DOS `access`
search loop and all four original logical OMF fields.

The [complete `stdiobuf::seekoff` C++ boss](MAINL_STDIOBUF_SEEKOFF_BOSS_NATIVE_REVIEW.md)
adds 291 original CODE bytes, real 32-bit stream offsets and put/get buffer
reset logic, with all four original logical external far FIXUPPs.

The [complete original DOS `_putenv` environment manager](MAINL_PUTENV_ENVIRONMENT_BOSS_NATIVE_REVIEW.md)
adds 261 CODE bytes, far environment vector mutation and all ten original
literal ordered FIXUPP fields with a byte-exact full Japanese native link.

The [eight original NEC/IBM machine-dispatch and DOS ABI leaves](MAINL_EIGHT_MACHINE_DISPATCH_LEAVES_NATIVE_REVIEW.md)
add 295 CODE bytes across 16-bit device-type selection, cursor services,
Pascal-cleanup GOTOXY and DOS isatty, with four scoped near-call frame gaps.

The [complete DOS absolute read/write boss](MAINL_ABSOLUTE_DOS_DISK_IO_BOSS_NATIVE_REVIEW.md)
adds 292 CODE, 2 initialized DATA and 2 BSS bytes, native 16-bit INT25h/26h
paths and eight logical OMF FIXUPPs in both exact Japanese EXE/MAP rounds.

The [two full `streambuf` bulk-transfer bosses](MAINL_STREAMBUF_BULK_TRANSFER_BOSSES_NATIVE_REVIEW.md)
add 352 CODE bytes across far buffered input/output, real virtual
underflow/overflow fallbacks and two literal original ordered FIXUPPs.

The [complete `ostream << streambuf*` boss](MAINL_OSTREAM_STREAMBUF_INSERTION_BOSS_NATIVE_REVIEW.md)
adds 290 CODE bytes including real 16-bit stream/vtable traversal,
underflow/overflow and opfx/osfx paths with all three logical FIXUPPs.

The [twelve original DOS memory/system/file leaves](MAINL_TWELVE_DOS_SYSCALL_LEAVES_NATIVE_REVIEW.md)
add 396 CODE bytes and preserve 11/12 literal ordered FIXUPPs, with a
single scoped DOSERROR near frame gap and the proved active-vs-vendor
`setblock` GROUP identity difference kept explicit.

The [complete NEC PC-98 BIOS equipment/memory/time boss](MAINL_NEC_BIOS_EQUIPMENT_BOSS_NATIVE_REVIEW.md)
adds 262 source CODE and 41 actual signature DATA bytes including real
x87/mouse/memory probes, with the literal ordered original CODE-DATA FIXUPP.

The [complete NEC PC-98 BIOS serial controller boss](MAINL_NEC_BIOS_SERIAL_CONTROLLER_BOSS_NATIVE_REVIEW.md)
adds 227 original-equal CODE bytes including BIOS INT19h/D4h/D5h,
firmware-vector handling, and original zero external FIXUPPs.

The [complete IBM text VRAM boss](MAINL_IBM_TEXT_VRAM_BOSS_NATIVE_REVIEW.md)
adds 201 CODE bytes across near pointer, synchronized copy and refresh,
with all seven original literal ordered OMF FIXUPPs.


The [eight original MBCS/far-string/BGI/strstream leaves](MAINL_EIGHT_MBCS_STRING_BGI_LEAVES_NATIVE_REVIEW.md)
add 335 CODE bytes; six members preserve literal ordered Borland OMF
FIXUPPs and two retain explicitly audited record-order gaps.

The [original NEC BIOS disk controller boss](MAINL_NEC_BIOS_DISK_CONTROLLER_BOSS_NATIVE_REVIEW.md)
adds 171 CODE and eight authentic command-table DATA bytes, the actual
INT1Bh firmware I/O path and its original literal CODE-DATA relocation.

The [complete NEC console scroll boss](MAINL_NEC_CONSOLE_SCROLL_BOSS_NATIVE_REVIEW.md)
adds 170 CODE bytes and original move/clear branches, with five
specific attested near-call OMF frame-method gaps and an exact native link.

The [complete six-way NEC/IBM console color boss](MAINL_SIX_CONSOLE_COLOR_BOSS_NATIVE_REVIEW.md)
adds six exact far APIs, 216 original CODE bytes, and all 24 logical
original OMF relocations, retaining the Borland/TASM ordering distinction.

The [original PC-98 equipment and x87 capability boss](MAINL_PC98_EQUIPMENT_FPU_BOSS_NATIVE_REVIEW.md)
adds 213 CODE bytes including the original inline infinity constant and
all ordered CS-targeted FIXUPPs for the coprocessor probe.

The [twelve original DOS drive, NEC/IBM video, MBCS and ios ABI leaves](MAINL_TWELVE_DRIVE_VIDEO_MBCS_IOS_LEAVES_NATIVE_REVIEW.md)
add 640 source CODE bytes across 12 original CRT slots, including five
specific near-call OMF frame gaps and a repaired Borland jump target.

The [complete 383-CODE/12-DATA `stdiostream(FILE*)` Boss](MAINL_STDIOSTREAM_FILE_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
recovers the actual constructor plus four typed in-CODE RTTI records,
all 15 original logical OMF fields, and both original Japanese native links.

The [paired original `stdiostream` destructor boss](MAINL_STDIOSTREAM_DESTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 356 CODE and 12 DATA bytes, four complete typed in-CODE RTTI records
and 14 logical original OMF relocations, preserving exact native EXE/MAP.

The [complete 356-CODE/12-DATA stdiostream destructor boss](MAINL_STDIOSTREAM_DESTRUCTOR_BOSS_NATIVE_REVIEW.md)
recovers real embedded/based C++ destructors, four typed RTTI records and
all 14 original logical OMF relocations in two source-bound native rounds.

The [complete ostream_withassign() constructor boss](MAINL_OSTREAM_WITHASSIGN_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 349 CODE, 20 initialized DATA bytes, three real typed RTTI records
and the symbolic CODE+131 destructor thunk, with all 16 logical FIXUPPs.

The [complete ostream_withassign destructor boss](MAINL_OSTREAM_WITHASSIGN_DESTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 333 CODE and 20 initialized DATA bytes, the true local far
this-adjusting thunk, three typed RTTI blocks and all 16 logical FIXUPPs.

The [eight original C++ stream/DOS file/NEC-IBM sound leaves](MAINL_EIGHT_STREAM_DOS_SOUND_LEAVES_NATIVE_REVIEW.md)
add 496 CODE bytes with complete native byte equality and all original
logical FIXUPPs, six with exact literal record chronology.

The [complete ostream(streambuf*) constructor boss](MAINL_OSTREAM_STREAMBUF_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 266 CODE and 20 DATA bytes with real typed RTTI, symbolic destructor
adjustment thunk and all 13 logical original OMF relocations.

The [complete istream(streambuf*) constructor boss](MAINL_ISTREAM_STREAMBUF_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 275 CODE and 20 DATA bytes, real typed input-stream RTTI,
CODE+143 destructor thunk and all 13 original logical OMF fields.

The [complete strstreambuf underflow, NEC GOTOXY and far strnset](MAINL_UNDERFLOW_NEC_FAR_STRING_NATIVE_REVIEW.md)
add 320 native-source CODE bytes, eight logical FIXUPPs and two exact
Japanese EXE/MAP rounds, including all literal NEC video FIXUPPs.

The [complete strstreambuf buffer constructor and typed vtable](MAINL_STRSTREAMBUF_BUFFER_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
add 239 CODE / 52 DATA bytes, with 20 exact original logical OMF fields,
including the distinct real DATA+28 and DATA+32 virtual method targets.

The [complete istream_withassign destructor boss](MAINL_ISTREAM_WITHASSIGN_DESTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 333 source CODE and 20 DATA bytes, a real +6 FAR this-adjustment,
three typed RTTI records and all 16 original logical OMF FIXUPPs.

The [complete istream(streambuf*,ostream*) constructor boss](MAINL_ISTREAM_TIED_STREAM_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 305 CODE and 20 DATA bytes, genuine skip/tie initialization and
all 15 original logical OMF relocations in two native rounds.

The [complete istream_withassign constructor and typed RTTI](MAINL_ISTREAM_WITHASSIGN_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 349 CODE and 20 DATA bytes, the real +6 FAR thunk and
all 16 original logical OMF relocation fields.

The [complete strstreambuf init and console clrscr recovery](MAINL_STRSTREAM_INIT_CONSOLE_CLEAR_NATIVE_REVIEW.md)
adds 272 original-equal CODE bytes across 2 native members and
12 original logical OMF fields with one narrowly attested near-call frame gap.

The [complete original istream/ostream base destructors](MAINL_BASE_ISTREAM_OSTREAM_DESTRUCTORS_NATIVE_REVIEW.md)
add 483 source CODE and 40 initialized DATA bytes with the original
FAR local thunks and all 25 true logical vtable/RTTI OMF fixups.

The [complete strstreambuf default constructor boss](MAINL_STRSTREAMBUF_DEFAULT_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 250 CODE / 52 DATA bytes with 19 exact logical OMF relocations,
two typed RTTI records, and the authentic 11-slot virtual table.

The [complete strstreambuf far-buffer constructor](MAINL_STRSTREAMBUF_FAR_BUFFER_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 254 CODE / 52 DATA bytes, two actual far buffer boundaries,
11 symbolic virtual-function slots and 19 exact logical OMF fixups.

The [complete dynamic strstreambuf(int) constructor](MAINL_STRSTREAMBUF_DYNAMIC_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 320 CODE and 52 DATA bytes, original allocation/setb behavior,
11 real virtual method symbols and all 21 original logical OMF fixups.

The [eleven original format/scanner and conio CRT leaves](MAINL_ELEVEN_FORMAT_SCAN_CONSOLE_LEAVES_NATIVE_REVIEW.md)
add 515 source CODE bytes and all 43 original logical OMF relocation
sites with fifteen explicit Borland-vs-TASM near-call frame differences.

The [complete strstreambuf destructor boss](MAINL_STRSTREAMBUF_DESTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 265 CODE / 52 DATA bytes, real far callback vs owned-array cleanup
and all 20 original logical RTTI and virtual-table OMF relocations.

The [complete istream input-prefix boss](MAINL_ISTREAM_PREFIX_BOSS_NATIVE_REVIEW.md)
adds 262 CODE bytes with true tied-stream flush, buffered character-count
checks, `skipws`, and four exact original logical OMF references.

The [complete original filebuf virtual-setbuf constructor](MAINL_FILEBUF_VIRTUAL_SETBUF_CONSTRUCTOR_NATIVE_REVIEW.md)
adds 259 CODE and 52 DATA bytes, real typed RTTI, virtual setbuf dispatch
and 19 original logical OMF FIXUPPs.

The [complete filebuf destructor and original public openprot](MAINL_FILEBUF_DESTRUCTOR_BOSS_NATIVE_REVIEW.md)
add 247 CODE / 54 DATA bytes, both native cleanup paths, the DATA+0
public ABI and all 20 logical RTTI/vtable relocations.

The [complete original streambuf base constructor boss](MAINL_STREAMBUF_BASE_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 237 original CODE and 52 DATA bytes, typed RTTI and all 16
logical OMF virtual-function table fields.

The [complete streambuf base destructor, RTTI and virtual table](MAINL_STREAMBUF_BASE_DESTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 153 source-built CODE and 52 DATA bytes, with both original far
buffer/object deletion paths and all 17 exact logical original OMF fields.

The [complete streambuf(far buffer, length) constructor boss](MAINL_STREAMBUF_BUFFER_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 258 original CODE bytes and 52 initialized DATA bytes, recovering
length-dependent far-buffer initialization, RTTI/vtable and all 16
original logical OMF relocations.

The [full streambuf setb far-buffer ownership leaf](MAINL_STREAMBUF_SETB_BUFFER_MANAGEMENT_NATIVE_REVIEW.md)
adds 176 original-equal CODE bytes and its complete literal far
delete[] FIXUPP, including conditional release, range and flag setup.

The [complete filebuf::attach descriptor boss](MAINL_FILEBUF_ATTACH_DESCRIPTOR_BOSS_NATIVE_REVIEW.md)
adds 238 original CODE bytes, handling conditional 0x204-byte far
allocation and exact put/get buffer setup with all four original
symbolic OMF relocations.

The [complete original istream() default constructor boss](MAINL_ISTREAM_DEFAULT_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 254 CODE and 20 DATA bytes including the embedded ios base,
dual virtual tables, real this-adjustment destructor thunk and all 12
original logical OMF relocations.

The [complete original ostream() default constructor boss](MAINL_OSTREAM_DEFAULT_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 245 CODE and 20 DATA bytes, recovering the ios subobject, two
virtual dispatch pointers, far this-adjustment destructor thunk,
real typed RTTI and 12 original logical FIXUPPs.

The [original strstreambuf dynamic doallocate](MAINL_STRSTREAMBUF_DYNAMIC_DOALLOCATE_NATIVE_REVIEW.md)
adds 141 original-equal CODE bytes; both allocator paths, signed
callback count, far range registration and two logical FIXUPPs
are restored without any output patching.

The [complete locale collation state machine boss](MAINL_LOCALE_COLLATION_STATE_MACHINE_BOSS_NATIVE_REVIEW.md)
adds 265 CODE bytes, retaining the true DS/ES-aware two-string
level-by-level comparison and all three **literal ordered** OMF
relocations, including the real two near weight-call references.

The [complete original IBM console DBCS scroll boss](MAINL_IBM_CONSOLE_SCROLL_DBCS_BOSS_NATIVE_REVIEW.md)
adds 184 original-equal CODE bytes, correcting a subtle wclrnorm
versus wgarbage global distinction. All 13 relocation sites, targets
and widths match; seven exact Borland TARGET-versus-TASM CODE near-call
frame gaps are independently attested and disclosed.

The [complete unsigned-char far-buffer strstreambuf constructor](MAINL_STRSTREAMBUF_UNSIGNED_BUFFER_CONSTRUCTOR_NATIVE_REVIEW.md)
adds 239 original CODE and 52 DATA bytes, with 50-byte C++ object
construction, real inherited RTTI, 11 symbolic vtable slots and
20 complete original logical OMF FIXUPPs.

The [char-pointer strstreambuf constructor](MAINL_STRSTREAMBUF_CHAR_BUFFER_CONSTRUCTOR_NATIVE_REVIEW.md)
adds another 239 CODE / 52 DATA bytes and all 20 original logical
fixups, including true RTTI and the full C++ base/vtable initialization.

The [complete stdiobuf destructor and virtual overflow flush boss](MAINL_STDIOBUF_DESTRUCTOR_VIRTUAL_FLUSH_BOSS_NATIVE_REVIEW.md)
adds 224 CODE and 52 DATA bytes, preserving the real virtual overflow
call, base destruction, conditional far delete, both typed RTTI
records and all 19 original logical OMF relocation fields.

The [complete filebuf::setbuf range and ownership routine](MAINL_FILEBUF_SETBUF_RANGE_MANAGEMENT_NATIVE_REVIEW.md)
adds 191 original CODE bytes, including the exact far-buffer guards,
threshold rules and three symbolic setb/setp/setg OMF references.

The [complete filebuf::close virtual flush and descriptor boss](MAINL_FILEBUF_CLOSE_FLUSH_DESCRIPTOR_NATIVE_REVIEW.md)
adds 174 original-equal CODE bytes including actual virtual overflow,
DOS handle cleanup, original failure states and a literal-equal OMF
FIXUPP for the far close call.

The [complete far multibyte tokenizer state-machine boss](MAINL_FAR_MBCS_TOKENIZER_STATE_MACHINE_NATIVE_REVIEW.md)
adds 230 CODE and 4 initialized DATA bytes, with a real saved far
cursor, correct DBCS lead-byte handling and all 12 original logical
OMF fixups; the native DATA-first GROUP is also original-exact.

The [complete MBSTOK multibyte tokenizer](MAINL_MBCS_TOKENIZER_STATE_MACHINE_NATIVE_REVIEW.md)
adds another 230 original CODE / 4 DATA bytes with its own saved
far cursor, true mbspbrk/mbsspnp imports, DBCS lead-byte rules,
original GROUP and all 12 logical relocation fields.

The [PC-98 video mode translator and gettextinfo boss](MAINL_PC98_VIDEO_TEXTINFO_BOSS_NATIVE_REVIEW.md)
adds 231 original-equal CODE and 16 typed DATA bytes with the actual
display-mode permutation, screen/window state and 14 OMF references.
The sole Borland/TASM WHEREXY near-call frame gap is site-locked.

The [six original stdio macro ABI entrypoints](MAINL_SIX_STDIO_INLINE_ENTRYPOINTS_BOSS_NATIVE_REVIEW.md)
add 234 original-equal CODE bytes across the actual getc/getchar/
putchar/putc/feof/ferror routines, with all 12 **literal ordered**
OMF fields matching the original.

The [exception-aware setjmp/longjmp runtime boss](MAINL_EXCEPTION_AWARE_SETJMP_LONGJMP_BOSS_NATIVE_REVIEW.md)
adds 214 original-equal CODE bytes with the real FAR saved-context
and two-stage Borland unwind paths; all four literal ordered OMF
relocation fields match.

The [original bidirectional Shift-JIS MBTOMB conversion boss](MAINL_SHIFTJIS_MBTOMB_TABLE_BOSS_NATIVE_REVIEW.md)
adds 207 original CODE and **432 real initialized DATA bytes** across
five typed Japanese character-map tables and two full conversion
procedures, with all six exact logical OMF table references.

The [complete original BCD x87 emulation conversion boss](MAINL_BCD_X87_EMULATOR_CONVERSION_BOSS_NATIVE_REVIEW.md)
adds **398 CODE and 140 typed DATA bytes** across the private exponent
helper and four FAR exports, with all 23 original emulator/data
logical OMF fixups and full native link equality. Correct TASM EMUL
restores FIDRQQ/FIERQQ/FIWRQQ naturally.

The [complete four-function complex x87 arithmetic boss](MAINL_COMPLEX_X87_FPU_ARITHMETIC_BOSS_NATIVE_REVIEW.md)
adds 364 native CODE bytes with all 55 exact original logical FPU
emulator/call OMF fields, including the true FAR complex-result
allocator and the original ordered FIERQQ/FIDRQQ/FIWRQQ imports.

The [complete far-vector-delete C++ dispatch boss](MAINL_FAR_VECTOR_DELETE_DISPATCH_BOSS_NATIVE_REVIEW.md)
adds 215 native original CODE bytes with both array metadata paths,
the real reference-count/multiply step and both far deletion calls.
Its single N_LXMUL near-call frame exception is site/target-locked.

The [complete DOS ftime/timezone/DST boss](MAINL_DOS_FTIME_TIMEZONE_DST_BOSS_NATIVE_REVIEW.md)
adds 235 original CODE bytes with true INT 21h date/time helpers,
DOS-to-Unix conversion, timezone arithmetic and native DST calls;
two exact near-call TARGET-vs-CODE frame gaps are separately audited.

The [PC-98/IBM conio rectangle dispatch boss](MAINL_PC98_IBM_CONIO_TEXT_DISPATCH_BOSS_NATIVE_REVIEW.md)
adds 210 original-equal CODE bytes with three complete FAR APIs,
six native NEC/IBM backend paths and all twelve original logical OMF
fixups, including six exact conio-type references.

The [complete original DOS DBCS path initializer and INITDATA boss](MAINL_DOS_DBCS_PATH_INITDATA_BOSS_NATIVE_REVIEW.md)
adds 208 CODE, 16 typed DATA and 6 registered INITDATA bytes
with a genuine symbolic CODE+0 initializer and all eight
original literal ordered OMF FIXUPPs. Both FAR path predicates
and the native DOS 21h 6300h bootstrap are recovered.

The [complete original localeconv FAR structure and monetary flags](MAINL_LOCALECONV_FAR_STRUCTURE_BOSS_NATIVE_REVIEW.md)
adds 212 native CODE bytes restoring ten locale far pointers,
eight numeric fields and all 41 exact logical original OMF FIXUPPs.

The [complete DOS packed date/time to UTC and DST boss](MAINL_DOS_PACKED_TIME_UTC_DST_BOSS_NATIVE_REVIEW.md)
adds 214 original CODE bytes with genuine leap-year arithmetic,
timezone/DST conversion and all five **literal ordered** OMF fixups,
including the exact negative monthDay lookup addend.

The [large x87 original OMF location-frame investigation](MAINL_LARGE_X87_LOCATION_FRAME_OMF_ANALYSIS.md)
adds a separately tested read-only decoder for isteldbl and cplx2:
their 112 and 860 original FIXUPPs, 85/734 method-4 frames,
and cplx2's true 6-byte INITDATA plus 16 unmaterialized DATA sites.
These are analysis findings, **not additional source-linked members**.

The [original stdio getw two-byte leaf](MAINL_STDIO_GETW_TWO_BYTE_LEAF_NATIVE_REVIEW.md)
adds 130 original CODE bytes, retaining both FILE buffer fast paths,
two genuine far __fgetc fallbacks and original EOF control flow.

The [complete Borland FAR heap linear search, find and insert boss](MAINL_FAR_HEAP_LINEAR_SEARCH_BOSS_NATIVE_REVIEW.md)
adds 209 CODE bytes including a true near generic search core,
FAR comparison callback, both FAR public interfaces, conditional
heap insertion and the original external N_PADA@ stride adjustment.

The [complete original DOS text-mode read/CRLF and Ctrl-Z boss](MAINL_DOS_TEXT_READ_CRLF_BOSS_NATIVE_REVIEW.md)
adds 207 original CODE bytes with real text-mode conversion,
ES-prefixed far-buffer streaming and all eight original literal
ordered OMF references, including true original GROUP layout.

The [complete original DOS int86/int86x interrupt trampoline boss](MAINL_DOS_INT86_TRAMPOLINE_BOSS_NATIVE_REVIEW.md)
adds 207 original-equal CODE bytes across both FAR APIs,
true stack-resident INT nn generation, input/output register
images and two exact literal ordered OMF references.

The [complete original FAR strtok persistent cursor and BSS boss](MAINL_FAR_STRTOK_BSS_BOSS_NATIVE_REVIEW.md)
adds 203 CODE and four actual BSS bytes, preserving all
twelve original symbolic OMF DATA/BSS-style references,
delimiter loops and native FAR token state.

The [cplx2 first-three-complete-division-functions scoped recovery](MAINL_CPLX2_THREE_DIVISION_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
proves 692 original CODE bytes and 97 original relocation
sites/targets/addends from three complete FAR C++ operators
using true EMUL x87 source. It separately discloses the 90
Borland frame-4/TASM frame-5 gaps and **does not count cplx2
as another complete CRT source member**.

The [original stdio putw little-endian two-byte leaf](MAINL_STDIO_PUTW_TWO_BYTE_LEAF_NATIVE_REVIEW.md)
adds 125 original CODE bytes retaining both FAR __fputc fallback
calls, actual Borland FILE buffer fast paths and both original
logical OMF fixups.

The [complete DOS EOF device and seek probe leaf](MAINL_DOS_EOF_SEEK_PROBE_LEAF_NATIVE_REVIEW.md)
adds 125 original-equal CODE bytes and three literal ordered
original OMF FIXUPPs, recovering DOS IOCTL, seek/end and
restore-offset probes with genuine __IOERROR propagation.

The [complete DOS chsize grow/truncate zero-fill boss](MAINL_DOS_CHSIZE_GROW_TRUNCATE_BOSS_NATIVE_REVIEW.md)
adds 199 source-equal CODE bytes with authentic 128-byte fill
loop, original file-offset restoration and two literal ordered
OMF fixups.

The [complete original ios setbase manipulator and callback boss](MAINL_IOS_SETBASE_MANIPULATOR_BOSS_NATIVE_REVIEW.md)
adds 205 CODE bytes across the basefield FAR setter and allocated
C++ manipulator object, with six logical original OMF FIXUPPs,
including true CODE segment and offset function pointers.

The [PC-98 timer IRQ, callback and INT 1Ch registration boss](MAINL_PC98_TIMER_IRQ_CALLBACK_BOSS_NATIVE_REVIEW.md)
adds 162 original CODE and 5 DATA bytes, recovering a genuine
IRQ entry, FAR callback/flags and 13 exact original logical
OMF fields including the segment-of-DGROUP relocation.

The [complete IBM PIT delay and CRT calibration INITDATA boss](MAINL_IBM_PIT_DELAY_INITDATA_BOSS_NATIVE_REVIEW.md)
adds 188 source-equal CODE bytes, four real initialized DATA
bytes and six INITDATA bytes including the symbolic FAR
CODE+35 initializer pointer. All seven original literal
ordered OMF relocations match exactly.

The [cplx2 fourth full acos body, two precise FAR-call encoding gaps](MAINL_CPLX2_ACOS_FOUR_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends natural large-Boss x87 source through original CODE+1078:
three exact division functions plus a complete acos body with
two disclosed local FAR-call shortenings. All 159 remaining
original OMF references are checked by site/target/addend and
the original 143 frame-4 fields remain unnormalized.
This is **partial, no full-source CRT credit**.

The [complete original overlap-safe FAR memory-move leaf](MAINL_FAR_MEMMOVE_OVERLAP_LEAF_NATIVE_REVIEW.md)
adds 119 native CODE bytes with authentic STD/CLD, aligned
MOVSB/REP MOVSW, two FAR exported APIs and original literal
near N_PCMP@ FIXUPP at CODE+19.

The [complete TStringRef character/capacity constructor boss](MAINL_TSTRINGREF_CHARACTER_CONSTRUCTOR_BOSS_NATIVE_REVIEW.md)
adds 197 original-equal CODE bytes with authentic FAR object
allocation, capacity rounding, malloc, memset and xalloc
address-exception handling; all seven original OMF fields match.

The [complete DOS Ctrl-Z trim/append with private seek/read helpers](MAINL_DOS_CTRLZ_TRIM_APPEND_BOSS_NATIVE_REVIEW.md)
adds 189 original CODE bytes across four native near functions,
real DOS I/O, native text sentinel handling and the original
single literal ordered far lseek FIXUPP.

The [complete original DOS spawn saved-stack/PSP exec boss](MAINL_DOS_SPAWN_CODE_STACK_STATE_BOSS_NATIVE_REVIEW.md)
adds a 198-byte source-built CODE segment, preserving its
four actual unmaterialized SS:SP words and 194 native CODE
instruction bytes, true DOS EXEC lifecycle and all seven
original literal ordered OMF fixups.

The [complete ios::setf(long) 32-bit format flag boss](MAINL_IOS_32BIT_FORMAT_FLAGS_BOSS_NATIVE_REVIEW.md)
adds 195 native CODE bytes with full mutually exclusive adjust,
base and float groups, real ios state updates and all twelve
original logical symbolic OMF relocations.

The [complete original ios(streambuf FAR*) constructor with typed RTTI](MAINL_IOS_STREAMBUF_CONSTRUCTOR_TYPED_RTTI_BOSS_NATIVE_REVIEW.md)
adds 153 original CODE and 12 initialized DATA bytes, including
the true ios vtable/destructor function pointer and all seven
original logical OMF relocations.

The [large cplx2 fifth full arg(complex) body](MAINL_CPLX2_ARG_FIVE_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends original complex x87 source through CODE+1216:
five complete FAR bodies, with 182 compared relocation
targets/addends, 163 disclosed frame-method-4 differences
and the two still-unresolved same-segment FAR call encodings.
This remains **partial, with no added complete CRT member**.

The [original ios() default constructor with typed RTTI](MAINL_IOS_DEFAULT_CONSTRUCTOR_RTTI_NATIVE_REVIEW.md)
adds 135 CODE and 12 DATA bytes, restoring the distinct native
default-construction ABI (no streambuf initializer), the
CODE+81 class descriptor, and the real DATA destructor vtable
with all six logical original OMF fields.

The [three complete itoa/ultoa/ltoa radix conversion APIs](MAINL_RADIX_ITOA_ULTOA_LTOA_NATIVE_REVIEW.md)
add 124 original CODE bytes with the true signed-decimal
conversion ABI, all three public entrypoints, and the
three precise __LONGTOA near-frame differences.

The [complete original string::contains exception/RTTI boss](MAINL_STRING_CONTAINS_EXCEPTION_RTTI_BOSS_NATIVE_REVIEW.md)
adds 200 original CODE bytes with the real native 32-byte
exception frame, typed CODE+142 string class descriptor,
actual temporary construction/find/destruction and all
11 original logical OMF relocations.

The [complete native DOS intdos/intdosx register bridge](MAINL_DOS_INTDOS_REGISTER_BRIDGE_NATIVE_REVIEW.md)
adds 146 original CODE bytes and both original literal
ordered OMF fixups, including the true INT 21h register
and FLAGS return ABI.

The [complete original FAR heap binary search boss](MAINL_FAR_HEAP_BINARY_SEARCH_BOSS_NATIVE_REVIEW.md)
adds 145 source-equal CODE bytes with real 32-bit element
midpoint arithmetic, native FAR comparator and three
precisely site-locked near-call OMF frame differences.

The [complete IBM conio six-color FAR entrypoints](MAINL_IBM_CONIO_SIX_COLOR_APIS_NATIVE_REVIEW.md)
add 160 original-equal CODE bytes with true Borland video
color/background/attribute/intensity handling and all 11
original logical __video OMF references.

The [complete DOS stime/time setter and rollover-safe getter](MAINL_DOS_STIME_TIME_ROLLOVER_NATIVE_REVIEW.md)
adds 170 original-equal CODE bytes, two native FAR APIs
and all seven exact logical DOS/Unix time OMF references.

The [complete original MKNAME/TMPNAM temporary filename and BSS boss](MAINL_DOS_TMP_NAME_COUNTER_BOSS_NATIVE_REVIEW.md)
adds 188 source-equal CODE bytes, actual nine-byte TMP/.$$$
DATA strings and a real 13-byte BSS filename buffer, with
all seven source-bound logical original OMF fixups.

The [sixth complete cplx2 FAR asin(complex) function](MAINL_CPLX2_ASIN_SIX_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends original large-Boss semantic source through CODE+1607,
with 391 more byte-exact asin instructions. All 246 emitted
relocation sites, original target names and addends match.
The two known local FAR call gaps and 218 method-4 FPU
frame differences remain explicitly unresolved; **no
complete original CRT source-member credit is claimed**.

The [complete Borland stdio startup/INITDATA boss](MAINL_STDIO_SETUPIO_INITDATA_BOSS_NATIVE_REVIEW.md)
adds 164 original CODE bytes and a real six-byte INITDATA
record. All 18 original literal ordered OMF FIXUPPs match
including 11 genuine __streams FILE-state references and
the symbolic CRT initializer pointer.

The [complete CRT exit/atexit shutdown lifecycle boss](MAINL_CRT_EXIT_ATEXIT_LIFECYCLE_BOSS_NATIVE_REVIEW.md)
adds 170 original CODE and 12 typed FAR callback DATA bytes.
It also recovers the native reverse DATA FIXUPP chronology
8/4/0 that restores exact original MZ relocation table
ordering without patching the linked executable.

The [original srand/rand 32-bit LCG seed leaf](MAINL_SRAND_RAND_NATIVE_LCG_LEAF_REVIEW.md)
adds 62 source-equal CODE and four typed mutable seed DATA
bytes, with all eight symbolic original OMF references
and the single bounded N_LXMUL near frame difference.

The [original srand/rand 32-bit LCG leaf](MAINL_RAND_LCG_SEED_LEAF_NATIVE_REVIEW.md)
adds 62 byte-exact CODE and four genuine seed DATA bytes,
with all eight original logical fields and the sole precise
N_LXMUL@ near-frame gap at CODE+38 documented.

The [original DOS region lock/unlock FAR leaf](MAINL_DOS_LOCK_UNLOCK_LEAF_NATIVE_REVIEW.md)
adds 78 byte-exact CODE bytes, both DOS 21h 5Cxxh API paths,
and both literal ordered near __IOERROR OMF references.

The [original large cplx2 seventh full atan(complex) function](MAINL_CPLX2_ATAN_SEVEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends meaningful x87 source through CODE+1890, adding
283 exact original atan bytes. 295 emitted OMF targets
and addends are now audited against 297 original prefix
fixups, with two local FAR-call gaps and 261 original
method-4 frames disclosed. No complete CRT-source credit
is claimed for partial cplx2.

The [seventh complete cplx2 FAR atan(complex) boss](MAINL_CPLX2_ATAN_SEVEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends natural x87 source through original CODE+1890,
recovering another 283 exact CODE bytes with genuine
atan/abs/arg/log and FAR allocation paths. Of 297
original fixups, 295 emitted ones match their original
locations, target names and addends. The two known
same-CODE FAR call gaps and 261 frame-method-4 FPU
differences remain independently recorded. This is
partial and **does not count as a complete CRT member**.

The [eighth complete large-cplx2 cos(complex) function](MAINL_CPLX2_COS_EIGHT_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends semantic x87 source to original CODE+2123 with
233 newly recovered cos bytes; 335 symbolic original OMF
targets/addends are checked across 337 original prefix fixups.
Two known local FAR call gaps and 295 method-4 FPU frames
remain disclosed; **no complete CRT member credit**.

The [original DOS getpass no-echo and static password buffer](MAINL_DOS_GETPASS_BSS_NATIVE_REVIEW.md)
adds 168 original CODE bytes, three prompt DATA bytes and
a genuine 9-byte BSS buffer with all nine logical OMF
references to the real stderr stream and DOS BDOS API.

The [ninth cplx2 FAR cosh(complex) function](MAINL_CPLX2_COSH_NINE_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 234 complete original-equal CODE bytes and extends the
verified source prefix through original CODE+2357. All 375
emitted symbolic OMF fields match the 377 original prefix
records except the two disclosed direct FAR calls; 329
frame-4 FPU differences remain unnormalized. No full
CRT member credit is claimed.

The [complete original DOS file-create family with four FAR exports](MAINL_DOS_CREAT_FAMILY_NATIVE_REVIEW.md)
adds 170 byte-exact CODE bytes, a true private DOS creation
engine and four native entrypoints with all four literal
ordered original OMF references.

The [complete ios::usersize FAR array growth boss](MAINL_IOS_USERSIZE_FAR_ARRAY_BOSS_NATIVE_REVIEW.md)
adds 156 original CODE bytes with actual FAR new[],
original memcpy/free, per-entry zero initialization
and three exact logical original OMF references.

The [tenth complete cplx2 exp(complex) body](MAINL_CPLX2_EXP_TEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 206 original-equal complex exponential bytes and
extends maintained source to original CODE+2563. All 403
emitted symbolic OMF fixups match original sites, names
and addends across 405 original prefix fields, retaining
two explicit local FAR-call and 353 frame-method-4 gaps.
This is partial and adds zero complete CRT members.

The [original DOS clock and CRT baseline INITDATA leaf](MAINL_CLOCK_BSS_INITDATA_NATIVE_REVIEW.md)
adds 113 exact CODE bytes, real six-byte BSS timestamp
state and six-byte CRT initialization record, with one
site-locked near N_LXMUL@ frame difference.

The [eleventh cplx2 FAR log(complex) function](MAINL_CPLX2_LOG_ELEVEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 144 fully original-equal CODE bytes; its complete
source prefix covers 2,708 original bytes and 417 matching
native symbolic fixups. The two local FAR calls and 364
original location-frame FPU differences remain disclosed.
This partial source earns no complete CRT member credit.

The [twelfth original cplx2 log10(complex) function](MAINL_CPLX2_LOG10_TWELVE_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends native large-boss source through original CODE+2867
with 160 more fully equal CODE bytes, typed exact double
DATA+28..35 and 433 matching symbolic relocations. Two
local FAR-call encodings and 377 Borland frame-method-4
differences remain explicit; cplx2 is still partial.

The [complete original ios destructor, global fmtflags and typed RTTI](MAINL_IOS_DESTRUCTOR_RTTI_VTABLE_NATIVE_REVIEW.md)
adds 141 CODE, 30 DATA and 4 BSS bytes, with five actual DATA
exports, a real BSS stdioflush symbol and all seven original
symbolic CODE/DATA relocation fields.

The [complete original DOS __rtl_read/__read two FAR entries](MAINL_DOS_RTL_READ_TWO_FAR_NATIVE_REVIEW.md)
add 78 byte-exact CODE bytes with genuine INT 21h
read, descriptor state, and both literal ordered original
OMF references at CODE+12/+44.

The [h_ldiv twelve-public 32-bit arithmetic-core source and MAP tie audit](MAINL_H_LDIV_TWELVE_API_MAP_ALIAS_PROBE.md)
recovers all 174 original CODE bytes and twelve near/far
DIV/MOD entrypoints. A real linked EXE is original-equal,
but two MAP alias ties are reversed, so this remains a
**scoped unaccepted source** and adds zero complete members.

The [full istream::do_get streambuf underflow boss](MAINL_ISTREAM_DO_GET_VIRTUAL_UNDERFLOW_NATIVE_REVIEW.md)
adds 158 byte-exact original CODE bytes, a true vtable
underflow call, FAR byte-buffer path and exactly matching
original literal ios::setstate OMF reference.

The [original cplx2 thirteenth FAR pow(complex,double) body](MAINL_CPLX2_POW_DOUBLE_THIRTEEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 358 original-equal CODE bytes and expands natural
large-boss source through original CODE+3225 with 490
matching original symbolic OMF references. The two
local-call encoding gaps and 425 FPU framing differences
remain explicitly unresolved. No complete CRT-member credit.

The [complete ostream FAR pointer and ios formatting boss](MAINL_OSTREAM_POINTER_FORMAT_FLAGS_NATIVE_REVIEW.md)
adds 135 original CODE bytes with real ios flag masking,
ulong pointer insertion, restoration of stream state
and all seven original logical symbolic OMF references.

The [fourteenth cplx2 FAR pow(double,complex) operator](MAINL_CPLX2_POW_SCALAR_COMPLEX_FOURTEEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 306 original-equal CODE bytes and a typed exact
pi double at DATA+36..43; the verified original prefix
reaches CODE+3531 with 544 matching symbolic OMF fields.
Two existing direct FAR-call gaps and 473 location-frame
FPU differences remain disclosed, with zero full-source
CRT member credit for this partial program.

The [fourteenth complete cplx2 pow(double,complex) body](MAINL_CPLX2_POW_DOUBLE_COMPLEX_FOURTEEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
extends natural large-Boss source to original CODE+3531,
adds 306 original-equal CODE bytes and exact typed pi at
DATA+36..43. All 544 emitted native OMF symbol references
are checked against 546 original prefix FIXUPPs; two FAR
call encodings and 473 frame-method-4 references remain
explicit. This is partial and adds no complete CRT credit.

The [fifteenth cplx2 pow(complex,complex) original FAR body](MAINL_CPLX2_POW_COMPLEX_COMPLEX_FIFTEEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 209 original CODE bytes and extends natural FPU
source through CODE+3740, with 572/574 symbolic
relocations audited and 496 original method-4 framing
differences still explicit. No complete CRT member credit.

The [complete original ios::pword FAR user-slot and usersize boss](MAINL_IOS_PWORD_USER_ARRAY_NATIVE_REVIEW.md)
adds 97 original CODE and four typed DATA bytes, with
real one-based userword indexing, conditional FAR
usersize expansion and four original logical OMF fields.

The [original ios::iword FAR user-array slot access](MAINL_IOS_IWORD_USER_ARRAY_NATIVE_REVIEW.md)
adds 97 CODE and four DATA bytes, true usersize expansion
and four precise logical OMF fields. Both native MAINL
EXE/MAP rounds remain original-equal.

The [complete original DOS _creat and live __exitopen callback boss](MAINL_DOS_CREAT_EXITOPEN_CALLBACK_NATIVE_REVIEW.md)
adds 156 source-equal CODE bytes, true DOS creation and
ioctl state handling and all nine literal ordered original
OMF FIXUPPs including dynamic FAR __xclose callback fields.

The [complete ios::iword FAR indexed user-slot companion](MAINL_IOS_IWORD_USER_ARRAY_NATIVE_REVIEW.md)
adds 97 byte-exact CODE and four original sentinel DATA
bytes, with exact conditional usersize expansion and
four original logical OMF relocation fields. It is a
distinct complete original module from ios::pword.

The [sixteenth complete cplx2 sin(complex) FAR function](MAINL_CPLX2_SIN_SIXTEEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 233 byte-exact CODE and the original typed -0.5
double at DATA+44, extending source to original CODE+3973.
All sixteen exports and 612/614 native symbolic OMF fields
are checked, retaining two local FAR-call and 530
frame-method-4 differences. No complete CRT-member credit.

The [seventeenth complete cplx2 sinh(complex) FAR function](MAINL_CPLX2_SINH_SEVENTEEN_FUNCTIONS_PARTIAL_NATIVE_REVIEW.md)
adds 234 byte-exact original CODE bytes through CODE+4207.
All 652 emitted symbolic OMF references match the 654
original prefix sites and targets, with two shorter acos
calls and 564 frame-method-4 differences still disclosed.
This is partial source, with zero full CRT-member credit.

The [complete original DOS dup/dup2 descriptor and exitclose boss](MAINL_DOS_DUP_DUP2_CLOSE_CALLBACK_NATIVE_REVIEW.md)
adds 116 exact CODE bytes, two native FAR interfaces,
real DOS 21h handle duplication and all 14 original
literal ordered OMF fields including FAR exitclose pointers.

The [complete original FAR strncat/strlen/fmovmem leaf](MAINL_FAR_STRNCAT_MOVMEM_LEAF_NATIVE_REVIEW.md)
adds 105 original CODE bytes, two source-real FAR
strlen calls and one real FAR memory-move call with
three exact logical OMF reference fields.

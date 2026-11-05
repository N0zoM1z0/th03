# MAINL working CRT reconstruction — historical source index

These are **historical, scoped reconstruction notes** extracted from the
former long-form agent handoff on 2026-11-05. They are not the current
acceptance ledger and should not be summed to claim product coverage;
individual module review files provide the relevant original OMF and
source/receipt details. For the verified, live total and command, return
to [the current handoff](RE_HANDOFF.md). Several historical paragraphs
refer to intermediate snapshots, not the current 536-member chain.

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

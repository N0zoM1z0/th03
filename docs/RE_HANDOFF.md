# TH03 reconstruction — agent handoff (updated 2026-11-05)

**Start here:** `git status -sb`, `git log -5 --oneline`,
[workflow](RE_WORKFLOW.md), [architecture](ARCHITECTURE.md), and
[generated progress](PROGRESS.md). Treat **all dirty work as your own**; do
not discard it because no second agent is expected to be editing this tree.
Commit meaningful advances as `gpt-web: ...`, preferably in several scoped
commits; do not push without explicit authorization.

## Current, verified MAINL working-source checkpoint

The **original Japanese PC-98** targets are pinned in
`config/targets.toml`, provenance `candidate-local-attested`. MAINL is the
ending program. **Do not** substitute translated versions, patched outputs,
TH04 binaries or the packed-game image for the pinned original decoded EXE.

| Working-source property | Current verified value |
| --- | ---: |
| Original Borland CRT member slots | 893 |
| Slots rebuilt from complete source | **397** |
| Original contextual vendor programs left unchanged | **496** |
| Source-compiled original-equal CRT CODE | **127,393 bytes** |
| Decoded original Japanese MAINL EXE size | **67,372 bytes** |
| Ordered DOS MZ relocations | **677** |
| Normal native TASM/TLIB/TLINK verification | **2 independent byte-exact EXE/MAP rounds** |

**Live proof:** `scripts/review_th03_mainl_after350_work.py stdio-flush-finalizers`
and `tests.test_mainl_after350_work`, bound to
`.analysis/work/mainl-after350-stdio-flush-finalizers-build.json`. The exact original
`after330` [13-API isctype member](MAINL_ISCTYPE_FAMILY_NATIVE_REVIEW.md)
and its independent native receipts remain available and are revalidated as
this layer's parent. The inherited
source-bound reviewers validate original OBJ/LIB/EXE/MAP vectors and logs,
without a new cold replay. This is **not** a
397-provider accepted ledger publication, a complete MAINL source tree, or
proof of byte-identical individual BCC OBJ record serialization.

Recent substantive original-source recoveries: C++ `fstreambase`,
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
The [complete `stringio` 11-API boss](MAINL_STRINGIO_BOSS_NATIVE_REVIEW.md)
adds **1,466** original-equal executable CODE bytes and far stream/string
read, write, getline and complete typed exception/RTTI support.
The [complete 13-API locale classifier](MAINL_ISCTYPE_FAMILY_NATIVE_REVIEW.md)
adds another 333 original-equal CODE bytes with an exact original framed
`__pLocale` relocation.

### Working source is not formally accepted scope

The [generated progress](PROGRESS.md) and the pinned acceptance manifests
separate decoded function ownership from the packed-file unit ledger.
Current accepted **decoded** source scope, not including the 397-source
working-only CRT expansion:

| Product | Decoded accepted scope |
| --- | --- |
| MAIN | 106 extents / 459 functions / 78,737 CODE bytes |
| OP | 60 extents / 92 procedures / 14,985 bytes (13,221 CODE + 1,764 initialized DATA) |
| MAINL | 211 extents / 288 procedures / 36,946 bytes (34,333 CODE + 2,607 initialized DATA + 6 uninitialized file DATA) |
| ZUN | 77 extents / 8,635 bytes (6,179 CODE + 2,456 DATA) |

MAINL decoded accepted source is **16,695 authored + 20,251 library bytes**,
and its accepted CRT has **28 source providers**. A linked EXE/MAP match
does **not** promote the working 397 members into the accepted ledger;
Factory acceptance and packed-file canonical unit credit remain separate.

### Open technical issues — don't overclaim

- **`xxv`**: all 649 CODE / 296 initialized DATA / 4 BSS bytes, all 24
  CODE/DATA publics (9 CODE + 15 DATA) and one BSS public and 16 relocation sites/targets/frames
  match. The typed `ORG` ordering also yields the original **ordered MZ
  table**. Literal original BCC-vs-TASM **OMF FIXUPP record order differs**.
- **`cnectxmd`**: original 505 CODE / 35 DATA match. Its 51 relocation
  sites/targets match, but near CODE+18 has TARGET frame5 in BCC and CODE
  frame0 in TASM; the literal FIXUPP sequence also differs.
- Older discrepancies in `ctime`, locale, `fclose`, `strftime`, etc. are
  indexed in [MAINL OMF gaps](MAINL_OMF_GAPS.md). These are *reviewed
  historical observations*, not universal claims about today's build.
- Source ownership of the **whole game** remains open, even with a fully
  reproduced decoded MAINL working binary. Never confuse a diagnostic
  emulator test, build receipt, accepted extent and exact source identity.

## Next agent: practical workflow

1. Inspect `git status -sb` and own any dirty files; reread actual target
   records, ABI and disassembly before relying on earlier notes.
2. Keep progress balanced: **larger Bosses** with complete executable body,
   RTTI, jump tables and DATA/BSS, plus full **small leaf** functions.
   Investigate additional game-module MAIN/OP/ZUN owned extents and
   remaining CRT members not yet source-replaced; do not assume
   historical suggested candidates are still open.
3. Rebuild only changed/impacted members using native TASM/TLIB/TLINK or
   BCC as appropriate, serialize the Wine writer, and check original selected
   OBJ sections, publics/imports, logical FIXUPPs and the entire linked
   Japanese EXE/MAP. **Do not run a new full cold replay** on an unchanged
   source-bound parent chain.
4. Record what is genuinely original, what differs only in OMF metadata,
   and what is *accepted* by the separate ledger. Commit substantial
   progress in multiple `gpt-web: ...` commits; leave no unexplained dirt.

**Small affected-scope audit (not a cold replay):**

```sh
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after350_work.py stdio-flush-finalizers
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after349_work tests.test_mainl_after350_work -v
.venv/bin/python scripts/validate_tracking.py
git diff --check
git status -sb
```

The live reviewer validates **the inherited post-62 source layers** and their
latest round, so do **not** delete inherited `.analysis/work/after*-round*`
OBJ/LIB/EXE/MAP vectors, build receipts or phase logs just because they look
old. The [storage audit](STORAGE_HANDOFF_2026-11-05.md) lists safe
regenerable scratch and notes which historical branches were retired. The
Wine prefix, Borland tools, pinned targets, runtime images and old-named
`reference.tar` are **not disposable**. Use a scoped dry-run first; the
`clean_generated.py` general preview is **not a dependency oracle**.

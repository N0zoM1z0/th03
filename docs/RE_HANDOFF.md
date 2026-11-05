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
| Slots rebuilt from complete source | **360** |
| Original contextual vendor programs left unchanged | **533** |
| Source-compiled original-equal CRT CODE | **115,155 bytes** |
| Decoded original Japanese MAINL EXE size | **67,372 bytes** |
| Ordered DOS MZ relocations | **677** |
| Normal native TASM/TLIB/TLINK verification | **2 independent byte-exact EXE/MAP rounds** |

**Live proof:** `scripts/review_th03_mainl_after334_work.py stream-path-leaves`
and `tests.test_mainl_after334_work`, bound to
`.analysis/work/mainl-after334-stream-path-leaves-build.json`. The exact original
`after330` [13-API isctype member](MAINL_ISCTYPE_FAMILY_NATIVE_REVIEW.md)
and its independent native receipts remain available and are revalidated as
this layer's parent. The inherited
source-bound reviewers validate original OBJ/LIB/EXE/MAP vectors and logs,
without a new cold replay. This is **not** a
360-provider accepted ledger publication, a complete MAINL source tree, or
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
FIXUPP ordering. Eight [directory/file/stream helper leaves](MAINL_STREAM_PATH_LEAVES_NATIVE_REVIEW.md)
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
Current accepted **decoded** source scope, not including the 360-source
working-only CRT expansion:

| Product | Decoded accepted scope |
| --- | --- |
| MAIN | 106 extents / 459 functions / 78,737 CODE bytes |
| OP | 60 extents / 92 procedures / 14,985 bytes (13,221 CODE + 1,764 initialized DATA) |
| MAINL | 211 extents / 288 procedures / 36,946 bytes (34,333 CODE + 2,607 initialized DATA + 6 uninitialized file DATA) |
| ZUN | 77 extents / 8,635 bytes (6,179 CODE + 2,456 DATA) |

MAINL decoded accepted source is **16,695 authored + 20,251 library bytes**,
and its accepted CRT has **28 source providers**. A linked EXE/MAP match
does **not** promote the working 360 members into the accepted ledger;
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
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after334_work.py stream-path-leaves
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after333_work tests.test_mainl_after334_work -v
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

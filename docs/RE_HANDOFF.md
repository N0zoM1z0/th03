# TH03 reconstruction — current handoff

**Source checkpoint: check actual Git HEAD.** New original-source work now includes `sprintf`, `calloc`, `puts`, the complete `ctime` calendar boss, `strerror`, `bsearch`, `strdup`, `abort`, `atexit`, `strcpy` and `strcat`; original source-only proof is distinct from formally accepted scope. All new commits use `gpt-web: xxx`. This file contains the operative status, not 60+ milestone entries; individual reviews retain original experiments and provenance. The next agent owns all dirty changes.

## Proven current source-only MAINL state

Use the original Japanese PC-98 TH03 targets pinned in `config/targets.toml` with provenance **`candidate-local-attested`**. MAINL is the ending program. Never substitute translated binaries, TH04 references, patched output or the packed MAINL database for the pinned original decoded target.

The *working* 893-member Borland CRT library now has **73 genuine source-compiled members** at the original member positions; **820 other member program records are unchanged**. These 73 modules emit **30,764 raw-equal original CODE bytes** (2,165 new since the 62-member carrier), with 451 additional original-equal initialized `ctime` DATA bytes and 44 bytes BSS. Two independent BCC/TASM/TLIB/TLINK rounds reproduce the **entire 67,372-byte decoded Japanese MAINL EXE and full original MAP byte-for-byte**, preserving all **677 original MZ relocations**. This does not establish complete source ownership of MAINL.

**Current 73-source proof:** `scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort-atexit-strcpy-strcat`, `tests.test_mainl_after66_work` (two independent native rounds). **Earlier 70-source proof:** `scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort` and `tests/test_mainl_after66_work.py`. **67-source incremental proof:** `scripts/review_th03_mainl_after66_work.py strerror` and `tests/test_mainl_after66_work.py`; build entry `scripts/build_th03_mainl_after66_work.py strerror` (two original native rounds). **Inherited 66-source proof:** `scripts/review_th03_mainl_after62_work.py sprintf-calloc-puts-ctime` with `tests/test_mainl_after62_work.py`. Build entry: `scripts/build_th03_mainl_after62_work.py sprintf-calloc-puts-ctime`. The inherited 62-source proof remains `scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower` and its two retained OBJ/LIB/EXE/MAP output vectors. These native incremental builds reuse the unchanged original cold pair.

**The xx boss is complete in working source.** `src/mainl/crt/xx.cpp` produces all **12,622 original CODE bytes and 187 literally equal ordered OMF fixups** via native BCC4.5 `-c -y`. **All 50 linked xx function bodies agree**, including initCatchArg, _ExceptionHandler and RTTI. Older S/TASM miniatures are separate diagnostic profiles and may have different sizes. See [complete native xx product review](MAINL_XX_PRODUCT_REVIEW.md).

The **`ctime` calendar boss** is now in working source: all 1,278 CODE / 451 DATA / 44 BSS and 101 genuine fixup locations/targets (see [ctime review](MAINL_CTIME_NATIVE_REVIEW.md)). `sprintf`/`vsprintf` (144 CODE), `calloc` (97 CODE) and `puts` (97 CODE) are also newly source-recovered; see [sprintf](MAINL_SPRINTF_NATIVE_REVIEW.md) and [calloc/puts](MAINL_CALLOC_PUTS_NATIVE_REVIEW.md). Other important original-source modules: both qsort bosses; scanner; `putc` (974 CODE); `splitpth` (850 CODE including real symbolic CODE tables); `stat` (556 CODE/4 DATA); `open` (459 CODE); `direct` (517 CODE/9 DATA); `strftime` (1,256 CODE/18 DATA); `_timecvt` (820 CODE/12 DATA); `tempnam` (395 CODE/6 DATA); and `tzset` (744 CODE/48 DATA/8 BSS/6 INITDATA). The four-segment `tzset` has **48/48 literally original ordered CODE/DATA/INITDATA fixups**. Detailed reviews: [tzset](MAINL_TZSET_NATIVE_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), [time conversion](MAINL_TIMECVT_WORK_REVIEW.md), [directory](MAINL_DIRECT_NATIVE_REVIEW.md), [putc](MAINL_PUTC_NATIVE_REVIEW.md), [splitpath](MAINL_SPLITPTH_NATIVE_REVIEW.md), [qsort](MAINL_QSORT_NATIVE_REVIEW.md), [hqsort](MAINL_HQSORT_NATIVE_REVIEW.md), [scanner](MAINL_SCANNER_NATIVE_REVIEW.md).

## Open original-object metadata gaps — do not overclaim

The **73-source linked EXE/MAP is byte-exact**, but literal native OMF details remain open for multiple existing and new members; five older members and `sprintf`, `calloc`, `puts`, `ctime`, `strerror` differ from the original **native OMF metadata**. Their source-generated CODE is original-byte-equal and their logical relocation sites/targets are reviewed, but the following are **not fully literal OMF-equal**:

| Module | Complete CODE bytes | Remaining original-OMF difference |
| --- | ---: | --- |
| `fopen` | 556 | Twelve logical fixups match, but BCC writes paired fields in a different **record order** from TASM. |
| `fclose` | 192 | Near `__MKNAME` call at CODE+163: BCC TARGET frame5, TASM CODE frame0. |
| `_timecvt` | 820 plus 12 DATA | 18 near external-helper calls: BCC TARGET frame5, TASM CODE frame0. |
| `strftime` | 1,256 plus 18 DATA | Four near `__UTOA` calls at +723/774/811/879: TARGET frame5 vs CODE frame0. |
| `tempnam` | 395 plus 6 DATA | Near `__MKNAME` call at +309: TARGET frame5 vs CODE frame0. |
| `sprintf` | 144 | TASM field ordering and two near `__VPRINTER` frame differences. |
| `calloc` | 97 | TASM field ordering and near multiply helper frame difference. |
| `puts` | 97 | TASM field ordering and near output helper frame difference. |
| `ctime` | 1,278 plus 451 DATA | Field ordering and 57 different frame methods (17 near calls, 40 DATA pointers); all 101 locations/targets agree. |
| `strerror` | 176 plus 26 DATA | Field order differs, but all twelve frames and sites/targets match. |

See [fopen](MAINL_FOPEN_WORK_REVIEW.md), [fclose](MAINL_FCLOSE_WORK_REVIEW.md), [timecvt](MAINL_TIMECVT_WORK_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), and [tempnam](MAINL_TEMPNAM_WORK_REVIEW.md). Do not silently normalize these differences or add padding, original executable byte arrays, or binary OBJ patches. The internal *far* call frame in putc was solved naturally with zero-byte scoped `ASSUME CS:NOTHING`; that is not a proven fix for the remaining external *near* calls.

## Formal accepted scope is separate

The 73-source CRT and its 30,764 original CODE bytes are **working, source-only native evidence, not new accepted ledger credit**. In the current decoded acceptance:

| Product | Accepted decoded source ownership |
| --- | --- |
| MAIN | 106 extents / 459 functions / **78,737 CODE bytes** |
| OP | 60 extents / 92 procedures / **13,221 CODE + 1,764 initialized DATA = 14,985 bytes** |
| MAINL | 211 extents / 288 procedures / **34,333 CODE + 2,607 initialized DATA + 6 uninitialized file DATA = 36,946 bytes** |
| ZUN | 77 extents / **6,179 CODE + 2,456 DATA = 8,635 bytes** |

MAINL decoded accepted scope comprises **16,695 authored + 20,251 library bytes** and its accepted CRT has **28 source providers**. The source-only 73-member working CRT is **not** a formally accepted 73-provider publication. Packed-file canonical unit credit and decoded owned source bytes are different metrics; see [generated progress](PROGRESS.md). No whole-game source-completion percentage is established.

## Next agent — commands and rules

Inspect `git status -sb` and take responsibility for all dirty work. **Commit format `gpt-web: xxx`**, with multiple focused commits for real advances; do not push without authorization.

```sh
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after62_work.py sprintf-calloc-puts-ctime
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort-atexit-strcpy-strcat
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after66_work tests.test_mainl_after62_work tests.test_mainl_posttzset_work tests.test_mainl_tzset_work
PYTHONPATH=scripts .venv/bin/python scripts/validate_tracking.py
git diff --check
```

These are *retained source-bound proof checks* with original OBJ/LIB/EXE/MAP vectors and actual writer phase logs, **not a cold replay**. If a native producer changes, rebuild just it and its dependent normal link/reviews; do not edit old receipt hashes to pass a check. Use the existing Wine lock, one allowed CPU at nice10, empty DISPLAY/WAYLAND_DISPLAY and `.venv/bin/python`; serialize all Borland writers. Re-attest a Ghidra DB before using new observations. Details: [workflow](RE_WORKFLOW.md), [architecture](ARCHITECTURE.md), [ABI/rejected hypotheses](RE_NOTES.md) and `.agents/skills/th03-re/SKILL.md`.

### Genuine next priorities

- **Other medium/large CRT units:** `strerror` (176 CODE / 26 DATA / 161 BSS) is recovered in working source ([review](MAINL_STRERROR_NATIVE_REVIEW.md)). `bsearch`, `strdup`, `abort`, `atexit`, `strcpy` and `strcat` are also now covered by [native source review](MAINL_BSEARCH_STRDUP_ABORT_NATIVE_REVIEW.md). `atexit` (49 CODE / 2 DATA / 128 BSS) plus `strcpy` and `strcat` are recovered too ([native review](MAINL_ATEXIT_STRINGS_NATIVE_REVIEW.md)). The initial `atexit` link caught missing DATA/BSS PUBDEFs, and a corresponding audit corrected five missing original `ctime` DATA PUBLICs; **never infer ABI from CODE publics alone**. Remaining candidates include other string routines and untouched calendar/stream modules. `setvbuf` (289 CODE) and `write` (358 CODE) have standalone vendor OBJ records **different from the actual selected original CRT library member**. Use the selected member as the oracle; the prior source candidates are not new recoveries.
- **Resolve literal OMF FIXUPP gaps** including `ctime` and `strerror`, keeping frame and ordering distinctions explicit; link equality alone is not literal object equality.
- **Finish the five literal OMF gaps**, always by genuine source/compiler or assembler semantics; do not treat logical link equality as literal original-OBJ equality.
- Work on MAIN/OP/ZUN through their own scoped evidence; source presence, diagnostic miniatures and target-equal mixed builds must not be counted as formal accepted ownership. Check member identity first: strncat, strncpy, memchr, strchr, memset and others are **already represented** in the source carrier.

## Protected local files and storage

Preserve installed `.analysis/toolchain/wineprefix/` (BC45, TC4, TASM and DOS drive), `.tools/` (Ghidra/JDK), `.venv/`, `_reference/ReC98/`, `ghidra-project/`, `.analysis/targets/`, `.analysis/runtime/images/` and the live `.analysis/work/` proof files. The historic-named `.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar` is **an actual OP/MAINL source input** — do not remove it.

The large `.analysis/work/` *.lib, *.exe and *.map native rounds, their source transports, context/responses, logs, and source-bound receipts form the **live cumulative verification chain**. Reviewers derive some file paths dynamically; a generic cleanup preview is not a dependency oracle. **Do not bulk prune those raw pairs.** Completed isolated Wine `TH03ML/probe/` scratch and standard Python bytecode caches, by contrast, can be regenerated. See [working-file rules](RE_WORKFLOW.md#working-files).

The accepted MAINL publication SHA256 is `de7276df0d534f40e8bb1ab84f2d054688fd1960bf8cdf92d4a8108d7b34a551`. Fixed target provenance and accepted scope belong to `config/` and current reviewers, not historic narrative snapshots. Detailed per-unit reviews are retained as historical evidence rather than repeated wholesale in this handoff. See the [2026-11-03 storage audit](STORAGE_HANDOFF_2026-11-03.md) for reclaimed scratch and protected native proofs.

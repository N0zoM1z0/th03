# TH03 reconstruction — current handoff

**Source checkpoint: 005093d** (last source recovery before handoff/cleanup commits); inspect the actual Git HEAD. All new commits use `gpt-web: xxx`. This file contains the operative status, not 60+ milestone entries; individual reviews retain original experiments and provenance. The next agent owns all dirty changes.

## Proven current source-only MAINL state

Use the original Japanese PC-98 TH03 targets pinned in `config/targets.toml` with provenance **`candidate-local-attested`**. MAINL is the ending program. Never substitute translated binaries, TH04 references, patched output or the packed MAINL database for the pinned original decoded target.

The *working* 893-member Borland CRT library has **62 genuine source-compiled members** at the original member positions; **831 other member program records are unchanged**. Those 62 modules emit **28,599 raw-equal original CODE bytes**. Two independent BCC/TASM/TLIB/TLINK rounds reproduce the **entire 67,372-byte decoded Japanese MAINL EXE and full original MAP byte-for-byte**, preserving all **677 original MZ relocations**. This does not establish complete source ownership of MAINL.

**Primary proof:** `scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower` and `tests/test_mainl_posttzset_work.py`, bound to `.analysis/work/mainl-posttzset-lsearch-getenv-access-tolower-{build,review}.json` and two retained raw OBJ/LIB/EXE/MAP output vectors. Source rebuild entry: `scripts/build_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower`.

**The xx boss is complete in working source.** `src/mainl/crt/xx.cpp` produces all **12,622 original CODE bytes and 187 literally equal ordered OMF fixups** via native BCC4.5 `-c -y`. **All 50 linked xx function bodies agree**, including initCatchArg, _ExceptionHandler and RTTI. Older S/TASM miniatures are separate diagnostic profiles and may have different sizes. See [complete native xx product review](MAINL_XX_PRODUCT_REVIEW.md).

Other important original-source modules: both qsort bosses; scanner; `putc` (974 CODE); `splitpth` (850 CODE including real symbolic CODE tables); `stat` (556 CODE/4 DATA); `open` (459 CODE); `direct` (517 CODE/9 DATA); `strftime` (1,256 CODE/18 DATA); `_timecvt` (820 CODE/12 DATA); `tempnam` (395 CODE/6 DATA); and `tzset` (744 CODE/48 DATA/8 BSS/6 INITDATA). The four-segment `tzset` has **48/48 literally original ordered CODE/DATA/INITDATA fixups**. Detailed reviews: [tzset](MAINL_TZSET_NATIVE_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), [time conversion](MAINL_TIMECVT_WORK_REVIEW.md), [directory](MAINL_DIRECT_NATIVE_REVIEW.md), [putc](MAINL_PUTC_NATIVE_REVIEW.md), [splitpath](MAINL_SPLITPTH_NATIVE_REVIEW.md), [qsort](MAINL_QSORT_NATIVE_REVIEW.md), [hqsort](MAINL_HQSORT_NATIVE_REVIEW.md), [scanner](MAINL_SCANNER_NATIVE_REVIEW.md).

## Open original-object metadata gaps — do not overclaim

The **62-source linked EXE/MAP is byte-exact**, but five sources still differ from the original **native OMF metadata**. Their source-generated CODE is original-byte-equal and their logical relocation sites/targets are reviewed, but the following are **not fully literal OMF-equal**:

| Module | Complete CODE bytes | Remaining original-OMF difference |
| --- | ---: | --- |
| `fopen` | 556 | Twelve logical fixups match, but BCC writes paired fields in a different **record order** from TASM. |
| `fclose` | 192 | Near `__MKNAME` call at CODE+163: BCC TARGET frame5, TASM CODE frame0. |
| `_timecvt` | 820 plus 12 DATA | 18 near external-helper calls: BCC TARGET frame5, TASM CODE frame0. |
| `strftime` | 1,256 plus 18 DATA | Four near `__UTOA` calls at +723/774/811/879: TARGET frame5 vs CODE frame0. |
| `tempnam` | 395 plus 6 DATA | Near `__MKNAME` call at +309: TARGET frame5 vs CODE frame0. |

See [fopen](MAINL_FOPEN_WORK_REVIEW.md), [fclose](MAINL_FCLOSE_WORK_REVIEW.md), [timecvt](MAINL_TIMECVT_WORK_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), and [tempnam](MAINL_TEMPNAM_WORK_REVIEW.md). Do not silently normalize these differences or add padding, original executable byte arrays, or binary OBJ patches. The internal *far* call frame in putc was solved naturally with zero-byte scoped `ASSUME CS:NOTHING`; that is not a proven fix for the remaining external *near* calls.

## Formal accepted scope is separate

The 62-source CRT and its 28,599 original CODE bytes are **working, source-only native evidence, not new accepted ledger credit**. In the current decoded acceptance:

| Product | Accepted decoded source ownership |
| --- | --- |
| MAIN | 106 extents / 459 functions / **78,737 CODE bytes** |
| OP | 60 extents / 92 procedures / **13,221 CODE + 1,764 initialized DATA = 14,985 bytes** |
| MAINL | 211 extents / 288 procedures / **34,333 CODE + 2,607 initialized DATA + 6 uninitialized file DATA = 36,946 bytes** |
| ZUN | 77 extents / **6,179 CODE + 2,456 DATA = 8,635 bytes** |

MAINL decoded accepted scope comprises **16,695 authored + 20,251 library bytes** and its accepted CRT has **28 source providers**. The source-only 62-member working CRT is **not** a formally accepted 62-provider publication. Packed-file canonical unit credit and decoded owned source bytes are different metrics; see [generated progress](PROGRESS.md). No whole-game source-completion percentage is established.

## Next agent — commands and rules

Inspect `git status -sb` and take responsibility for all dirty work. **Commit format `gpt-web: xxx`**, with multiple focused commits for real advances; do not push without authorization.

```sh
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttzset_work tests.test_mainl_tzset_work
PYTHONPATH=scripts .venv/bin/python scripts/validate_tracking.py
git diff --check
```

These are *retained source-bound proof checks* with original OBJ/LIB/EXE/MAP vectors and actual writer phase logs, **not a cold replay**. If a native producer changes, rebuild just it and its dependent normal link/reviews; do not edit old receipt hashes to pass a check. Use the existing Wine lock, one allowed CPU at nice10, empty DISPLAY/WAYLAND_DISPLAY and `.venv/bin/python`; serialize all Borland writers. Re-attest a Ghidra DB before using new observations. Details: [workflow](RE_WORKFLOW.md), [architecture](ARCHITECTURE.md), [ABI/rejected hypotheses](RE_NOTES.md) and `.agents/skills/th03-re/SKILL.md`.

### Genuine next priorities

- **Large boss `ctime`** (original member212): **1,278 CODE / 451 initialized DATA / 44 BSS, 101 native OMF fields**, six public routines and significant original weekday/month strings and far-pointer DATA tables. This is **not** in the 62-member source carrier.
- **Other medium/large CRT units:** `setvbuf` (289 CODE) and `write` (358 CODE) have standalone vendor OBJ records **different from the actual selected original CRT library member**. Use the selected member as the real oracle. `sprintf` (144 CODE) and other untouched units remain available.
- **Finish the five literal OMF gaps**, always by genuine source/compiler or assembler semantics; do not treat logical link equality as literal original-OBJ equality.
- Work on MAIN/OP/ZUN through their own scoped evidence; source presence, diagnostic miniatures and target-equal mixed builds must not be counted as formal accepted ownership. Check member identity first: strncat, strncpy, memchr, strchr, memset and others are **already represented** in the source carrier.

## Protected local files and storage

Preserve installed `.analysis/toolchain/wineprefix/` (BC45, TC4, TASM and DOS drive), `.tools/` (Ghidra/JDK), `.venv/`, `_reference/ReC98/`, `ghidra-project/`, `.analysis/targets/`, `.analysis/runtime/images/` and the live `.analysis/work/` proof files. The historic-named `.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar` is **an actual OP/MAINL source input** — do not remove it.

The large `.analysis/work/` *.lib, *.exe and *.map native rounds, their source transports, context/responses, logs, and source-bound receipts form the **live cumulative verification chain**. Reviewers derive some file paths dynamically; a generic cleanup preview is not a dependency oracle. **Do not bulk prune those raw pairs.** Completed isolated Wine `TH03ML/probe/` scratch and standard Python bytecode caches, by contrast, can be regenerated. See [working-file rules](RE_WORKFLOW.md#working-files).

The accepted MAINL publication SHA256 is `de7276df0d534f40e8bb1ab84f2d054688fd1960bf8cdf92d4a8108d7b34a551`. Fixed target provenance and accepted scope belong to `config/` and current reviewers, not historic narrative snapshots. Detailed per-unit reviews are retained as historical evidence rather than repeated wholesale in this handoff. See the [2026-11-03 storage audit](STORAGE_HANDOFF_2026-11-03.md) for reclaimed scratch and protected native proofs.

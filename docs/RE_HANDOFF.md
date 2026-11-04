# TH03 reconstruction — current handoff

**Source checkpoint: check actual Git HEAD.** New original-source work now includes `sprintf`, `calloc`, `puts`, the complete `ctime` calendar boss, `strerror`, `bsearch`, `strdup`, `abort`, `atexit`, `strcpy`, `strcat` and the full `vprinter` formatting boss, the `collate`/`_strxfrm` multi-function collation pair, and the four-segment `locale` lifecycle boss, and nine new far-string/ctype/math leaves; original source-only proof is distinct from formally accepted scope. All new commits use `gpt-web: xxx`. This file contains the operative status, not 60+ milestone entries; individual reviews retain original experiments and provenance. The next agent owns all dirty changes.

## Proven current source-only MAINL state

Use the original Japanese PC-98 TH03 targets pinned in `config/targets.toml` with provenance **`candidate-local-attested`**. MAINL is the ending program. Never substitute translated binaries, TH04 references, patched output or the packed MAINL database for the pinned original decoded target.

The *working* 893-member Borland CRT library now has **118 genuine source-compiled members** at the original member positions; **775 other member program records are unchanged**. These 118 modules emit **57,276 raw-equal original CODE bytes** (28,677 new since the 62-member carrier), with 451 additional original-equal initialized `ctime` DATA bytes and 44 bytes BSS. Two independent BCC/TASM/TLIB/TLINK rounds reproduce the **entire 67,372-byte decoded Japanese MAINL EXE and full original MAP byte-for-byte**, preserving all **677 original MZ relocations**. This does not establish complete source ownership of MAINL.

**Current 118-source proof:** `scripts/review_th03_mainl_after117_work.py pc98com` and `tests.test_mainl_after117_work` (ten PC-98 serial API functions, exact GROUP target at CODE+10 and two native full EXE/MAP rounds). **Inherited 117-source proof:** `scripts/review_th03_mainl_after116_work.py istelng` and `tests.test_mainl_after116_work` (full 1,439-byte C++ long input boss, two independent normal native links). **Inherited 116-source proof:** `scripts/review_th03_mainl_after112_work.py vector-family` and `tests.test_mainl_after112_work`, four original complete vector algorithms and two independent full native EXE/MAP rounds. **Inherited 112-source proof:** `scripts/review_th03_mainl_after106_work.py scan-vectors-time` and `tests.test_mainl_after106_work` (six complete original DOS/scan members and two independent normal full EXE/MAP rounds). **Inherited 106-source proof:** `scripts/review_th03_mainl_after105_work.py ioststd` and `tests.test_mainl_after105_work` (all five C++ stream lifecycle sections and two independent normal native link rounds). **Inherited 105-source proof:** `scripts/review_th03_mainl_after104_work.py constrea` and `tests.test_mainl_after104_work` (17 original C++ exports, complete RTTI/vtables and two independent native EXE/MAP rounds). **Inherited 104-source proof:** `scripts/review_th03_mainl_after103_work.py cputn` and `tests.test_mainl_after103_work`, including seven symbolic console dispatch entries, two original BSS exports and two independent native full EXE/MAP rounds. **Inherited 103-source proof:** `scripts/review_th03_mainl_after100_work.py system-scanners` and `tests.test_mainl_after100_work`, with two independent original EXE/MAP rounds. **Inherited 100-source proof:** `scripts/review_th03_mainl_after97_work.py lsetlocl-wild-vappv` and `tests.test_mainl_after97_work` (32-way vector dispatcher, two original native full EXE/MAP rounds). **Inherited 99-source proof:** `scripts/review_th03_mainl_after97_work.py lsetlocl-wild` and `tests.test_mainl_after97_work` (original CODE scratch, uninitialized DATA and two normal EXE/MAP rounds). **Inherited 98-source proof:** `scripts/review_th03_mainl_after97_work.py lsetlocl` and `tests.test_mainl_after97_work` (real 4,652-byte locale-library Boss in two independent full native EXE/MAP rounds). **Inherited 97-source proof:** `scripts/review_th03_mainl_after89_work.py utime-console` and `tests.test_mainl_after89_work` (two independent original native rounds, including all seven console/path members). **Inherited 90-source proof:** `scripts/review_th03_mainl_after89_work.py utime` and `tests.test_mainl_after89_work`, including an ancestry-DAG hash audit without recursive cold replay. **Inherited 89-source proof:** `scripts/review_th03_mainl_after87_work.py signal-fheapchk` and `tests.test_mainl_after87_work` (2 native rounds); `fheapchk` preserves all 19 literal original OMF fixups. **Inherited 88-source proof:** `scripts/review_th03_mainl_after87_work.py signal` and `tests.test_mainl_after87_work` (two independent source-bound native rounds). **Inherited 87-source proof:** `scripts/review_th03_mainl_after86_work.py lstrftim` and `tests.test_mainl_after86_work` (two complete original native rounds). **Inherited 86-source proof:** `scripts/review_th03_mainl_after77_work.py strings-ctype-math` and `tests.test_mainl_after77_work`, with two native rounds and exact `DX:AX`/ctype ABI. **Inherited 82-source proof:** `scripts/review_th03_mainl_after77_work.py strings` with `tests.test_mainl_after77_work`, 2 independent original native OBJ/LIB/EXE/MAP rounds. **Inherited 77-source proof:** `scripts/review_th03_mainl_after73_work.py vprinter-collate-strxfrm-locale` and `tests.test_mainl_after73_work`; real four-segment `locale` native source and complete EXE/MAP. **Inherited 76-source proof:** `scripts/review_th03_mainl_after73_work.py vprinter-collate-strxfrm` and `tests.test_mainl_after73_work`; the three new modules contain 31/31 literally original ordered OMF fixups. **Inherited 74-source proof:** `scripts/review_th03_mainl_after73_work.py vprinter` and `tests.test_mainl_after73_work` (two independent original native rounds). **Inherited 73-source proof:** `scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort-atexit-strcpy-strcat`, `tests.test_mainl_after66_work` (two independent native rounds). **Earlier 70-source proof:** `scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort` and `tests/test_mainl_after66_work.py`. **67-source incremental proof:** `scripts/review_th03_mainl_after66_work.py strerror` and `tests/test_mainl_after66_work.py`; build entry `scripts/build_th03_mainl_after66_work.py strerror` (two original native rounds). **Inherited 66-source proof:** `scripts/review_th03_mainl_after62_work.py sprintf-calloc-puts-ctime` with `tests/test_mainl_after62_work.py`. Build entry: `scripts/build_th03_mainl_after62_work.py sprintf-calloc-puts-ctime`. The inherited 62-source proof remains `scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower` and its two retained OBJ/LIB/EXE/MAP output vectors. These native incremental builds reuse the unchanged original cold pair.

**The xx boss is complete in working source.** `src/mainl/crt/xx.cpp` produces all **12,622 original CODE bytes and 187 literally equal ordered OMF fixups** via native BCC4.5 `-c -y`. **All 50 linked xx function bodies agree**, including initCatchArg, _ExceptionHandler and RTTI. Older S/TASM miniatures are separate diagnostic profiles and may have different sizes. See [complete native xx product review](MAINL_XX_PRODUCT_REVIEW.md).

The **`ctime` calendar boss** is now in working source: all 1,278 CODE / 451 DATA / 44 BSS and 101 genuine fixup locations/targets (see [ctime review](MAINL_CTIME_NATIVE_REVIEW.md)). `sprintf`/`vsprintf` (144 CODE), `calloc` (97 CODE) and `puts` (97 CODE) are also newly source-recovered; see [sprintf](MAINL_SPRINTF_NATIVE_REVIEW.md) and [calloc/puts](MAINL_CALLOC_PUTS_NATIVE_REVIEW.md). Other important original-source modules: both qsort bosses; scanner; `putc` (974 CODE); `splitpth` (850 CODE including real symbolic CODE tables); `stat` (556 CODE/4 DATA); `open` (459 CODE); `direct` (517 CODE/9 DATA); `strftime` (1,256 CODE/18 DATA); `_timecvt` (820 CODE/12 DATA); `tempnam` (395 CODE/6 DATA); and `tzset` (744 CODE/48 DATA/8 BSS/6 INITDATA). The four-segment `tzset` has **48/48 literally original ordered CODE/DATA/INITDATA fixups**. Detailed reviews: [tzset](MAINL_TZSET_NATIVE_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), [time conversion](MAINL_TIMECVT_WORK_REVIEW.md), [directory](MAINL_DIRECT_NATIVE_REVIEW.md), [putc](MAINL_PUTC_NATIVE_REVIEW.md), [splitpath](MAINL_SPLITPTH_NATIVE_REVIEW.md), [qsort](MAINL_QSORT_NATIVE_REVIEW.md), [hqsort](MAINL_HQSORT_NATIVE_REVIEW.md), [scanner](MAINL_SCANNER_NATIVE_REVIEW.md).

## Open original-object metadata gaps — do not overclaim

The **118-source linked EXE/MAP is byte-exact**, but literal native OMF details remain open for multiple existing and new members; five older members and `sprintf`, `calloc`, `puts`, `ctime`, `strerror`, `strxfrm` differ from the original **native OMF metadata**. Their source-generated CODE is original-byte-equal and their logical relocation sites/targets are reviewed, but the following are **not fully literal OMF-equal**:

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
| `strxfrm` | 66 | Original member129 two far-call frames/sites agree, but record ordering differs from TASM (distinct from `_strxfrm` member192). |
| `lstrftim` | 1,831 plus 23 DATA | 85 symbolic jump-table fixups agree logically; `__UTOA` at CODE+1377 uses TARGET frame5 versus TASM CODE frame0; order also differs. |
| `signal` | 769 plus 38 DATA | All 55 site-sorted frame/target fields agree; original compiler emits different FIXUPP record order. |
| `utime` | 654 plus 12 DATA | 13 external near helper calls differ TARGET frame5 vs TASM CODE frame0; all 24 sites/targets agree. |
| `lsetlocl` | 4,652 plus 59 DATA | 227 sites/targets; three near `N_LDIV@` calls: TARGET frame5 vs CODE frame0; ordering differs. |
| `wild` | 795 extent, 10 uninitialized DATA | 38 site-sorted fixups, including all frames, equal; original FIXUPP order differs. |
| `vappv` | 848 | 32 symbolic handler pointers, 34 site/target/frame-equal fixups; original record order differs. |
| `system`/`sscanf`/`scanf` | 385 / 136 / 39 plus 19 DATA | Five near external helper calls TARGET frame5 vs TASM CODE frame0, other original fields match. |
| `cputn` | 546 + 2 DATA / 4 BSS | 18 near video/output helpers use TARGET frame5 vs TASM CODE frame0; all 76 sites/targets match. |
| `constrea` | 3,241 CODE + 92 DATA | 152 site-sorted FIXUPPs including frames agree; original Borland record order differs. |
| `ioststd` | 2,088 CODE + 190 BSS + 12 INIT + 12 EXIT | 148 site-sorted FIXUPPs including frames agree; original Borland record order differs. |
| `vscanf` / `vfscanf` | 40 / 41 | One `__scanner` near-call TARGET frame5 versus CODE frame0 in each. |
| `vapp` / `vdelf` / `vnewf` / `vnewvf` | 674 / 657 / 707 / 786 | 108 sites/targets; seven near arithmetic helper frames differ TARGET5 vs CODE0; original record order differs. |
| `istelng` | 1,439 | 19 site/target/frame-equal fixups; original record order differs. |
| `pc98com` | 1,467 + 55 DATA / 54 BSS | 130 site/target/frame-equal FIXUPPs, including correct GROUP relocation; original record order differs. |
| `getcwd` | 142 | Seven sites/targets/frames agree; FIXUPP order differs. |
| `printf` / `putch` | 31 / 25 | Near formatter/output helpers: TARGET frame5 vs CODE frame0. |

See [fopen](MAINL_FOPEN_WORK_REVIEW.md), [fclose](MAINL_FCLOSE_WORK_REVIEW.md), [timecvt](MAINL_TIMECVT_WORK_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), and [tempnam](MAINL_TEMPNAM_WORK_REVIEW.md). Do not silently normalize these differences or add padding, original executable byte arrays, or binary OBJ patches. The internal *far* call frame in putc was solved naturally with zero-byte scoped `ASSUME CS:NOTHING`; that is not a proven fix for the remaining external *near* calls.

## Formal accepted scope is separate

The 118-source CRT and its 57,276 original CODE bytes are **working, source-only native evidence, not new accepted ledger credit**. In the current decoded acceptance:

| Product | Accepted decoded source ownership |
| --- | --- |
| MAIN | 106 extents / 459 functions / **78,737 CODE bytes** |
| OP | 60 extents / 92 procedures / **13,221 CODE + 1,764 initialized DATA = 14,985 bytes** |
| MAINL | 211 extents / 288 procedures / **34,333 CODE + 2,607 initialized DATA + 6 uninitialized file DATA = 36,946 bytes** |
| ZUN | 77 extents / **6,179 CODE + 2,456 DATA = 8,635 bytes** |

MAINL decoded accepted scope comprises **16,695 authored + 20,251 library bytes** and its accepted CRT has **28 source providers**. The source-only 118-member working CRT is **not** a formally accepted 118-provider publication. Packed-file canonical unit credit and decoded owned source bytes are different metrics; see [generated progress](PROGRESS.md). No whole-game source-completion percentage is established.

## Next agent — commands and rules

Inspect `git status -sb` and take responsibility for all dirty work. **Commit format `gpt-web: xxx`**, with multiple focused commits for real advances; do not push without authorization.

```sh
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after62_work.py sprintf-calloc-puts-ctime
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort-atexit-strcpy-strcat
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after73_work.py vprinter-collate-strxfrm-locale
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after77_work.py strings-ctype-math
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after86_work.py lstrftim
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after87_work.py signal-fheapchk
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after89_work.py utime-console
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after97_work.py lsetlocl-wild-vappv
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after100_work.py system-scanners
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after103_work.py cputn
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after104_work.py constrea
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after105_work.py ioststd
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after106_work.py scan-vectors-time
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after112_work.py vector-family
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after116_work.py istelng
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after117_work.py pc98com
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after117_work tests.test_mainl_after116_work tests.test_mainl_after112_work tests.test_mainl_after106_work tests.test_mainl_after105_work tests.test_mainl_after104_work tests.test_mainl_after103_work tests.test_mainl_after100_work tests.test_mainl_after97_work tests.test_mainl_after89_work tests.test_mainl_after87_work tests.test_mainl_after86_work tests.test_mainl_after77_work tests.test_mainl_after73_work tests.test_mainl_after66_work tests.test_mainl_after62_work tests.test_mainl_posttzset_work tests.test_mainl_tzset_work
PYTHONPATH=scripts .venv/bin/python scripts/validate_tracking.py
git diff --check
```

These are *retained source-bound proof checks* with original OBJ/LIB/EXE/MAP vectors and actual writer phase logs, **not a cold replay**. If a native producer changes, rebuild just it and its dependent normal link/reviews; do not edit old receipt hashes to pass a check. Use the existing Wine lock, one allowed CPU at nice10, empty DISPLAY/WAYLAND_DISPLAY and `.venv/bin/python`; serialize all Borland writers. Re-attest a Ghidra DB before using new observations. Details: [workflow](RE_WORKFLOW.md), [architecture](ARCHITECTURE.md), [ABI/rejected hypotheses](RE_NOTES.md) and `.agents/skills/th03-re/SKILL.md`.

### Genuine next priorities

- **PC-98 serial `pc98com` boss:** selected member494 has 1,467 CODE / 55 initialized DATA / 54 BSS, ten public functions and all 130 site/target/frame equal OMF fields; CODE+10 is a **DGROUP segment** relocation, not `_TEXT` ([native review](MAINL_PC98COM_NATIVE_REVIEW.md)). 118-source original EXE/MAP equal.

- **C++ long integer istream `istelng` boss:** 1,439 original-equal `_TEXTA` CODE, 4 internal routines, 19 site/target/frame identical native fixups; 117-source full original EXE/MAP ([review](MAINL_ISTELNG_NATIVE_REVIEW.md)). Literal BCC FIXUPP enumeration remains different.

- **Full vector lifecycle:** `vapp`, `vdelf`, `vnewf`, `vnewvf` now add 2,824 original-equal CODE bytes and 80 symbolic handler pointers, all 108 fixup sites/targets, seven near-call frame gaps; full 116-source link ([review](MAINL_VECTOR_FAMILY_NATIVE_REVIEW.md)).

- **Six new DOS and scanner complete native leaves:** `vscanf`, `vfscanf`, `dosvect`, `getvect`, `getdate`, `setdate` (253 original CODE, complete public ABI and 112-source product link; [review](MAINL_DOS_SCANNER_LEAVES_NATIVE_REVIEW.md)). The two near `__scanner` frames remain separate OMF gaps.

- **New full `ioststd` C++ standard stream lifecycle boss:** 2,088 CODE, 190 BSS and 12 INITDATA + 12 EXITDATA, with seven BSS PUBLICs and all **148 site/target/frame-equivalent OMF fields**; 106-source original EXE/MAP byte-exact ([review](MAINL_IOSTSTD_NATIVE_REVIEW.md)). Original FIXUPP order remains different.

- **New full `constrea` C++ console boss:** 3,241 CODE and 92 DATA, 17 C++ method PUBLICs, 2 DATA PUBLICs, five typed Borland class RTTI names and 152 site/target/frame-equal native relocations; 105-source original EXE/MAP equal ([review](MAINL_CONSTREA_NATIVE_REVIEW.md)). Literal OMF ordering remains open.

- **`cputn` PC-98 text output engine:** 546 CODE + 2 DATA + 4 BSS, 7 symbolic dispatch entries, native `__CPUTN` near callback +450 and two BSS cursor exports; 104-source original MAINL EXE/MAP equal ([review](MAINL_CPUTN_NATIVE_REVIEW.md)). 18 near-call OMF frame gaps remain bounded.

- **`system` and scanners:** DOS COMSPEC shell construction (385 CODE, 19 DATA) plus `sscanf`/`vsscanf` and `scanf` (136+39 CODE) are source-original with 33 fixup sites/targets; five original near-call frame gaps remain ([review](MAINL_SYSTEM_SCANNERS_NATIVE_REVIEW.md)). Full 103-source EXE/MAP equality.

- **New full `vappv` vector dispatcher:** 848 CODE, 32 original descriptor selectors and 32 symbolic handler offsets, all 34 site-sorted fixups (including frames), 100-source original EXE/MAP equal ([review](MAINL_VAPPV_NATIVE_REVIEW.md)). Literal BCC FIXUPP order still differs.

- **DOS startup wildcard module `wild`:** all 793 original materialized CODE bytes in its 795-byte span, all ten unmaterialized DATA bytes, full 38 site-sorted original OMF relocation frames and 99-source EXE/MAP match ([review](MAINL_WILD_NATIVE_REVIEW.md)). Original FIXUPP order is still distinct.

- **`wild` original DOS startup argument boss:** 795 CODE extent (two unmaterialized scratch bytes), 10 entirely uninitialized DATA, original 38 frame/target-matching fixups, with 99-source full EXE/MAP proof ([review](MAINL_WILD_NATIVE_REVIEW.md)). Do not confuse zero-filled view with materialized OMF bytes.

- **New locale-library Boss `lsetlocl`:** 4,652 original-equal CODE / 59 DATA, 11 complete functions, two symbolic CODE jump tables (15+7), 227 relocation sites/targets, just three near-call frame gaps; 98-source original EXE/MAP equality ([native review](MAINL_LSETLOCL_NATIVE_REVIEW.md)).

- **Console/path/printf sources:** `kbhit`, `getch`, `getche`, `ungetch`, `putch`, `printf` and `getcwd` add 338 original-equal CODE bytes plus two original `kbhit` DATA publics; [native review](MAINL_CONSOLE_PATH_NATIVE_REVIEW.md). Exact linked original Japanese 97-source EXE/MAP; separate three member-level FIXUPP gaps are not hidden.

- **New `utime` time conversion source:** original member326, 654 CODE / 12 DATA, 24 relocation sites/targets, 13 known near-call TARGET-frame versus CODE-frame differences; two 90-source original EXE/MAP rounds ([review](MAINL_UTIME_NATIVE_REVIEW.md)). A new topological source-bound receipt walker replaces exponential recursive historical review while preserving all raw evidence.

- **New `fheapchk` boss:** 665 CODE, 10 original public aliases and 19/19 literally original fixups, original 89-source EXE/MAP equal ([review](MAINL_FHEAPCHK_NATIVE_REVIEW.md)). Different from already accepted `farheap` allocator; never double-count the latter.

- **New complete `signal` boss:** original member180 now real 769 CODE / 38 DATA / 4 BSS, `_signal` and `_raise`, 55/55 relocation sites/frames and full 88-source EXE/MAP ([review](MAINL_SIGNAL_NATIVE_REVIEW.md)). Original field ordering remains a known gap. **Do not double-count `farheap`:** the existing accepted CRT already has that source owner; the standalone vendor object is a different program from the active selected slot.

- **New complete `lstrftim` boss:** selected member213 now real 1,831 CODE / 23 DATA with both ordinal/date routines and all 85 symbolic CODE dispatch entries; 128 field sites/targets, only one external near frame and original field order remain open ([native review](MAINL_LSTRFTIM_NATIVE_REVIEW.md)). Full 87-source Japanese MAINL EXE/MAP equal.

- **Numeric and ctype originals:** `toupper`, `atol`/`atoi`, `abs` and `labs` now source-equal (248 CODE with original native ABI and literal numeric fixups; [review](MAINL_AFTER77_CTYPE_MATH_REVIEW.md)).
- **Far string source batch:** `stricmp`, `strnicmp`, `strncmp`, `strcoll`, public `strxfrm` now original-CODE-equal (284 CODE; [native proof](MAINL_AFTER77_STRINGS_NATIVE_REVIEW.md)). The separate full internal `_strxfrm` is already recovered; original `strxfrm` FIXUPP order remains open.

- **New complete major `vprinter` format boss:** 1,243 CODE / 103 DATA, with all 29 original literal ordered fixups, [native review](MAINL_VPRINTER_NATIVE_REVIEW.md). Unlike most earlier source additions it matches even the fixup frame/order.
- **Native collation pair:** complete `collate` (435 CODE, six exports) and `_strxfrm` (382 CODE, two exports), including the exact two typed external OMF fixup frames [review](MAINL_COLLATE_STRXFRM_NATIVE_REVIEW.md).
- **Large locale lifecycle boss recovered:** `locale` has 950 CODE / 22 DATA / 6 EXITDATA, all 113 field sites/frames/targets and full 77-source link ([review](MAINL_LOCALE_NATIVE_REVIEW.md)). Literal OMF serialization order is still open.
- **Other medium/large CRT units:** `strerror` (176 CODE / 26 DATA / 161 BSS) is recovered in working source ([review](MAINL_STRERROR_NATIVE_REVIEW.md)). `bsearch`, `strdup`, `abort`, `atexit`, `strcpy` and `strcat` are also now covered by [native source review](MAINL_BSEARCH_STRDUP_ABORT_NATIVE_REVIEW.md). `atexit` (49 CODE / 2 DATA / 128 BSS) plus `strcpy` and `strcat` are recovered too ([native review](MAINL_ATEXIT_STRINGS_NATIVE_REVIEW.md)). The initial `atexit` link caught missing DATA/BSS PUBDEFs, and a corresponding audit corrected five missing original `ctime` DATA PUBLICs; **never infer ABI from CODE publics alone**. Remaining candidates include other string routines and untouched calendar/stream modules. `setvbuf` (289 CODE) and `write` (358 CODE) have standalone vendor OBJ records **different from the actual selected original CRT library member**. Use the selected member as the oracle; the prior source candidates are not new recoveries.
- **Resolve literal OMF FIXUPP gaps** including `ctime` and `strerror`, keeping frame and ordering distinctions explicit; link equality alone is not literal object equality.
- **Finish the five literal OMF gaps**, always by genuine source/compiler or assembler semantics; do not treat logical link equality as literal original-OBJ equality.
- Work on MAIN/OP/ZUN through their own scoped evidence; source presence, diagnostic miniatures and target-equal mixed builds must not be counted as formal accepted ownership. Check member identity first: strncat, strncpy, memchr, strchr, memset and others are **already represented** in the source carrier.

## Protected local files and storage

Preserve installed `.analysis/toolchain/wineprefix/` (BC45, TC4, TASM and DOS drive), `.tools/` (Ghidra/JDK), `.venv/`, `_reference/ReC98/`, `ghidra-project/`, `.analysis/targets/`, `.analysis/runtime/images/` and the live `.analysis/work/` proof files. The historic-named `.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar` is **an actual OP/MAINL source input** — do not remove it.

The large `.analysis/work/` *.lib, *.exe and *.map native rounds, their source transports, context/responses, logs, and source-bound receipts form the **live cumulative verification chain**. Reviewers derive some file paths dynamically; a generic cleanup preview is not a dependency oracle. **Do not bulk prune those raw pairs.** Completed isolated Wine `TH03ML/probe/` scratch and standard Python bytecode caches, by contrast, can be regenerated. See [working-file rules](RE_WORKFLOW.md#working-files).

The accepted MAINL publication SHA256 is `de7276df0d534f40e8bb1ab84f2d054688fd1960bf8cdf92d4a8108d7b34a551`. Fixed target provenance and accepted scope belong to `config/` and current reviewers, not historic narrative snapshots. Detailed per-unit reviews are retained as historical evidence rather than repeated wholesale in this handoff. See the [2026-11-03 storage audit](STORAGE_HANDOFF_2026-11-03.md) for reclaimed scratch and protected native proofs.

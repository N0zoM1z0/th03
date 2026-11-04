# TH03 reconstruction — current handoff

**Source checkpoint: check actual Git HEAD.** New original-source work now includes `sprintf`, `calloc`, `puts`, the complete `ctime` calendar boss, `strerror`, `bsearch`, `strdup`, `abort`, `atexit`, `strcpy`, `strcat` and the full `vprinter` formatting boss, the `collate`/`_strxfrm` multi-function collation pair, and the four-segment `locale` lifecycle boss, and nine new far-string/ctype/math leaves; original source-only proof is distinct from formally accepted scope. All new commits use `gpt-web: xxx`. This file contains the operative status, not 60+ milestone entries; individual reviews retain original experiments and provenance. The next agent owns all dirty changes.

## Proven current source-only MAINL state

Use the original Japanese PC-98 TH03 targets pinned in `config/targets.toml` with provenance **`candidate-local-attested`**. MAINL is the ending program. Never substitute translated binaries, TH04 references, patched output or the packed MAINL database for the pinned original decoded target.

The *working* 893-member Borland CRT library now has **261 genuine source-compiled members** at the original member positions; **632 other member program records are unchanged**. These 261 modules emit **97,661 raw-equal original CODE bytes** (69,062 new since the 62-member carrier), with 451 additional original-equal initialized `ctime` DATA bytes and 44 bytes BSS. Two independent BCC/TASM/TLIB/TLINK rounds reproduce the **entire 67,372-byte decoded Japanese MAINL EXE and full original MAP byte-for-byte**, preserving all **677 original MZ relocations**. This does not establish complete source ownership of MAINL.

**Current 261-source proof:** `scripts/review_th03_mainl_after260_work.py nec-textmode` and `tests.test_mainl_after260_work` (whole NEC video textmode boss and typed CODE jump tables, 51 original sites/targets, 50/51 frames and two exact native EXE/MAP rounds). **Inherited 260-source proof:** `scripts/review_th03_mainl_after259_work.py nec-screen-text` and `tests.test_mainl_after259_work` (three real NEC screen text APIs, all nine literally original OMF FIXUPP fields and two full native EXE/MAP rounds). **Inherited 259-source proof:** `scripts/review_th03_mainl_after258_work.py ostrstream-constructor` and `tests.test_mainl_after258_work` (extra complete C++ ostrstream constructor, two executable far adjustors, 27 exact site/target/frame fields and two original EXE/MAP rounds). **Inherited 258-source proof:** `scripts/review_th03_mainl_after256_work.py strstreambase-constructors` and `tests.test_mainl_after256_work` (two whole original C++ strstreambase constructors, genuine far thunks, 36 site/target/frame-equal relocations and two native EXE/MAP rounds). **Inherited 256-source proof:** `scripts/review_th03_mainl_after252_work.py fstreambase-constructors` and `tests.test_mainl_after252_work` (four real C++ fstreambase constructor bosses with executable far adjustors, 73 exact relocation sites/targets/frames and two original EXE/MAP rounds). **Inherited 252-source proof:** `scripts/review_th03_mainl_after232_work.py bios-dos-core-leaves` and `tests.test_mainl_after232_work` (20 original PC-98/DOS low-level algorithms, correctly encoded far indirect BIOS calls, exact empty FIXUPPs and two full native EXE/MAP rounds). **Inherited 232-source proof:** `scripts/review_th03_mainl_after214_work.py jis-multibyte-leaves` and `tests.test_mainl_after214_work` (18 complete JIS/multibyte algorithms, literal empty FIXUPPs, two exact normal EXE/MAP rounds). **Inherited 214-source proof:** `scripts/review_th03_mainl_after209_work.py ofstream-lifecycle` and `tests.test_mainl_after209_work` (four complete `ofstream` constructors, destructor, ten executable far adjustors, 135 exact frame fields and two normal native EXE/MAP rounds). **Inherited 209-source proof:** `scripts/review_th03_mainl_after204_work.py ifstream-lifecycle` and `tests.test_mainl_after204_work` (four real `ifstream` constructors and destructor, ten executable far adjustors, 135 site/target/frame original fixups and two full native EXE/MAP rounds). **Inherited 204-source proof:** `scripts/review_th03_mainl_after202_work.py filebuf-constructors` and `tests.test_mainl_after202_work` (two complete filebuf constructors and 52-byte virtual tables, two original native EXE/MAP rounds). **Inherited 202-source proof:** `scripts/review_th03_mainl_after201_work.py istrstream-more-constructors` and `tests.test_mainl_after201_work` (three complete `istrstream` C++ constructors, original class RTTI/unwind and two normal EXE/MAP rounds). **Inherited 201-source proof:** `scripts/review_th03_mainl_after185_work.py hardware-io-leaves` and `tests.test_mainl_after185_work` (16 original DOS/PC-98/C++ leaf units, literal empty OMF FIXUPPs, and two source-bound normal EXE/MAP rounds). **Inherited 185-source proof:** `scripts/review_th03_mainl_after177_work.py file-stream-methods` and `tests.test_mainl_after177_work` (eight complete filebuf/stdiobuf/istream algorithms, 32 site/target/frame-original OMF fields, two original EXE/MAP rounds). **Inherited 177-source proof:** `scripts/review_th03_mainl_after174_work.py strstream-family` and `tests.test_mainl_after174_work` (three real strstream lifecycle members, nine far destructor adjustors, 109 native fixups and two exact EXE/MAP rounds). **Inherited 174-source proof:** `scripts/review_th03_mainl_after173_work.py fstream-destructor` and `tests.test_mainl_after173_work` (real far `fstream` destructor with `EA` adjustor thunks, 36 native site/target/frame-original relocations and two full EXE/MAP rounds). **Inherited 173-source proof:** `scripts/review_th03_mainl_after169_work.py fstream-constructors` and `tests.test_mainl_after169_work` (four real fstream constructors, 12 executable far adjustor thunks, 144 site/target/frame original fixups and two complete native EXE/MAP rounds). **Inherited 169-source proof:** `scripts/review_th03_mainl_after168_work.py stsync` and `tests.test_mainl_after168_work` (real `ios::sync_with_stdio`, three typed exception frames, 66 OMF site/target/frame-equivalent fields and two full native EXE/MAP rounds). **Inherited 168-source proof:** `scripts/review_th03_mainl_after155_work.py far-string-algorithms` and `tests.test_mainl_after155_work` (13 complete far-string search/memory algorithms, literal empty FIXUPP records and two original normal EXE/MAP rounds). **Inherited 155-source proof:** `scripts/review_th03_mainl_after153_work.py strstream-destructors` and `tests.test_mainl_after153_work` (two complete C++ destructors with typed RTTI, 54 site/target/frame-equal fields and two original full EXE/MAP rounds). **Inherited 153-source proof:** `scripts/review_th03_mainl_after151_work.py strstream-constructors` and `tests.test_mainl_after151_work` (six full far C++ constructors, 89 site/target/frame-equivalent fixups and two original native EXE/MAP rounds). **Inherited 151-source proof:** `scripts/review_th03_mainl_after149_work.py constructors` and `tests.test_mainl_after149_work` (complete two `istream` / two `ostream` constructors, all 91 original relocation site/target/frame fields and two normal EXE/MAP rounds). **Inherited 149-source proof:** `scripts/review_th03_mainl_after137_work.py streambuf-ios-leaves` and `tests.test_mainl_after137_work` (12 original C++ streambuf/ios methods, 843 complete CODE bytes and two normal EXE/MAP rounds). **Inherited 137-source proof:** `scripts/review_th03_mainl_after136_work.py ostischr` and `tests.test_mainl_after136_work` (597-byte ostream character output and two normal EXE/MAP rounds). **Inherited 136-source proof:** `scripts/review_th03_mainl_after134_work.py strstream-bosses` and `tests.test_mainl_after134_work` (complete 600/512-byte seekoff/overflow and two normal EXE/MAP rounds). **Inherited 134-source proof:** `scripts/review_th03_mainl_after133_work.py cibmgptx` and `tests.test_mainl_after133_work` (three original PC-98 screen text routines with all 25 literal native FIXUPPs; full original EXE/MAP twice). **Inherited 133-source proof:** `scripts/review_th03_mainl_after131_work.py video-chain` and `tests.test_mainl_after131_work` (PC-98 BIOS initialization, real ES override, VRAM output and two native normal link rounds). **Inherited 131-source proof:** `scripts/review_th03_mainl_after130_work.py cibmscrn` and `tests.test_mainl_after130_work` (six PC-98 screen APIs and all 30 literally original ordered OMF FIXUPPs, two native full EXE/MAP rounds). **Inherited 130-source proof:** `scripts/review_th03_mainl_after129_work.py ostoutst` and `tests.test_mainl_after129_work` (815 CODE, 11 original native fields, two independent full EXE/MAP rounds). **Inherited 129-source proof:** `scripts/review_th03_mainl_after128_work.py pc98comx` and `tests.test_mainl_after128_work`, a complete 1,383-byte extended PC-98 serial boss with two independent original EXE/MAP rounds. **Inherited 128-source proof:** `scripts/review_th03_mainl_after119_work.py far-memory-leaves` and `tests.test_mainl_after119_work` (nine whole far-memory/string sources, two original normal native EXE/MAP rounds). **Inherited 119-source proof:** `scripts/review_th03_mainl_after118_work.py ostint` and `tests.test_mainl_after118_work` (original CODE/DATA, 17 native fields, one-pass source-bound 62→118 receipt DAG, and two independent original native links). **Inherited 118-source proof:** `scripts/review_th03_mainl_after117_work.py pc98com` and `tests.test_mainl_after117_work` (ten PC-98 serial API functions, exact GROUP target at CODE+10 and two native full EXE/MAP rounds). **Inherited 117-source proof:** `scripts/review_th03_mainl_after116_work.py istelng` and `tests.test_mainl_after116_work` (full 1,439-byte C++ long input boss, two independent normal native links). **Inherited 116-source proof:** `scripts/review_th03_mainl_after112_work.py vector-family` and `tests.test_mainl_after112_work`, four original complete vector algorithms and two independent full native EXE/MAP rounds. **Inherited 112-source proof:** `scripts/review_th03_mainl_after106_work.py scan-vectors-time` and `tests.test_mainl_after106_work` (six complete original DOS/scan members and two independent normal full EXE/MAP rounds). **Inherited 106-source proof:** `scripts/review_th03_mainl_after105_work.py ioststd` and `tests.test_mainl_after105_work` (all five C++ stream lifecycle sections and two independent normal native link rounds). **Inherited 105-source proof:** `scripts/review_th03_mainl_after104_work.py constrea` and `tests.test_mainl_after104_work` (17 original C++ exports, complete RTTI/vtables and two independent native EXE/MAP rounds). **Inherited 104-source proof:** `scripts/review_th03_mainl_after103_work.py cputn` and `tests.test_mainl_after103_work`, including seven symbolic console dispatch entries, two original BSS exports and two independent native full EXE/MAP rounds. **Inherited 103-source proof:** `scripts/review_th03_mainl_after100_work.py system-scanners` and `tests.test_mainl_after100_work`, with two independent original EXE/MAP rounds. **Inherited 100-source proof:** `scripts/review_th03_mainl_after97_work.py lsetlocl-wild-vappv` and `tests.test_mainl_after97_work` (32-way vector dispatcher, two original native full EXE/MAP rounds). **Inherited 99-source proof:** `scripts/review_th03_mainl_after97_work.py lsetlocl-wild` and `tests.test_mainl_after97_work` (original CODE scratch, uninitialized DATA and two normal EXE/MAP rounds). **Inherited 98-source proof:** `scripts/review_th03_mainl_after97_work.py lsetlocl` and `tests.test_mainl_after97_work` (real 4,652-byte locale-library Boss in two independent full native EXE/MAP rounds). **Inherited 97-source proof:** `scripts/review_th03_mainl_after89_work.py utime-console` and `tests.test_mainl_after89_work` (two independent original native rounds, including all seven console/path members). **Inherited 90-source proof:** `scripts/review_th03_mainl_after89_work.py utime` and `tests.test_mainl_after89_work`, including an ancestry-DAG hash audit without recursive cold replay. **Inherited 89-source proof:** `scripts/review_th03_mainl_after87_work.py signal-fheapchk` and `tests.test_mainl_after87_work` (2 native rounds); `fheapchk` preserves all 19 literal original OMF fixups. **Inherited 88-source proof:** `scripts/review_th03_mainl_after87_work.py signal` and `tests.test_mainl_after87_work` (two independent source-bound native rounds). **Inherited 87-source proof:** `scripts/review_th03_mainl_after86_work.py lstrftim` and `tests.test_mainl_after86_work` (two complete original native rounds). **Inherited 86-source proof:** `scripts/review_th03_mainl_after77_work.py strings-ctype-math` and `tests.test_mainl_after77_work`, with two native rounds and exact `DX:AX`/ctype ABI. **Inherited 82-source proof:** `scripts/review_th03_mainl_after77_work.py strings` with `tests.test_mainl_after77_work`, 2 independent original native OBJ/LIB/EXE/MAP rounds. **Inherited 77-source proof:** `scripts/review_th03_mainl_after73_work.py vprinter-collate-strxfrm-locale` and `tests.test_mainl_after73_work`; real four-segment `locale` native source and complete EXE/MAP. **Inherited 76-source proof:** `scripts/review_th03_mainl_after73_work.py vprinter-collate-strxfrm` and `tests.test_mainl_after73_work`; the three new modules contain 31/31 literally original ordered OMF fixups. **Inherited 74-source proof:** `scripts/review_th03_mainl_after73_work.py vprinter` and `tests.test_mainl_after73_work` (two independent original native rounds). **Inherited 73-source proof:** `scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort-atexit-strcpy-strcat`, `tests.test_mainl_after66_work` (two independent native rounds). **Earlier 70-source proof:** `scripts/review_th03_mainl_after66_work.py strerror-bsearch-strdup-abort` and `tests/test_mainl_after66_work.py`. **67-source incremental proof:** `scripts/review_th03_mainl_after66_work.py strerror` and `tests/test_mainl_after66_work.py`; build entry `scripts/build_th03_mainl_after66_work.py strerror` (two original native rounds). **Inherited 66-source proof:** `scripts/review_th03_mainl_after62_work.py sprintf-calloc-puts-ctime` with `tests/test_mainl_after62_work.py`. Build entry: `scripts/build_th03_mainl_after62_work.py sprintf-calloc-puts-ctime`. The inherited 62-source proof remains `scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access-tolower` and its two retained OBJ/LIB/EXE/MAP output vectors. These native incremental builds reuse the unchanged original cold pair.

**The xx boss is complete in working source.** `src/mainl/crt/xx.cpp` produces all **12,622 original CODE bytes and 187 literally equal ordered OMF fixups** via native BCC4.5 `-c -y`. **All 50 linked xx function bodies agree**, including initCatchArg, _ExceptionHandler and RTTI. Older S/TASM miniatures are separate diagnostic profiles and may have different sizes. See [complete native xx product review](MAINL_XX_PRODUCT_REVIEW.md).

The **`ctime` calendar boss** is now in working source: all 1,278 CODE / 451 DATA / 44 BSS and 101 genuine fixup locations/targets (see [ctime review](MAINL_CTIME_NATIVE_REVIEW.md)). `sprintf`/`vsprintf` (144 CODE), `calloc` (97 CODE) and `puts` (97 CODE) are also newly source-recovered; see [sprintf](MAINL_SPRINTF_NATIVE_REVIEW.md) and [calloc/puts](MAINL_CALLOC_PUTS_NATIVE_REVIEW.md). Other important original-source modules: both qsort bosses; scanner; `putc` (974 CODE); `splitpth` (850 CODE including real symbolic CODE tables); `stat` (556 CODE/4 DATA); `open` (459 CODE); `direct` (517 CODE/9 DATA); `strftime` (1,256 CODE/18 DATA); `_timecvt` (820 CODE/12 DATA); `tempnam` (395 CODE/6 DATA); and `tzset` (744 CODE/48 DATA/8 BSS/6 INITDATA). The four-segment `tzset` has **48/48 literally original ordered CODE/DATA/INITDATA fixups**. Detailed reviews: [tzset](MAINL_TZSET_NATIVE_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), [time conversion](MAINL_TIMECVT_WORK_REVIEW.md), [directory](MAINL_DIRECT_NATIVE_REVIEW.md), [putc](MAINL_PUTC_NATIVE_REVIEW.md), [splitpath](MAINL_SPLITPTH_NATIVE_REVIEW.md), [qsort](MAINL_QSORT_NATIVE_REVIEW.md), [hqsort](MAINL_HQSORT_NATIVE_REVIEW.md), [scanner](MAINL_SCANNER_NATIVE_REVIEW.md).

## Open original-object metadata gaps — do not overclaim

The **261-source linked EXE/MAP is byte-exact**, but literal native OMF details remain open for multiple existing and new members; five older members and `sprintf`, `calloc`, `puts`, `ctime`, `strerror`, `strxfrm` differ from the original **native OMF metadata**. Their source-generated CODE is original-byte-equal and their logical relocation sites/targets are reviewed, but the following are **not fully literal OMF-equal**:

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
| `ostint` | 884 + 54 DATA | 17 site/target/frame-equal FIXUPPs; original BCC record order differs. |
| `getcwd` | 142 | Seven sites/targets/frames agree; FIXUPP order differs. |
| `printf` / `putch` | 31 / 25 | Near formatter/output helpers: TARGET frame5 vs CODE frame0. |

See [fopen](MAINL_FOPEN_WORK_REVIEW.md), [fclose](MAINL_FCLOSE_WORK_REVIEW.md), [timecvt](MAINL_TIMECVT_WORK_REVIEW.md), [strftime](MAINL_STRFTIME_WORK_REVIEW.md), and [tempnam](MAINL_TEMPNAM_WORK_REVIEW.md). Do not silently normalize these differences or add padding, original executable byte arrays, or binary OBJ patches. The internal *far* call frame in putc was solved naturally with zero-byte scoped `ASSUME CS:NOTHING`; that is not a proven fix for the remaining external *near* calls.

## Formal accepted scope is separate

The 261-source CRT and its 97,661 original CODE bytes are **working, source-only native evidence, not new accepted ledger credit**. In the current decoded acceptance:

| Product | Accepted decoded source ownership |
| --- | --- |
| MAIN | 106 extents / 459 functions / **78,737 CODE bytes** |
| OP | 60 extents / 92 procedures / **13,221 CODE + 1,764 initialized DATA = 14,985 bytes** |
| MAINL | 211 extents / 288 procedures / **34,333 CODE + 2,607 initialized DATA + 6 uninitialized file DATA = 36,946 bytes** |
| ZUN | 77 extents / **6,179 CODE + 2,456 DATA = 8,635 bytes** |

MAINL decoded accepted scope comprises **16,695 authored + 20,251 library bytes** and its accepted CRT has **28 source providers**. The source-only 261-member working CRT is **not** a formally accepted 261-provider publication. Packed-file canonical unit credit and decoded owned source bytes are different metrics; see [generated progress](PROGRESS.md). No whole-game source-completion percentage is established.

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
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after118_work.py ostint
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after119_work.py far-memory-leaves
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after128_work.py pc98comx
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after129_work.py ostoutst
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after130_work.py cibmscrn
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after131_work.py video-chain
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after133_work.py cibmgptx
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after134_work.py strstream-bosses
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after136_work.py ostischr
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after137_work.py streambuf-ios-leaves
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after149_work.py constructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after151_work.py strstream-constructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after153_work.py strstream-destructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after155_work.py far-string-algorithms
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after168_work.py stsync
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after169_work.py fstream-constructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after173_work.py fstream-destructor
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after174_work.py strstream-family
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after177_work.py file-stream-methods
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after185_work.py hardware-io-leaves
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after201_work.py istrstream-more-constructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after202_work.py filebuf-constructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after204_work.py ifstream-lifecycle
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after209_work.py ofstream-lifecycle
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after214_work.py jis-multibyte-leaves
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after232_work.py bios-dos-core-leaves
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after252_work.py fstreambase-constructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after256_work.py strstreambase-constructors
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after258_work.py ostrstream-constructor
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after259_work.py nec-screen-text
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after260_work.py nec-textmode
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after260_work tests.test_mainl_after259_work tests.test_mainl_after258_work tests.test_mainl_after256_work tests.test_mainl_after252_work tests.test_mainl_after232_work tests.test_mainl_after214_work tests.test_mainl_after209_work tests.test_mainl_after204_work tests.test_mainl_after202_work tests.test_mainl_after201_work tests.test_mainl_after185_work tests.test_mainl_after177_work tests.test_mainl_after174_work tests.test_mainl_after173_work tests.test_mainl_after169_work tests.test_mainl_after168_work tests.test_mainl_after155_work tests.test_mainl_after153_work tests.test_mainl_after151_work tests.test_mainl_after149_work tests.test_mainl_after137_work tests.test_mainl_after136_work tests.test_mainl_after134_work tests.test_mainl_after133_work tests.test_mainl_after131_work tests.test_mainl_after130_work tests.test_mainl_after129_work tests.test_mainl_after128_work tests.test_mainl_after119_work tests.test_mainl_after118_work tests.test_mainl_after117_work tests.test_mainl_after116_work tests.test_mainl_after112_work tests.test_mainl_after106_work tests.test_mainl_after105_work tests.test_mainl_after104_work tests.test_mainl_after103_work tests.test_mainl_after100_work tests.test_mainl_after97_work tests.test_mainl_after89_work tests.test_mainl_after87_work tests.test_mainl_after86_work tests.test_mainl_after77_work tests.test_mainl_after73_work tests.test_mainl_after66_work tests.test_mainl_after62_work tests.test_mainl_posttzset_work tests.test_mainl_tzset_work
PYTHONPATH=scripts .venv/bin/python scripts/validate_tracking.py
git diff --check
```

These are *retained source-bound proof checks* with original OBJ/LIB/EXE/MAP vectors and actual writer phase logs, **not a cold replay**. If a native producer changes, rebuild just it and its dependent normal link/reviews; do not edit old receipt hashes to pass a check. Use the existing Wine lock, one allowed CPU at nice10, empty DISPLAY/WAYLAND_DISPLAY and `.venv/bin/python`; serialize all Borland writers. Re-attest a Ghidra DB before using new observations. Details: [workflow](RE_WORKFLOW.md), [architecture](ARCHITECTURE.md), [ABI/rejected hypotheses](RE_NOTES.md) and `.agents/skills/th03-re/SKILL.md`.

### Genuine next priorities

- **Original NEC `cnectxmd` textmode Boss:** 505 real CODE + 35 ESC DATA, 20 symbolic local relocation table entries; all 51 OMF sites/targets but one near-call frame difference at CODE+18, and **261-source** byte-identical EXE/MAP ([review](MAINL_NEC_TEXTMODE_NATIVE_REVIEW.md)).

- **Real NEC PC-98 screen `cnecgptx` APIs:** selected original slot540, three complete functions, 475 original CODE bytes, all nine literally original ordered OMF FIXUPPs, and **260-source** full exact EXE/MAP ([review](MAINL_NEC_SCREEN_TEXT_NATIVE_REVIEW.md)).

- **Remaining complete `ostrstream` constructor:** actual slot 801 `osrctr2`, 616 CODE / 28 DATA, two executable far adjustors and 27 original site/target/frame fields; **259-source** original EXE/MAP ([review](MAINL_OSTRSTREAM_DEFAULT_CONSTRUCTOR_NATIVE_REVIEW.md)).

- **Two original `strstreambase` constructors:** actual slots 850/851, 873 CODE / 40 DATA, two far adjustors, 36 original site/target/frame FIXUPPs and **258-source** Japanese EXE/MAP ([review](MAINL_STRSTREAMBASE_CONSTRUCTORS_NATIVE_REVIEW.md)).

- **Four genuine `fstreambase` constructors:** slots 719–722, 1,722 CODE / 80 DATA, four executable far adjustor thunks and 73 original site/target/frame-matched FIXUPPs; **256-source** original EXE/MAP ([review](MAINL_FSTREAMBASE_CONSTRUCTORS_NATIVE_REVIEW.md)).

- **Twenty original DOS/PC-98 BIOS and low-level CRT routines:** `longtoa`, `pc98clk`, `intr`, sound, font, near/far input and port helpers. 1,566 original CODE bytes; all literal OMF FIXUPPs empty, three original `FF /3` far stack-indirect calls, and **252-source** full original EXE/MAP ([review](MAINL_BIOS_DOS_CORE_LEAVES_NATIVE_REVIEW.md)).

- **18 original Japanese JIS/multibyte functions:** `FMBSNBSE`, `MBSNBSET`, `FMBSSET`, `MBSSET`, JIS/JMS converters, kana transforms and character classes; 1,035 original CODE bytes, literal empty FIXUPP fields and **232-source** original EXE/MAP ([review](MAINL_JIS_MULTIBYTE_LEAVES_NATIVE_REVIEW.md)).

- **Complete original C++ `ofstream` lifecycle:** selected `ofsctr1`–`ofsctr4` and `ofsdtr`, 2,984 original CODE + 140 DATA, ten real far adjustor thunks and 135 site/target/frame-original OMF fields, **214-source** exact Japanese EXE/MAP ([review](MAINL_OFSTREAM_LIFECYCLE_NATIVE_REVIEW.md)).

- **Five original C++ `ifstream` lifecycle members:** selected `ifsctr1`–`ifsctr4` and `ifsdtr`, 2,984 whole original CODE + 140 DATA, ten genuine far adjustor thunks, typed RTTI and 135 site/target/frame-equal OMF fields; **209-source** exact full EXE/MAP ([review](MAINL_IFSTREAM_LIFECYCLE_NATIVE_REVIEW.md)).

- **Two genuine C++ `filebuf` constructors:** selected original `fsbctr1`/`fsbctr2`, 719 original CODE + 104 initialized virtual table DATA bytes, 46 original OMF site/target/frame fields; **204-source** full original EXE/MAP ([review](MAINL_FILEBUF_CONSTRUCTORS_NATIVE_REVIEW.md)).

- **Extra original `istrstream` triple-constructor Boss:** selected `isrctr2`, 1,016 original CODE + 28 DATA, three full far constructors, typed RTTI and 43 site/target/frame-identical OMF fixups; **202-source** original full EXE/MAP ([review](MAINL_ISTRSTREAM_EXTRA_CONSTRUCTORS_NATIVE_REVIEW.md)).

- **Sixteen selected DOS/PC-98 BIOS and C++ streambuf leaves:** 1,007 whole original CODE, 16 literal empty OMF FIXUPP inventories, intact real-mode hardware/port ABI and two original **201-source** native full EXE/MAP rounds ([review](MAINL_DOS_PC98_IO_LEAVES_NATIVE_REVIEW.md)).

- **Eight original C++ file/stream input methods:** selected `fsbskoff`, `fsbuflow`, `fsbsync`, `sdbuflow`, `istgbuf`, `istebuf`, `istechp`, `sdbsync`: 3,076 original CODE, 32 site/target/frame original fields and **185-source** exact original EXE/MAP ([review](MAINL_FILE_INPUT_STREAM_METHODS_NATIVE_REVIEW.md)).

- **Original C++ `strstream` full lifecycle:** selected `iosrctr1`/`iosrctr2`/`iosrdtr`, 2,413 CODE + 108 DATA, nine genuine far 8086 destructor-adjustor thunks, original RTTI and 109 site/target/frame-original fields; **177-source** original EXE/MAP ([review](MAINL_STRSTREAM_FAMILY_NATIVE_REVIEW.md)).

- **Original C++ `fstream` destructor:** selected `iofsdtr`, full 735 CODE + 36 DATA, all 36 OMF site/target/frame fields including real self-targeted far `EA` thunk jumps (TASM required `ASSUME CS:NOTHING`), **174-source** original EXE/MAP ([review](MAINL_FSTREAM_DESTRUCTOR_NATIVE_REVIEW.md)).

- **Four original C++ `fstream` constructors:** selected `iofsctr1`..`iofsctr4`, 3,121 original CODE + 144 DATA, 12 real 8086 far destructor-adjustor thunks, original class RTTI and all 144 site/target/frame-identical fields; **173-source** full original EXE/MAP ([review](MAINL_FSTREAM_CONSTRUCTORS_NATIVE_REVIEW.md)).

- **C++ `ios::sync_with_stdio` Boss:** selected original `stsync`, 761 CODE + 2 DATA, 19 imports, three typed exception frames, original `cin/cout/cerr/clog` and C `FILE` buffer ownership, all 66 site/target/frame-original relocations; 169-source exact original EXE/MAP ([review](MAINL_STSYNC_NATIVE_REVIEW.md)). Literal BCC FIXUPP record sequence differs.

- **13 complete far-string search/memory leaf algorithms:** selected `fstrstr`, `fstrspn`, `fstrpbrk`, `fstrcspn`, `fstrnicm`, `fstricmp`, `fstrcat`, `fstrrev`, `fmemchr`, `fmemcmp`, `fstrlen`, `fstrlwr`, `fstrupr`, totaling 777 original CODE bytes with literally original empty FIXUPP inventories; full **168-source** product ([review](MAINL_FAR_STRING_ALGORITHMS_NATIVE_REVIEW.md)).

- **C++ `istrstream`/`ostrstream` destructor Bosses:** selected `isrdtr`/`osrdtr`, 1,158 original CODE + 56 DATA, two complete far destructors, typed RTTI and 54 site/target/frame-original relocations, **155-source** exact original EXE/MAP ([review](MAINL_STRSTREAM_DESTRUCTORS_NATIVE_REVIEW.md)). Original FIXUPP enumeration remains different.

- **Six genuine `istrstream`/`ostrstream` constructors:** selected `isrctr1`/`osrctr1`, 2,212 original CODE + 56 DATA, class RTTI/exception unwind and 89 site/target/frame-original relocations; 153-source original EXE/MAP ([review](MAINL_STRSTREAM_CONSTRUCTORS_NATIVE_REVIEW.md)). BCC FIXUPP record order still differs.

- **New original C++ `istream` / `ostream` constructor Bosses:** original selected `istx`/`ostx`, 971+927 CODE and 40 DATA, 4 complete far constructor bodies, seven RTTI/class strings per module and 91 site/target/frame-equal OMF fields; 151-source normal Japanese EXE/MAP ([review](MAINL_IO_CONSTRUCTORS_NATIVE_REVIEW.md)). Original FIXUPP sequence remains different.

- **Twelve original C++ streambuf/ios leaf functions:** 843 complete CODE bytes, original PUBLIC offsets, correct two far virtual calls, literal empty OMF FIXUPP inventories, and **149-source** exact EXE/MAP ([review](MAINL_STREAMBUF_IOS_LEAVES_NATIVE_REVIEW.md)).

- **Original C++ `ostream` character insertion:** complete 597 CODE, three genuine far virtual calls, all 5 site/target/frame-equal fixups and **137-source original EXE/MAP** ([review](MAINL_OSTISCHR_NATIVE_REVIEW.md)). Original fixup record ordering remains different.

- **Original C++ `strstreambuf` seekoff/overflow:** 600 + 512 original CODE, both complete `streambuf` pointer/growth algorithms, 9 frame-equivalent relocations and 136-source full EXE/MAP ([review](MAINL_STRSTREAM_BUFFERS_NATIVE_REVIEW.md)). BCC FIXUPP record order remains different.

- **Original PC-98 screen `cibmgptx`:** three complete text get/put/size functions, 554 CODE, all 25 original FIXUPPs literally ordered and full original **134-source** EXE/MAP ([review](MAINL_CIBMGPTX_NATIVE_REVIEW.md)); topological source-bound DAG verification replaces nested historical reviews.

- **PC-98 video `cibminit` + `cibmputn`:** complete BIOS/VRAM, 663 + 433 original CODE, 7 DATA and 12 BSS, seven-plus-four exports and 105 site/target/frame original fixups; **133-source** full original Japanese EXE/MAP ([review](MAINL_PC98_VIDEO_CHAIN_NATIVE_REVIEW.md)).

- **PC-98 `cibmscrn` direct-screen/DBCS boss:** six public APIs, 969 CODE, 15 original near/far imports, and **all 30 literally original ordered FIXUPP records**; 131-source full original EXE/MAP ([review](MAINL_CIBMSCRN_NATIVE_REVIEW.md)).

- **C++ `ostream::outstr` output core:** original member818, full 815 CODE, three far virtual calls and all 11 site/target/frame-equivalent fixups; 130-source original EXE/MAP exact ([review](MAINL_OSTOUTST_NATIVE_REVIEW.md)). Original field ordering remains different.

- **Extended PC-98 serial `pc98comx` boss:** real slot495, ten complete APIs, 1,383 original CODE / 35 DATA / 70 BSS and 58 native site/target/frame-equivalent FIXUPPs; 129-source full original EXE/MAP equal ([review](MAINL_PC98COMX_NATIVE_REVIEW.md)).

- **Nine original far-memory/string complete functions:** selected `memccpy`, `fmemccpy`, `fstrcpy`, `fstrncpy`, `fstrcmp`, `fstrncmp`, `fstrchr`, `fmemset` (two publics) and `fmemcpy` add 479 original-equal CODE bytes with fully exact **empty original OMF fixup inventory**, and 128-source original EXE/MAP ([review](MAINL_FAR_MEMORY_STRINGS_NATIVE_REVIEW.md)).

- **`ostint` signed/unsigned long output:** original member813, 884 CODE / 54 DATA, 17 site/target/frame-equal OMF relocations and full 119-source EXE/MAP ([review](MAINL_OSTINT_NATIVE_REVIEW.md)). The 62→118 original receipt DAG is now verified in one pass rather than exponentially recomputed; no cold replay.

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

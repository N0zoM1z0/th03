# MAINL working-source OMF discrepancies — historical review index

This table records **per-member differences observed during earlier source
reconstruction**, not a blanket claim that the current 319-source EXE/MAP is
wrong. The decoded Japanese EXE/MAP is **byte-identical**, including all 677
ordered MZ relocations. An original OBJ's literal OMF FIXUPP **record order**
and its frame methods are a stricter, separate acceptance question.

These notes were moved out of the live handoff on 2026-11-05. Individual
review documents and the actual original selected CRT member are authoritative
when a discrepancy is revisited; do not copy an older hypothesis untested.

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

Additional verified working-source cases:

| Module | Original selected sections | Remaining original-OMF distinction |
| --- | --- | --- |
| `xxv` | 649 CODE, 296 initialized DATA, 4 BSS | All 16 logical OMF sites/targets/frames match. Original FIXUPP record ordering differs, but source-level typed `ORG` layout recovers the **exact ordered product MZ table**; see [exception boss](MAINL_CXX_EXCEPTION_NATIVE_REVIEW.md). |
| `cnectxmd` | 505 CODE, 35 DATA | 51 logical relocation sites/targets match; only near helper call at CODE+18 uses BCC TARGET frame5 vs TASM CODE frame0, plus record order; see [NEC textmode](MAINL_NEC_TEXTMODE_NATIVE_REVIEW.md). |
| C++ `fstream` / `ifstream` / `ostream` / `iostream` families | Multiple selected CODE/DATA programs | Entire CODE/DATA and ordered linked EXE/MAP match; many selected members retain BCC-vs-TASM **literal FIXUPP record-order** differences. See the individual `MAINL_*_NATIVE_REVIEW.md` reports. |

The accepted ledger has **not** been increased by these working sources.
Do not write a native-object acceptance claim based solely on byte-identical
linked output, even when every logical relocation site and target matches.

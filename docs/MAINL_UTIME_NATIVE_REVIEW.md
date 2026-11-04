# Original Japanese TH03 MAINL CRT `utime`: timestamp conversion recovery

The actual selected Borland large-model CRT member `utime` is original slot
**326**, not a translated or standalone alternate. `src/mainl/crt/utime.asm`
recovers the complete **654-byte CODE / 12-byte initialized DATA / zero BSS**
module: DOS file opening and modification timestamp update, current DOS
calendar fallback, 32-bit epoch/tz arithmetic, leap year and daylight-saving
handling, and native DOS date/time encoding. The month-length table is
symbolic `db 31,28,...` in initialized DATA, not a padded original CODE
array or edited object. The source exposes the original far `_utime` entry
and all eleven original ordered EXTDEF imports.

TASM 5.0 `/m /mx /kh32768 /t` reproduces **all 654 CODE bytes** and all
**12 initialized DATA bytes**. The original `_BSS,_DATA` group, public name,
segment layout and all **24 native OMF relocation sites, locations, target
methods, target names and addends** match. A bounded OMF difference remains:
**13 near external helper calls** (`N_LMOD@`, `N_LDIV@`, `__ISDST`)
use the original compiler's TARGET frame5 while TASM uses CODE frame0.
Record order also differs. These are not silently normalized to literal
native-OBJ equality. Actual linked output is checked separately.

`scripts/build_th03_mainl_after89_work.py utime` starts from the retained
**89-source original Japanese MAINL CRT**. Its scoped inherited-proof walker
validates the complete 62→89 source bound DAG in topological order: original
member program records, complete stored OBJ/LIB/EXE/MAP vectors, two writer
rounds, hash-bound sources and drivers, and actual compiler/linker phase logs.
This replaces an expensive repeatedly nested reviewer invocation; it does
**not** skip any ancestor's ownership evidence or rebuild a cold product.

Two independent TASM/TLIB/TLINK rounds successfully place the recovered
`utime` at its original member index, while preserving the **803 remaining
vendor CRT programs**. Both rebuilds exactly reproduce the **complete
67,372-byte decoded Japanese MAINL EXE** and its **original MAP**, including
all **677 ordered MZ relocations**. The working CRT reaches **90 source-built
members and 38,225 original-equal CODE bytes**, with no additional formal
accepted ledger credit or claim of whole-source ownership.

Retained raw vectors and phase logs are in `.analysis/work/after89-utime-*`,
with source-hash-bound receipts `.analysis/work/mainl-after89-utime-*`.
Verify using `review_th03_mainl_after89_work.py utime` and
`tests.test_mainl_after89_work`. **No full cold replay** ran.

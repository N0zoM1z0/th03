# Entire Borland DOS tzset / ISDST: exact four-segment native source and MAINL

The original Japanese Borland C++4.5 CRT tzset owner (library member324)
is now maintained as actual 8086 source in src/mainl/crt/tzset.asm.
Its first 508 bytes implement the far _tzset initializer: environment
TZ string parsing through original __ctype/strncpy/strlen/getenv/strcpy,
the long multiplication helper, fallback JST configuration and
standard/daylight name buffers. The near __ISDST at CODE+508 is the
original 236-byte Gregorian/leap-date and daylight-saving time
predicate. These are two substantial actual algorithmic functions,
not stubs or object-code byte arrays.

The source preserves all four original native Borland OMF segments:
**744 CODE bytes**, **48 initialized DATA bytes**, **8 real BSS
bytes** and **6 actual INITDATA bytes**. The DATA contains original
month-cumulative-day WORDs, two far BSS name pointers, the original
JST -32400-second timezone default and literal TZ/JST strings.
INITDATA contains the real far _tzset initializer reference.
All six native public symbols, including DATA-exported __monthDay,
__tzname, __timezone and __daylight, and the original eight CRT
import names and indices are preserved.

The source emits **all 48 literal original ordered OMF FIXUPPs**:
45 in CODE, two far BSS pointers initialized from DATA and one
far initialization pointer in INITDATA. The exact original record
sequence, site, width, target/index, frame method, addend and
segment ownership all match. The difficult group/order traps were
resolved *at source level*: historical GRPDEF is 0aff03ff02 despite
SEGDEF ordering; the real grouped far pointer expressions must use
DGROUP:tz_buf_standard and DGROUP:tz_buf_daylight to emit original
GROUP-frame rather than TASM's default TARGET-frame. These edits
change no machine instructions or binary object records. The
maintained code is real labeled 8086 instructions with symbolic
calendar data and initialized far pointers, never copied CODE DB
arrays, synthetic NOPs or patched fixup records.

The original 893-member CRT is reconstructed with this new tzset
source in original slot324 and the previous 57 authentic source
members, including large xx, two quicksort bosses, numeric
scanner, file/path/stream modules, timecvt, strftime and tempnam.
**835 other original member program records remain byte-identical.**
Both genuine Borland TASM/TLIB/TLINK rounds reproduce the **entire
67,372-byte decoded Japanese MAINL EXE and original MAP bit-for-bit**
with all **677 original DOS MZ relocations**. The simultaneous
58-source carrier now supplies **28,211 original CODE bytes**, with
additional authentic DATA/BSS/INITDATA ownership.

Inherited original OMF metadata differences in the *other*
fopen, fclose, timecvt, strftime and tempnam modules remain open;
the new tzset member itself has complete original ordered OMF
equality. The accepted28-provider CRT, formal211-owner MAINL
ledger, pinned candidate-local-attested Japanese original and
retained cold pair are unchanged. Normal-link working-source
exactness is not new formal accepted byte credit. No full cold
replay, DIET repacking or ancestor rebuild was run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_tzset_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_tzset_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_tzset_work

Actual two-round source OBJ/LIB/EXE/MAP vectors, Borland writer
logs, source/input hashes and review receipts remain under
.analysis/work/tzset-* and mainl-tzset-native-{build,review}.json.

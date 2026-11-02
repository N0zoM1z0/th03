# Natural original DOS access: 26-byte far wrapper and 61-source Japanese MAINL

The original Borland DOS large-model CRT access (member193) now
has maintained high-level C++ source in src/mainl/crt/access.cpp.
The historical far-cdecl wrapper passes the real caller-supplied
far path and 16-bit mode to the original far __access runtime,
preserving original argument order, caller cleanup, and signed
return/error handling without modernized policy checks or stubs.

Actual BCC4.5 compilation generates **all 26 original CODE bytes**,
one native far _access public at offset0, original EXTDEF __access
and its single TARGET-framed far CALL relocation at CODE+15,
and the literal original 08ff02ff03 DATA/BSS group with no DATA
or BSS storage. The leading C underscore in the import declaration
is intentional: historical Borland C linkage emits the native
double-underscore __access external. No copied machine-code
instructions, synthesized OBJ records, padding or patches are used.

The scoped builder includes this genuine original member193
alongside the 60 previously verified original CRT source modules,
including full tzset/ISDST, lsearch/lfind, getenv, xx, two quicksort
bosses, numeric scanner and file/path/string modules. **832 other
vendor program records in the 893-member CRT remain byte-identical**.
Two independent genuine BCC/TASM/TLIB/TLINK source rounds reproduce
the **entire 67,372-byte decoded Japanese MAINL EXE** and original
MAP bit-for-bit with all **677 original MZ relocation entries**.
The simultaneous 61-source carrier now produces **28,551 exact
original CODE bytes**.

Earlier independent fopen/fclose/timecvt/strftime/tempnam raw
OMF frame/order gaps remain explicitly open; access itself is
fully native-original. The formal accepted28-provider CRT and
211-owner MAINL publication, pinned candidate-local-attested
Japanese original, and retained cold pair are unchanged.
No full cold replay or new accepted ledger credit is claimed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttzset_work.py lsearch-getenv-access
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttzset_work.py lsearch-getenv-access
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttzset_work

Both raw original OBJ/LIB/EXE/MAP native build vectors and real
compiler phase logs are retained under
.analysis/work/posttzset-lsearch-getenv-access-*.

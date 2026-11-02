# Original DOS searchstr: exact far path-resolution logic and 25-source link

The original Borland DOS large-model path search helper __searchstr
at CRT member282 now has complete maintained 8086 assembler source
in src/mainl/crt/srchstr.asm. The original function is not a small
copy leaf: it composes and tests current-directory candidates,
recognizes DOS backslash/slash/drive separators and double-byte
trailing-character boundaries, walks semicolon-separated search
path elements, checks access, then uses the original __fullpath,
_strcpy and _free services to canonicalize and release temporary
far storage. It preserves the caller's far path buffer and the
original unchecked BP frame / far-parameter ABI.

The actual Borland TASM output reproduces **all 322 original CODE
bytes and both initialized DATA bytes** (DOS backslash, NUL),
as well as the public __searchstr at offset0, empty BSS,
literal DATA/BSS group 08ff02ff03, and all eight original
EXTDEF names in the exact original order:
__getdcwd, _strcat, _strcpy, _strlen, _free, __fullpath,
__access and ___path_issbcs.

**All ten original literal ordered OMF FIXUPPs match**, including
the descending CODE-site writer order (309,298,268,167,150,
130,120,107,44,22). This mattered: the first ordinary forward
TASM source had complete byte-exact CODE/DATA and all ten
targets, but emitted the fields in ascending order, and the
backslash DATA offset used TARGET frame rather than original
DGROUP frame. The maintained source explicitly references
DGROUP for the backslash and groups **eleven non-overlapping
semantic control-flow blocks** in reverse original OMF writer
order. Each source block is assembled from real 8086 instructions,
real far calls and symbolic branch labels at original segment
coordinates. The ORG directives do not insert target padding;
the combined native CODE coverage is the entire original
322 bytes with no missing or overlapping byte. The resulting
OMF LEDATA records are physically divided differently from
the compiler's one contiguous record, but literal ordered
relocations, segment/data ownership, and linked results match.
There are no byte arrays containing original executable CODE
and no object-file or EXE patches.

The scoped native builder combines this member at original
index282 with the already proved 24 original source CRT units
including strrchr, both qsort sorting algorithms, the complete
xx exception/RTTI, signed/unsigned scanners and the
1,282-CODE/128-DATA scanner. The other **868 of893 original
CRT member program records** are untouched. Two independent
TASM/TLIB/TLINK rounds produce the **complete 67,372-byte
decoded Japanese MAINL EXE** and its original MAP bitwise equal,
retaining **677 MZ relocation entries**. The simultaneous
original source CODE scope is now **18,167 bytes across
25 source members**, plus this newly recovered 2-byte DATA
literal; do not confuse gross source scope with accepted credit.

The accepted28-provider CRT, frozen211-owner MAINL publication,
fixed candidate-local-attested Japanese target and all cold
outputs remain unchanged. This is independently verified
source-only native exactness, **not automatically accepted
source-ledger credit**. No full cold or DIET replay took place.

Affected-only native reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_postscanner_work.py strrchr-srchstr
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_postscanner_work.py strrchr-srchstr
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_postscanner_work

Two real raw OBJ/LIB/EXE/MAP rounds, source/driver hash receipts
and TASM/TLIB/TLINK original writer logs are retained in
.analysis/work/mainl-postscanner-strrchr-srchstr-{build,review}.json
and .analysis/work/postscanner-strrchr-srchstr-*.

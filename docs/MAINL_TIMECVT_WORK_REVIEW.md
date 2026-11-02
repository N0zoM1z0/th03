# DOS/Unix time conversion: 820 CODE, 12 DATA and 48-source MAINL

The original 16-bit Japanese Borland DOS CRT member _timecvt (index184)
is now represented by maintained mnemonic 8086 source at
src/mainl/crt/_timecvt.asm. It contains both complete public far
conversion functions: __dostounix (301 original CODE bytes) and
__unixtodos (519 bytes). The source preserves the original 32-bit
time_t arithmetic, timezone offset, daylight savings correction,
date/month/year and DOS-time packing, and genuine imported near
N_LXMUL@, N_LMOD@ and N_LDIV@ operations. Its twelve initialized
DATA bytes are actual non-leap calendar month lengths, not
executable machine-code padding.

Real TASM 5.0 emits **all 820 original CODE bytes and all 12
original DATA bytes** with the correct two original public far
offsets and seven EXTDEF names/indices. Its zero BSS and literal
08ff02ff03 DATA-before-BSS group also match. **All 29 original
OMF relocation fields are present in the original literal
descending CODE-site order**, with the original field sites,
target kinds, target indices, widths and addends. Disjoint,
non-overlapping symbolic code ranges at actual instruction
boundaries restore Borland's descending FIXUPP writer order
without padding or target bytes embedded as CODE data arrays.

**An actual original OMF mismatch remains.** The 18 near CRT
external calls to __ISDST, N_LXMUL@, N_LMOD@ and N_LDIV@ use the
original Borland compiler's TARGET frame-method5, whereas
TASM's same semantic near calls use CODE-segment frame-method0.
The other eleven fields match original OMF literally. Native
trials of explicit near ptr, CS qualifiers, far external
declarations, GROUP-qualified targets and scoped ASSUME
directives established that simple TASM source forms do not
change these 18 frames without assembler errors or altered
codegen. The 29 logical relocations and the original CODE/DATA
are exact, but **the native OBJ is not declared fully identical**.
The reviewer checks all 18 differences explicitly and rejects
additional mismatches.

Despite the original OMF frame distinction, both real
TASM/TLIB/TLINK rounds produce the **entire original 67,372-byte
Japanese decoded MAINL EXE** and its complete MAP byte-for-byte,
with all **677 original MZ relocations**. The genuine original
893-member library contains 48 actual source modules (whole xx,
two qsort bosses, scanners, DOS file/string, path and buffer
subsystems plus this time converter); the other **845 original
member program records remain byte-identical**. The total
working source CODE extent is **25,447 exact bytes**.

The inherited fopen OMF writer-order and fclose near-call frame
gaps also remain open. The accepted28-provider CRT, published
211-owner MAINL ledger and candidate-local-attested Japanese
target remain unchanged; this source-only product matching is
not new formally accepted byte credit. No full cold/DIET replay
or unrelated ancestor chain has run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_timecvt_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_timecvt_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_timecvt_work

Complete two-round real OBJ/LIB/EXE/MAP vectors, native tool logs
and source/driver/original-bound build and review receipts are
retained under .analysis/work/timecvt-* and
mainl-timecvt-native-{build,review}.json.

# DOS strcmp source and cumulative three-member MAINL native link

The new original-DOS 8086 source src/mainl/crt/strcmp.asm reproduces the
complete 48-byte far cdecl strcmp body. It retains the target's two-stage
string strategy: scan the second far string with REPNE SCASB and CX=FFFF,
restore its start, then compare both strings through REPE CMPSB. The signed
AX result is formed from the original byte AL and BL values, retaining the
original zeroed high bytes. DS and SI/DI are preserved. Source contains
ordinary mnemonic instructions and labels, never a target-byte array.

The original and emitted objects have identical 48 CODE bytes, zero literal
relocation fields, public _strcmp and no imports, plus genuinely empty
_DATA/_BSS segments and their original BSS-before-DATA GRPDEF. Both source
and original OMF storage boundaries and native group bytes are checked.

The current builder inherits the actual two-source memcpy+memcmp library
from the earlier independently verified native pair, preserving its source
objects and complete program records, then replaces strcmp at original
zero-based member index292. Its cumulative library has 893 positions,
three real source members at260/261/292 and 890 untouched original vendor
member records. Two isolated original TASM/TLIB/TLINK rounds repeat raw
OBJ/LIB/EXE/MAP vectors. Both links exactly reproduce the 67,372-byte
decoded Japanese MAINL EXE and the entire original MAP, with all677 MZ
relocations. None of the accepted28-source library, cold pair, fixed
inputs, or original objects is overwritten.

The 36+40+48=124 reconstructed bytes are a bounded source-present native
result, not newly published accepted-ledger credit. The whole-game source
denominator remains unknown.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strcmp_combo_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strcmp_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strcmp_work

Preserve .analysis/work/mainl-strcmp-combo-build.json,
mainl-strcmp-combo-review.json, strcmp-roundN-* raw results and native logs,
and both inherited independent source library pairs for validation. No
full cold/DIET or ancestor runtime replay is required.
